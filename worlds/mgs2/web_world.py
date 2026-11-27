from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .Config import Config

class MGS2WebWorld(WebWorld):
    game = Config.GAME

    theme = "dirt"

    # Params
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        f"A guide to setting up {Config.GAME_NAME} for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["omgdanieltam"],
    )

    tutorials = [setup_en]

