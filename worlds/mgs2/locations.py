from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location, LocationProgressType
from rule_builder.rules import Has, HasAll, HasAny

from .Config import Regions, Config, Locations, Events, Items

from . import items

if TYPE_CHECKING:
    from .world import MGS2World

BASE_ID = Config.BASE_ID

locations_data_table: dict[str, Locations.MGS2LocationData] = {
    **Locations.tanker_start,
    **Locations.tanker_post_olga,
    **Locations.tanker_deck_2,
    **Locations.tanker_holds,
    **Locations.plant_one_off,
    **Locations.plant_shell_1,
    **Locations.plant_card_1,
    **Locations.plant_fortune,
    **Locations.plant_fatman,
    **Locations.plant_card_2,
    **Locations.plant_shell_1_core_lowers,
    **Locations.plant_arsenal_gear,
    **Locations.plant_card_3,
    **Locations.plant_shell_2,
    **Locations.plant_president,
    **Locations.plant_vamp_and_emma,
    
}

LOCATIONS_BY_REGION: dict[str, dict[str, int]] = {}
for name, data in locations_data_table.items():
    if data.address is not None:
        LOCATIONS_BY_REGION.setdefault(data.region, {})[name] = data.address
        

LOCATION_NAME_TO_ID: dict[str, int] = {
    name: data.address
    for name, data in locations_data_table.items() if data.address is not None
}


class MGS2Location(Location):
    game = Config.GAME


def create_all_locations(world: MGS2World) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: MGS2World) -> None:
    # Get regions
    tanker = world.get_region(Regions.TANKER)
    plant = world.get_region(Regions.PLANT)

    # Set locations to regions
    tanker.add_locations(LOCATIONS_BY_REGION.get(Regions.TANKER, {}), MGS2Location)
    plant.add_locations(LOCATIONS_BY_REGION.get(Regions.PLANT, {}), MGS2Location)

    # Excluded locations
    EXCLUDED_LOCATIONS = [
        "Strut A SeaDock - Ration (late)",
        "Strut A SeaDock - SOCOM Ammo (late 1)",
        "Strut A SeaDock - SOCOM Ammo (late 2)",
        "Strut E Heliport - SOCOM Ammo (Top of stairs)",
        "Shell 1 Core - M9 Ammo (Front door)",
        "Shell 1 Core - SOCOM Ammo (Front door)",
    ]

    for name in EXCLUDED_LOCATIONS:
        world.get_location(name).progress_type = LocationProgressType.EXCLUDED


def create_events(world: MGS2World) -> None:
    # Get regions
    tanker = world.get_region(Regions.TANKER)
    plant = world.get_region(Regions.PLANT)

    tanker.add_event(
        "Defeat Olga", Events.OLGA_DEFEATED,
        HasAny(Items.M9_SNAKE, Items.USP),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    tanker.add_event(
        "Access Deck 2", Events.ACCESS_DECK_2,
        Has(Items.USP),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    tanker.add_event(
        "Photograph Ray", Events.PHOTOGRAPH_RAY,
        HasAll(Events.ACCESS_DECK_2, Items.CAMERA),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    tanker.add_event(
        "Tanker Cleared", Events.TANKER_COMPLETE,
        Has(Events.PHOTOGRAPH_RAY),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    ### PLANT
    plant.add_event(
        "Has Card 1", Events.HAS_CARD_1,
        Has(Items.CARD, count=1),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Bomb Defusal", Events.BOMB_DEFUSAL,
        HasAll(Items.COOLANT, Events.HAS_CARD_1),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Fight Fortune", Events.FIGHT_FORTUNE,
        HasAll(Items.SENSOR_B, Events.BOMB_DEFUSAL),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Fight Fatman", Events.FIGHT_FATMAN,
        HasAll(Items.SOCOM, Events.FIGHT_FORTUNE),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Has Card 2", Events.HAS_CARD_2,
        Has(Items.CARD, count=2),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Access Shell 1 Core Lowers", Events.ACCESS_SHELL_1_LOWERS,
        HasAll(Items.BDU, Items.AKS_74U, Events.HAS_CARD_2),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Access Ames", Events.ACCESS_AMES,
        HasAll(Items.D_MIC, Events.ACCESS_SHELL_1_LOWERS),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Has Card 3", Events.HAS_CARD_3,
        Has(Items.CARD, count=3),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Access Harrier", Events.ACCESS_HARRIER,
        HasAll(Events.HAS_CARD_3, Items.PSG1),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Fight Harrier", Events.FIGHT_HARRIER,
        HasAll(Events.ACCESS_HARRIER, Items.STINGER),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Access Shell 2", Events.ACCESS_SHELL_2,
        HasAll(Events.FIGHT_HARRIER),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Access President", Events.ACCESS_PRESIDENT,
        HasAll(Events.ACCESS_SHELL_2, Items.NIKITA),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Has Card 4", Events.HAS_CARD_4,
        Has(Items.CARD, count=4),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Vamp and Emma", Events.VAMP_AND_EMMA,
        HasAll(Events.HAS_CARD_4, Events.ACCESS_SHELL_2),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Has Card 5", Events.HAS_CARD_5,
        HasAll(Events.VAMP_AND_EMMA, Items.COOLANT),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Access Arsenal Gear", Events.ACCESS_ARSENAL_GEAR,
        HasAll(Events.VAMP_AND_EMMA, Items.COOLANT, Items.THERMAL_GOGGLES_PLANT),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Fight Solidus", Events.FIGHT_SOLIDUS,
        HasAll(Events.ACCESS_ARSENAL_GEAR, Items.HF_BLADE),
        location_type=MGS2Location, item_type=items.MGS2Item
    )

    plant.add_event(
        "Plant Cleared", Events.PLANT_COMPLETE,
        Has(Events.FIGHT_SOLIDUS),
        location_type=MGS2Location, item_type=items.MGS2Item
    )
