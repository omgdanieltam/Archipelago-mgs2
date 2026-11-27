from typing import NamedTuple, Optional

from worlds.mgs2.Config import Regions, Config

BASE_ID = Config.BASE_ID

class MGS2LocationData(NamedTuple):
    region: str
    stage: str
    spawn: str
    address: Optional[int] = None

# All locations
tanker_start: dict[str, MGS2LocationData] = {
    "Aft Deck - Ration (Left side)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00a",
            spawn="NearbyLeftsideBodyDump",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x001
        ),
    "Aft Deck - Bandage (Right side lifeboats)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00a",
            spawn="RightsideLifeboats",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x003
        ),
    "Aft Deck - Bandage (Under left stairs)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00a",
            spawn="UnderLeftsideStairs",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x004
        ),
    "Aft Deck - Pentazemin (Right side)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00a",
            spawn="NearbyRightsideBodyDump",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x005
        ),
    "Aft Deck - Chaff Grenade (Right side behind crates)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00a",
            spawn="RightsideBehindCrates",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x006
        ),
    "Deck A Crew Quarters - M9 Ammo (Locker)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01a",
            spawn="Locker1",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x008
        ),
    "Deck A Crew Quarters - Ration (Locker)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01a",
            spawn="Locker2",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x009
        ),
    "Deck A Crew Quarters Starboard - M9 Ammo (Under right stairs)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01b",
            spawn="UnderRightsideStairs",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x00A
        ),
    "Deck A Crew Quarters Starboard - Ration (Right side alcove)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01b",
            spawn="RightsideAlcove",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x00B
        ),
    "Deck A Crew Quarters Starboard - USP Ammo (Locker)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01b",
            spawn="Locker",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x00C
        ),
    "Deck A Crew Lounge - M9 Ammo (Bar)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01f",
            spawn="Bar",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x00D
        ),
    "Deck A Crew Lounge - Ration (TV)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01f",
            spawn="TV",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x00E
        ),
    "Deck A Crew Lounge - USP Ammo (Stinky ration man)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01f",
            spawn="StinkyRationMan",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x00F
        ),
    "Deck A Crew Lounge - Stun Grenade (Engine room access)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01f",
            spawn="EngineRoomAccess",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x010
        ),
    "Deck C Crew Quarters - Ration (Crawlspace)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01c",
            spawn="Crawlspace",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x011
        ),
    "Deck C Crew Quarters - Chaff Grenade (Locker)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01c",
            spawn="Locker",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x012
        ),
    "Deck D Crew Quarters - M9 Ammo (Under table)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01d",
            spawn="UnderTable1",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x013
        ),
    "Deck D Crew Quarters - M9 Ammo (Pantry)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01d",
            spawn="Pantry1",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x014
        ),
    "Deck D Crew Quarters - USP Ammo (Under table)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01d",
            spawn="UnderTable2",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x015
        ),
    "Deck D Crew Quarters - USP Ammo (Under camera)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01d",
            spawn="NextToCamera",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x016
        ),
    "Deck D Crew Quarters - Ration (Stove)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01d",
            spawn="Stove",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x017
        ),
    "Deck D Crew Quarters - Box (Pantry)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01d",
            spawn="Pantry2",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x018
        ),
    "Deck E Bridge - USP Ammo (Right side)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w01e",
            spawn="NearRightDoor",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x019
        ),
    "Engine Room - USP Ammo (Under left stairs)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w02a",
            spawn="UnderLeftsideStairs",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x01A
        ),
    "Engine Room - USP Ammo (Left side alcove)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w02a",
            spawn="LeftsideAlcove",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x01B
        ),
    "Engine Room - USP Ammo (Small port side room)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w02a",
            spawn="SmallPortSideRoom",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x01C
        ),
    "Engine Room - USP Ammo (Raven crates)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w02a",
            spawn="RavenCrates",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x01D
        ),
    "Engine Room - M9 Ammo (Under right stairs)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w02a",
            spawn="UnderRightsideStairs",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x01E
        ),
    "Engine Room - Ration (Right side catwalk)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w02a",
            spawn="RightsideConnectingCatwalk",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x01F
        ),
    "Tanker Start - M9":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00a",
            spawn="TankerStartM9",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x020
        ),
    "Tanker Start - Camera":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00a",
            spawn="TankerStartCamera",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x021
        ),
    "Tanker Start - Cigs":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00a",
            spawn="TankerStartCigs",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x022
        ),
    "Tanker Start - AP Sensor":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00a",
            spawn="TankerStartAPSensor",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x023
        ),
}

