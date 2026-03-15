# Pykemon

A complete, text-based Pokémon RPG written in pure Python — no external game
engine required.  Play through the entire Kanto region, earn all 8 Gym Badges,
defeat the Elite Four, and become the Pokémon Champion.

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Running the Game](#running-the-game)
5. [Gameplay Guide](#gameplay-guide)
   - [Starting Out](#starting-out)
   - [The Menu System](#the-menu-system)
   - [Travelling the Kanto Region](#travelling-the-kanto-region)
   - [Wild Pokémon Encounters](#wild-pokémon-encounters)
   - [Fishing](#fishing)
   - [Safari Zone](#safari-zone)
   - [Trainer Battles](#trainer-battles)
   - [Gym Battles](#gym-battles)
   - [Your Rival Gary](#your-rival-gary)
   - [Team Rocket](#team-rocket)
   - [The Pokémon League](#the-pokémon-league)
   - [Saving and Loading](#saving-and-loading)
6. [Battle System](#battle-system)
7. [Key Systems](#key-systems)
8. [The Kanto Story Path](#the-kanto-story-path)
9. [Gym Badge Roadmap](#gym-badge-roadmap)
10. [Running the Tests](#running-the-tests)
11. [Project Structure](#project-structure)

---

## Features

- **Full Kanto story** — 33 locations from Pallet Town to Indigo Plateau
- **100 + Pokémon** with accurate stats, types, learnsets, and evolutions
- **Turn-based battle engine** — type effectiveness, status effects, weather,
  stat stages, STAB, critical hits, evasion/accuracy, held items
- **6 rival encounters** with Gary — his team scales with your progress, and he
  always starts with the Pokémon that is *weak against* your chosen starter
- **8 Gyms + Elite Four + Champion** — gym trainers must be beaten first; the
  Leader rewards you with a TM on victory
- **Catching system** — Poké Ball, Great Ball, Ultra Ball, Master Ball, and
  Safari Ball, each with accurate catch-rate formulae
- **Fishing** — Old Rod, Good Rod, and Super Rod with location-specific pools
- **Safari Zone** — unique throw-bait / throw-rock mechanic
- **Evolution** — level, item, trade, friendship, time-of-day, move-known
- **Pokédex** — see/catch tracking, detailed species look-up
- **Bag** — pockets for Medicine, Poké Balls, TMs/HMs, Held Items, Key Items,
  and more; items usable in and out of battle
- **TMs and HMs** — 50 TMs, 8 HMs, teachable to compatible Pokémon
- **Shiny Pokémon** — 1/4096 encounter rate
- **Friendship / Affection system** — affects certain evolutions and moves
- **Day / Night cycle** — some Pokémon only appear or evolve at certain times
- **Ride Pokémon** — HM replacement system (Fly, Surf, etc.)
- **Save / Load** — full game state persisted to `pykemon_save.json`
- **Legendary encounters** — Articuno (Seafoam Islands), Zapdos (Power Plant),
  Moltres (Victory Road), Mewtwo (post-game Cerulean Cave)

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Python      | **3.10 or later** (3.12 recommended) |
| pytest      | 9.x (test-only, optional) |

The game itself has **no third-party runtime dependencies** — it runs on the
Python standard library alone.

---

## Installation

```bash
# 1 — Clone the repository
git clone https://github.com/Lagcoder/Pykemon.git
cd Pykemon

# 2 — (Optional but recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows

# 3 — Install test dependencies (optional)
pip install pytest
```

That's it — there are no other packages to install.

---

## Running the Game

```bash
python main.py
```

> **Windows users:** if `python` is not on your PATH, try `py main.py` or
> `python3 main.py`.

On launch you will see the Professor Oak introduction, choose your name, and
pick your starter Pokémon.  Everything is driven by numbered menus — just type
the number next to the option you want and press **Enter**.

### Resuming a saved game

If a `pykemon_save.json` file exists in the same directory, the game will
offer to load it when you start:

```
  1. New Game
  2. Load Game (pykemon_save.json)
```

---

## Gameplay Guide

### Starting Out

1. **Enter your name** when Professor Oak asks.
2. **Choose your starter** — Bulbasaur, Charmander, or Squirtle.
   - Your rival Gary will always receive the starter that is *weak* against
     yours (e.g. pick Charmander → Gary gets Bulbasaur, which Fire beats).
3. You begin in **Pallet Town** with 5 Poké Balls and 5 Potions.
4. Your first goal is to reach Viridian City, deliver Oak's Parcel, then head
   north toward Pewter City and the first Gym.

---

### The Menu System

Every location presents a numbered list of actions.  Type the number and press
Enter.  Type **0** (or nothing) at any prompt to go back / skip.

Common options you will see:

| Option | What it does |
|--------|--------------|
| **Walk in tall grass** | Triggers a random wild Pokémon encounter |
| **Fish (Old Rod / …)** | Fishes in nearby water (rod must be in your Bag) |
| **Enter Safari Zone** | Special catch-only zone with its own mechanics |
| **Battle local trainers** | Fight NPC trainers at the current location |
| **★ Challenge Gym** | Challenge the Gym Leader (appears when you have not yet earned their badge) |
| **Pokémon Center** | Fully heals your entire party, free of charge |
| **Poké Mart** | Buy items; stock expands as you earn more Badges |
| **View Party** | See all six Pokémon; choose one to read its full summary |
| **Bag** | View all items; use medicine directly from here |
| **Pokédex** | Browse seen/caught counts; look up any species by name or number |
| **Ride Pokémon** | Use an HM move outside battle without needing HM items |
| **Badge Case** | See all 8 Badges and their effects |
| **Save Game** | Write your progress to `pykemon_save.json` |
| **Travel to next location →** | Advance to the next stop on the story path |
| **Quit without saving** | Exit immediately without overwriting your save |

---

### Travelling the Kanto Region

The story advances along a fixed path that mirrors the original Kanto journey.
Select **"Travel to next location →"** from the location menu when you are
ready to move on.  Before you can travel from a Gym city, the game will
automatically offer you the Gym challenge.

The full route is listed in [The Kanto Story Path](#the-kanto-story-path).

---

### Wild Pokémon Encounters

Select **"Walk in tall grass"** to meet a random wild Pokémon.  During a wild
battle you can:

- **Fight** — choose one of your active Pokémon's moves
- **Bag** — use an item (Poké Ball to catch, Potion to heal, etc.)
- **Switch** — send out a different Pokémon
- **Run** — flee from the battle (works against wild Pokémon)

Catching works on a weighted formula — the Pokémon's remaining HP, its catch
rate, and the Ball type all matter.  Weakening the Pokémon first (and applying
Sleep or Paralysis) dramatically increases your chances.

---

### Fishing

Fishing lets you catch Water-type Pokémon that do not appear in tall grass.

1. Obtain a rod as a Key Item (available in-game from certain NPCs):
   - **Old Rod** — catches mostly Magikarp; available early
   - **Good Rod** — a wider variety of Water-types; mid-game
   - **Super Rod** — rare and powerful Water-types; late-game
2. Travel to any location that has water (coastal routes, lakes, sea routes).
3. Select **"Fish (Old Rod)"** (or Good/Super Rod) from the location menu.
4. A wild battle starts just like a normal encounter — you can catch or defeat
   the hooked Pokémon.

> Rods only appear in the menu when you own that rod *and* the current
> location has a fish-encounter pool for it.

---

### Safari Zone

The **Fuchsia City Safari Zone** uses its own rules — you cannot use regular
moves.  Instead, each turn you choose:

| Action | Effect |
|--------|--------|
| **Throw Safari Ball** | Attempts to catch; catch chance decreases with higher Pokémon level |
| **Throw Bait** | Makes the Pokémon less likely to flee (but harder to catch next turn) |
| **Throw Rock** | Raises catch chance but increases flee chance |
| **Run** | Leave safely without catching |

Rare Pokémon like Scyther, Chansey, Kangaskhan, Tauros, and Dratini can only
be found in the Safari Zone.

---

### Trainer Battles

Select **"Battle local trainers"** to fight any NPC trainer at the current
location.  Unlike wild battles you *cannot* run from a trainer fight.

Defeating a trainer earns money (prize = trainer's highest-level Pokémon's
level × trainer class multiplier) and may trigger story dialogue.

---

### Gym Battles

Each Gym city has a **★ Challenge Gym** option.

1. **Gym trainers** — before facing the Leader, you must beat the trainers
   inside the Gym.  Losing to any trainer sends you to the nearest Pokémon
   Center.
2. **Gym Leader battle** — a standard trainer battle.  On victory you receive
   the Badge *and* a TM.
3. Badges unlock higher-level obedience and let Poké Mart stock better items.

---

### Your Rival Gary

Gary appears **six times** across the adventure.  His team grows at every
encounter and is always slightly ahead of your own level:

| # | Location | Party size |
|---|----------|-----------|
| 0 | Pallet Town | 1 |
| 1 | Cerulean City (Nugget Bridge) | 3 |
| 2 | S.S. Anne, Vermilion City | 5 |
| 3 | Silph Co., Saffron City | 5 |
| 4 | Victory Road | 6 |
| 5 | Indigo Plateau (Champion) | 6 |

Gary's starter is always the one that is **weak against your starter**:

| Your starter | Gary's starter |
|--------------|---------------|
| Bulbasaur 🌿 | Squirtle 💧 (Water is weak to Grass) |
| Charmander 🔥 | Bulbasaur 🌿 (Grass is weak to Fire) |
| Squirtle 💧 | Charmander 🔥 (Fire is weak to Water) |

---

### Team Rocket

Team Rocket blocks your path at several key points:

- **Mt. Moon** — two Grunts guard the fossil chamber
- **Pokémon Tower, Lavender Town** — Rocket agent hides the Silph Scope
- **Celadon City Game Corner** — Rocket hideout beneath the casino
- **Silph Co., Saffron City** — full building takeover; battle Giovanni himself
- **Viridian City Gym** — Giovanni is the final Gym Leader

Clearing each arc advances the story and unlocks new areas.

---

### The Pokémon League

Once you hold all **8 Badges**, travel to **Indigo Plateau** to face:

1. **Elite Four** — four specialist trainers in a row (no healing between
   battles unless you use items)
2. **Champion Gary** — the final boss; he is fully healed before the battle

Winning the championship triggers the credits and the Hall of Fame entry.
After the credits the game continues in post-game mode, unlocking the
legendary **Mewtwo** encounter in Cerulean Cave.

---

### Saving and Loading

- **During the game** — select **"Save Game"** from any location menu.  Your
  progress is written to `pykemon_save.json` in the current directory.
- **On the next launch** — choose **"Load Game"** from the start screen.
- The save file stores: player name, money, Badges, Bag contents, full party
  (with HP, moves, PP, IVs, EVs, friendship, shininess), story flags,
  visit history, Pokédex data, current location, and your starter choice
  (so Gary always gets the right counter-starter even after reloading).

> **Tip:** Save often — the game does *not* auto-save.

---

## Battle System

| Mechanic | Notes |
|----------|-------|
| **Type chart** | 15 types × 15 types; super-effective (×2), not very effective (×0.5), immune (×0) |
| **STAB** | Same-type attack bonus: ×1.5 damage |
| **Critical hits** | ~6.25 % base chance; raises to 12.5 % with high-crit moves |
| **Stat stages** | ±6 stages for Atk / Def / Sp. Atk / Sp. Def / Speed / Accuracy / Evasion |
| **Status effects** | Burn, Freeze, Paralysis, Poison, Toxic, Sleep, Confusion |
| **Weather** | Sun, Rain, Sand, Hail — each turn and type modifiers apply |
| **Held items** | Leftovers, Choice Band, Lum Berry, and more |
| **Priority moves** | Quick Attack, Extreme Speed, etc. always go first |
| **Two-turn moves** | Solar Beam, Fly, Dig, Dive, Sky Attack |
| **Recoil / drain** | Take Down, Double-Edge, Flamethrower burn chance, etc. |

---

## Key Systems

### Pokémon Center

Free full-party heal at every town.  Select **"Pokémon Center"** from the
location menu — the nurse heals all HP, PP, and status conditions instantly.

### Poké Mart

Costs money; stock unlocks with Badge count:

| Badges | New stock unlocked |
|--------|--------------------|
| 0 | Poké Ball, Potion, Antidote, Paralyze Heal |
| 2 | Super Potion, Great Ball |
| 4 | Hyper Potion, Ultra Ball, Revive |
| 6 | Max Potion, Max Revive, Full Heal |
| 8 | Max Elixir, Full Restore |

### Evolution

Pokémon evolve automatically after a battle when conditions are met.  Common
triggers: reaching a level threshold, using an Evolution Stone from the Bag,
high friendship at level-up, or holding a specific item while "trading"
(simulated in-game).

### Pokédex

Every time you encounter or catch a new Pokémon it is registered
automatically.  Use the **"Pokédex"** menu option to:

- View seen / caught totals
- Browse the full list
- Look up any species by name or number for its type, stats, and Pokédex entry

---

## The Kanto Story Path

```
Pallet Town  →  Route 22  →  Route 1  →  Viridian City  →  Route 2
→  Viridian Forest  →  Pewter City  →  Route 3  →  Mt. Moon  →  Route 4
→  Route 24  →  Route 25  →  Cerulean City  →  Route 5  →  Route 9
→  Rock Tunnel  →  Route 8  →  Lavender Town  →  Route 6  →  Vermilion City
→  Route 11  →  Route 7  →  Celadon City  →  Route 13  →  Cycling Road
→  Fuchsia City  →  Saffron City  →  Sea Route 19  →  Cinnabar Island
→  Pokémon Mansion  →  Viridian City (Return)  →  Victory Road  →  Indigo Plateau
```

---

## Gym Badge Roadmap

| # | City | Leader | Type | Badge | TM reward |
|---|------|--------|------|-------|-----------|
| 1 | Pewter City | Brock | Rock | Boulder Badge | TM80 |
| 2 | Cerulean City | Misty | Water | Cascade Badge | TM18 |
| 3 | Vermilion City | Lt. Surge | Electric | Thunder Badge | TM24 |
| 4 | Celadon City | Erika | Grass | Rainbow Badge | TM22 |
| 5 | Fuchsia City | Koga | Poison | Soul Badge | TM06 |
| 6 | Saffron City | Sabrina | Psychic | Marsh Badge | TM29 |
| 7 | Cinnabar Island | Blaine | Fire | Volcano Badge | TM38 |
| 8 | Viridian City | Giovanni | Ground | Earth Badge | TM26 |

---

## Running the Tests

```bash
# Install pytest if you haven't already
pip install pytest

# Run the full test suite (159 tests)
pytest tests/

# Run a single test class
pytest tests/test_pykemon.py::TestStorySystem -v

# Run with verbose output
pytest tests/ -v
```

The test suite covers: Pokémon stats and moves, type effectiveness, battle
engine, catching, evolution, Pokédex, Bag, TMs/HMs, Gym system, story flags,
GameState save/load, all 37 Kanto locations, all NPC trainer parties and
species, fishing encounter pools, rival escalation, and more.

---

## Project Structure

```
Pykemon/
├── main.py                  # Entry point — story loop, menus, all events
├── pykemon_save.json        # Created when you save (not tracked in git)
├── pykemon/
│   ├── core/
│   │   ├── pokemon.py       # Pokemon class, create_pokemon(), Move
│   │   ├── trainer.py       # Trainer, Bag, TRAINER_CLASSES, GymData
│   │   ├── pokedex.py       # Pokédex seen/caught tracking
│   │   └── battle.py        # Battle engine, BattleResult
│   ├── data/
│   │   ├── pokemon_data.py  # All species definitions (SpeciesData)
│   │   ├── moves.py         # All move definitions (MoveData)
│   │   └── items.py         # All item definitions (ItemData)
│   ├── story/
│   │   ├── events.py        # StoryFlag constants, GameState, save/load
│   │   ├── locations.py     # All 37 Kanto locations + STORY_PATH
│   │   └── rival.py         # Gary — 6 escalating encounters
│   ├── systems/
│   │   ├── evolution.py     # Evolution checker and handler
│   │   ├── friendship.py    # Friendship / Affection updates
│   │   └── time.py          # Day/Night cycle helpers
│   └── world/
│       ├── gym.py           # GymBadgeSystem, GymChallenge, gym battle flow
│       ├── center.py        # PokémonCenter heal logic
│       ├── mart.py          # PokéMart stock and purchase logic
│       ├── fossil.py        # FossilLab revival
│       └── ride.py          # RideSystem (HM replacement)
└── tests/
    └── test_pykemon.py      # 159-test suite (pytest)
```

