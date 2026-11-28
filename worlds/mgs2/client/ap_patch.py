"""
POC patcher: turn every Tanker and Plant world pickup into an AP marker.

For each spawn in spawn_fields.json, the stage script's spawn call

    proc_<vanilla award> (<spawn id>, x, y, z, r, ...)

is redirected (same length, only the 3-byte proc id changes) to a new proc
built by gcxpatch.marker_proc:

    if (varbuf[flag] == 0) {
        item actor with the vanilla item's look, awards 1 Razor,
        on pickup: varbuf[flag] = area-load counter (>= 0x80)
    }

`flag` is the location's byte from FLAG_MAP.md: the collected field the game
reserved for the spawn where there is one (its vanilla guard keeps working),
otherwise one of our bytes at varbuf 0x280+.

The vanilla award proc is no longer called, so its own conditions (difficulty
inside the proc, "holds no Wet Box", ...) and its callback no longer apply.
Conditions *around* the spawn call stay, except:

    - "Snake/Raiden holds no item N" around a spawn (w01d pantry Box, the
      Plant's backup Thermals, Mine Detector, ...) becomes varbuf[flag] == 0,
      so an AP grant can't hide the marker.
    - w04a LeftLadder2 (a backup Thermal Goggles, not an AP location) is
      redirected to an empty proc so it can never hand out vanilla Thermals.

Difficulty and NG+ gates around spawn calls are kept, so on Normal the
NOT_ON_NORMAL spots simply never appear. A spawn the catalogue lists twice
(same spawn id) is one location; ALIAS spawns share another spawn's flag.
"Variant" rows (gen_fields.STAGE_FAMILIES) are the same pickup in a sibling
stage file of the same area (e.g. w16b, the Dining Hall after Stillman): their
call is patched to the same marker and flag, and they add no location.

Beyond the world spawns (EXTRA below, all same-length byte edits):

    - n_title: the Tanker start kit is emptied in all 5 initialize arrays
      (M9 -> not held; Cigarettes, Camera, A.P. Sensor -> 0).
    - w00a: the two Camera writes (Camera = 0 on arrival from the intro,
      Camera = 1 at story 14) now write Razor = 0, which is harmless; and
      the pad-demo menu no longer equips the M9 / Cigarettes / Cutscene
      Camera (the randomizer's FixW00aDemoBug).
    - n_title: Raiden's start kit (Binoculars, A.P. Sensor) is emptied the
      same way; the client sends the Plant Start checks.

Scripted rewards (REWARDS below): each item write in the reward script
becomes a call to a new proc that sets the reward's flag and gives nothing:
Olga's USP, the Plant's SOCOM (+ Pliskin's Cigarettes), Coolant, Sensor A,
B.D.U., Phone, M.O. Disc and the five card levels.

Writes ap_manifest.json (location -> stage, flag) for the client.

Usage:
    python ap_patch.py --dry-run          # build everything, write nothing to the game
    python ap_patch.py --apply            # close the game first
    python ap_patch.py --restore          # put every vanilla stage file back
"""

import argparse
import json
import os
import re
import shutil
import struct

import gcxpatch as g

DEFAULT_INSTALL = r"C:\Program Files (x86)\Steam\steamapps\common\MGS2"
GCX_DIR = os.path.join("assets", "gcx", "eu", "_bp")
ROOT = os.path.dirname(os.path.abspath(__file__))
FIELDS_JSON = os.path.join(ROOT, "spawn_fields.json")
MANIFEST = os.path.join(ROOT, "ap_manifest.json")

RAZOR = 28
MARKER_BASE = 0xA90000          # marker proc id = MARKER_BASE | flag
EMPTY_PROC = 0xA9FFFF           # suppressed spawns call this

SUPPRESS = {("w04a", "LeftLadder2")}   # backup Thermal Goggles; not an AP location

# Uncatalogued spawn calls that must give nothing (redirected to EMPTY_PROC).
SUPPRESS_CALLS = {
    "w32a": [0x33C73D],   # Strut L sniping: backup Thermal Goggles (only without Thermals); AP gives them
}

# A spot whose spawn id is shared with another location: these calls go to `to`'s marker.
REASSIGN_CALLS = {
    # Shell 1-2 bridge, 2nd Front fire spot: PSG1-T Ammo if the PSG1-T is held, else PSG1
    # Ammo with the 1st spot's spawn id. Call 1 of FrontFire is that else-branch.
    ("w25b", "FrontFire"): {1: "FrontFire#2"},
}

