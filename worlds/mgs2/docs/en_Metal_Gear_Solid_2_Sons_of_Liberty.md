# Metal Gear Solid 2: Sons of Liberty

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to
configure and export a config file. MGS2 has no game-specific options yet; the YAML only needs your
slot name.

## What is Metal Gear Solid 2: Sons of Liberty?

A stealth action game in two chapters. In the **Tanker**, Solid Snake infiltrates a disguised tanker
to photograph a new Metal Gear. In the **Plant**, Raiden infiltrates the Big Shell offshore cleanup
facility to rescue the President. This world supports the **Master Collection** release on PC
(Steam).

## What does randomization do to this game?

Every item spot in both chapters becomes an Archipelago location: picking one up sends a check
instead of giving its usual item. The items you need (weapons, equipment, keycards and supplies)
are shuffled into the multiworld and arrive from wherever they ended up. Both start kits are
empty: what Snake and Raiden normally start with are locations too.

Logic follows the game's own requirements: for example Coolant for the bomb disposal, the PSG1 and
Stinger for Harrier, and keycard levels for locked doors.

## What is the goal?

Finish **both** chapters, in any order: the Tanker (after photographing Metal Gear RAY) and the
Plant (after the final battle).

## What items and locations get shuffled?

**Items:** the weapons, ammo, equipment and supplies of both chapters (boxes, goggles, sensors,
Coolant, Directional Microphone, B.D.U., suppressors and so on), and **Progressive Cards** for the
Plant's keycard levels. Each Progressive Card raises your card level by one. Card 5 is still given by
its story scene, so four Progressive Cards are in the pool.

**Locations:**
- every item pickup spot in the Tanker and the Plant;
- the start kits (Snake's M9, Camera, Cigarettes and A.P. Sensor; Raiden's A.P. Sensor and Binoculars);
- items characters give you (Olga's USP, Pliskin's SOCOM, Stillman's gifts, the B.D.U., Phone,
  M.O. Disc and keycards);
- one reward per boss: Olga, the Guard Rush, Fortune, Fatman, Ames, Harrier, Vamp, Vamp at Strut L, RAY;
- completing each chapter.

A few spots only exist at one point in the story and can be missed for good. Those only ever hold
filler items.

Items the game hands out by itself aren't locations: boss-fight supplies and their resupplies,
enemy drops, and your gear returned in Arsenal Gear. The client points these out when you pick one
up.

## Which items can be in another player's world?

Any of them. Your keycards, weapons and equipment can be found by other players, and you can find
theirs.

## What does another world's item look like in MGS2?

Every Archipelago pickup in the game keeps its usual look, and while the client is connected,
picking it up shows **ARCHIPELAGO ITEM**, whether it's yours or another player's. If it shows
**RAZOR**, the client isn't connected: the pickup still counts and is sent when you reconnect.

## When the player receives an item, what happens?

It's added to your inventory straight away. Items found in your own world are given the moment you
pick them up, even while disconnected. Some details:

- The Tanker and the Plant are separate saves, and each one only receives its own chapter's
  items. The other chapter's items wait for that save.
- Ammo for a gun you don't have yet is kept and added when you get the gun.
- During Arsenal Gear, while your gear is taken from you, received items wait until you get it
  back.
- Starting a new game of either chapter gives you every item for that chapter received so far.

## Known limitations

- Only **Normal** difficulty is supported (the logic assumes it).
- Only the **PC Master Collection** release (Steam, Windows).