tanker_post_olga: dict[str, MGS2LocationData] = {
    "Navigational Deck - Olga (Reward)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00c",
            spawn="OlgaDefeated",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x024
        ),
    "Navigational Deck - Olga (USP)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00c",
            spawn="OlgaUSP",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x0DA
        ),
    "Navigational Deck - Ration (Left side platform)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00c",
            spawn="NearLeftsidePlatform",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x025
        ),
    "Navigational Deck - Wet Box (Right side platform)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00c",
            spawn="RightsidePlatform",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x026
        ),
    "Navigational Deck - Thermal Goggles (Crow's Nest)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w00c",
            spawn="CrowsNest1",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x027
        ),
    "Engine Room - Grenade (Left side bottom front)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w02a",
            spawn="LeftsideBottomFront",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x028
        ),
}

tanker_deck_2: dict[str, MGS2LocationData] = {
    "Deck 2 Port - USP Ammo (Middle short hallway)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w03a",
            spawn="MiddleShortHallway",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x029
        ),
    "Deck 2 Port - USP Ammo (Close side room)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w03a",
            spawn="CloseSideRoom",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x02A
        ),
    "Deck 2 Port - Ration (Deadguy side room)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w03a",
            spawn="DeadguySideRoom",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x02B
        ),
    "Deck 2 Starboard - USP Ammo (Entryway)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w03b",
            spawn="StartOfHallway",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x02C
        ),
    "Deck 2 Starboard - USP Ammo (Side rooms pipes)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w03b",
            spawn="SideRoomPipes",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x02D
        ),
    "Deck 2 Starboard - M9 Ammo (Entryway pipes)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w03b",
            spawn="EntrywayPipes",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x02E
        ),
    "Deck 2 Starboard - Ration (Side room)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w03b",
            spawn="Sideroom",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x02F
        ),
    "Deck 2 - Guard Rush (Reward)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w03b",
            spawn="GuardRush",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x030
        )
}

tanker_holds: dict[str, MGS2LocationData] = {
    "Hold 1 - M9 Ammo (Left ladder)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w04a",
            spawn="LeftLadder1",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x032
        ),
    "Hold 1 - M9 Ammo (Behind hatch)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w04a",
            spawn="BehindHatch1",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x033
        ),
    "Hold 1 - Ration (Behind hatch)":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w04a",
            spawn="BehindHatch2",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x034
        ),
    "Tanker Complete":
        MGS2LocationData(
            region=Regions.TANKER,
            stage="w05b",
            spawn="TankerComplete",
            address=BASE_ID + Regions.TANKER_BASE_ID + 0x031
        )
}

plant_one_off: dict[str, MGS2LocationData] = {
    "Strut E Parcel Room - Digital Camera (Level 5 door room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20a",
            spawn="Level5DoorRoom",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x05D
        ),
    "Shell 1 Core Hostage Room - Progressive Card":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20b",
            spawn="AmesReward",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x06D
        ),
    "Shell 1 Core Hostage Room - Ames (Reward)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20b",
            spawn="Ames",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0D2
        ),
    "Shell 1-2 Connecting Bridge - Harrier (Reward)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25b",
            spawn="Shell12Bridge",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x087
        ),
    "Shell 1-2 Connecting Bridge - Stinger":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25a",
            spawn="HarrierStinger",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x088
        ),
    "Shell 1-2 Connecting Bridge - AKS-74u Suppressor (Behind fire)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25b",
            spawn="BehindFireOtherwise",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0A6
        ),
    "Shell 1-2 Connecting Bridge - Ration (Broken stairs)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25b",
            spawn="BrokenStairs",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0AA
        ),
     "KL Connecting Bridge with Emma - Progressive Card":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25d",
            spawn="KLCardScene",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0D1
        )
}