# Inline item actors (.chara(ITEM_ACTOR, id) written in the script, not an award-proc call):
# item -> Razor, and the pickup callback's `varbuf[flag] = 1` -> a call to a proc setting the
# flag to the area-load counter (>= 0x80, like every flag) and resetting the Razor.
INLINE_SPAWNS = {
    # positions: the actor's own 'p' param (x, height, y), as there's no spawn call to read.
    "w41a": [{"spawn": "ColdMedicine", "spawn_id": 0x1D18015, "flag": 0x988, "vanilla_item": "ColdMeds",
              "ap_name": "Arsenal Stomach - Cold Medicine (Torture room)", "positions": [[2500, 200, -7200]]}],
}

# Spots that never appear on a Normal new game (TASKS.md §1.16; Plant from NORMAL_LOCATIONS.md).
NOT_ON_NORMAL = {
    ("w00a", "NearSnakeSpawn"): "Very Easy only",
    ("w00a", "Overlook"): "Hard and up",
    ("w01e", "NearLeftDoor"): "Easy and below",
    ("w00c", "CrowsNest2"): "NG+ only",
    ("w11a", "WhiteCrates1"): "Easy and below",
    ("w11a", "WhiteCrates2"): "Easy and below",
    ("w11a", "UnderWireRack"): "Very Easy only",
    ("w11a", "DivingCage"): "Hard and up",
    ("w12a", "LeftCage"): "Easy and below",
    ("w12b", "UnderPipes"): "Easy and below",
    ("w14a", "BottomSideElectrical"): "Very Easy only",
    ("w22a", "AKRoom1"): "Very Easy only",
    ("w24a", "LockerRoom1"): "Very Easy only",
}

# Alternatives at one spot share one location: the ammo spawns only once the
# suppressor is held, the suppressor otherwise.
ALIAS = {
    ("w25b", "BehindFireHaveAkSupp"): ("w25b", "BehindFireOtherwise"),   # AK Suppressor / AKS-74u Ammo
    ("w22a", "RoomAcrossNode3.2"): ("w22a", "RoomAcrossNode2"),          # SOCOM Suppressor / SOCOM Ammo (story >= 0x74)
}


def assign(array: int, size: int, slot: int, value: int) -> bytes:
    """The statement `linkvarbuf_<array>[slot,size] = value` as script bytes."""
    return g.expr(b"\x21\x80" + array.to_bytes(2, "big") + g.value(size) + g.value(slot), g.value(value), g.ASSIGN)


SNAKE_WEAPONS, SNAKE_ITEMS, RAIDEN_WEAPONS, RAIDEN_ITEMS = 0x15C, 0x1EC, 0x2AC, 0x33C
# Slots are offsets.WEAPONS / offsets.ITEMS position + 1.
SOCOM, COOLANT = 3, 14
CIGARETTES, SENSOR_A, BDU, PHONE, MO_DISC, CARD = 17, 10, 6, 20, 34, 18

