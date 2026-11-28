# Metal Gear Solid 2: Sons of Liberty Randomizer Setup Guide

## Required Software

- **Metal Gear Solid 2** from the **Master Collection on Steam** (Windows).
- **[Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)**, version 0.6.7 or newer.
- **`mgs2.apworld`**, from the Releases page of the MGS2 apworld's GitHub repository.
  <!-- TODO: link the releases page here -->

You don't need Python or anything else: the MGS2 client and patcher come inside `mgs2.apworld`
and run from the Archipelago Launcher.

## Installing

1. Install Archipelago.
2. Double-click `mgs2.apworld`. Archipelago installs it into its `custom_worlds` folder. (You can
   also copy the file there yourself.)

## Creating your YAML

The release includes a template, `MGS2.yaml`. Open it in a text editor and set `name` to your slot
name (it must be unique among the players in the multiworld):

```yaml
name: YourSlotName
game: "Metal Gear Solid 2: Sons of Liberty"
"Metal Gear Solid 2: Sons of Liberty":
  progression_balancing: 50
  accessibility: full
```

Give it to whoever generates the multiworld, or generate it yourself together with the other
players' YAMLs.

## Patching the game (once)

1. **Close MGS2.** The patcher rewrites game files the game reads while it runs, so the client
   won't patch while the game is open.
2. In the Archipelago Launcher, open **MGS2 Client**.
3. Type `/patch`. The client finds MGS2 through Steam and patches it. If it can't find the game,
   give the folder: `/patch C:\Program Files (x86)\Steam\steamapps\common\MGS2`

The patch is the same for every seed, so you only do this once, not per session or per seed.
Redo it if Steam restores the original files (a game update, or "Verify integrity of game
files"); the client warns you when the game it attaches to isn't patched.

## How to play

1. Open **MGS2 Client** from the Archipelago Launcher.
2. Connect: type `/connect <address>` (for example `/connect archipelago.gg:12345`) and enter your
   slot name. You can also click the connect link on the room page, which opens the client.
3. Start MGS2 from Steam.
4. Start a **new game on Normal difficulty** (the logic assumes Normal). Once you've entered
   another area, **save**: that links the save to this seed.

Connecting and starting the game can happen in either order.

### While playing

- **Pickups:** every item spot in the game is an Archipelago pickup. While the client is
  connected, picking one up says **ARCHIPELAGO ITEM**. If it says **RAZOR**, the client isn't
  connected (or isn't running): the pickup isn't lost, it's sent as soon as you reconnect.
- **Your items:** items found in your own world are given to you right away, even while
  disconnected. Items from other players arrive while connected.
- **Tanker and Plant are separate saves.** Each one gets the items for its own chapter. Starting a
  new game of either chapter gives you every item for that chapter received so far.
- **Supplies:** some items the game hands out itself (boss-fight supplies, enemy drops, the
  Arsenal returning your gear) aren't checks. The client says so when you pick one up.
- **Goal:** finish both the Tanker and the Plant, in any order.

### Webhost Room

If the site you use accepts multiworlds with custom worlds, upload the generated multiworld on its
Host Game page, then connect to the address the room page shows (or click its connect link).
Otherwise, host it locally (below).

### Locally hosted room

Host the generated multiworld with the Launcher's **Host** option, then connect to
`localhost:38281` (or the host's address and port, for other players).

## Client commands

| Command | What it does |
|---|---|
| `/patch` | Patch MGS2 for Archipelago (game closed). Optionally give the MGS2 folder. |
| `/unpatch` | Put MGS2's original files back (game closed). |
| `/connect <address>` | Connect to an Archipelago server. |
| `/mgs2` | Show what the client sees in the game (stage, save, items processed). |
| `/nearest` | List the AP spots nearest to you in the current area. |
| `/debug` | Show detail messages (checks, grants, stage changes) in the client window. |

## Switching Rooms

Each save remembers the seed it belongs to. A save from another seed is left alone by the client
(it says so); start a new game for the new seed. The patch doesn't change between seeds.

## Going back to normal MGS2

The patched game turns every item spot into an Archipelago pickup, so for a normal playthrough
close the game and run `/unpatch` in the client. Run `/patch` again before your next
Archipelago game. Keep Archipelago saves in separate save slots from normal playthroughs.

## Troubleshooting

- **"Couldn't find MGS2 through Steam"**: give the folder, `/patch <folder>`.
- **"MGS2 isn't patched for Archipelago"**: close the game, run `/patch`, start it again.
- **The client can't attach to the game**: start the Archipelago Launcher as administrator.
- **Logs**: the client's log is in Archipelago's `logs` folder (`MGS2Client_<date>.txt`). Include
  it when reporting a problem.

## Auto-Tracking

Not available yet.
