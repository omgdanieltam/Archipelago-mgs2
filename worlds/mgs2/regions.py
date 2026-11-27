from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from .Config import Regions

if TYPE_CHECKING:
    from .world import MGS2World


def create_and_connect_regions(world: MGS2World) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: MGS2World) -> None:
    # Define regions
    menu = Region("Menu", world.player, world.multiworld)

    # Tanker
    tanker = Region(Regions.TANKER, world.player, world.multiworld)

    # Plant
    plant = Region(Regions.PLANT, world.player, world.multiworld)

    # Regions into list
    regions = [
        menu,
        tanker,
        plant
    ]

    # Add to multiworld.regions
    world.multiworld.regions += regions


def connect_regions(world: MGS2World) -> None:

    # Get regions
    menu = world.get_region("Menu")
    tanker = world.get_region(Regions.TANKER)

    plant = world.get_region(Regions.PLANT)

    # Connect regions
    menu.connect(tanker, "Menu to Tanker")

    menu.connect(plant, "Menu to Plant")