# Scripted rewards: AP location -> (stages and the vanilla writes there, give the item anyway).
# Each write becomes a call to a proc that sets the location's flag (from spawn_fields.json).
REWARDS: dict[str, tuple[dict[str, list[tuple[bytes, int]]], bool]] = {
    "Navigational Deck - Olga (Reward)": ({
        "w00c": [(assign(SNAKE_WEAPONS, 36, 2, 0), 1)],                # USP = 0 (owned, empty)
    }, False),
    "Strut B Transformer Room - Pliskin SOCOM": ({
        "d010p01": [(assign(RAIDEN_WEAPONS, 36, SOCOM, 13), 1)],
        "w14a": [(assign(RAIDEN_WEAPONS, 36, SOCOM, 13), 2),
                 (assign(RAIDEN_ITEMS, 48, CIGARETTES, 1), 2)],       # Cigarettes come from AP too
    }, False),
    "Strut C Dining Hall - Stillman Coolant": ({
        "w16a": [(assign(RAIDEN_WEAPONS, 36, COOLANT, 1), 1)],
        "w16b": [(assign(RAIDEN_WEAPONS, 36, COOLANT, 1), 1)],
    }, False),
    "Strut C Dining Hall - Stillman Sensor A": ({
        "w16a": [(assign(RAIDEN_ITEMS, 48, SENSOR_A, 1), 1)],
        "w16b": [(assign(RAIDEN_ITEMS, 48, SENSOR_A, 1), 1)],
    }, False),
    "Strut E Heliport - B.D.U.": ({
        stage: [(assign(RAIDEN_ITEMS, 48, BDU, 1), 1)] for stage in ("w20b", "w20c", "w20d")
    }, False),
    "Strut E Heliport - Phone": ({
        **{stage: [(assign(RAIDEN_ITEMS, 48, PHONE, 1), 1)] for stage in ("w20b", "w20c", "w20d")},
        "d021p01": [(assign(RAIDEN_ITEMS, 48, PHONE, 1), 1)],
    }, False),
    "Shell 2 Core - M.O. Disc": ({
        "w31a": [(assign(RAIDEN_ITEMS, 48, MO_DISC, 1), 1)],
    }, False),
    # Card level = count of item slot 18; each card reward sets the level outright.
    "Strut C Dining Hall - Stillman Progressive Card": ({
        "w16a": [(assign(RAIDEN_ITEMS, 48, CARD, 1), 1)],
        "w16b": [(assign(RAIDEN_ITEMS, 48, CARD, 1), 1)],
    }, False),
    "Strut E Heliport - Progressive Card": ({
        stage: [(assign(RAIDEN_ITEMS, 48, CARD, 2), 1)] for stage in ("w20b", "w20c", "w20d")
    }, False),
    "Shell 1 Core Hostage Room - Progressive Card": ({
        "w24b": [(assign(RAIDEN_ITEMS, 48, CARD, 3), 1)],             # Ames, story 0xB0-0xB2
    }, False),
    "Shell 2 Core - Progressive Card": ({
        "w31a": [(assign(RAIDEN_ITEMS, 48, CARD, 4), 1)],
    }, False),
    # Kept (owner's call, 2026-11-16): without Card 5 the scene leaves you stuck behind a
    # Level 5 door. The proc sets the flag and re-does Card = 5. Gating the scene on
    # Card 5 instead is noted for later (APWORLD_PENDING.md, "Card 5 softlock").
    "KL Connecting Bridge with Emma - Progressive Card": ({
        "w25d": [(assign(RAIDEN_ITEMS, 48, CARD, 5), 1)],
    }, True),
}
# The stage a reward's check belongs to (the client reads it only in a save of that chapter).
REWARD_STAGE = {
    "Navigational Deck - Olga (Reward)": "w00c",
    "Strut B Transformer Room - Pliskin SOCOM": "w14a",
    "Strut C Dining Hall - Stillman Coolant": "w16a",
    "Strut C Dining Hall - Stillman Sensor A": "w16a",
    "Strut E Heliport - B.D.U.": "w20b",
    "Strut E Heliport - Phone": "w20b",
    "Shell 2 Core - M.O. Disc": "w31a",
    "Strut C Dining Hall - Stillman Progressive Card": "w16a",
    "Strut E Heliport - Progressive Card": "w20b",
    "Shell 1 Core Hostage Room - Progressive Card": "w24b",
    "Shell 2 Core - Progressive Card": "w31a",
    "KL Connecting Bridge with Emma - Progressive Card": "w25d",
}

# The Razor works with no client running: every marker pickup sets both characters'
# Razor count back to 0, and n_title raises its max from 1 to RAZOR_MAX in every
# inventory-max init table. The max covers a callback that runs before the item is
# added (the count then sits at 1); with a max of 1 the next marker would be refused.
RAZOR_RESET = (assign(SNAKE_ITEMS, 48, RAZOR, 0), assign(RAIDEN_ITEMS, 48, RAZOR, 0))
RAZOR_MAX = 50
SNAKE_ITEM_MAX, RAIDEN_ITEM_MAX = 0x24C, 0x39C
MAX_INIT = bytes.fromhex("083506974fc7")       # .command(0xC74F97, <array>[0,48], max per slot...)


def apply_razor_max(raw: bytes) -> tuple[bytes, list[str]]:
    raw = bytearray(raw)
    patched = 0
    for array in (SNAKE_ITEM_MAX, RAIDEN_ITEM_MAX):
        head = MAX_INIT + b"\x21\x80" + array.to_bytes(2, "big") + g.value(48) + g.value(0)
        for at in _find_all(bytes(raw), head):
            slot = at + len(head) + RAZOR                   # every value before it is one byte
            if any(b < 0xC1 for b in raw[at + len(head):slot + 1]) or raw[slot] != g.value(1)[0]:
                raise SystemExit(f"n_title: unexpected max table at {at:#x}")
            raw[slot] = g.value(RAZOR_MAX)[0]
            patched += 1
    if patched != 11:
        raise SystemExit(f"n_title: expected 11 inventory-max tables, found {patched}")
    return bytes(raw), [f"  Razor max 1 -> {RAZOR_MAX} ({patched} tables)"]