plant_shell_1: dict[str, MGS2LocationData] = {
    "Plant Start - AP Sensor":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w11a",
            spawn="PlantStartAPSensor",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x001
        ),
    "Plant Start - Binoculars":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w11a",
            spawn="PlantStartBinoculars",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x002
        ),
    "Strut A SeaDock - Ration (Locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w11a",
            spawn="Locker",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x003
        ),
    "Strut A SeaDock - Ration (Right side alcove)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w11a",
            spawn="RightSideAlcove",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x004
        ),
    "Strut A SeaDock - Thermal Goggles (Pool)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w11a",
            spawn="Pool",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x005
        ),
    "Strut A SeaDock - Ration (Story)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w11a",
            spawn="StoryRation",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x006
        ),
    "Strut A Roof - Bandage (Boxes)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w12a",
            spawn="Boxes",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x007
        ),
    "Strut A Roof - Chaff Grenade (Right cage)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w12a",
            spawn="RightCage",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x008
        ),
    "Strut A Roof - M9 Ammo (Bottom left)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w12a",
            spawn="BottomLeft",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x009
        ),
    "Strut A Pump Room - M9 Ammo (Under desk near node)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w12b",
            spawn="UnderDeskNearNode",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x00A
        ),
    "Strut A Pump Room - M9 Ammo (Top of stairs)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w12b",
            spawn="TopOfStairs",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x00B
        ),
    "Strut A Pump Room - SOCOM Ammo (Locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w12b",
            spawn="Locker1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x00C
        ),
    "Strut A Pump Room - Ration (Locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w12b",
            spawn="Locker2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x00D
        ),
    "FA Connecting Bridge - Chaff Grenade (Bottom bridge)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w23a",
            spawn="BottomBridgeLeftSide",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x00E
        ),
    "Strut F Warehouse - SOCOM Ammo (Outside PSG1 room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="OutsidePSG1Room",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x00F
        ),
    "Strut F Warehouse - Ration (Outside M9 room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="OutsideM9Room",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x010
        ),
    "Strut F Warehouse - Book (Bottom floor middle crates)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="BottomFloorMiddleCrates",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x011
        ),
    "Strut F Warehouse - Stun Grenade (Outside AK room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="OutsideAKRoom",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x012
        ),
    "Strut F Warehouse - M9 Ammo (Bottom floor parkour boxes)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="BottomFloorParkourBoxes",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x013
        ),
    "Strut F Warehouse - SOCOM Ammo (Bottom floor right crates)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="BottomFloorRightCrates",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x014
        ),
    "Strut F Warehouse - Chaff Grenade (Outside node room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="OutsideNodeRoom",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x015
        ),
    "Strut F Warehouse - M9 Ammo (M9 room 1)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="M9Room1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x016
        ),
    "Strut F Warehouse - M9 Ammo (M9 room 2)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="M9Room2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x017
        ),
    "Strut F Warehouse - M9 Ammo (M9 room 3)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="M9Room3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x018
        ),
    "Strut B Transformer Room - M9 Ammo (Catwalk)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w14a",
            spawn="Catwalk",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x026
        ),
    "Strut B Transformer Room - SOCOM Ammo (Node)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w14a",
            spawn="Node",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x027
        ),
    "Strut B Transformer Room - SOCOM Ammo (Locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w14a",
            spawn="Locker1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x028
        ),
    "Strut B Transformer Room - Ration (Locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w14a",
            spawn="Locker2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x029
        ),
    "BC Connecting Bridge - Chaff Grenade (Broken bridge)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w15a",
            spawn="BrokenBridge",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x02A
        ),
    "Strut C Dining Hall - M9 Ammo (Ladies room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w16a",
            spawn="LadiesRoom1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x02B
        ),
    "Strut C Dining Hall - SOCOM Ammo (Mens room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w16a",
            spawn="MensRoom",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x02C
        ),
    "Strut C Dining Hall - Pentazemin (Ladies room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w16a",
            spawn="LadiesRoom2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x02D
        ),
    "Strut C Dining Hall - Ration (Dining room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w16a",
            spawn="DiningRoom",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x02E
        ),
    "Strut B Transformer Room - Pliskin SOCOM":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w14a",
            spawn="PliskinReward",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x02F
        ),
    "Strut C Dining Hall - Stillman Coolant":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w16a",
            spawn="StillmanCoolant",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x030
        ),
    "Strut C Dining Hall - Stillman Sensor A":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w16a",
            spawn="StillmanSensorA",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x031
        ),
    "Strut C Dining Hall - Stillman Progressive Card":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w16a",
            spawn="StillmanCard",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x032
        ),
}

