from worlds.LauncherComponents import Component, Type, components, launch

from .Config import Config
from .world import MGS2World as MGS2World


def run_client(*args: str) -> None:
    """The Launcher's "MGS2 Client" button (and archipelago:// links for this game)."""
    from .client.ap_client import launch as launch_client   # imported on use: keeps world loading light
    launch(launch_client, name="MGS2Client", args=args)


components.append(Component(
    "MGS2 Client",
    func=run_client,
    component_type=Type.CLIENT,
    game_name=Config.GAME,
    supports_uri=True,
    description="Connect Metal Gear Solid 2 (Master Collection) to Archipelago. /patch patches the game.",
))