KIT_ITEMS = bytes.fromhex("218001ecf1c1c2" + "c1" * 16 + "c2" + "c1" * 3 + "c2" + "c1" * 3 + "1406027d")
# Raiden: Binoculars (slot 14) = 1, A.P. Sensor (slot 25) = varbuf_0x27D, like Snake's.
RAIDEN_KIT_ITEMS = bytes.fromhex("2180033cf1c1c2" + "c1" * 13 + "c2" + "c1" * 10 + "1406027d")
# Boss-fight supplies (the drops when a fight starts, and the trap that re-spawns them
# while you're low) stay vanilla and are not locations; gen_fields.FIGHT_SUPPLIES keeps
# them out. The exception is the Fortune fight, which reuses two Sea Dock spots that are
# locations (also on the floor before the fight, in w11b):
#   - The first call is the location (marker). Later calls are the resupply: vanilla.
#   - The spot sets a "resupply item out" flag (varbuf_0x33B kinds) that only its vanilla
#     pickup clears. A marker pickup doesn't, which would end the resupply for the rest
#     of the fight, so that write becomes 0.
FIGHT_DROPS = {
    "w11c": {"LateRation", "LateSocomAmmo2"},                        # Fortune
    # Shell 2 Core: two one-time Nikita Ammo spots; a trap re-drops Nikita Ammo there while the
    # Nikita has <= 0 rounds (so you can always reach the President). Same layout as Fortune.
    "w31a": {"CameraRoomConditional", "RightsideStairsConditional"},
}

def is_flag_set(stmt: bytes) -> bool:
    """`$var:varbuf_<n> = 1` as stage bytes: 37 14 <kind> <offset:2> c2 b6 a0."""
    return len(stmt) == 8 and stmt[:2] == b"\x37\x14" and stmt[5:] == b"\xc2\xb6\xa0"

# linkvarbuf_0x106 is the equipped item (an item slot). Stillman's scene (story 0x4F)
# equips Sensor A right after giving it; the gift is patched out, so it would equip an
# item held 0 times. Suspected in a crash there (2026-10-17); it now unequips instead.
EQUIPPED = 0x106
EQUIP_SENSOR_A = g.expr(g.linkvar_scalar(EQUIPPED), g.value(SENSOR_A), g.ASSIGN)
UNEQUIP = g.expr(g.linkvar_scalar(EQUIPPED), g.value(0), g.ASSIGN)

EXTRA: dict[str, list[tuple[str, bytes, bytes, int]]] = {
    # (what, vanilla bytes, patched bytes, expected matches)
    **{stage: [("Stillman: don't equip Sensor A (not given any more)", EQUIP_SENSOR_A, UNEQUIP, 1)]
       for stage in ("w16a", "w16b")},
    # Warehouse SOCOM Suppressor / SOCOM Ammo (one location, ALIAS): the ammo branch runs
    # when the suppressor branch doesn't (engine bit linkvarbuf_0x114 & 16, probably
    # "suppressor attached") and waited for story 0x74. Gate -> story >= 0, so the spot's
    # one check is there from the start either way. Bytes: the gate, then its guard call.
    "w22a": [("SOCOM Suppressor / Ammo spot: ammo branch story >= 0x74 -> >= 0",
              bytes.fromhex("3811000068" "0274" "b0a0" "8d337a235b08" "22000761fdca"),
              bytes.fromhex("3811000068" "0200" "b0a0" "8d337a235b08" "22000761fdca"), 1)],
    "n_title": [
        ("start kit weapons: M9 -> not held",
         bytes.fromhex("2180015ce5c1c2" "11000a5c"), bytes.fromhex("2180015ce5c1c2" "06ffff00"), 5),
        ("start kit items: Cigarettes, Camera, A.P. Sensor -> 0",
         KIT_ITEMS, bytes.fromhex("218001ecf1c1c2" + "c1" * 24 + "06000000"), 5),
        ("Raiden start kit items: Binoculars, A.P. Sensor -> 0",
         RAIDEN_KIT_ITEMS, bytes.fromhex("2180033cf1c1c2" + "c1" * 24 + "06000000"), 5),
    ],
    "w00a": [
        ("Camera = 0 on arrival -> Razor = 0",
         bytes.fromhex("39218001ecf1d6c1b6a0"), bytes.fromhex("39218001ecf1ddc1b6a0"), 1),
        ("Camera = 1 at story 14 -> Razor = 0",
         bytes.fromhex("39218001ecf1d6c2b6a0"), bytes.fromhex("39218001ecf1ddc1b6a0"), 1),
        ("pad demo: don't equip M9",
         bytes.fromhex("4706863aa2526ec25363c2c200"), bytes.fromhex("4706863aa2526ec25363c1c100"), 1),
        ("pad demo: don't equip Cigarettes / Cutscene Camera",
         bytes.fromhex("4706863aa2526ec4547001000257" "63c1d2c1c1c1e000"),
         bytes.fromhex("4706863aa2526ec4547001000257" "63c1c1c1c1c1c100"), 1),
    ],
}


def apply_extra(raw: bytes, stage: str) -> tuple[bytes, list[str]]:
    notes = []
    for what, old, new, expected in EXTRA.get(stage, []):
        if len(old) != len(new):
            raise SystemExit(f"{stage} {what}: patch is not the same length")
        found = raw.count(old)
        if found != expected:
            raise SystemExit(f"{stage} {what}: expected {expected} match(es), found {found}")
        raw = raw.replace(old, new)
        notes.append(f"  {what} ({found}x)")
    return raw, notes


