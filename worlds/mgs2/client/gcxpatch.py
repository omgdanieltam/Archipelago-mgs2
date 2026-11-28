"""
Read, modify and rebuild MGS2 stage scripts (.gcx), and assemble GCX bytecode.

File layout (all little-endian), confirmed on w01d:

    0x00  4   "LCGB"-style timestamp
    0x04  4   version
    0x08  8n  proc table: (proc id u32, offset into proc data u32), sorted by id
          8   zero terminator
    S     20  offset table: script offset, resource table, string table,
              font data, key -- all relative to S
    S+20  ..  resources / strings (untouched)
    S+so  4   proc data size
          ..  proc data (each proc's table offset points here)
          4   main size
          ..  main
          ..  trailing bytes (kept verbatim)

The offset table is relative to its own start, so growing the proc table only
shifts it. The randomizer relies on the same (GcxEditor.BuildGcxFile).

Bytecode: each element is a type nibble plus a length; nibble D means a 1-byte
length follows, E a 2-byte length. Containers end with 0x00. Expressions are
postfix. Types seen:

    3  expression      5  parameter ('letter' + value)
    6  command         7  proc call (id + args)
    8  block (proc body or lambda)

Values: 0xC1 + n for 0..62; 01 u16; 06 u24 (hashes, spawn ids); 4n = $argn.
Operators: AB ==, AD <, B5 &&, B4 ||, B6 assign; A0 ends an expression.
Variables: 11 80 hi lo = linkvarbuf scalar; 21 80 hi lo len idx = linkvarbuf
word array; 22 00 hi lo len idx = varbuf byte array (offsets big-endian).
"""

import struct

# ---------------------------------------------------------------- file format


class Gcx:
    def __init__(self, raw: bytes):
        self.header = raw[:8]
        table: list[tuple[int, int]] = []
        p = 8
        while raw[p:p + 8] != bytes(8):
            table.append(struct.unpack_from("<II", raw, p))
            p += 8
        strres = p + 8
        script_offset = struct.unpack_from("<I", raw, strres)[0]
        size_at = strres + script_offset
        proc_size = struct.unpack_from("<I", raw, size_at)[0]
        data_at = size_at + 4
        main_size = struct.unpack_from("<I", raw, data_at + proc_size)[0]
        main_at = data_at + proc_size + 4

        self.table = table
        self.strres = raw[strres:size_at]
        self.procs = bytearray(raw[data_at:data_at + proc_size])
        self.main = raw[main_at:main_at + main_size]
        self.trailing = raw[main_at + main_size:]

    def ids(self) -> set[int]:
        return {proc_id for proc_id, _ in self.table}

    def proc_bytes(self, proc_id: int) -> bytes:
        offset = dict(self.table)[proc_id]
        return bytes(self.procs[offset:offset + element_length(self.procs, offset)])

    def add_proc(self, proc_id: int, body: bytes) -> None:
        if proc_id in self.ids():
            raise ValueError(f"proc {proc_id:#x} already exists")
        if proc_id > 0xFFFFFF:
            raise ValueError("proc ids are 24-bit")
        self.table.append((proc_id, len(self.procs)))
        self.table.sort()
        self.procs += body

    def build(self) -> bytes:
        out = bytearray(self.header)
        for proc_id, offset in self.table:
            out += struct.pack("<II", proc_id, offset)
        out += bytes(8)
        out += self.strres
        out += struct.pack("<I", len(self.procs)) + self.procs
        out += struct.pack("<I", len(self.main)) + self.main
        out += self.trailing
        return bytes(out)


def element_length(data: bytes, at: int) -> int:
    """Total length (header included) of the element starting at `at`."""
    nibble = data[at] & 0x0F
    if nibble == 0x0D:
        return 2 + data[at + 1]
    if nibble == 0x0E:
        return 3 + struct.unpack_from("<H", data, at + 1)[0]
    return 1 + nibble


# ---------------------------------------------------------------- assembler


