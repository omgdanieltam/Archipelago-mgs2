from collections.abc import Mapping
from typing import Any

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

from .Config import Config

# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world
from . import options as mgs2_options  # rename due to a name conflict with World.options

class MGS2World(World):
    """
    Metal Gear Solid 2: Sons of Liberty is a 2001 action-adventure stealth game developed and published 
    by Konami for the PlayStation 2. Directed, produced, designed, and written by Hideo Kojima, it is the 
    fourth mainline game in the Metal Gear series and the sequel to Metal Gear Solid (1998).
    """

    game = Config.GAME

    web = web_world.MGS2WebWorld()

    options_dataclass = mgs2_options.MGS2Options
    options: mgs2_options.MGS2Options

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Menu"

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.MGS2Item:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {"apworld_version": Config.APWORLD_VERSION}