def stage_path(install: str, stage: str) -> str:
    return os.path.join(install, GCX_DIR, f"scenerio_stage_{stage}.gcx")


# ---------------------------------------------------------------- bytecode reading


def read_value(data: bytes, at: int) -> tuple[int, int]:
    """Decode one value element; returns (value, length)."""
    tag = data[at]
    if tag >= 0xC1:
        return tag - 0xC1, 1
    if tag == 0x01:
        return struct.unpack_from("<H", data, at + 1)[0], 3
    if tag == 0x06:
        return int.from_bytes(data[at + 1:at + 4], "little"), 4
    if tag in (0x09, 0x0D):
        return struct.unpack_from("<I", data, at + 1)[0], 5
    raise ValueError(f"unknown value tag {tag:#04x} at {at:#x}")


def look_of(proc: bytes) -> tuple[int, int, int]:
    """The k/s/l (model, shadow, label) params of the award proc's item actor."""
    found = dict.fromkeys("ksl")
    for at in range(len(proc) - 2):
        if proc[at] & 0xF0 == 0x50 and chr(proc[at + 1]) in "ksl" and found[chr(proc[at + 1])] is None:
            try:
                found[chr(proc[at + 1])], _ = read_value(proc, at + 2)
            except ValueError:
                pass
    if None in found.values():
        raise ValueError(f"award proc has no complete k/s/l look: {found}")
    return found["k"], found["s"], found["l"]


HOLDS = re.compile(r"(Snake|Raiden) holds no item (\d+)")
HOLDS_NO_WEAPON = re.compile(r"linkvarbuf_0x(15C|2AC)\[(\d+),36\] == -1")
NOT_HELD = 0xC0                    # the value element for -1


def holds_no_item(who: str, slot: int) -> bytes:
    """The operand sequence `linkvarbuf_<items>[slot,48] == 0` (inside any condition)."""
    array = SNAKE_ITEMS if who == "Snake" else RAIDEN_ITEMS
    return b"\x21\x80" + array.to_bytes(2, "big") + g.value(48) + g.value(slot) + g.value(0) + g.EQ


def holds_no_weapon(array: int, slot: int) -> bytes:
    """The operand sequence `linkvarbuf_<weapons>[slot,36] == -1`."""
    return b"\x21\x80" + array.to_bytes(2, "big") + g.value(36) + g.value(slot) + bytes([NOT_HELD]) + g.EQ


def ownership_checks(condition: str) -> list[tuple[str, bytes]]:
    """(label, operand bytes) for every "doesn't hold X" test in a spawn condition."""
    found = [(f"{who} holds no item {slot}", holds_no_item(who, int(slot)))
             for who, slot in HOLDS.findall(condition)]
    found += [(f"{'Raiden' if array == '2AC' else 'Snake'} holds no weapon {slot}",
               holds_no_weapon(int(array, 16), int(slot)))
              for array, slot in HOLDS_NO_WEAPON.findall(condition)]
    return found


def reward_proc(flag: int, keep: bytes | None) -> bytes:
    """Sets the reward's flag like a pickup does; `keep` re-does the vanilla write."""
    body = [g.expr(g.varbuf_byte(flag), g.linkvar_scalar(g.LINK_LOAD_COUNTER), g.ASSIGN)]
    if keep is not None:
        body.append(keep)
    return g.block(*body)


def apply_rewards(raw: bytes, stage: str, flags: dict[str, int]) -> tuple[bytes, list[tuple[int, bytes]], list[str]]:
    """Replace each reward write with a call to its flag proc; returns the procs to add."""
    procs, notes = [], []
    for name, (sites, keep) in REWARDS.items():
        if stage not in sites:
            continue
        flag = flags[name]
        proc_id = MARKER_BASE | flag
        for old, expected in sites[stage]:
            new = g.call(proc_id, g.value(0x80), g.value(0), g.value(0))   # args are padding
            if len(new) != len(old):
                raise SystemExit(f"{stage} {name}: call is {len(new)} bytes, write is {len(old)}")
            found = raw.count(old)
            if found != expected:
                raise SystemExit(f"{stage} {name}: expected {expected} match(es), found {found}")
            raw = raw.replace(old, new)
            notes.append(f"  {name} -> flag {flag:#05x} ({found}x{', item kept' if keep else ''})")
        procs.append((proc_id, reward_proc(flag, sites[stage][0][0] if keep else None)))
    return raw, procs, notes