def element(kind: int, payload: bytes) -> bytes:
    n = len(payload)
    if n <= 0x0C:
        return bytes([kind << 4 | n]) + payload
    if n <= 0xFF:
        return bytes([kind << 4 | 0x0D, n]) + payload
    if n <= 0xFFFF:
        return bytes([kind << 4 | 0x0E]) + struct.pack("<H", n) + payload
    raise ValueError("element too long")


def value(v: int) -> bytes:
    if 0 <= v <= 0x3E:
        return bytes([0xC1 + v])
    if 0 <= v <= 0xFFFF:
        return b"\x01" + struct.pack("<H", v)
    if 0 <= v <= 0xFFFFFF:
        return b"\x06" + v.to_bytes(3, "little")
    raise ValueError(f"value {v:#x} out of range")


def arg(n: int) -> bytes:
    return bytes([0x40 + n])


def varbuf_byte(offset: int) -> bytes:
    """varbuf_<offset>[0,1]: a one-element byte array at varbuf + offset."""
    return b"\x22\x00" + offset.to_bytes(2, "big") + value(1) + value(0)


def linkvar_scalar(offset: int) -> bytes:
    return b"\x11\x80" + offset.to_bytes(2, "big")


EQ, LT, AND, OR, ASSIGN, END = b"\xab", b"\xad", b"\xb5", b"\xb4", b"\xb6", b"\xa0"


def expr(*parts: bytes) -> bytes:
    return element(3, b"".join(parts) + END)


def block(*statements: bytes) -> bytes:
    return element(8, b"".join(statements) + b"\x00")


def param(letter: str, *values: bytes) -> bytes:
    return element(5, letter.encode() + b"".join(values))


def call(proc_id: int, *args: bytes) -> bytes:
    return element(7, proc_id.to_bytes(3, "little") + b"".join(args) + b"\x00")


CMD_IF = 0x000D86
CMD_CHARA = 0x6592A7


def command(cmd: int, args: bytes, *params: bytes) -> bytes:
    return element(6, cmd.to_bytes(3, "little") + bytes([len(args)]) + args + b"".join(params) + b"\x00")


def if_(condition: bytes, body: bytes) -> bytes:
    return command(CMD_IF, condition + body)


# ---------------------------------------------------------------- item pickups

ITEM_ACTOR = 0x9AFF54        # .chara type used by every award proc
PICKUP_TIMER = 0x12C         # 'h' param, identical in every award proc seen
LINK_LOAD_COUNTER = 0x4CA    # area-load counter; vanilla stores it on pickup


def pickup(model: int, shadow: int, label: int, kind: int, item: int, count: bytes,
           callback: bytes | None = None) -> bytes:
    """The .chara item-actor command every award proc uses. Args follow the
    spawn call: $arg1 spawn id, $arg2-4 position, $arg5 rotation."""
    params = [
        param("b", value(0)),
        param("p", arg(2), arg(3), arg(4)),
        param("k", value(model)),
        param("s", value(shadow)),
        param("l", value(label)),
        param("f", value(kind)),
        param("i", value(item)),
        param("n", count),
        param("r", arg(5)),
        param("h", value(PICKUP_TIMER)),
    ]
    if callback is not None:
        params.append(param("x", callback))
    return command(CMD_CHARA, value(ITEM_ACTOR) + arg(1), *params)


def marker_proc(flag: int, model: int, shadow: int, label: int, item: int,
                on_pickup: tuple[bytes, ...] = ()) -> bytes:
    """AP marker: spawns only while varbuf[flag] == 0, awards 1 of `item`, and on
    pickup stores the area-load counter (>= 0x80) in varbuf[flag] -- the same
    convention as vanilla collected fields, so readers treat both alike.
    `on_pickup` statements run in the pickup callback after the flag write."""
    collected = block(expr(varbuf_byte(flag), linkvar_scalar(LINK_LOAD_COUNTER), ASSIGN), *on_pickup)
    spawn = pickup(model, shadow, label, kind=0, item=item, count=value(1), callback=collected)
    return block(if_(expr(varbuf_byte(flag), value(0), EQ), block(spawn)))
