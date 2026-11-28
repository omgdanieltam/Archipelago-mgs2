"""
POC Archipelago client for MGS2 (Normal). Not hardened -- it's for proving the
whole loop works in game. ap_patch.py turns Tanker and Plant pickups into
markers and both chapters' rewards into flags.

Lives in worlds/mgs2/client of the Archipelago checkout. Needs the game
patched with `python ap_patch.py --apply` (markers, empty start kit, Olga flag),
which also writes ap_manifest.json next to this file.

What it does every tick (CLIENT_DESIGN.md §2.2, §5, §6):
    - keeps the Razor (the marker item) at max 999 / count 0
    - chapter: from the stage code (w0x = Tanker, w1x and up = Plant). The
      save's chapter is kept at varbuf 0x2FA; checks, story checks and
      victory only count for that chapter.
    - new game: fingerprint at varbuf 0x2FC is 0 -> zero the ammo stash,
      write this seed's fingerprint and the chapter. A different non-zero
      fingerprint means a save from another seed: the client does nothing to it.
    - checks: every manifest flag >= 0x80 is sent as a location check
    - grants: items_received[N:] are applied, N (varbuf 0x2F8) advances
      after each one. Items for the other chapter are skipped, so each new
      Tanker or Plant game gets every item of its own chapter. A save that
      moves Tanker -> Plant restarts N at 0. Ammo for an unowned gun goes to
      its max field (the stash) and is added when the gun arrives.
    - story checks (both chapters): locations with no flag (Guard Rush and Tanker
      Complete; Fortune, Fatman, Harrier, Vamp, Vamp sniping and RAY defeated, and
      Plant Complete) are sent once the story counter passes them
    - victory (Tanker): story counter (varbuf 0x6) >= 46 -> CLIENT_GOAL

Run with the Archipelago venv (it has pymem), from the Archipelago root:
    venv\\Scripts\\python.exe worlds\\mgs2\\client\\ap_client.py --connect localhost:38281 --name DanielMGS2
    add --nogui for a console-only client.

Client commands: /mgs2 (state dump)
"""

import asyncio
import importlib.util
import json
import math
import os
import random
import re
import struct
import sys
import time
import zlib

ROOT = os.path.dirname(os.path.abspath(__file__))
AP_ROOT = os.path.abspath(os.path.join(ROOT, "..", "..", ".."))   # client -> mgs2 -> worlds -> root
sys.path.insert(0, AP_ROOT)
sys.path.insert(1, ROOT)

import Utils  # noqa: E402

LOG_DIR = os.path.join(ROOT, "logs")   # next to this script, wherever the client folder lives
KEEP_LOGS = 20


def move_log_file(folder: str) -> None:
    """Utils.init_logging always writes to Archipelago's own logs/ folder. Swap its file
    handler for an identical one in `folder`, and keep only the newest KEEP_LOGS there."""
    import glob
    import logging
    root_logger = logging.getLogger()
    for handler in list(root_logger.handlers):
        if not isinstance(handler, logging.FileHandler):
            continue
        old = handler.baseFilename
        root_logger.removeHandler(handler)
        handler.close()
        try:                            # carry over what init_logging already wrote (its first line)
            with open(old, encoding="utf-8-sig") as f:
                written = f.read()
            os.remove(old)
        except OSError:
            written = ""
        os.makedirs(folder, exist_ok=True)
        moved = logging.FileHandler(os.path.join(folder, os.path.basename(old)), "w", encoding="utf-8-sig")
        moved.setFormatter(handler.formatter)
        for f in handler.filters:
            moved.addFilter(f)
        if written:
            moved.stream.write(written)
            moved.flush()
        root_logger.addHandler(moved)
    logs = sorted(glob.glob(os.path.join(folder, "MGS2Client_*.txt")), key=os.path.getmtime)
    for path in logs[:-KEEP_LOGS]:
        try:
            os.remove(path)
        except OSError:
            pass


if __name__ == "__main__":
    Utils.init_logging("MGS2Client", exception_logger="Client")
    move_log_file(LOG_DIR)

from CommonClient import (ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled,  # noqa: E402
                          handle_url_arg, logger, server_loop)
import logging  # noqa: E402

# Detail messages (checks, grants, stage changes...) always go to the log file
# (Archipelago's logs/MGS2Client_<date>.txt). The window and terminal only show them
# with --debug or after /debug. "MGS2" isn't one of the loggers the GUI displays, and
# NoStream keeps it off the terminal; the file handler takes everything.
detail_logger = logging.getLogger("MGS2")
DEBUG = False


def detail(msg: str) -> None:
    if DEBUG:
        logger.info(msg)
    else:
        detail_logger.info(msg, extra={"NoStream": True})


def file_only(msg: str) -> None:
    """Log file only, even with --debug (the seed info and spoiler: never on screen)."""
    detail_logger.info(msg, extra={"NoStream": True})
from NetUtils import ClientStatus  # noqa: E402

import mgs2mem  # noqa: E402