def apply_inline(raw: bytes, stage: str) -> tuple[bytes, list[tuple[int, bytes]], list[str]]:
    """Turn each INLINE_SPAWNS actor into a marker; returns the flag procs to add."""
    procs, notes = [], []
    raw = bytearray(raw)
    for spot in INLINE_SPAWNS.get(stage, []):
        head = g.ITEM_ACTOR.to_bytes(3, "little") + b"\x0d" + spot["spawn_id"].to_bytes(4, "little")
        at = _find_all(bytes(raw), head)
        if len(at) != 1:
            raise SystemExit(f"{stage} {spot['spawn']}: expected one inline actor, found {len(at)}")
        body = at[0] + len(head)
        window = bytes(raw[body:body + 0x60])
        item = window.find(b"\x52\x69")                                   # .param('i') { <value> }
        flag_set = b"\x37\x12\x00" + spot["flag"].to_bytes(2, "big") + b"\xc2\xb6\xa0"   # varbuf[flag] = 1
        callback = window.find(flag_set)
        if item < 0 or callback < 0 or window[item + 2] < 0xC1:
            raise SystemExit(f"{stage} {spot['spawn']}: inline actor layout not as expected")
        raw[body + item + 2] = g.value(RAZOR)[0]
        proc_id = MARKER_BASE | spot["flag"]
        call = g.call(proc_id, g.value(0x80))                             # arg is padding
        if len(call) != len(flag_set):
            raise SystemExit(f"{stage} {spot['spawn']}: call is {len(call)} bytes, write is {len(flag_set)}")
        raw[body + callback:body + callback + len(call)] = call
        procs.append((proc_id, g.block(g.expr(g.varbuf_byte(spot["flag"]),
                                              g.linkvar_scalar(g.LINK_LOAD_COUNTER), g.ASSIGN), *RAZOR_RESET)))
        notes.append(f"  {spot['spawn']:<28} flag {spot['flag']:#05x}  inline actor -> Razor")
    return bytes(raw), procs, notes


# ---------------------------------------------------------------- patching


