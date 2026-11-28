"""
Static memory map for MGS2 Master Collection, ported from the cheat trainer's
MGS2_CheatTrainer_Mk2/Models/MGS2ApplicationNavigator.cs and Models/Constants.cs.

Source: the MGS2-Cheat-Trainer clone -- see repos.py (repos.NAVIGATOR).

IMPORTANT: the pointer values below are RVAs -- offsets from the module base of
METAL GEAR SOLID2.exe, not absolute addresses. The trainer's own comments show
they shift between game patches (values are annotated there for 2.0.1 and 2.0.2).
If the game updates, these are the first thing to re-verify.
"""

PROCESS_NAME = "METAL GEAR SOLID2.exe"

# RVAs. Each of these addresses holds a POINTER; dereference once to get the
# struct it points at, then add the offsets further down.
PLAYER_POINTER_RVA = 0x00949340
CURRENT_AMMO_POINTER_RVA = 0x01540C20

# GCX stage-variable block ("varbuf" in decompiled scripts). A script's
# $var:varbuf_0xNNN[k] is deref(VARBUF_POINTER_RVA) + 0xNNN + k. Holds every
# stage's per-spawn "collected" fields. Found by varscan.py --pointers; the
# player struct (PLAYER_POINTER_RVA) is the script's linkvarbuf. Both targets
# move on area loads -- dereference every time.
VARBUF_POINTER_RVA = 0x00949330

# Offsets from the dereferenced PLAYER_POINTER.
CURRENT_STAGE_OFFSET = 0x2C
CURRENT_STAGE_LENGTH = 4
CURRENT_DIFFICULTY_OFFSET = 0x10

# Player position, found with findpos.py (see FINDINGS.md section 3).
# Stored as signed integers, NOT floats. The axis order matches the randomizer's
# own Location(posX, posZ, posY, rot) constructor -- height sits in the middle.
#
# Signed 32-bit fields (confirmed 2026-11-27: Shell 1 Core reads y -56160). The
# randomizer catalogue stored 16-bit values, which wrap past +/-32767; the client
# uses the stage scripts' own spawn positions instead. POSITION_ROT's upper half
# holds something unrelated, so it must be masked to 16 bits.
# The Razor's (item slot 28's) display name: the exe's NUL-padded "RAZOR" string and
# the one 8-byte pointer to it in the item-name pointer table (one per item slot,
# table at 0x9474D8). Repointing it renames the pickup live (tested 2026-11-27).
RAZOR_NAME_RVA = 0x72FFF4
RAZOR_NAME_POINTER_RVA = 0x9475B0

POSITION_X_OFFSET = 0xE8
POSITION_HEIGHT_OFFSET = 0xEC   # the catalog calls this posZ
POSITION_Y_OFFSET = 0xF0
POSITION_ROT_OFFSET = 0xF4      # 0..4095
ROTATION_MAX = 4096

# The 0x4A4..0x4C0 cluster is the CAMERA, not the player -- it all responds to
# turning in place, and 0x4C0 is a pure camera yaw. Don't mistake it for position.

# Offsets from the dereferenced CURRENT_AMMO_POINTER.
# BaseWeapon starts at 2; BaseItem is BaseWeapon.Start + 144 = 146.
BASE_WEAPON_OFFSET = 2
BASE_ITEM_OFFSET = 146

# Each count is a 2-byte unsigned value. Indices below are already byte offsets
# within their array (they step by 2), so an item's count lives at:
#   deref(CURRENT_AMMO_POINTER) + BASE_ITEM_OFFSET + index
ENTRY_SIZE = 2

# Max counts sit a fixed distance past the current count (Constants.cs:13-14,
# ItemMinMaxCountDiff / WeaponMinMaxCountDiff).
ITEM_MAX_DIFF = 96
WEAPON_MAX_DIFF = 72

# name -> index, from Constants.cs ItemList
ITEMS: dict[str, int] = {
    "Ration": 0,
    "Scope1": 2,
    "Cold Medicine": 4,
    "Bandage": 6,
    "Pentazemin": 8,
    "B.D.U.": 10,
    "Body Armor": 12,
    "Stealth": 14,
    "Mine Detector": 16,
    "Sensor A": 18,
    "Sensor B": 20,
    "N.V.G.": 22,
    "Thermal Goggles": 24,
    "Scope2": 26,
    "Digital Camera": 28,
    "Box 1": 30,
    "Cigarettes": 32,
    "Card": 34,
    "Shaver": 36,
    "Phone": 38,
    "Camera": 40,
    "Box 2": 42,
    "Box 3": 44,
    "Wet Box": 46,
    "A.P. Sensor": 48,
    "Box 4": 50,
    "Box 5": 52,
    "Unknown Item": 54,
    "SOCOM Suppressor": 56,
    "AK Suppressor": 58,
    "Cutscene Camera": 60,
    "Bandana": 62,
    "Dog Tags": 64,
    "M.O. Disc": 66,
    "U.S.P. Suppressor": 68,
    "Infinity Wig": 70,
    "Blue Wig": 72,
    "Orange Wig": 74,
    "Color Wig 1": 76,
    "Color Wig 2": 78,
}

# name -> index, from Constants.cs WeaponList
WEAPONS: dict[str, int] = {
    "M9": 0,
    "USP": 2,
    "SOCOM": 4,
    "PSG1": 6,
    "RGB-6": 8,
    "Nikita": 10,
    "Stinger": 12,
    "Claymore": 14,
    "C4": 16,
    "Chaff Grenade": 18,
    "Stun Grenade": 20,
    "Directional Microphone": 22,
    "High Frequency Blade": 24,
    "Coolant Spray": 26,
    "AKS-74u": 28,
    "Magazine": 30,
    "Grenade": 32,
    "M4": 34,
    "PSG1-T": 36,
    "Directional Microphone(Movie)": 38,
    "Book": 40,
}

ITEM_BLOCK_SIZE = max(ITEMS.values()) + ENTRY_SIZE
WEAPON_BLOCK_SIZE = max(WEAPONS.values()) + ENTRY_SIZE

# Items guards can drop -- the 14 Drop* procs in the "Dropped objects" region of
# the randomizer's GcxProcs.cs (repos.GCX_PROCS). A count increase for one of
# these may be a guard drop rather than a world pickup, so these are poor
# choices as location marker items later on.
GUARD_DROPPABLE = {
    "Ration", "Dog Tags", "Bandage", "Pentazemin",
    "Stun Grenade", "Chaff Grenade", "Grenade",
    "M9", "USP", "SOCOM", "M4", "Stinger", "PSG1-T", "Nikita",
}