def _load_world_config():
    """worlds/mgs2/Config/Config.py, loaded by path: importing worlds.mgs2 would load every world."""
    spec = importlib.util.spec_from_file_location("mgs2_world_config",
                                                  os.path.join(ROOT, "..", "Config", "Config.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_config = _load_world_config()
GAME = _config.GAME
APWORLD_VERSION = _config.APWORLD_VERSION  # the seed's slot_data must match
MANIFEST = os.path.join(ROOT, "ap_manifest.json")

POLL_SECONDS = 0.25
STABLE_SECONDS = 2.0                # stage must be unchanged this long before we write
VARBUF_SPAN = 0x1600                 # Plant flags reach 0x14C0
STORY = 0x6                         # u16 story counter (Tanker)
PLANT_STORY = 0x68                  # u16 story counter the Plant scripts compare
N_SLOT = 0x2F8                      # u16 received-items processed (this save, this chapter)
CHAPTER_SLOT = 0x2FA                # u8 chapter N belongs to; a change resets N
SAVE_ID_SLOT = 0x2FB                # u8 random id per game (1-255), keys this save's local-grant record
FINGERPRINT = 0x2FC                 # u32 seed fingerprint
LOAD_COUNTER = 0x4CA                # player struct: area-load counter, what a pickup stores in its flag
LOCAL_GRANTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_grants")
VICTORY_STORY = 46                  # first reached in d12t after the RAY photos
PLANT_CLEAR_STORY = 0x1D6           # w61a sets it when the Solidus fight ends, then loads d082p01
# The goal is both chapters cleared. Each clear is a location the client sends from the story counter
# (STORY_CHECKS); the goal goes out once the server has both, so they can come from different saves.
# A seed without these locations keeps the old goal: Tanker story >= VICTORY_STORY.
COMPLETION_CHECKS = ("Tanker Complete", "Plant Complete")

RAZOR = "Unknown Item"
REMOTE_NAME = "ARCHIPELAGO ITEM"     # what a spot holding another player's item is called in game
RAZOR_MAX = 999
NOT_HELD = 0xFFFF
ANTI_CLAMP_MAX = 300                # owned gun max; a max >= this means "stash already flushed"
ITEM_MAX = {"Ration": 30}           # raised on a new game and on every grant

# Each chapter is its own save with its own inventory. A save only receives its
# chapter's items; the rest are skipped (N still advances) and land in the
# other chapter's save, which replays the whole list from N = 0.
TANKER, PLANT = 1, 2
CHAPTER_NAME = {TANKER: "Tanker", PLANT: "Plant"}
CHAPTER_STAGE = {TANKER: re.compile(r"^w0\d[a-z]$"), PLANT: re.compile(r"^w[1-9]\d[a-z]$")}

# No physical spot: sent automatically once a save of that chapter carries this seed's fingerprint (§2.2).
# ap_patch.py empties both start kits.
START_CHECKS = {
    TANKER: ["Tanker Start - M9", "Tanker Start - Camera", "Tanker Start - Cigs", "Tanker Start - AP Sensor"],
    PLANT: ["Plant Start - AP Sensor", "Plant Start - Binoculars"],
}
# No flag and no spawn: sent once a save of that chapter has its story counter at the value or past it
# (Tanker varbuf 0x6, Plant 0x68; CLIENT_DESIGN.md §8 item 4). Names not in the seed are ignored.
STORY_CHECKS = {
    # 34 is what d10t (the cutscene after the rush) showed; lower it once the end-of-rush value is measured.
    TANKER: {"Deck 2 - Guard Rush (Reward)": 34,
             "Tanker Complete": VICTORY_STORY},
    # The first value after each fight, from logged Plant runs (2026-10/11).
    PLANT: {
        "Strut A SeaDock - Fortune (Reward)": 0x74,       # w11c fight 0x6E-0x73, then w12c
        "Strut A Pump Room - Fortune (Reward)": 0x74,     # older name of the same check
        "Strut E Heliport - Fatman (Reward)": 0x77,       # fight at 0x76, then cutscene d021
        "Shell 1 Core Hostage Room - Ames (Reward)": 0xB0,        # D. Mic at 0xA1, Ames scenes d036 to 0xAF, back in w24b
        "Shell 1-2 Connecting Bridge - Harrier (Reward)": 0xBE,   # w25a fight at 0xBD, then d046
        "Shell 2 Filtration Chamber 2 - Vamp (Reward)": 0x102,   # w31f fight at 0x101, then d055
        "Strut L Sniping - Vamp (Reward)": 0x143,         # w32a sniping 0x139-0x13B, w32b 0x13C-0x141, then w20a
        "Arsenal Gear - RAY (Reward)": 0x19C,             # w46a fight 0x196-0x19B, then d080
        "Plant Complete": PLANT_CLEAR_STORY,              # Solidus: w61a sets 0x1D6, then d082
    },
}

# AP item name -> (kind, game slot name, amount), per chapter. CLIENT_DESIGN.md §3.1.
# Kinds: weapon (count is ammo), tool (weapon slot without ammo), ammo, unique item, stack item.
GRANTS = {
    TANKER: {
        "M9 (Snake)": ("weapon", "M9", 16),
        "USP": ("weapon", "USP", 16),
        "Grenade (Tanker)": ("weapon", "Grenade", 3),
        "Stun Grenade (Tanker)": ("weapon", "Stun Grenade", 3),
        "Chaff Grenade (Tanker)": ("weapon", "Chaff Grenade", 3),
        "M9 Ammo (Tanker)": ("ammo", "M9", 16),
        "USP Ammo": ("ammo", "USP", 16),
        "Camera": ("unique", "Camera", 1),
        "Cigarettes (Tanker)": ("unique", "Cigarettes", 1),
        "A.P. Sensor (Tanker)": ("unique", "A.P. Sensor", 1),
        "Thermal Goggles (Tanker)": ("unique", "Thermal Goggles", 1),
        "USP Suppressor": ("unique", "U.S.P. Suppressor", 1),
        "Box": ("unique", "Box 1", 1),
        "Wet Box": ("unique", "Wet Box", 1),
        "Ration (Tanker)": ("stack", "Ration", 2),
        "Bandage (Tanker)": ("stack", "Bandage", 5),
        "Pentazemin (Tanker)": ("stack", "Pentazemin", 5),
        "Cold Medicine (Tanker)": ("stack", "Cold Medicine", 1),
    },
    # Plant amounts are provisional (untested in game).
    PLANT: {
        "M9 (Raiden)": ("weapon", "M9", 16),
        "SOCOM": ("weapon", "SOCOM", 12),
        "PSG1": ("weapon", "PSG1", 10),
        "PSG1-T": ("weapon", "PSG1-T", 10),
        "M4": ("weapon", "M4", 30),
        "AKS-74u": ("weapon", "AKS-74u", 30),
        "Stinger": ("weapon", "Stinger", 4),
        "RGB6": ("weapon", "RGB-6", 6),
        "Nikita": ("weapon", "Nikita", 4),
        "Claymore": ("weapon", "Claymore", 2),
        "C4": ("weapon", "C4", 2),
        "Grenade (Plant)": ("weapon", "Grenade", 3),
        "Stun Grenade (Plant)": ("weapon", "Stun Grenade", 3),
        "Chaff Grenade (Plant)": ("weapon", "Chaff Grenade", 3),
        "HF Blade": ("tool", "High Frequency Blade", 1),
        "Coolant": ("tool", "Coolant Spray", 1),
        "D. Mic": ("tool", "Directional Microphone", 1),
        "Book": ("tool", "Book", 1),
        "M9 Ammo (Plant)": ("ammo", "M9", 16),
        "SOCOM Ammo": ("ammo", "SOCOM", 12),
        "PSG1 Ammo": ("ammo", "PSG1", 10),
        "PSG1-T Ammo": ("ammo", "PSG1-T", 10),
        "M4 Ammo": ("ammo", "M4", 30),
        "AKS-74u Ammo": ("ammo", "AKS-74u", 30),
        "Stinger Ammo": ("ammo", "Stinger", 4),
        "RGB6 Ammo": ("ammo", "RGB-6", 6),
        "Nikita Ammo": ("ammo", "Nikita", 4),
        "Cigarettes (Plant)": ("unique", "Cigarettes", 1),
        "A.P. Sensor (Plant)": ("unique", "A.P. Sensor", 1),
        "Thermal Goggles (Plant)": ("unique", "Thermal Goggles", 1),
        "Box 1": ("unique", "Box 1", 1),
        "Box 2": ("unique", "Box 2", 1),
        "Box 3": ("unique", "Box 3", 1),
        "Box 4": ("unique", "Box 4", 1),
        "Sensor A": ("unique", "Sensor A", 1),
        "Sensor B": ("unique", "Sensor B", 1),
        "BDU": ("unique", "B.D.U.", 1),
        "Mine Detector": ("unique", "Mine Detector", 1),
        "Digital Camera": ("unique", "Digital Camera", 1),
        "AKS-74u Suppressor": ("unique", "AK Suppressor", 1),
        "SOCOM Suppressor": ("unique", "SOCOM Suppressor", 1),
        "Body Armor": ("unique", "Body Armor", 1),
        "NVG": ("unique", "N.V.G.", 1),
        "Binoculars": ("unique", "Scope2", 1),
        "Box 5": ("unique", "Box 5", 1),
        "Phone": ("unique", "Phone", 1),
        "M.O. DISC": ("unique", "M.O. Disc", 1),
        # Card level = the number of Progressive Cards received so far (4 in the pool: levels 1-4).
        # Level 5 comes from the KL bridge scene, which the patch keeps; a grant never lowers a level.
        "Progressive Card": ("card", "Card", 1),
        "Ration (Plant)": ("stack", "Ration", 2),
        "Bandage (Plant)": ("stack", "Bandage", 5),
        "Pentazemin (Plant)": ("stack", "Pentazemin", 5),
        "Cold Medicine (Plant)": ("stack", "Cold Medicine", 1),
    },
}
# An item name may carry its chapter as a suffix ("Box 5 (Plant)", "USP (Tanker)"); the table is
# keyed by the name without it, or by the full name where both chapters have the item.
CHAPTER_SUFFIX = {" (Tanker)": TANKER, " (Plant)": PLANT}
GRANTS[TANKER]["M9"] = GRANTS[TANKER]["M9 (Snake)"]      # "M9 (Tanker)"
GRANTS[PLANT]["M9"] = GRANTS[PLANT]["M9 (Raiden)"]       # "M9 (Plant)"


def grant_entry(item_name: str) -> tuple[int, str, str, int] | None:
    """(chapter, kind, slot, amount) for an AP item name, or None if it has no grant."""
    for chapter, table in GRANTS.items():
        if item_name in table:
            return (chapter, *table[item_name])
    for suffix, chapter in CHAPTER_SUFFIX.items():
        if item_name.endswith(suffix) and item_name[:-len(suffix)] in GRANTS[chapter]:
            return (chapter, *GRANTS[chapter][item_name[:-len(suffix)]])
    return None
# Guns that have AP ammo items: ammo received before the gun waits in the gun's max field.
STASH_WEAPONS = {chapter: tuple(dict.fromkeys(slot for kind, slot, _ in table.values() if kind == "ammo"))
                 for chapter, table in GRANTS.items()}
# Weapons that are their own ammo (grenades, Claymores, C4) have no stash, so they don't
# need ANTI_CLAMP_MAX: their max is WEAPON_CAP, and grants stop there.
WEAPON_CAP = 50
# Arsenal Gear: w41a takes Raiden's gear, w43a gives it back. Grants wait while it's gone.
CONFISCATION_STAGES = {"w41a", "w42a"}
CAPPED_WEAPONS = {chapter: tuple(dict.fromkeys(slot for kind, slot, _ in table.values()
                                               if kind == "weapon" and slot not in STASH_WEAPONS[chapter]))
                  for chapter, table in GRANTS.items()}


def chapter_of(stage: str) -> int | None:
    """The chapter a gameplay stage belongs to; None for menus and cutscenes."""
    for chapter, pattern in CHAPTER_STAGE.items():
        if pattern.match(stage or ""):
            return chapter
    return None


# --------------------------------------------------------------------------- memory

class Game:
    """Thin wrapper over mgs2mem that (re)attaches lazily and never raises SystemExit."""

    def __init__(self):
        self.mem: mgs2mem.Mgs2 | None = None
        self.next_attach = 0.0
        self.razor: mgs2mem.RazorName | None = None   # the pickup name; None if it couldn't be set up

    def attached(self) -> bool:
        if self.mem is None and time.time() >= self.next_attach:
            try:
                self.mem = mgs2mem.Mgs2()
                logger.info("Attached to MGS2.")
            except BaseException:  # mgs2mem raises SystemExit when the game isn't running
                self.next_attach = time.time() + 3
                return False
            try:
                self.razor = mgs2mem.RazorName(self.mem.pm, self.mem.module_base)
            except Exception as e:
                self.razor = None
                logger.warning(f"Pickup names disabled (every AP spot will say Razor): {e}")
        return self.mem is not None

    def detach(self) -> None:
        if self.mem is not None:
            logger.info("Lost the game process; will retry.")
        self.mem = None
        self.razor = None              # its buffer died with the process
        self.next_attach = time.time() + 3

    def release_name(self) -> None:
        """Client closing: give the game its own RAZOR name back."""
        if self.razor is not None:
            try:
                self.razor.restore()
            except Exception:
                pass
            self.razor = None

    # varbuf
    def varbuf_bytes(self) -> tuple[int, bytes]:
        pointer = self.mem.varbuf()
        return pointer, self.mem.pm.read_bytes(pointer, VARBUF_SPAN)

    def write_varbuf(self, offset: int, fmt: str, value: int) -> None:
        data = struct.pack(fmt, value)
        self.mem.pm.write_bytes(self.mem.varbuf() + offset, data, len(data))

    def mark_collected(self, flag: int) -> None:
        """Set a location's flag the way a pickup does (the area-load counter, >= 0x80)."""
        counter = self.mem.pm.read_bytes(self.mem.player_struct() + LOAD_COUNTER, 1)[0] | 0x80
        self.write_varbuf(flag, "<B", counter)

    # inventory
    def count(self, name: str, weapon: bool) -> int:
        return self.mem.get_count(name, weapon)

    def set_count(self, name: str, value: int, weapon: bool) -> None:
        self.mem.set_count(name, value, weapon)

    def max(self, name: str, weapon: bool) -> int:
        return self.mem.get_max(name, weapon)

    def set_max(self, name: str, value: int, weapon: bool) -> None:
        self.mem.set_max(name, value, weapon)


class Frame:
    """One consistent read: stage + varbuf, with the pointer re-checked afterwards."""

    def __init__(self, game: Game):
        self.stage = game.mem.current_stage()
        pointer, self.varbuf = game.varbuf_bytes()
        self.consistent = game.mem.varbuf() == pointer and game.mem.current_stage() == self.stage
        self.story = struct.unpack_from("<H", self.varbuf, STORY)[0]
        self.plant_story = struct.unpack_from("<H", self.varbuf, PLANT_STORY)[0]
        self.n = struct.unpack_from("<H", self.varbuf, N_SLOT)[0]
        self.save_chapter = self.varbuf[CHAPTER_SLOT]     # 0 until the client claims the save
        self.chapter = chapter_of(self.stage)               # None outside gameplay stages
        self.fingerprint = struct.unpack_from("<I", self.varbuf, FINGERPRINT)[0]
        self.save_id = self.varbuf[SAVE_ID_SLOT]          # 0 on saves from before local grants

    def flag(self, offset: int) -> bool:
        return self.varbuf[offset] >= 0x80


# --------------------------------------------------------------------------- grants

def reset_stash(game: Game, chapter: int) -> None:
    """Empty the stash of every unowned gun (new game or chapter switch: the max may hold anything)."""
    for w in STASH_WEAPONS[chapter]:
        if game.count(w, True) == NOT_HELD:
            game.set_max(w, 0, True)
    for item, value in ITEM_MAX.items():
        if game.max(item, False) < value:
            game.set_max(item, value, False)


def flush_stash(game: Game, chapter: int) -> None:
    """A gun that just became owned gets the ammo stashed in its max."""
    for w in STASH_WEAPONS[chapter]:
        current = game.count(w, True)
        if current == NOT_HELD:
            continue
        stash = game.max(w, True)          # read before writing current
        if stash >= ANTI_CLAMP_MAX:        # a stash is always below it (asserted when stashing)
            continue
        game.set_max(w, ANTI_CLAMP_MAX, True)
        game.set_count(w, current + stash, True)
        detail(f"  {w}: now owned, added {stash} stashed rounds -> {current + stash}")
    # Saves from before WEAPON_CAP carry a max of 300 on these; bring them down.
    for w in CAPPED_WEAPONS[chapter]:
        if game.max(w, True) > WEAPON_CAP:
            game.set_max(w, WEAPON_CAP, True)
            current = game.count(w, True)
            if current != NOT_HELD and current > WEAPON_CAP:
                game.set_count(w, WEAPON_CAP, True)


def apply_grant(game: Game, item_name: str, chapter: int, copies: int = 1) -> str:
    """Write one AP item into the inventory; returns a log line. `copies` is how many of this
    item have been received up to and including this one (used by progressive items)."""
    entry = grant_entry(item_name)
    if entry is None:
        return f"{item_name}: no mapping, skipped"
    item_chapter, kind, slot, amount = entry
    if item_chapter != chapter:
        return f"for the {CHAPTER_NAME[item_chapter]} save, skipped here"

    if kind == "card":
        current = game.count(slot, False)
        current = 0 if current == NOT_HELD else current
        level = max(current, copies * amount)
        if game.max(slot, False) < level:
            game.set_max(slot, level, False)
        game.set_count(slot, level, False)
        return f"{slot}: level {current} -> {level}"

    if kind == "tool":
        if game.count(slot, True) in (0, NOT_HELD):
            if game.max(slot, True) < amount:
                game.set_max(slot, amount, True)
            game.set_count(slot, amount, True)
            return f"{slot}: granted"
        return f"{slot}: already held"

    if kind == "weapon" and slot in CAPPED_WEAPONS[chapter]:
        current = game.count(slot, True)
        held = 0 if current == NOT_HELD else current
        new = min(held + amount, WEAPON_CAP)
        game.set_max(slot, WEAPON_CAP, True)
        game.set_count(slot, new, True)
        capped = " (at the cap)" if held + amount > WEAPON_CAP else ""
        return f"{slot}: {'granted' if current == NOT_HELD else f'{held} ->'} {new}{capped}"

    if kind == "weapon":
        current = game.count(slot, True)
        if current == NOT_HELD:
            stash = game.max(slot, True) if slot in STASH_WEAPONS[chapter] else 0
            game.set_max(slot, ANTI_CLAMP_MAX, True)
            game.set_count(slot, amount + stash, True)
            return f"{slot}: granted with {amount}" + (f" + {stash} stashed" if stash else "")
        new = current + amount
        if game.max(slot, True) < new:
            game.set_max(slot, max(new, ANTI_CLAMP_MAX), True)
        game.set_count(slot, new, True)
        return f"{slot}: already held, +{amount} -> {new}"

    if kind == "ammo":
        current = game.count(slot, True)
        if current == NOT_HELD:
            stash = game.max(slot, True) + amount
            if stash >= ANTI_CLAMP_MAX:
                return f"{slot} ammo: stash would reach {stash}, skipped"
            game.set_max(slot, stash, True)
            return f"{slot} ammo: weapon not held, stashed -> {stash} pending"
        new = current + amount
        if game.max(slot, True) < new:
            game.set_max(slot, max(new, ANTI_CLAMP_MAX), True)
        game.set_count(slot, new, True)
        return f"{slot} ammo: +{amount} -> {new}"

    current = game.count(slot, False)
    if current == NOT_HELD:
        current = 0
    new = max(current, amount) if kind == "unique" else current + amount
    wanted = max(new, ITEM_MAX.get(slot, 0))
    if game.max(slot, False) < wanted:
        game.set_max(slot, wanted, False)
    game.set_count(slot, new, False)
    return f"{slot}: {current} -> {new}"


# --------------------------------------------------------------------------- spot positions

def floor_distance(a, b) -> float:
    """Distance across the floor (x and y only). Heights vary by spot (a shelf vs. the
    floor), so height is reported separately and only used to rule out other levels."""
    return math.hypot(a[0] - b[0], a[2] - b[2])


def nearest_spots(manifest: list[dict], frame: Frame, position: tuple[int, int, int],
                  uncollected_only: bool = False) -> list[tuple[float, int, dict, list[int]]]:
    """Razor spots in the current stage, nearest first: (floor distance, height difference
    (spot minus you), manifest row, the spot's nearest [x, height, y])."""
    out = []
    for m in manifest:
        points = m.get("positions", {}).get(frame.stage)
        if not points or (uncollected_only and frame.flag(m["flag"])):
            continue
        point = min(points, key=lambda p: floor_distance(p, position))
        out.append((floor_distance(point, position), point[1] - position[1], m, point))
    out.sort(key=lambda t: t[0])
    return out


# Pickup naming (CLIENT_DESIGN.md, Presentation). Off for now (owner's call, 2026-11-27):
# every AP spot says ARCHIPELAGO ITEM while connected (RAZOR when not: a connection light).
# True turns the per-spot real names back on (own items by name, nearest-spot matching below).
REAL_PICKUP_NAMES = False
# Tuned from /nearest readings: standing at a spot reads ~550-1100 across the floor;
# side-by-side lockers are 1000 apart.
NAME_RANGE = 1500          # the nearest spot must be this close (floor distance) to be named
NAME_CLEAR_RATIO = 1.5     # ...and the next spot with a different name at least this much farther
NAME_LEVEL_GAP = 3000      # spots this far above/below you are on another level: ignored
# The pickup message keeps reading the name while it's on screen, so once the named spot
# is picked up its name stays put (2026-11-27: switching straight to the next spot made
# the message read ARCHIPELAGO ITEM). It's released early as soon as another spot is
# nearer to you than the one just picked up (two quick pickups both showed the first
# name with a plain timer), and at the latest after this long.
NAME_HOLD_SECONDS = 6.0


def spot_distance(m: dict, frame: Frame, position: tuple[int, int, int]) -> float:
    """Floor distance from you to a manifest spot's nearest position in this stage."""
    points = m.get("positions", {}).get(frame.stage)
    return min(floor_distance(p, position) for p in points) if points else math.inf


class PickupNamer:
    """Decides the pickup name each tick, including holding it while a message shows."""

    def __init__(self):
        self.held: dict | None = None      # spot just picked up; the name stays while its message shows
        self.hold_until = 0.0
        self.stage: str | None = None
        self.collected: set[int] = set()   # flags of this stage's spots already collected
        self.why = ""                      # reason for the current decision (/namelog)

    def update(self, ctx: "MGS2Context", frame: Frame, position: tuple[int, int, int] | None,
               now: float, own_save: bool) -> str | None:
        """The name to show now, or None to leave the current one as it is."""
        if not own_save or position is None:
            self.held, self.stage = None, None
            self.why = "not this seed's save, or not in gameplay"
            return REMOTE_NAME

        # Any spot in this area picked up since the last tick? Its message is showing now
        # with whatever name was set, even ARCHIPELAGO ITEM, so freeze that name.
        here = [m for m in ctx.manifest if frame.stage in m.get("positions", {})]
        collected = {m["flag"] for m in here if frame.flag(m["flag"])}
        if frame.stage == self.stage:
            new = [m for m in here if m["flag"] in collected - self.collected]
            if new:
                self.held = min(new, key=lambda m: spot_distance(m, frame, position))
                self.hold_until = now + NAME_HOLD_SECONDS
        else:
            self.held = None               # entering an area: nothing was just picked up here
        self.stage, self.collected = frame.stage, collected

        name, spot, nearest, why = choose_pickup_name(ctx, frame, position)
        if self.held is not None and now < self.hold_until:
            # Keep the name until you're in range of another uncollected spot that's nearer
            # than the one just picked up. Then move on, even to ARCHIPELAGO ITEM when that
            # spot is unclear: neutral beats a wrong name.
            held_distance = spot_distance(self.held, frame, position)
            if nearest > NAME_RANGE or nearest >= held_distance:
                self.why = f"holding for {self.held['location']} ({held_distance:.0f} away)"
                return None
        self.held, self.why = None, why
        return name


def choose_pickup_name(ctx: "MGS2Context", frame: Frame,
                       position: tuple[int, int, int]) -> tuple[str, dict | None, float, str]:
    """(name, the spot it names or None, floor distance to the nearest uncollected spot on
    your level, why) for the spot you're about to pick up. The name is REMOTE_NAME when no
    spot is clearly the one."""
    spots = [s for s in nearest_spots(ctx.manifest, frame, position, uncollected_only=True)
             if abs(s[1]) <= NAME_LEVEL_GAP]
    if not spots:
        return REMOTE_NAME, None, math.inf, "no uncollected spot on this level"
    nearest = spots[0][0]
    if nearest > NAME_RANGE:
        return REMOTE_NAME, None, nearest, f"nearest spot {nearest:.0f} away (> {NAME_RANGE})"
    name = ctx.pickup_name(spots[0][2])
    for distance, _, m, _ in spots[1:]:
        if distance >= nearest * NAME_CLEAR_RATIO:
            break
        if ctx.pickup_name(m) != name:   # two different spots about equally close: don't guess
            return (REMOTE_NAME, None, nearest,
                    f"unclear: {spots[0][2]['location']} {nearest:.0f} vs {m['location']} {distance:.0f}")
    return name, spots[0][2], nearest, f"{spots[0][2]['location']} at {nearest:.0f}"


# --------------------------------------------------------------------------- AP context

class MGS2CommandProcessor(ClientCommandProcessor):
    def _cmd_debug(self) -> bool:
        """Toggle showing detail messages (checks, grants, stage changes) here. They always go to the log file."""
        global DEBUG
        DEBUG = not DEBUG
        self.output(f"Detail messages {'shown' if DEBUG else 'hidden (still written to the log file)'}.")
        return True

    def _cmd_namelog(self) -> bool:
        """Toggle logging of pickup-name changes (position and the reason for each name)."""
        ctx: MGS2Context = self.ctx
        ctx.name_log = not ctx.name_log
        self.output(f"Pickup-name log {'on' if ctx.name_log else 'off'}.")
        return True

    def _cmd_nearest(self, count: str = "3") -> bool:
        """Show your position and the nearest AP spots in this area (checks the coordinates)."""
        ctx: MGS2Context = self.ctx
        game = ctx.game_mem
        if not game.attached():
            self.output("Game not attached.")
            return True
        try:
            frame = Frame(game)
            position = game.mem.player_position()
        except Exception as e:
            self.output(f"read failed: {e}")
            return True
        n = int(count) if count.isdigit() else 3
        self.output(f"stage {frame.stage}: position {position}")
        showing = ("Razor (pickup names disabled)" if game.razor is None
                   else game.razor.current or "RAZOR (not connected, or not this seed's save)")
        self.output(f"  a pickup right now would say: {showing}")
        spots = nearest_spots(ctx.manifest, frame, position)
        if not spots:
            self.output(f"  no AP spots with positions in {frame.stage}")
        else:
            self.output("     floor  height  spot")
        for distance, height, m, point in spots[:n]:
            state = "collected" if frame.flag(m["flag"]) else "uncollected"
            name = ctx.pickup_name(m) if ctx.ready else "(connect to see names)"
            self.output(f"  {distance:8.0f}  {height:+6d}  {m['location']}  at {tuple(point)}, {state}")
            self.output(f"                    holds: {name}" + ("" if REAL_PICKUP_NAMES else "  (shown as ARCHIPELAGO ITEM)"))
        return True

    def _cmd_mgs2(self) -> bool:
        """Show the game-side state the client sees."""
        ctx: MGS2Context = self.ctx
        game = ctx.game_mem
        if not game.attached():
            self.output("Game not attached.")
            return True
        try:
            frame = Frame(game)
            own = "this seed" if frame.fingerprint == ctx.fingerprint else (
                "empty (new game)" if frame.fingerprint == 0 else f"OTHER SEED ({frame.fingerprint:#010x})")
            save = CHAPTER_NAME.get(frame.save_chapter, "unclaimed")
            self.output(f"stage {frame.stage}, story {frame.story}, plant story {frame.plant_story:#x}, "
                        f"{save} save, N {frame.n} of "
                        f"{len(ctx.items_received)} received, fingerprint {own}")
            got = [m["location"] for m in ctx.manifest
                   if m["chapter"] == frame.save_chapter and frame.flag(m["flag"])]
            self.output(f"{len(got)} manifest flags set; {len(ctx.checked_locations)} checked on the server")
            for w in STASH_WEAPONS.get(frame.save_chapter, ()):
                self.output(f"  {w}: count {game.count(w, True)}, max {game.max(w, True)}")
        except Exception as e:
            self.output(f"read failed: {e}")
        return True


class MGS2Context(CommonContext):
    game = GAME
    items_handling = 0b111
    command_processor = MGS2CommandProcessor

    def __init__(self, server_address, password, ignore_version: bool):
        super().__init__(server_address, password)
        self.ignore_version = ignore_version
        self.game_mem = Game()
        self.manifest = [m for m in json.load(open(MANIFEST, encoding="utf-8")) if m["normal"]]
        for m in self.manifest:
            m["chapter"] = chapter_of(m["stage"])   # a flag is only read in a save of its chapter
        self.ready = False                    # connected + version ok + ids mapped
        self.fingerprint = 0
        self.location_id: dict[str, int] = {}  # manifest location -> AP id
        self.start_ids: dict[int, list[int]] = {}   # chapter -> AP ids of its Start checks
        self.story_ids: dict[int, tuple[int, int]] = {}   # AP id -> (chapter, story value that sends it)
        self.completion_ids: list[int] = []     # AP ids of COMPLETION_CHECKS; empty = old Tanker-only goal
        self.local_items: dict[int, int] = {}   # own-world location id -> own item id (slot_data); rest is remote
        self.location_row: dict[int, dict] = {} # AP location id -> its manifest row (flag, chapter)
        self._local_grants: dict[str, set[int]] | None = None   # save id -> location ids granted at pickup
        self.spoiler_logged_for: str | None = None   # seed the spoiler was written for (once per session)
        self.spoiler_pending = False
        self.name_log = False                   # /namelog: log each pickup-name decision
        self.warned: set[str] = set()

    # Local grants (CLIENT_DESIGN.md, step 5): own items are given at pickup, even offline,
    # and the server's copy is skipped when this save already got it.
    def local_grant_name(self, code: int, chapter: int) -> str | None:
        """The item name if location `code` holds one of our own items that can be granted
        straight away in a `chapter` save; None otherwise. Progressive Cards stay
        server-granted (their level counts every card received)."""
        item = self.local_items.get(code)
        if item is None:
            return None
        name = self.item_names.lookup_in_game(item, GAME)
        entry = grant_entry(name)
        if entry is None or entry[0] != chapter or entry[1] == "card":
            return None
        return name

    def _grants_file(self) -> str:
        return os.path.join(LOCAL_GRANTS_DIR, f"{self.fingerprint:08x}.json")

    def granted_locally(self, save_id: int) -> set[int]:
        """Location ids this save (by its save id) was given at pickup, for this seed."""
        if self._local_grants is None:
            try:
                with open(self._grants_file(), encoding="utf-8") as f:
                    self._local_grants = {k: set(v) for k, v in json.load(f).items()}
            except (OSError, ValueError):
                self._local_grants = {}
        return self._local_grants.setdefault(str(save_id), set())

    def record_local_grant(self, save_id: int, code: int) -> None:
        self.granted_locally(save_id).add(code)
        os.makedirs(LOCAL_GRANTS_DIR, exist_ok=True)
        with open(self._grants_file(), "w", encoding="utf-8") as f:
            json.dump({k: sorted(v) for k, v in self._local_grants.items()}, f)

    def server_live(self) -> bool:
        """The server connection is open right now (the check CommonContext.send_msgs uses).
        `ready` alone stays True through an outage; this doesn't."""
        return bool(self.server and self.server.socket.open and not self.server.socket.closed)

    def pickup_name(self, m: dict) -> str:
        """What the Razor should say for this manifest spot: the item's name in capitals
        if it's one of ours, else ARCHIPELAGO ITEM (another player's, or unknown)."""
        item = self.local_items.get(self.location_id.get(m["location"], -1))
        if item is None:
            return REMOTE_NAME
        return self.item_names.lookup_in_game(item, GAME).upper()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.ready = False
        await super().disconnect(allow_autoreconnect)

    def log_spoiler(self) -> None:
        """Write every location of this world and what it holds to the log file (testing aid)."""
        order = {self.location_id[m["location"]]: i for i, m in enumerate(self.manifest)
                 if m["location"] in self.location_id}
        rows = []
        for code in sorted(self.server_locations, key=lambda c: (order.get(c, len(order)), c)):
            info = self.locations_info.get(code)
            location = self.location_names.lookup_in_game(code, GAME)
            if info is None:
                rows.append(f"  {location:62}  (not scouted)")
                continue
            item = self.item_names.lookup_in_slot(info.item, info.player)
            owner = "yours" if info.player == self.slot else f"for {self.player_names.get(info.player, info.player)}"
            mark = "*" if info.flags & 0b001 else " "        # * = progression
            rows.append(f"  {location:62} {mark} {item}  ({owner})")
        file_only(f"=== Spoiler: {len(rows)} locations in this world (* = progression) ===\n" + "\n".join(rows))

    def on_package(self, cmd: str, args: dict):
        if cmd == "LocationInfo" and self.spoiler_pending:
            self.spoiler_pending = False
            self.log_spoiler()
            return
        if cmd != "Connected":
            return
        self.ready = False
        slot_data = args.get("slot_data") or {}
        version = slot_data.get("apworld_version")
        if version != APWORLD_VERSION:
            msg = (f"apworld version mismatch: seed has {version!r}, client expects {APWORLD_VERSION!r}. "
                   "Regenerate the seed with the current apworld.")
            if not self.ignore_version:
                logger.error(msg + " Client will not touch the game. (--ignore-version to override)")
                return
            logger.warning(msg + " Continuing because of --ignore-version.")

        names = self.location_names[GAME]         # id -> name, from the server's data package
        by_name = {name: code for code, name in names.items()}
        self.location_id = {}
        for m in self.manifest:
            if m["location"] in by_name:
                self.location_id[m["location"]] = by_name[m["location"]]
            else:
                detail(f"Manifest location not in this seed: {m['location']}")
        self.start_ids = {chapter: [by_name[n] for n in names if n in by_name]
                          for chapter, names in START_CHECKS.items()}
        self.story_ids = {by_name[n]: (chapter, story) for chapter, checks in STORY_CHECKS.items()
                          for n, story in checks.items() if n in by_name}
        self.completion_ids = ([by_name[n] for n in COMPLETION_CHECKS]
                               if all(n in by_name for n in COMPLETION_CHECKS) else [])
        unmapped = ({code for code in names if code > 0} - set(self.location_id.values())
                    - {code for ids in self.start_ids.values() for code in ids} - set(self.story_ids))
        for code in sorted(unmapped):
            detail(f"Seed location with no flag in the manifest: {names[code]}")
        for code, name in sorted(self.item_names[GAME].items()):
            if code > 0 and grant_entry(name) is None:
                detail(f"Seed item the client can't grant: {name}")

        # Which spots hold our own items (apworld 0.0.3+). Missing on an older seed: every
        # spot is then treated as remote and named ARCHIPELAGO ITEM.
        self.local_items = {int(code): int(item) for code, item in (slot_data.get("local_items") or {}).items()}
        self.location_row = {self.location_id[m["location"]]: m for m in self.manifest
                             if m["location"] in self.location_id}
        self._local_grants = None                  # reloaded for this seed's fingerprint on first use

        seed = f"{self.server_seed_name}|{self.team}|{self.slot}"
        self.fingerprint = (zlib.crc32(seed.encode()) & 0xFFFFFFFF) or 1
        logger.info(f"MGS2 ready: {len(self.location_id)} locations mapped, {len(self.local_items)} hold your "
                    f"own items, fingerprint {self.fingerprint:#010x}")
        self.warned.clear()
        self.ready = True

        # Seed info and spoiler, to the log file only (kept while the game is being tested).
        file_only(f"Seed info: seed {self.server_seed_name}, slot {self.username!r} (#{self.slot}), "
                  f"team {self.team}, fingerprint {self.fingerprint:#010x}, apworld {version}, "
                  f"{len(self.server_locations)} locations, {len(self.local_items)} hold own items")
        if self.spoiler_logged_for != seed:
            self.spoiler_logged_for = seed
            self.spoiler_pending = True
            asyncio.create_task(self.send_msgs([{"cmd": "LocationScouts", "create_as_hint": 0,
                                                 "locations": sorted(self.server_locations)}]))

    def warn_once(self, key: str, msg: str) -> None:
        if key not in self.warned:
            self.warned.add(key)
            logger.warning(msg)

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "MGS2 Client (POC)"
        return ui


# --------------------------------------------------------------------------- the loop

# Real items the game hands out that are not locations (resupplies, scripted supplies, mines):
# (stages, inventory names or None for any, Plant story range or None, where they come from).
# Anything else that arrives from the game is logged as an enemy drop or supply box.
GAME_SUPPLIES = [
    ({"w11c"}, None, None, "the Fortune fight's resupply"),
    ({"w20b", "w20c", "w20d"}, None, (0x76, 0x76), "the Fatman fight's supplies"),
    ({"w31f"}, None, None, "the Vamp fight's supplies"),
    ({"w31c"}, None, (0, 0x101), "the Vamp fight's supplies"),
    ({"w32a", "w32b"}, None, None, "the Strut L sniping supplies"),
    ({"w25a"}, None, None, "the Harrier fight's supplies"),
    ({"w31a"}, {"Nikita (weapon)"}, None, "the Shell 2 Core Nikita Ammo resupply"),
    ({"w25d"}, {"Card"}, None, "the KL bridge scene (Card 5 is kept so the Level 5 door can't strand you; "
                               "the location check was sent separately)"),
    ({"w24d"}, {"Book (weapon)"}, None, "the books that fall off the locker"),
    ({"w21a", "w12c"}, {"Claymore (weapon)"}, None, "the Claymores placed on the bridge"),
    ({"w41a", "w42a", "w43a", "w44a", "w45a", "w46a", "w51a", "w61a"}, None, None,
     "Arsenal Gear (your inventory coming back, or its supplies)"),
]


def report_game_items(frame: Frame, before: dict[str, int], after: dict[str, int]) -> None:
    """Log every item the game itself added since the last tick, so a supply isn't taken for a missed location."""
    for name, count in after.items():
        old = before.get(name)
        if name == RAZOR or old is None or count == NOT_HELD:
            continue
        if old == NOT_HELD:
            what = f"{name.replace(' (weapon)', '')} (now held, {count})"
        elif count > old:
            what = f"{name.replace(' (weapon)', '')} +{count - old}"
        else:
            continue
        source = next((label for stages, names, story, label in GAME_SUPPLIES
                       if frame.stage in stages and (names is None or name in names)
                       and (story is None or story[0] <= frame.plant_story <= story[1])),
                      "an enemy drop or a supply box")
        logger.info(f"FROM GAME {what}: {source}. A real item, not a location check.")


async def game_loop(ctx: MGS2Context) -> None:
    game = ctx.game_mem
    last_stage = None
    stable_since = 0.0
    flag_state: dict[str, bool] = {}    # manifest location -> its flag last tick (None before the first read)
    first_frame = True
    last_inventory: dict[str, int] | None = None   # inventory at the end of the last tick, after our own writes
    namer = PickupNamer()               # which name the Razor shows (CLIENT_DESIGN.md, Presentation)

    while not ctx.exit_event.is_set():
        await asyncio.sleep(POLL_SECONDS)
        if not game.attached():
            continue
        try:
            frame = Frame(game)
        except mgs2mem.Mgs2NotReady:
            continue
        except Exception:
            if not _process_alive(game):
                game.detach()
            continue
        if not frame.consistent:
            continue

        now = time.time()
        if frame.stage != last_stage:
            detail(f"[stage {frame.stage}] story {frame.story}")
            last_stage, stable_since = frame.stage, now
        gameplay = frame.chapter is not None
        stable = gameplay and now - stable_since >= STABLE_SECONDS
        if not stable:
            last_inventory = None   # stage loads, saves loading, Arsenal confiscation: start a fresh baseline

        # Pickup name, which doubles as a connection light: ARCHIPELAGO ITEM only while the
        # server connection is live and this save belongs to the connected seed; otherwise
        # the game's own RAZOR. It's exe data, not stage data, so writing it during loads
        # is fine.
        if game.razor is not None:
            try:
                linked = ctx.ready and ctx.server_live() and frame.fingerprint == ctx.fingerprint
                if not linked:
                    # Only report the connection itself; another seed's save has its own warning.
                    if game.razor.restore() and not (ctx.ready and ctx.server_live()):
                        logger.info("Not connected to Archipelago. Pickups are kept and sent when you reconnect.")
                    namer = PickupNamer()
                elif not REAL_PICKUP_NAMES:
                    if game.razor.set(REMOTE_NAME):
                        logger.info("Connected to Archipelago.")
                else:
                    own_save = stable
                    position = game.mem.player_position() if own_save else None
                    was_held = namer.held
                    name = namer.update(ctx, frame, position, now, own_save)
                    changed = name is not None and game.razor.set(name)
                    if ctx.name_log and namer.held is not None and namer.held is not was_held:
                        logger.info(f"[names] picked up {namer.held['location']}: keeping "
                                    f"{game.razor.current!r} at {position}")
                    elif ctx.name_log and changed:
                        logger.info(f"[names] now {name!r} at {position}: {namer.why}")
            except Exception as e:
                ctx.warn_once(f"name-{type(e).__name__}", f"pickup name update failed ({e}); retrying")

        try:
            # Items the game handed out since the last tick (our own writes are in the baseline).
            if stable and ctx.ready and last_inventory is not None and frame.fingerprint == ctx.fingerprint:
                report_game_items(frame, last_inventory, game.mem.snapshot())

            # The patch already resets the Razor on pickup (max 50); this only tops up old
            # saves. Never write mid-load: a write during a transition is a crash suspect.
            if stable:
                if game.max(RAZOR, False) < RAZOR_MAX:
                    game.set_max(RAZOR, RAZOR_MAX, False)
                if 0 < game.count(RAZOR, False) < NOT_HELD:
                    game.set_count(RAZOR, 0, False)

            if not ctx.ready:
                continue

            # --- seed guard / new game
            if frame.fingerprint != ctx.fingerprint:
                if frame.fingerprint != 0:
                    ctx.warn_once("other-seed", f"This save belongs to a different seed "
                                  f"(fingerprint {frame.fingerprint:#010x}). Not touching it.")
                    continue
                if not stable:
                    continue
                reset_stash(game, frame.chapter)
                game.write_varbuf(CHAPTER_SLOT, "<B", frame.chapter)
                game.write_varbuf(FINGERPRINT, "<I", ctx.fingerprint)
                logger.info(f"New {CHAPTER_NAME[frame.chapter]} game started on this seed. "
                            f"Save after entering another area to keep it.")
                detail(f"  fingerprint written, N = {frame.n}.")
                continue                                    # re-read next tick

            # --- chapter switch: Tanker -> Plant in one save (or a save from before chapters existed)
            if stable and frame.save_chapter != frame.chapter:
                if frame.save_chapter == 0:                 # older client: N is already this chapter's
                    game.write_varbuf(CHAPTER_SLOT, "<B", frame.chapter)
                    continue
                reset_stash(game, frame.chapter)
                game.write_varbuf(N_SLOT, "<H", 0)
                game.write_varbuf(CHAPTER_SLOT, "<B", frame.chapter)
                logger.info(f"Save moved from the {CHAPTER_NAME.get(frame.save_chapter, '?')} to the "
                            f"{CHAPTER_NAME[frame.chapter]}: replaying received items for it.")
                continue

            # --- save id: keys this save's record of items given at pickup (local grants)
            if frame.save_id == 0:
                if stable:
                    save_id = random.randint(1, 255)
                    game.write_varbuf(SAVE_ID_SLOT, "<B", save_id)
                    detail(f"Save id {save_id} assigned (used to avoid granting an item twice).")
                continue                                    # re-read next tick

            # --- checks (only for the chapter this save is in)
            tanker = frame.save_chapter == TANKER
            new_ids = [code for code in ctx.start_ids.get(frame.save_chapter, [])
                       if code not in ctx.locations_checked]
            for code, (chapter, story) in ctx.story_ids.items():
                current = frame.story if chapter == TANKER else frame.plant_story
                if frame.save_chapter == chapter and current >= story and code not in ctx.locations_checked:
                    detail(f"CHECK {ctx.location_names.lookup_in_game(code, GAME)} (story {current:#x})")
                    new_ids.append(code)
            for m in ctx.manifest:
                if m["chapter"] != frame.save_chapter or m["location"] not in ctx.location_id:
                    continue
                now_set = frame.flag(m["flag"])
                was_set = flag_state.get(m["location"])
                flag_state[m["location"]] = now_set
                if not now_set:
                    continue
                code = ctx.location_id[m["location"]]
                already = code in ctx.locations_checked or code in ctx.checked_locations
                if not first_frame and was_set is False:          # picked up just now
                    if already:
                        logger.info(f"ALREADY CHECKED {m['location']}: picked up again after a reload, "
                                    f"so no new item is sent")
                    else:
                        detail(f"CHECK {m['location']}")
                    # One of our own items: give it now, even offline. (After a reload the
                    # save rolled back, N too, so the server's copy is processed again and
                    # skipped by the rule in the grants section.)
                    name = ctx.local_grant_name(code, frame.save_chapter)
                    if name and stable and frame.stage not in CONFISCATION_STAGES:
                        line = apply_grant(game, name, frame.save_chapter)
                        ctx.record_local_grant(frame.save_id, code)
                        detail(f"LOCAL GRANT {name}: {line}")
                elif first_frame and not already:
                    # Set before the client started: picked up while it was closed. The
                    # item comes from the server (nothing was given at pickup).
                    detail(f"CHECK {m['location']} (found while the client was closed)")
                if not already:
                    new_ids.append(code)
            if new_ids:
                ctx.locations_checked.update(new_ids)
                await ctx.check_locations(new_ids)
            first_frame = False

            # --- victory: both chapter clears checked on the server (or, for an older seed, the Tanker's ending)
            if not ctx.finished_game:
                if ctx.completion_ids:
                    done = ctx.checked_locations | ctx.locations_checked
                    won = all(code in done for code in ctx.completion_ids)
                else:
                    won = tanker and frame.story >= VICTORY_STORY
                if won:
                    ctx.finished_game = True
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    logger.info("VICTORY sent: " + ("Tanker and Plant cleared." if ctx.completion_ids
                                                    else f"Tanker story {frame.story}."))

            # --- grants
            if not stable:
                continue
            received = ctx.items_received
            n = frame.n
            if n > len(received):
                # Normal while disconnected (the received list is emptied until reconnect).
                if ctx.server_live():
                    ctx.warn_once(f"n-ahead-{n}", f"Game says {n} items processed but the server has sent "
                                  f"{len(received)}. Waiting.")
                last_inventory = game.mem.snapshot()
                continue
            chapter = frame.chapter                         # stable, so it equals the save's chapter
            if n < len(received) and frame.stage in CONFISCATION_STAGES:
                # Raiden has no gear here; items wait (N doesn't move) until w43a hands it back.
                ctx.warn_once(f"arsenal-hold-{len(received)}", f"Holding {len(received) - n} item(s) until "
                              f"the Arsenal gives your gear back.")
                last_inventory = game.mem.snapshot()
                continue
            flush_stash(game, chapter)
            skipped = 0
            replay_from_start = n == 0 and len(received) > 0   # new game, or a save moved to the other chapter
            while n < len(received):
                item = received[n]
                name = ctx.item_names.lookup_in_game(item.item, GAME)
                sender = ctx.player_names.get(item.player, f"player {item.player}")
                copies = sum(1 for earlier in received[:n + 1] if earlier.item == item.item)
                # One of our own items from a spot in this chapter: the flag says whether this
                # save has the spot; the record says whether it was given at pickup.
                row = ctx.location_row.get(item.location) if item.player == ctx.slot else None
                if row is not None and row["chapter"] == chapter and ctx.local_grant_name(item.location, chapter):
                    if frame.flag(row["flag"]) and item.location in ctx.granted_locally(frame.save_id):
                        line = "already given at pickup, skipped"
                    else:
                        line = apply_grant(game, name, chapter, copies)
                        if not frame.flag(row["flag"]):
                            game.mark_collected(row["flag"])    # so the spot can't give it again
                            # Our own write, not a pickup: without this the checks loop sees
                            # the flag go unset -> set next tick and grants the item again
                            # (2026-11-27: every replayed item in a fresh Plant game doubled).
                            flag_state[row["location"]] = True
                            line += "; spot marked collected"
                else:
                    line = apply_grant(game, name, chapter, copies)
                n += 1
                game.write_varbuf(N_SLOT, "<H", n)          # item first, counter second
                entry = grant_entry(name)
                if entry is None or entry[0] == chapter:
                    detail(f"GRANT #{n} {name} (from {sender}): {line}")
                else:
                    skipped += 1
            if skipped:
                detail(f"  {skipped} item(s) for the other chapter skipped; its save gets them.")
            if replay_from_start:
                given = len(received) - skipped
                other = CHAPTER_NAME[PLANT if chapter == TANKER else TANKER]
                logger.info(f"Re-granted the {given} item(s) received so far to this {CHAPTER_NAME[chapter]} save"
                            + (f" ({skipped} more are for your {other} save)." if skipped else "."))
            flush_stash(game, chapter)
            last_inventory = game.mem.snapshot()   # baseline includes our own grants
        except mgs2mem.Mgs2NotReady:
            continue
        except Exception as e:
            if not _process_alive(game):
                game.detach()
            else:
                ctx.warn_once(f"err-{type(e).__name__}", f"tick failed ({type(e).__name__}: {e}); retrying")

    game.release_name()        # client closing: the game says Razor again


def _process_alive(game: Game) -> bool:
    try:
        game.mem.pm.read_bytes(game.mem.module_base, 2)
        return True
    except Exception:
        return False


async def main(args) -> None:
    ctx = MGS2Context(args.connect, args.password, args.ignore_version)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    loop_task = asyncio.create_task(game_loop(ctx), name="game loop")
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    ctx.server_address = None
    loop_task.cancel()
    await ctx.shutdown()


if __name__ == "__main__":
    import colorama
    import logging

    logging.getLogger().setLevel(logging.INFO)
    parser = get_base_parser(description="MGS2 Archipelago client (POC)")
    parser.add_argument("--name", default=None, help="Slot name to connect as.")
    parser.add_argument("--ignore-version", action="store_true", help="Run even if the apworld version differs.")
    parser.add_argument("--debug", action="store_true",
                        help="Show detail messages (checks, grants, stage changes) in the window too. "
                             "They always go to the log file.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = handle_url_arg(parser.parse_args(), parser=parser)
    DEBUG = args.debug
    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()