def patch_stage(raw: bytes, stage: str, rows: list[dict],
                reward_flags: dict[str, int] | None = None) -> tuple[bytes, list[str]]:
    raw, notes = apply_extra(raw, stage)
    if stage == "n_title":
        raw, max_notes = apply_razor_max(raw)
        notes += max_notes
    raw, procs, reward_notes = apply_rewards(raw, stage, reward_flags or load_reward_flags())
    notes += reward_notes
    raw, inline_procs, inline_notes = apply_inline(raw, stage)
    notes += inline_notes
    script = g.Gcx(raw)
    script.main = bytearray(script.main)
    for proc_id, body in procs + inline_procs:
        script.add_proc(proc_id, body)
    empty_needed = False
    moved: dict[str, list] = {}                 # REASSIGN_CALLS: spawn -> calls taken from another row

    for r in rows:
        key = (stage, r["spawn"])
        hits, ends = [], []
        for region in (script.procs, script.main):
            for at, _, end in call_sites(region, r["spawn_id"]):
                hits.append((region, at))
                ends.append(end)
        if not hits:
            raise SystemExit(f"{stage} {r['spawn']}: no spawn call for {r['spawn_id']:#x}")
        for n, to in REASSIGN_CALLS.get(key, {}).items():
            if n >= len(hits):
                raise SystemExit(f"{stage} {r['spawn']}: no call {n} to reassign to {to}")
            moved.setdefault(to, []).append(hits[n])
        if key in REASSIGN_CALLS:
            keep_calls = [n for n in range(len(hits)) if n not in REASSIGN_CALLS[key]]
            hits, ends = [hits[n] for n in keep_calls], [ends[n] for n in keep_calls]
        resupply = []
        if r["spawn"] in FIGHT_DROPS.get(stage, ()):
            # The drop is the first call; it must be followed by its "item out" flag write.
            (region, _), end = hits[0], ends[0]
            if not is_flag_set(bytes(region[end:end + 8])):
                raise SystemExit(f"{stage} {r['spawn']}: no resupply flag write after the drop")
            region[end + 5] = 0xC1                                    # `= 1` -> `= 0`
            resupply, hits = hits[1:], hits[:1]
        awards = {int.from_bytes(region[at:at + 3], "little") for region, at in hits}
        if len(awards) != 1:
            raise SystemExit(f"{stage} {r['spawn']}: calls go to several procs {sorted(map(hex, awards))}")
        award = awards.pop()
        if g.ITEM_ACTOR.to_bytes(3, "little") not in script.proc_bytes(award):
            raise SystemExit(f"{stage} {r['spawn']}: proc {award:#x} is not an item award proc")
        taken = moved.pop(r["spawn"], [])        # REASSIGN_CALLS: another row's calls for this spot
        hits += taken

        if key in SUPPRESS:
            target = EMPTY_PROC
            empty_needed = True
            notes.append(f"  {r['spawn']:<28} suppressed ({r['vanilla_item']})")
        else:
            target = MARKER_BASE | r["flag"]
            if target not in script.ids():                    # an ALIAS reuses its partner's marker
                look = look_of(script.proc_bytes(award))
                script.add_proc(target, g.marker_proc(r["flag"], *look, item=RAZOR, on_pickup=RAZOR_RESET))
            extra = f", same location as {r['alias'][1]}" if r.get("alias") else ""
            if r.get("variant_of"):
                extra += f", variant of {r['variant_of']}"
            # A grant must not hide the marker: "holds no item N" -> "flag not collected".
            # Skipped for spots that aren't on Normal (they never spawn there anyway).
            for condition in r["conditions"] if key not in NOT_ON_NORMAL else []:
                for label, old in ownership_checks(condition):
                    new = g.varbuf_byte(r["flag"]) + g.value(0) + g.EQ
                    if len(old) != len(new):
                        raise SystemExit(f"{stage} {r['spawn']}: condition lengths differ")
                    # Prefer the condition standing alone (`.if(holds no item)`); else the one
                    # compound condition that contains it.
                    for needle in (g.element(3, old + g.END), old):
                        found = [(region, at) for region in (script.procs, script.main)
                                 for at in _find_all(region, needle)]
                        if found:
                            break
                    if needle != old:
                        found = [(region, at + 1) for region, at in found]   # skip the element header
                    if len(found) > 1:
                        # Several: the one guarding this spawn is the nearest one before its call.
                        before = [(hit_at - at, region, at) for region, at in found
                                  for hit_region, hit_at in hits if hit_region is region and at < hit_at]
                        found = [min(before, key=lambda b: b[0])[1:]] if before else found
                    if len(found) != 1:
                        raise SystemExit(f"{stage} {r['spawn']}: expected one '{label}', found {len(found)}")
                    region, at = found[0]
                    region[at:at + len(old)] = new
                    extra += f", dropped '{label}'"
            if r["spawn"] in FIGHT_DROPS.get(stage, ()):
                extra += f", fight drop ({len(resupply)} resupply call(s) left vanilla)"
            if taken:
                extra += f", {len(taken)} call(s) reassigned from another spot's spawn id"
            notes.append(f"  {r['spawn']:<28} flag {r['flag']:#05x}  {len(hits)} call(s){extra}")

        for region, at in hits:
            region[at:at + 3] = target.to_bytes(3, "little")

    if moved:
        raise SystemExit(f"{stage}: reassigned calls with no target row: {sorted(moved)}")
    for spawn_id in SUPPRESS_CALLS.get(stage, []):
        calls = [(region, at) for region in (script.procs, script.main)
                 for at, _, _ in call_sites(region, spawn_id)]
        if not calls:
            raise SystemExit(f"{stage}: no call to suppress for {spawn_id:#x}")
        for region, at in calls:
            region[at:at + 3] = EMPTY_PROC.to_bytes(3, "little")
        empty_needed = True
        notes.append(f"  suppressed {spawn_id:#x}: {len(calls)} call(s)")

    if empty_needed:
        script.add_proc(EMPTY_PROC, g.block())
    script.main = bytes(script.main)
    return script.build(), notes


def _find_all(data: bytes, needle: bytes) -> list[int]:
    found, at = [], data.find(needle)
    while at >= 0:
        found.append(at)
        at = data.find(needle, at + 1)
    return found


def call_sites(data: bytes, spawn_id: int) -> list[tuple[int, int, int]]:
    """Calls whose first argument is spawn_id: (offset of the proc id, proc id, end of the call)."""
    sites = []
    for at in range(len(data) - 4):
        head = data[at]
        if head == 0x7D:
            body, size = at + 2, data[at + 1]
        elif 0x71 <= head <= 0x7C:
            body, size = at + 1, head & 0x0F
        else:
            continue
        if body + 4 > len(data):
            continue
        try:
            first, _ = read_value(data, body + 3)
        except (ValueError, struct.error, IndexError):
            continue
        if first == spawn_id:
            sites.append((body, int.from_bytes(data[body:body + 3], "little"), body + size))
    return sites


def load_rows() -> dict[str, list[dict]]:
    """World spawns by stage, both chapters. A spawn id catalogued twice in a stage is
    one pickup: the first row is kept. An ALIAS row takes its partner's flag."""
    rows = json.load(open(FIELDS_JSON, encoding="utf-8"))
    flags = {(r["stage"], r["spawn"]): r["flag"] for r in rows if r["stage"]}
    by_stage: dict[str, list[dict]] = {}
    seen = set()
    for r in rows:
        if not r["stage"] or (r["stage"], r["spawn_id"]) in seen:
            continue
        seen.add((r["stage"], r["spawn_id"]))
        alias = ALIAS.get((r["stage"], r["spawn"]))
        if alias:
            r = {**r, "flag": flags[alias], "alias": alias}
        by_stage.setdefault(r["stage"], []).append(r)
    return by_stage


