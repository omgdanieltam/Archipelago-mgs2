from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, Optional

from BaseClasses import Item, ItemClassification

from .Config import Config, Items

if TYPE_CHECKING:
    from .world import MGS2World

BASE_ID = Config.BASE_ID
ITEM_BASE_ID = BASE_ID + 0xA00

class MGS2Item(Item):
    game = Config.GAME

class MGS2ItemData(NamedTuple):
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    count: int = 1

# Items
weapon_item_data_table: dict[str, MGS2ItemData] = {
    Items.M9_SNAKE: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x001, 
        classification=ItemClassification.progression | ItemClassification.useful, 
        count=1
    ),
    Items.USP: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x002, 
        classification=ItemClassification.progression | ItemClassification.useful, 
        count=1
    ),
    Items.M9_RAIDEN: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x003, 
        classification=ItemClassification.progression | ItemClassification.useful, 
        count=1
    ),
    Items.SOCOM: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x004, 
        classification=ItemClassification.progression | ItemClassification.useful, 
        count=1
    ),
    Items.PSG1: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x005, 
        classification=ItemClassification.progression | ItemClassification.useful, 
        count=1
    ),
    Items.PSG1_T: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x006, 
        classification=ItemClassification.useful, 
        count=1
    ),
    Items.M4: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x007, 
        classification=ItemClassification.useful, 
        count=1
    ),
    Items.AKS_74U: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x008, 
        classification=ItemClassification.progression |ItemClassification.useful, 
        count=1
    ),
    Items.STINGER: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x009, 
        classification=ItemClassification.progression | ItemClassification.useful, 
        count=1
    ),
    Items.RGB6: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x00A, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.CLAYMORE: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x00B, 
        classification=ItemClassification.filler, 
        count=4
    ),
    Items.C4: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x00C, 
        classification=ItemClassification.filler, 
        count=6
    ),
    Items.NIKITA: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x00D, 
        classification=ItemClassification.progression | ItemClassification.useful, 
        count=1
    ),
    Items.HF_BLADE: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x00E, 
        classification=ItemClassification.progression | ItemClassification.useful, 
        count=1
    ),
    Items.GRENADE_TANKER: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x00F, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.STUN_GRENADE_TANKER: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x010, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.CHAFF_GRENADE_TANKER: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x011, 
        classification=ItemClassification.filler, 
        count=2
    ),
    Items.GRENADE_PLANT: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x012, 
        classification=ItemClassification.filler, 
        count=4
    ),
    Items.STUN_GRENADE_PLANT: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x013, 
        classification=ItemClassification.filler, 
        count=5
    ),
    Items.CHAFF_GRENADE_PLANT: MGS2ItemData(
        code=ITEM_BASE_ID + Items.WEAPON_BASE_ID + 0x014, 
        classification=ItemClassification.filler, 
        count=9
    )
}

ammo_item_data_table: dict[str, MGS2ItemData] = {
    Items.M9_AMMO_TANKER: MGS2ItemData(
        code=ITEM_BASE_ID + Items.AMMO_BASE_ID + 0x001, 
        classification=ItemClassification.filler, 
        count=9
    ),
    Items.USP_AMMO: MGS2ItemData(
        code=ITEM_BASE_ID + Items.AMMO_BASE_ID + 0x002, 
        classification=ItemClassification.filler, 
        count=13
    ),
    Items.M9_AMMO_PLANT: MGS2ItemData(
        code=ITEM_BASE_ID + Items.AMMO_BASE_ID + 0x003, 
        classification=ItemClassification.filler, 
        count=18
    ),
    Items.SOCOM_AMMO: MGS2ItemData(
        code=ITEM_BASE_ID + Items.AMMO_BASE_ID + 0x004, 
        classification=ItemClassification.filler, 
        count=31
    ),
    Items.PSG1_AMMO: MGS2ItemData(
        code=ITEM_BASE_ID + Items.AMMO_BASE_ID + 0x005, 
        classification=ItemClassification.filler, 
        count=9
    ),
    Items.PSG1_T_AMMO: MGS2ItemData(
        code=ITEM_BASE_ID + Items.AMMO_BASE_ID + 0x006, 
        classification=ItemClassification.filler, 
        count=7
    ),
    Items.M4_AMMO: MGS2ItemData(
        code=ITEM_BASE_ID + Items.AMMO_BASE_ID + 0x007, 
        classification=ItemClassification.filler, 
        count=13
    ),
    Items.AKS_74U_AMMO: MGS2ItemData(
        code=ITEM_BASE_ID + Items.AMMO_BASE_ID + 0x008, 
        classification=ItemClassification.filler, 
        count=12
    ),
    Items.STINGER_AMMO: MGS2ItemData(
        code=ITEM_BASE_ID + Items.AMMO_BASE_ID + 0x009, 
        classification=ItemClassification.filler, 
        count=3
    ),
    Items.RGB6_AMMO: MGS2ItemData(
        code=ITEM_BASE_ID + Items.AMMO_BASE_ID + 0x00A, 
        classification=ItemClassification.filler, 
        count=5
    ),
    Items.NIKITA_AMMO: MGS2ItemData(
        code=ITEM_BASE_ID + Items.AMMO_BASE_ID + 0x00B, 
        classification=ItemClassification.filler, 
        count=6
    )
}