plant_card_1: dict[str, MGS2LocationData] = {
    "Strut A Pump Room - SOCOM Ammo (Under camera)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w12b",
            spawn="UnderCamera",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x033
        ),
    "Strut A Pump Room - Bandage (Upper left)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w12b",
            spawn="UpperLeft",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x034
        ),
    "Strut A Pump Room - Box 1 (Lower left)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w12b",
            spawn="LowerLeft",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x035
        ),
    "Strut D Sediment Pool - M9 Ammo (Under stairs)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w18a",
            spawn="UnderStairs",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x036
        ),
    "Strut D Sediment Pool - PSG1 Ammo (Rightside door)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w18a",
            spawn="RightsideDoor",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x037
        ),
    "Strut D Sediment Pool - SOCOM Ammo (Leftside door)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w18a",
            spawn="LeftsideDoor",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x038
        ),
    "Strut D Sediment Pool - Ration (Center alcove)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w18a",
            spawn="CenterAlcove",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x039
        ),
    "DE Connecting Bridge - SOCOM Ammo (Lower bridge rightside)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w19a",
            spawn="LowerBridgeRightside1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x03A
        ),
    "DE Connecting Bridge - Stun Grenade (Lower bridge rightside)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w19a",
            spawn="LowerBridgeRightside2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x03B
        ),
    "Strut E Parcel Room - Mine Detector (Outside level 5 doors)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20a",
            spawn="OutsideLevel5Doors",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x03C
        ),
    "Strut E Parcel Room - Ration (Bottom floor crawlspace)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20a",
            spawn="BottomFloorCrawlspace",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x03D
        ),
    "Strut E Parcel Room - Box 5 (Unnamed)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20a",
            spawn="Unnamed",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x03E
        ),
    "Strut E Parcel Room - M4 Ammo (Bottomside middle boxes)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20a",
            spawn="BottomsideMiddleBoxes",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x03F
        ),
    "Strut E Parcel Room - M9 Ammo (Leftside middle boxes)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20a",
            spawn="LeftsideMiddleBoxes",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x040
        ),
    "Strut E Parcel Room - SOCOM Ammo (Under wire rack by ED bridge)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20a",
            spawn="UnderWireRackByEDBridge",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x041
        ),
    "Strut E Parcel Room - SOCOM Ammo (Under wire rack by node)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20a",
            spawn="UnderWireRackByNode",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x042
        ),
    "Strut E Parcel Room - Stun Grenade (Under conveyer belt)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20a",
            spawn="UnderConveyerBelt",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x043
        ),
    "Strut E Parcel Room - SOCOM Ammo (Perimeter access room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20a",
            spawn="PerimeterAccessRoom",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x044
        ),
    "Strut E Heliport - Box 3 (Roof bottom left racks)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20b",
            spawn="RoofBottomLeftRacks",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x045
        ),
    "Strut E Heliport - Claymore (Lower level sleeping guard)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20b",
            spawn="LowerLevelSleepingGuard",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x046
        ),
    "Strut E Heliport - Stun Grenade (Leftside crates)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20b",
            spawn="LeftsideCrates",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x047
        ),
    "Strut E Heliport - SOCOM Ammo (Top of stairs)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20b",
            spawn="TopOfStairs",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x048
        ),
    "EF Connecting Bridge - AKS-74u Ammo (Near shell 1 core)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w21a",
            spawn="NearShell1Core",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x049
        ),
    "Strut F Warehouse - SOCOM Ammo (Room across node 1)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="RoomAcrossNode1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x019
        ),
    "Strut F Warehouse - Mine Detector (Room across node)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="RoomAcrossNode3.1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x01A
        ),
    "Strut F Warehouse - SOCOM Ammo (Room across node 2)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="RoomAcrossNode2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x01B
        ),
    "Strut F Warehouse - Box 2 (Room with node)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="RoomWithNode",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x01C
        ),
    "Strut F Warehouse - Pentazemin (Locker near node)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="LockerNearNode1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x01D
        ),
    "Strut F Warehouse - Ration (Locker near node)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="LockerNearNode2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x01E
        ),
    "Strut F Warehouse - M9 Ammo (Room across node)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="RoomAcrossNode4",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x01F
        ),
    "Strut F Warehouse - Book (Locker near node)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="LockerNearNode3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x020
        ),
    "Strut F Warehouse - Grenade (Grenade room 1)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="GrenadeRoom1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x021
        ),
    "Strut F Warehouse - Grenade (Grenade room 2)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="GrenadeRoom2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x022
        ),
    "Strut F Warehouse - Grenade (Grenade room 3)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="GrenadeRoom3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x023
        ),
    "Strut F Warehouse - PSG1-T Ammo (Grenade room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="GrenadeRoom4",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x024
        ),
    "Strut F Warehouse - SOCOM Ammo (Grenade room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="GrenadeRoom5",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x025
        ),
    "Strut C Dining Hall - Sensor B (Pantry room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w16a",
            spawn="PantryRoom",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x04A
        ),
}