def load_reward_flags() -> dict[str, int]:
    """Flag byte of every scripted reward (non-spawn rows of spawn_fields.json)."""
    rows = json.load(open(FIELDS_JSON, encoding="utf-8"))
    flags = {r["ap_name"]: r["flag"] for r in rows if r["stage"] is None}
    missing = [name for name in REWARDS if name not in flags]
    if missing:
        raise SystemExit(f"rewards with no row in {FIELDS_JSON}: {missing}")
    return flags


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--restore", action="store_true")
    mode.add_argument("--dry-run", action="store_true")
    parser.add_argument("--install", default=DEFAULT_INSTALL)
    args = parser.parse_args()

    by_stage = load_rows()
    reward_flags = load_reward_flags()
    for stage in (list(EXTRA) + [s for sites, _ in REWARDS.values() for s in sites]
                  + list(SUPPRESS_CALLS) + list(INLINE_SPAWNS)):
        by_stage.setdefault(stage, [])

    if args.restore:
        for stage in sorted(by_stage):
            path = stage_path(args.install, stage)
            if os.path.exists(path + ".orig"):
                shutil.copyfile(path + ".orig", path)
                print(f"restored {stage}")
        return

    manifest = []
    built = {}
    for stage in sorted(by_stage):
        path = stage_path(args.install, stage)
        source = path + ".orig" if os.path.exists(path + ".orig") else path
        patched, notes = patch_stage(open(source, "rb").read(), stage, by_stage[stage], reward_flags)
        built[stage] = patched
        print(f"{stage}:")
        print("\n".join(notes))
        for r in by_stage[stage]:
            if (stage, r["spawn"]) in SUPPRESS or r.get("alias") or r.get("variant_of"):
                continue                     # no location of its own
            manifest.append({
                "location": r["ap_name"] or f"{stage} {r['spawn']}",
                "stage": stage,
                "spawn": r["spawn"],
                "vanilla_item": r["vanilla_item"],
                "flag": r["flag"],
                "normal": (stage, r["spawn"]) not in NOT_ON_NORMAL,
                "note": NOT_ON_NORMAL.get((stage, r["spawn"]), ""),
                "razor": True,
                # Where the pickup can appear ([x, height, y] per spawn call); the client
                # names the Razor after the nearest uncollected spot. Variant and alias
                # stages calling the same pickup are added below.
                "positions": {stage: r.get("positions", [])},
            })
        for spot in INLINE_SPAWNS.get(stage, []):
            manifest.append({"location": spot.get("ap_name") or f"{stage} {spot['spawn']}",
                             "stage": stage, "spawn": spot["spawn"],
                             "vanilla_item": spot["vanilla_item"], "flag": spot["flag"], "normal": True,
                             "note": "", "razor": True, "inline": True,
                             "positions": {stage: spot["positions"]}})
    # The same pickup called from a sibling stage file (variant) or an ALIAS stage shares
    # the location's flag; record its positions there too, keyed by that stage.
    by_flag = {m["flag"]: m for m in manifest if m.get("razor")}
    for stage, rows in by_stage.items():
        for r in rows:
            if (r.get("alias") or r.get("variant_of")) and r["flag"] in by_flag:
                by_flag[r["flag"]]["positions"].setdefault(stage, []).extend(
                    p for p in r.get("positions", []) if p not in by_flag[r["flag"]]["positions"].get(stage, []))
    for name in REWARDS:
        manifest.append({"location": name, "stage": REWARD_STAGE[name], "spawn": None,
                         "vanilla_item": None, "flag": reward_flags[name], "normal": True, "note": "",
                         "razor": False, "positions": {}})

    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    flags = [m["flag"] for m in manifest]
    if len(flags) != len(set(flags)):
        raise SystemExit("two locations share a flag")
    normal = sum(m["normal"] for m in manifest)
    print(f"\n{len(manifest)} markers ({normal} appear on Normal); manifest -> {MANIFEST}")

    if args.dry_run:
        for stage, data in built.items():
            g.Gcx(data)      # re-parse as a sanity check
        print("dry run: nothing written to the game")
        return

    for stage, data in built.items():
        path = stage_path(args.install, stage)
        if not os.path.exists(path + ".orig"):
            shutil.copyfile(path, path + ".orig")
        open(path, "wb").write(data)
    print(f"patched {len(built)} stage files (vanilla copies kept as .orig)")


if __name__ == "__main__":
    main()
