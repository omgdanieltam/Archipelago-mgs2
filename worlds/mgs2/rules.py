from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAll, HasAny

from .Config import Events, Items, Locations

if TYPE_CHECKING:
    from .world import MGS2World


def set_all_rules(world: MGS2World) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: MGS2World) -> None:
    return



def set_all_location_rules(world: MGS2World) -> None:
    # Tanker
    after_olga = Has(Events.OLGA_DEFEATED)
    deck_2 = Has(Events.ACCESS_DECK_2)

    # Plant
    card_1 = Has(Events.HAS_CARD_1)
    card_2 = Has(Events.HAS_CARD_2)
    card_3 = Has(Events.HAS_CARD_3)
    card_4 = Has(Events.HAS_CARD_4)
    card_5 = Has(Events.HAS_CARD_5)

    dg_camera = Has(Events.HAS_CARD_1) & HasAny(Items.BOX5, Events.HAS_CARD_5)
    bomb_defusal = HasAll(Events.HAS_CARD_1, Events.BOMB_DEFUSAL)
    fortune = HasAll(Events.FIGHT_FORTUNE)
    fatman = HasAll(Events.FIGHT_FATMAN)
    shell_1_core_lowers = HasAll(Events.HAS_CARD_2, Events.ACCESS_SHELL_1_LOWERS)
    shell_2 = HasAll(Events.ACCESS_SHELL_2)
    post_harrier_fire = HasAll(Events.ACCESS_SHELL_2, Items.COOLANT)
    president = HasAll(Events.ACCESS_PRESIDENT)
    vamp_and_emma = HasAll(Events.VAMP_AND_EMMA)
    arsenal_gear = HasAll(Events.ACCESS_ARSENAL_GEAR)
    solidus = HasAll(Events.FIGHT_SOLIDUS)

    # One-off locations
    world.set_rule(world.get_location("Strut E Parcel Room - Digital Camera (Level 5 door room)"), dg_camera)
    world.set_rule(world.get_location("Shell 1 Core Hostage Room - Progressive Card"), Has(Events.ACCESS_AMES))
    world.set_rule(world.get_location("Shell 1 Core Hostage Room - Ames (Reward)"), Has(Events.ACCESS_AMES))
    world.set_rule(world.get_location("Shell 1-2 Connecting Bridge - Stinger"), Has(Events.ACCESS_HARRIER))
    world.set_rule(world.get_location("Shell 1-2 Connecting Bridge - Harrier (Reward)"), Has(Events.FIGHT_HARRIER))
    world.set_rule(world.get_location("Shell 1-2 Connecting Bridge - AKS-74u Suppressor (Behind fire)"), post_harrier_fire)
    world.set_rule(world.get_location("Shell 1-2 Connecting Bridge - Ration (Broken stairs)"), post_harrier_fire)
    world.set_rule(world.get_location("KL Connecting Bridge with Emma - Progressive Card"), card_5) 

    # Get locations for Tanker
    post_olga_locations = [
        name for name, _ in Locations.tanker_post_olga.items()
    ]

    deck_2_locations = [
        name for name, _ in Locations.tanker_deck_2.items() 
    ]

    tanker_holds_locations = [
        name for name, _ in Locations.tanker_holds.items()
    ]

    # Get locations for Plant
    shell_1_card_1_locations = [
        name for name, _ in Locations.plant_card_1.items()
    ]

    fortune_locations = [
        name for name, _ in Locations.plant_fortune.items()
    ]

    fatman_locations = [
        name for name, _ in Locations.plant_fatman.items()
    ]

    shell_1_card_2_locations = [
        name for name, _ in Locations.plant_card_2.items()
    ]

    shell_1_core_lowers_locations = [
        name for name, _ in Locations.plant_shell_1_core_lowers.items()
    ]

    shell_2_locations = [
        name for name, _ in Locations.plant_shell_2.items()
    ]

    shell_1_card_3_locations = [
        name for name, _ in Locations.plant_card_3.items()
    ]

    president_locations = [
        name for name, _ in Locations.plant_president.items()
    ]

    vamp_and_emma_locations = [
        name for name, _ in Locations.plant_vamp_and_emma.items()
    ]

    arsenal_gear_locations = [
        name for name, _ in Locations.plant_arsenal_gear.items()
    ]

    # Set rules for Tanker
    for name in post_olga_locations:
        world.set_rule(world.get_location(name), after_olga)

    for name in deck_2_locations:
        world.set_rule(world.get_location(name), deck_2)

    for name in tanker_holds_locations:
        world.set_rule(world.get_location(name), deck_2)

    # Set rules for Plant
    for name in shell_1_core_lowers_locations:
        world.set_rule(world.get_location(name), shell_1_core_lowers)

    for name in fortune_locations:
        world.set_rule(world.get_location(name), fortune)

    for name in fatman_locations:
        world.set_rule(world.get_location(name), fatman)

    for name in shell_1_card_1_locations:
        world.set_rule(world.get_location(name), card_1)

    for name in shell_1_card_2_locations:
        world.set_rule(world.get_location(name), card_2)

    for name in shell_1_card_3_locations:
        world.set_rule(world.get_location(name), card_3)

    for name in shell_2_locations:
        world.set_rule(world.get_location(name), shell_2)

    for name in president_locations:
        world.set_rule(world.get_location(name), president)

    for name in vamp_and_emma_locations:
        world.set_rule(world.get_location(name), vamp_and_emma)

    for name in arsenal_gear_locations:
        world.set_rule(world.get_location(name), arsenal_gear)


def set_completion_condition(world: MGS2World) -> None:
    world.set_rule(world.get_location("Tanker Complete"), Has(Events.TANKER_COMPLETE))
    world.set_rule(world.get_location("Plant Complete"), Has(Events.PLANT_COMPLETE))

    # Completion condition
    world.set_completion_rule(HasAll(Events.PLANT_COMPLETE, Events.TANKER_COMPLETE))