plant_fortune: dict[str, MGS2LocationData] = {
    "Strut A SeaDock - Ration (late)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w11b",
            spawn="LateRation",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x04B
        ),
    "Strut A SeaDock - SOCOM Ammo (late 1)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w11b",
            spawn="LateSocomAmmo1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x04C
        ),
    "Strut A SeaDock - SOCOM Ammo (late 2)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w11b",
            spawn="LateSocomAmmo2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x04D
        ),
    "Strut A SeaDock - Fortune (Reward)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w12b",
            spawn="StrutASeaDockFortune",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x04E
        ),
}

plant_fatman: dict[str, MGS2LocationData] = {
    "Strut E Heliport - B.D.U.":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20b",
            spawn="HeliportBDU",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x04F
        ),
    "Strut E Heliport - Phone":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20b",
            spawn="HeliportPhone",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x050
        ),
    "Strut E Heliport - Progressive Card":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20b",
            spawn="HeliportCard",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x051
        ),
    "Strut E Heliport - Fatman (Reward)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20b",
            spawn="HeliportFatman",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x052
        ),
}

plant_card_2: dict[str, MGS2LocationData] = {
    "Shell 1 Core - Book (Locker room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24a",
            spawn="LockerRoom2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x053
        ),
    "Shell 1 Core - C4 (Locker room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24a",
            spawn="LockerRoom3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x054
        ),
    "Shell 1 Core - Chaff Grenade (Locker room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24a",
            spawn="LockerRoom4",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x055
        ),
    "Shell 1 Core - Claymore (Locker room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24a",
            spawn="LockerRoom5",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x056
        ),
    "Shell 1 Core - M4 Ammo (Locker room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24a",
            spawn="LockerRoom6",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x057
        ),
    "Shell 1 Core - M9 Ammo (Locker room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24a",
            spawn="LockerRoom7",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x058
        ),
    "Shell 1 Core - SOCOM Ammo (Broken door)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24a",
            spawn="BrokenDoor",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x059
        ),
    "Shell 1 Core - SOCOM Ammo (Locker room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24a",
            spawn="LockerRoom8",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x05A
        ),
    "Shell 1 Core - M9 Ammo (Front door)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24a",
            spawn="FrontDoor1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x05B
        ),
    "Shell 1 Core - SOCOM Ammo (Front door)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24a",
            spawn="FrontDoor2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x05C
        ),
}

plant_shell_1_core_lowers: dict[str, MGS2LocationData] = {
    "Shell 1 Core B1 - M4 Ammo (Hallway)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24b",
            spawn="Hallway",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x05E
        ),
    "Shell 1 Core B1 - SOCOM Ammo (Lounge locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24b",
            spawn="LoungeLocker1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x05F
        ),
    "Shell 1 Core B1 - Stun Grenade (Lounge locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24b",
            spawn="LoungeLocker2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x060
        ),
    "Shell 1 Core B1 - Ration (Node locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24b",
            spawn="NodeLocker",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x061
        ),
    "Shell 1 Core Hostage Room - Bandage (Bottom left)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24c",
            spawn="BottomLeft",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x062
        ),
    "Shell 1 Core Hostage Room - Ration (Bottom right)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24c",
            spawn="BottomRight",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x063
        ),
    "Shell 1 Core Hostage Room - Thermal Goggles (Podium)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24c",
            spawn="Podium",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x064
        ),
    "Shell 1 Core B2 - AKS-74u Ammo (Node)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24d",
            spawn="Node1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x065
        ),
    "Shell 1 Core B2 - Bandage (Under desk)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24d",
            spawn="UnderDesk",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x066
        ),
    "Shell 1 Core B2 - Box 4 (Node)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24d",
            spawn="Node2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x067
        ),
    "Shell 1 Core B2 - D. Mic (Parrot)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24d",
            spawn="Parrot",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x068
        ),
    "Shell 1 Core B2 - M4 Ammo (Locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24d",
            spawn="Locker1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x069
        ),
    "Shell 1 Core B2 - M9 Ammo (Locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24d",
            spawn="Locker2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x06A
        ),
    "Shell 1 Core B2 - SOCOM Ammo (Locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24d",
            spawn="Locker3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x06B
        ),
    "Shell 1 Core B2 - Ration (Right alcove)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w24d",
            spawn="RightAlcove",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x06C
        )
}

