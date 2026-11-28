"""
Attach to MGS2 and read its inventory / stage state.

No breakpoints: a shipped client can't freeze the game on every pickup, so
everything here is plain polled reads.
"""

import ctypes
import struct
import sys
from ctypes import wintypes

import pymem

try:                                    # as worlds.mgs2.client (Launcher / installed .apworld)
    from . import offsets, winmodules
except ImportError:                     # as a script / from the dev tools in a checkout
    import offsets
    import winmodules

_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
_kernel32.VirtualProtectEx.argtypes = [wintypes.HANDLE, wintypes.LPVOID, ctypes.c_size_t,
                                       wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
_kernel32.VirtualProtectEx.restype = wintypes.BOOL
_PAGE_READWRITE = 0x04


class Mgs2NotReady(Exception):
    """Attached, but the game isn't in a state where these reads make sense."""


class RazorName:
    """The name the game shows when a Razor (every AP spot) is picked up.

    The exe reads it through one pointer in its item-name table. Each distinct name
    gets its own buffer of ours (any length works), written once and never changed;
    changing the name repoints the pointer. A pickup message keeps the item *number*
    and looks the name up every frame (tested 2026-11-27: with per-name buffers, an
    older message still switched to the newer name), so every Razor message on screen
    shows the current name. restore() points it back at the exe's "RAZOR". Memory
    only: a game restart undoes everything."""

    BUFFER = 64

    def __init__(self, pm: pymem.Pymem, module_base: int):
        self.pm = pm
        self.slot = module_base + offsets.RAZOR_NAME_RVA
        self.pointer = module_base + offsets.RAZOR_NAME_POINTER_RVA
        # Refuse on an exe we don't recognise rather than write somewhere wrong.
        if not pm.read_bytes(self.slot, 6) == b"RAZOR\x00":
            raise RuntimeError(f"no RAZOR name at exe+{offsets.RAZOR_NAME_RVA:#x}; unknown game version?")
        target = struct.unpack("<Q", pm.read_bytes(self.pointer, 8))[0]
        if target != self.slot and not (target >> 32):
            raise RuntimeError(f"exe+{offsets.RAZOR_NAME_POINTER_RVA:#x} doesn't look like the name pointer")
        # One block, carved into BUFFER-sized slots (one per distinct name). A seed has
        # about 70 item names plus ARCHIPELAGO ITEM; SLOTS leaves plenty of room.
        self.block = pm.allocate(self.BUFFER * self.SLOTS)
        self.buffers: dict[str, int] = {}     # name -> its slot in the block
        self.current: str | None = None       # None: the game shows its own RAZOR

    SLOTS = 256

    def set(self, name: str) -> bool:
        """Show `name` on the next pickup. True if it changed."""
        if name == self.current:
            return False
        address = self.buffers.get(name)
        if address is None:
            if len(self.buffers) >= self.SLOTS:
                raise RuntimeError("out of name slots")
            raw = name.encode("ascii", "replace")[:self.BUFFER - 1]
            address = self.block + self.BUFFER * len(self.buffers)
            self.pm.write_bytes(address, raw + b"\x00" * (self.BUFFER - len(raw)), self.BUFFER)
            self.buffers[name] = address
        self._write_protected(self.pointer, struct.pack("<Q", address))
        self.current = name
        return True

    def restore(self) -> bool:
        """Point the game back at its own RAZOR string. True if it changed."""
        if self.current is None:
            return False
        self._write_protected(self.pointer, struct.pack("<Q", self.slot))
        self.current = None
        return True

    def _write_protected(self, address: int, data: bytes) -> None:
        old = wintypes.DWORD()
        if not _kernel32.VirtualProtectEx(self.pm.process_handle, address, len(data), _PAGE_READWRITE,
                                          ctypes.byref(old)):
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            self.pm.write_bytes(address, data, len(data))
        finally:
            _kernel32.VirtualProtectEx(self.pm.process_handle, address, len(data), old.value,
                                       ctypes.byref(wintypes.DWORD()))


class Mgs2:
    def __init__(self):
        try:
            self.pm = pymem.Pymem(offsets.PROCESS_NAME)
        except Exception as e:
            raise SystemExit(
                f"Failed to attach to '{offsets.PROCESS_NAME}': {e}\n"
                "Is the game running? Try an Administrator terminal if it's a permissions error."
            )

        self.module_base = self._find_module_base()

    def _find_module_base(self) -> int:
        target = offsets.PROCESS_NAME.lower()
        for module in winmodules.list_modules(self.pm.process_handle):
            if module.name.lower() == target:
                return module.base
        raise SystemExit(f"Attached, but could not locate the '{offsets.PROCESS_NAME}' module.")

    def _deref(self, rva: int) -> int:
        """Read the pointer stored at module_base + rva."""
        raw = self.pm.read_bytes(self.module_base + rva, 8)
        pointer = struct.unpack("<Q", raw)[0]
        if pointer == 0:
            raise Mgs2NotReady(f"pointer at +{rva:X} is null (game probably still loading)")
        return pointer

    def player_struct(self) -> int:
        return self._deref(offsets.PLAYER_POINTER_RVA)

    def varbuf(self) -> int:
        """GCX stage-variable block: script varbuf_0xNNN is at varbuf() + 0xNNN."""
        return self._deref(offsets.VARBUF_POINTER_RVA)

    def inventory_struct(self) -> int:
        return self._deref(offsets.CURRENT_AMMO_POINTER_RVA)

    def current_stage(self) -> str:
        address = self.player_struct() + offsets.CURRENT_STAGE_OFFSET
        raw = self.pm.read_bytes(address, offsets.CURRENT_STAGE_LENGTH)
        return raw.split(b"\x00")[0].decode("ascii", errors="replace")

    def current_difficulty(self) -> int:
        """Raw difficulty byte. Enum mapping isn't confirmed -- correlate it
        against the difficulty you actually selected."""
        address = self.player_struct() + offsets.CURRENT_DIFFICULTY_OFFSET
        return self.pm.read_bytes(address, 1)[0]

    def player_position(self) -> tuple[int, int, int]:
        """(x, height, y), signed 32-bit, in the same units and axis order as the
        spawn calls' positions (manifest "positions"). Confirmed in game 2026-11-27:
        Shell 1 Core reads y -56160, which a 16-bit read wraps to 9376."""
        base = self.player_struct()
        raw = self.pm.read_bytes(base + offsets.POSITION_X_OFFSET, 12)
        x = struct.unpack_from("<i", raw, 0)[0]
        height = struct.unpack_from("<i", raw, offsets.POSITION_HEIGHT_OFFSET - offsets.POSITION_X_OFFSET)[0]
        y = struct.unpack_from("<i", raw, offsets.POSITION_Y_OFFSET - offsets.POSITION_X_OFFSET)[0]
        return x, height, y

    def player_rotation(self) -> int:
        """Facing, 0..4095. The upper half of this slot holds something else."""
        address = self.player_struct() + offsets.POSITION_ROT_OFFSET
        raw = self.pm.read_bytes(address, 2)
        return struct.unpack("<H", raw)[0] % offsets.ROTATION_MAX

    def _read_counts(self, base_offset: int, size: int, table: dict[str, int]) -> dict[str, int]:
        block = self.pm.read_bytes(self.inventory_struct() + base_offset, size)
        return {
            name: struct.unpack_from("<H", block, index)[0]
            for name, index in table.items()
        }

    def item_counts(self) -> dict[str, int]:
        return self._read_counts(
            offsets.BASE_ITEM_OFFSET, offsets.ITEM_BLOCK_SIZE, offsets.ITEMS
        )

    def weapon_counts(self) -> dict[str, int]:
        return self._read_counts(
            offsets.BASE_WEAPON_OFFSET, offsets.WEAPON_BLOCK_SIZE, offsets.WEAPONS
        )

    def count_address(self, name: str, weapon: bool = False) -> int:
        table = offsets.WEAPONS if weapon else offsets.ITEMS
        base = offsets.BASE_WEAPON_OFFSET if weapon else offsets.BASE_ITEM_OFFSET
        if name not in table:
            raise KeyError(name)
        return self.inventory_struct() + base + table[name]

    def get_count(self, name: str, weapon: bool = False) -> int:
        raw = self.pm.read_bytes(self.count_address(name, weapon), 2)
        return struct.unpack("<H", raw)[0]

    def set_count(self, name: str, value: int, weapon: bool = False) -> None:
        address = self.count_address(name, weapon)
        self.pm.write_bytes(address, struct.pack("<H", value), 2)

    def max_address(self, name: str, weapon: bool = False) -> int:
        diff = offsets.WEAPON_MAX_DIFF if weapon else offsets.ITEM_MAX_DIFF
        return self.count_address(name, weapon) + diff

    def get_max(self, name: str, weapon: bool = False) -> int:
        raw = self.pm.read_bytes(self.max_address(name, weapon), 2)
        return struct.unpack("<H", raw)[0]

    def set_max(self, name: str, value: int, weapon: bool = False) -> None:
        self.pm.write_bytes(self.max_address(name, weapon), struct.pack("<H", value), 2)

    def snapshot(self) -> dict[str, int]:
        """All item and weapon counts in one pass, keyed by name."""
        counts = self.item_counts()
        for name, value in self.weapon_counts().items():
            counts[f"{name} (weapon)"] = value
        return counts