equipment_item_data_table: dict[str, MGS2ItemData] = {
    Items.CAMERA: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x001, 
        classification=ItemClassification.progression, 
        count=1
    ),
    Items.CIGS_TANKER: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x002, 
        classification=ItemClassification.useful, 
        count=1
    ),
    Items.AP_SENSOR_TANKER: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x003, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.THERMAL_GOGGLES_TANKER: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x004, 
        classification=ItemClassification.useful, 
        count=1
    ),
    Items.USP_SUPPRESSOR: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x005, 
        classification=ItemClassification.filler, 
        count=0
    ),
    Items.BOX: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x006, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.WET_BOX: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x007, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.BOX1: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x008, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.BOX2: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x009, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.BOX3: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x00A, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.BOX4: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x00B, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.BOX5: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x020, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.COOLANT: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x00C, 
        classification=ItemClassification.progression | ItemClassification.useful, 
        count=1
    ),
    Items.SENSOR_A: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x00D, 
        classification=ItemClassification.progression, 
        count=1
    ),
    Items.SENSOR_B: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x00E, 
        classification=ItemClassification.progression, 
        count=1
    ),
    Items.BDU: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x00F, 
        classification=ItemClassification.progression, 
        count=1
    ),
    Items.MINE_DETECTOR: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x010, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.DIGITAL_CAMERA: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x011, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.BOOK: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x012, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.AKS_74U_SUPPRESSOR: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x013, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.SOCOM_SUPPRESSOR: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x014, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.D_MIC: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x015, 
        classification=ItemClassification.progression | ItemClassification.useful, 
        count=1
    ),
    Items.BODY_ARMOR: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x016, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.THERMAL_GOGGLES_PLANT: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x017, 
        classification=ItemClassification.progression | ItemClassification.useful, 
        count=1
    ),
    Items.NVG: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x018, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.CIGS_PLANT: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x019, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.AP_SENSOR_PLANT: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x01A,
        classification=ItemClassification.filler,
        count=1
    ),
    Items.BINOCULARS: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x01B,
        classification=ItemClassification.useful,
        count=1
    ),
    Items.CARD: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x01C,
        classification=ItemClassification.progression,
        count=4
    ),
    Items.MODISC: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x01D,
        classification=ItemClassification.filler,
        count=1
    ),
    Items.PHONE: MGS2ItemData(
        code=ITEM_BASE_ID + Items.EQUIPMENT_BASE_ID + 0x01E,
        classification=ItemClassification.filler,
        count=1
    )
}

consumables_item_data_table: dict[str, MGS2ItemData] = {
    Items.RATION_TANKER: MGS2ItemData(
        code=ITEM_BASE_ID + Items.CONSUMABLES_BASE_ID + 0x001, 
        classification=ItemClassification.filler, 
        count=11
    ),
    Items.BANDAGE_TANKER: MGS2ItemData(
        code=ITEM_BASE_ID + Items.CONSUMABLES_BASE_ID + 0x002, 
        classification=ItemClassification.filler, 
        count=2
    ),
    Items.PENTAZEMIN_TANKER: MGS2ItemData(
        code=ITEM_BASE_ID + Items.CONSUMABLES_BASE_ID + 0x004, 
        classification=ItemClassification.filler, 
        count=1
    ),
    Items.RATION_PLANT: MGS2ItemData(
        code=ITEM_BASE_ID + Items.CONSUMABLES_BASE_ID + 0x005, 
        classification=ItemClassification.filler, 
        count=29
    ),
    Items.BANDAGE_PLANT: MGS2ItemData(
        code=ITEM_BASE_ID + Items.CONSUMABLES_BASE_ID + 0x006, 
        classification=ItemClassification.filler, 
        count=5
    ),
    Items.PENTAZEMIN_PLANT: MGS2ItemData(
        code=ITEM_BASE_ID + Items.CONSUMABLES_BASE_ID + 0x007, 
        classification=ItemClassification.filler, 
        count=8
    ),
}

item_data_table: dict[str, MGS2ItemData] = {
    **weapon_item_data_table,
    **ammo_item_data_table,
    **equipment_item_data_table,
    **consumables_item_data_table,
}

ITEM_NAME_TO_ID = {
    name: data.code 
    for name, data in item_data_table.items() if data.code is not None
}


# Random filler item
def get_random_filler_item_name(world: MGS2World) -> str:
    # only consider ammo and consumables as extra filler items
    filler_item_table: dict[str, MGS2ItemData] = {
        **ammo_item_data_table,
        **consumables_item_data_table
    }

    filler_items: list[str] = [
        name
        for name, _ in filler_item_table.items()
    ]

    return world.random.choice(filler_items)


# Create with classification
def create_item_with_correct_classification(world: MGS2World, name: str) -> MGS2Item:
    data = item_data_table[name]
    return MGS2Item(name, data.classification, data.code, world.player)


# Create items
def create_all_items(world: MGS2World) -> None:
    itempool: list[MGS2Item] = [
        world.create_item(name)
        for name, data in item_data_table.items()
        for _ in range(data.count)
    ]

    # Fill remaining
    num_items = len(itempool)
    num_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    num_to_fill = num_unfilled_locations - num_items
    itempool += [world.create_filler() for _ in range(num_to_fill)]

    # No separate starting inventory: the 4 "Tanker Start - *" locations are the
    # starting items (the client sends them on a new game).
    world.multiworld.itempool += itempool