plant_card_3: dict[str, MGS2LocationData] = {
    "Strut F Warehouse - AKS-74u Ammo (AK room 2)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="AKRoom2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x06E
        ),
    "Strut F Warehouse - AKS-74u Ammo (AK room 3)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="AKRoom3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x06F
        ),
    "Strut F Warehouse - AKS-74u Ammo (AK room 4-2)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="AKRoom4.2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x070
        ),
    "Strut F Warehouse - AKS-74u (AK room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="AKRoom4.1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x071
        ),
    "Strut F Warehouse - SOCOM Ammo (AK room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="AKRoom5",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x072
        ),
    "Strut F Warehouse - M4 Ammo (AK room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="AKRoom6",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x073
        ),
    "Strut F Warehouse - C4 (C4 room 1)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="C4Room1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x074
        ),
    "Strut F Warehouse - C4 (C4 room 2)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="C4Room2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x075
        ),
    "Strut F Warehouse - C4 (C4 room 3)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="C4Room3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x076
        ),
    "Strut F Warehouse - Claymore (C4 room 4)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="C4Room4",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x077
        ),
    "Strut F Warehouse - Claymore (C4 room 5)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="C4Room5",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x078
        ),
    "Strut F Warehouse - M4 Ammo (M4 room 1)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="M4Room1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x079
        ),
    "Strut F Warehouse - M4 Ammo (M4 room 2)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="M4Room2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x07A
        ),
    "Strut F Warehouse - M4 (M4 room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="M4Room3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x07B
        ),
    "Strut F Warehouse - PSG1 Ammo (M4 room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="M4Room4",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x07C
        ),
    "Strut F Warehouse - M4 Ammo (M4 room 5)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="M4Room5",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x07D
        ),
    "Strut F Warehouse - M4 Ammo (M4 room 6)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="M4Room6",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x07E
        ),
    "Strut F Warehouse - PSG1-T Ammo (RGB room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="RgbRoom1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x07F
        ),
    "Strut F Warehouse - RGB6 Ammo (RGB room 2)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="RgbRoom2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x080
        ),
    "Strut F Warehouse - RGB6 Ammo (RGB room 3)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="RgbRoom3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x081
        ),
    "Strut F Warehouse - RGB6 (RGB room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="RgbRoom4",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x082
        ),
    "Strut F Warehouse - PSG1 Ammo (PSG1 room 1)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="Psg1Room1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x083
        ),
    "Strut F Warehouse - PSG1 Ammo (PSG1 room 2)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="Psg1Room2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x084
        ),
    "Strut F Warehouse - PSG1 (PSG1 room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="Psg1Room3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x085
        ),
    "Strut F Warehouse - PSG1-T (PSG1 room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w22a",
            spawn="Psg1Room4",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x086
        ),
}

plant_shell_2: dict[str, MGS2LocationData] = {
    "Shell 1-2 Connecting Bridge - PSG1 Ammo (Front fire)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25b",
            spawn="FrontFire",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0A7
        ),
    "Shell 1-2 Connecting Bridge - PSG1-T Ammo (Front fire)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25b",
            spawn="FrontFire#2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0A8
        ),
    "Shell 1-2 Connecting Bridge - Ration (Pipe)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25b",
            spawn="Pipe",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0A9
        ),
    "Strut L Perimeter - AKS-74u Ammo (Lower catwalk)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25c",
            spawn="LowerCatwalk",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0AB
        ),
    "Strut L Perimeter - Chaff Grenade (Connecting bridge)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25c",
            spawn="ConnectingBridge",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0AC
        ),
    "Strut L Perimeter - PSG1 Ammo (Connecting bridge)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25c",
            spawn="ConnectingBridge#2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0AD
        ),
    "Strut L Perimeter - SOCOM Ammo (Connecting bridge)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25c",
            spawn="ConnectingBridge#3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0AE
        ),
    "Strut L Perimeter - Ration (Lower catwalk)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25c",
            spawn="LowerCatwalk#2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0AF
        ),
    "Shell 2 Core - Chaff Grenade (Strut H door)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="StrutHDoor1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0B0
        ),
    "Shell 2 Core - M4 Ammo (Rightside alcove)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="RightsideAlcove1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0B1
        ),
    "Shell 2 Core - M4 Ammo (Break room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="BreakRoom",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0B2
        ),
    "Shell 2 Core - M4 Ammo (Strut H door)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="StrutHDoor2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0B3
        ),
    "Shell 2 Core - M9 Ammo (Leftside stairs)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="LeftsideStairs",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0B4
        ),
    "Shell 2 Core - Nikita Ammo (Camera room conditional)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="CameraRoomConditional",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0B5
        ),
    "Shell 2 Core - Nikita Ammo (Rightside stairs conditional)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="RightsideStairsConditional",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0B6
        ),
    "Shell 2 Core - RGB6 Ammo (Rightside alcove)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="RightsideAlcove2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0B7
        ),
    "Shell 2 Core - SOCOM Ammo (Climbable boxes)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="ClimbableBoxes",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0B8
        ),
    "Shell 2 Core - Ration (Leftside landing)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="LeftsideLanding",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0B9
        ),
    "Shell 2 Filtration Chamber 1 - M4 Ammo (Middle hallway alcove)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31b",
            spawn="MiddleHallwayAlcove",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0BA
        ),
    "Shell 2 Filtration Chamber 1 - NVG (Deadend middle hallway)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31b",
            spawn="DeadendMiddleHallway",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0BB
        ),
    "Shell 2 Filtration Chamber 1 - Nikita (Nikita spawn)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31b",
            spawn="NikitaSpawn1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0BC
        ),
    "Shell 2 Filtration Chamber 1 - PSG1-T Ammo (Collapsed room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31b",
            spawn="CollapsedRoom1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0BD
        ),
    "Shell 2 Filtration Chamber 1 - RGB6 Ammo (Air pocket)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31b",
            spawn="AirPocket2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0BE
        ),
    "Shell 2 Filtration Chamber 1 - Stinger Ammo (Collapsed room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31b",
            spawn="CollapsedRoom2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0BF
        ),
    "Shell 2 Filtration Chamber 1 - Ration (Air pocket)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31b",
            spawn="AirPocket3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0C0
        ),
    "KL Connecting Bridge - Chaff Grenade (Shell entrance)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25d",
            spawn="ShellEntrance",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0C1
        ),
    "KL Connecting Bridge - M4 Ammo (Lower catwalk)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25d",
            spawn="LowerCatwalk",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0C2
        ),
    "KL Connecting Bridge - PSG1 Ammo (Shell entrance)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25d",
            spawn="ShellEntrance#2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0C3
        ),
    "KL Connecting Bridge - SOCOM Ammo (Lower catwalk)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25d",
            spawn="LowerCatwalk#2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0C4
        ),
    "KL Connecting Bridge - Ration (Shell entrance)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w25d",
            spawn="ShellEntrance#3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0C5
        )
}

plant_president: dict[str, MGS2LocationData] = {
    "Shell 2 Core - Book (Vents)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="Vents2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0A1
        ),
    "Shell 2 Core - Stinger Ammo (Vents)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="Vents1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0A2
        ),
    "Shell 2 Core - SOCOM Ammo (Electrical room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="ElectricalRoom",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0A3
        ),
    "Shell 2 Core - M.O. Disc":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="MODisc",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0A4
        ),
    "Shell 2 Core - Progressive Card": 
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31a",
            spawn="Shell2CoreCard",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0A5
        )
}

plant_vamp_and_emma: dict[str, MGS2LocationData] = {
    "Shell 2 Filtration Chamber 1 - M4 Ammo (Elevator)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31b",
            spawn="Elevator",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x089
        ),
    "Shell 2 Filtration Chamber 2 - Vamp (Reward)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31f",
            spawn="VampReward",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0CE
        ),
    "Shell 2 Filtration Chamber 2 - AKS-74u Ammo (Side room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31c",
            spawn="SideRoom1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x08A
        ),
    "Shell 2 Filtration Chamber 2 - Body Armor (Locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31c",
            spawn="Locker1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x08B
        ),
    "Shell 2 Filtration Chamber 2 - Book (Locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31c",
            spawn="Locker2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x08C
        ),
    "Shell 2 Filtration Chamber 2 - C4 (Locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31c",
            spawn="Locker3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x08D
        ),
    "Shell 2 Filtration Chamber 2 - C4 (Deadend hallway)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31c",
            spawn="DeadendHallway",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x08E
        ),
    "Shell 2 Filtration Chamber 2 - PSG1-T Ammo (Side room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31c",
            spawn="SideRoom2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x08F
        ),
    "Shell 2 Filtration Chamber 2 - Pentazemin (Node stairs)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31c",
            spawn="NodeStairs",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x090
        ),
    "Shell 2 Filtration Chamber 2 - Ration (Outside purification chamber)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31c",
            spawn="OutsidePurificationChamber",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x091
        ),
    "Shell 2 Filtration Chamber 2 - Thermal Goggles (Locker)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31c",
            spawn="Locker4",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x092
        ),
    "Shell 2 Core with Emma - AKS-74u Ammo (Rightside alcove)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31d",
            spawn="RightsideAlcove",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x093
        ),
    "Shell 2 Core with Emma - AKS-74u Ammo (Electrical room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31d",
            spawn="ElectricalRoom1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x094
        ),
    "Shell 2 Core with Emma - M9 Ammo (Electrical room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31d",
            spawn="ElectricalRoom2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x095
        ),
    "Shell 2 Core with Emma - PSG1 Ammo (Electrical room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31d",
            spawn="ElectricalRoom3",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x096
        ),
    "Shell 2 Core with Emma - PSG1-T Ammo (Vents)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31d",
            spawn="Vents1",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x097
        ),
    "Shell 2 Core with Emma - RGB6 Ammo (Vents)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31d",
            spawn="Vents2",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x098
        ),
    "Shell 2 Core with Emma - SOCOM Ammo (Leftside alcove)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31d",
            spawn="LeftsideAlcove",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x099
        ),
    "Shell 2 Core with Emma - SOCOM Ammo (Strut H door)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31d",
            spawn="StrutHDoor",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x09A
        ),
    "Shell 2 Core with Emma - Pentazemin (Leftside landing)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31d",
            spawn="LeftsideLanding",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x09B
        ),
    "Shell 2 Core with Emma - Ration (Electrical room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w31d",
            spawn="ElectricalRoom4",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x09C
        )
}

plant_arsenal_gear: dict[str, MGS2LocationData] = {
    "Sewage Treatment - SOCOM Ammo (Sewage treatment)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w28a",
            spawn="SewageTreatment",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x09E
        ),
    "Strut L Sniping - Vamp (Reward)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w32b",
            spawn="VampSnipingReward",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0CF
        ),
    "EF Connecting Bridge (Return) - Chaff Grenade (Near strut F)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w21b",
            spawn="NearStrutF",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x09D
        ),
    "Strut E Parcel Room - PSG1-T Ammo (Bottom right conveyer)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20a",
            spawn="BottomRightConveyer",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x09F
        ),
    "Strut E Parcel Room - Stinger Ammo (Under topside conveyer belt)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w20a",
            spawn="UnderTopsideConveyerBelt",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0A0
        ),
    "Arsenal Stomach - Ration (Torture room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w41a",
            spawn="TortureRoom",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0C6
        ),
    "Arsenal Stomach - Cold Medicine (Torture room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w41a",
            spawn="ColdMedicine",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0C7
        ),
    "Arsenal Jejunum - Box (Left catwalk)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w42a",
            spawn="LeftCatwalk",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0C8
        ),
    "Arsenal Jejunum - Cold Medicine (Back left main area)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w42a",
            spawn="BackLeftMainArea",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0C9
        ),
    "Arsenal Jejunum - Ration (Rightside main area)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w42a",
            spawn="RightsideMainArea",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0CA
        ),
    "Arsenal Ascending Colon - Ration (Back of hallway)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w43a",
            spawn="BackOfHallway",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0CB
        ),
    "Arsenal Sigmoid Colon - Ration (Entry room)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w45a",
            spawn="EntryRoom",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0CC
        ),
    "Arsenal Gear - RAY (Reward)":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w46a",
            spawn="RayReward",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0D0
        ),
    "Plant Complete":
        MGS2LocationData(
            region=Regions.PLANT,
            stage="w61a",
            spawn="PlantComplete",
            address=BASE_ID + Regions.PLANT_BASE_ID + 0x0CD
        )
}
