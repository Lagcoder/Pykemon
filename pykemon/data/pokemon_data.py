"""
Pokémon species data — stats, types, learnsets, evolutions, catch rates, etc.
Covers all 151 Generation I Pokémon (+ key Gen II/III additions for completeness).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from .types import PokemonType


@dataclass
class EvolutionCondition:
    """Describes when/how a Pokémon evolves."""
    evolves_to: str
    min_level: int = 0              # level-up at this level
    item: Optional[str] = None      # use-item evolution
    friendship: int = 0             # friendship threshold
    trade: bool = False             # trade evolution
    held_item: Optional[str] = None # held-item trade evolution
    time_of_day: Optional[str] = None  # "day" or "night"
    move_known: Optional[str] = None   # knows a specific move


@dataclass
class SpeciesData:
    number: int
    name: str
    types: list[PokemonType]
    base_hp: int
    base_atk: int
    base_def: int
    base_spa: int    # Sp. Atk
    base_spd: int    # Sp. Def
    base_spe: int    # Speed
    catch_rate: int  # 3-255
    base_exp: int
    growth_rate: str   # "slow", "medium_slow", "medium_fast", "fast", "erratic", "fluctuating"
    learnset: list[tuple[int, str]]  # (level, move_name)
    evolutions: list[EvolutionCondition] = field(default_factory=list)
    egg_groups: list[str] = field(default_factory=list)
    is_legendary: bool = False
    is_fossil: bool = False
    pokedex_entry: str = ""
    base_friendship: int = 70
    gender_ratio: float = 0.5  # probability of being female; -1 = genderless
    can_be_hidden: bool = True  # whether it can appear as shiny


SPECIES: dict[str, SpeciesData] = {}
SPECIES_BY_NUM: dict[int, SpeciesData] = {}


def _sp(s: SpeciesData) -> SpeciesData:
    SPECIES[s.name] = s
    SPECIES_BY_NUM[s.number] = s
    return s


# ────────────────────────────────────────────────────────────────────────────
# Generation I (original 151)
# ────────────────────────────────────────────────────────────────────────────

_sp(SpeciesData(1, "Bulbasaur",
    [PokemonType.GRASS, PokemonType.POISON],
    45, 49, 49, 65, 65, 45, 45, 64, "medium_slow",
    learnset=[(1,"Tackle"),(1,"Growl"),(3,"Vine Whip"),(6,"Growth"),(9,"Leech Seed"),(13,"Razor Leaf"),
              (20,"Poison Powder"),(25,"Sleep Powder"),(32,"Solar Beam"),(39,"Sweet Scent"),(46,"Growth")],
    evolutions=[EvolutionCondition("Ivysaur", min_level=16)],
    egg_groups=["Monster","Grass"],
    pokedex_entry="A strange seed was planted on its back at birth. The plant sprouts and grows with this Pokémon.",
    base_friendship=70))

_sp(SpeciesData(2, "Ivysaur",
    [PokemonType.GRASS, PokemonType.POISON],
    60, 62, 63, 80, 80, 60, 45, 142, "medium_slow",
    learnset=[(1,"Tackle"),(1,"Growl"),(1,"Vine Whip"),(3,"Vine Whip"),(6,"Growth"),(9,"Leech Seed"),
              (13,"Razor Leaf"),(20,"Poison Powder"),(25,"Sleep Powder"),(32,"Solar Beam"),(46,"Growth")],
    evolutions=[EvolutionCondition("Venusaur", min_level=32)],
    egg_groups=["Monster","Grass"]))

_sp(SpeciesData(3, "Venusaur",
    [PokemonType.GRASS, PokemonType.POISON],
    80, 82, 83, 100, 100, 80, 45, 236, "medium_slow",
    learnset=[(1,"Tackle"),(1,"Growl"),(1,"Vine Whip"),(3,"Vine Whip"),(6,"Growth"),(9,"Leech Seed"),
              (13,"Razor Leaf"),(20,"Poison Powder"),(25,"Sleep Powder"),(32,"Solar Beam"),(46,"Growth")],
    egg_groups=["Monster","Grass"]))

_sp(SpeciesData(4, "Charmander",
    [PokemonType.FIRE],
    39, 52, 43, 60, 50, 65, 45, 62, "medium_slow",
    learnset=[(1,"Scratch"),(1,"Growl"),(4,"Ember"),(8,"Smokescreen"),(15,"Dragon Rage"),(19,"Slash"),
              (22,"Flamethrower"),(28,"Fire Spin"),(38,"Inferno")],
    evolutions=[EvolutionCondition("Charmeleon", min_level=16)],
    egg_groups=["Monster","Dragon"],
    pokedex_entry="Obviously prefers hot places. When it rains, steam is said to spout from the tip of its tail.",
    base_friendship=70))

_sp(SpeciesData(5, "Charmeleon",
    [PokemonType.FIRE],
    58, 64, 58, 80, 65, 80, 45, 142, "medium_slow",
    learnset=[(1,"Scratch"),(1,"Growl"),(1,"Ember"),(4,"Ember"),(8,"Smokescreen"),(15,"Dragon Rage"),
              (22,"Slash"),(29,"Flamethrower"),(38,"Fire Spin")],
    evolutions=[EvolutionCondition("Charizard", min_level=36)],
    egg_groups=["Monster","Dragon"]))

_sp(SpeciesData(6, "Charizard",
    [PokemonType.FIRE, PokemonType.FLYING],
    78, 84, 78, 109, 85, 100, 45, 240, "medium_slow",
    learnset=[(1,"Scratch"),(1,"Growl"),(1,"Ember"),(1,"Smokescreen"),(15,"Dragon Rage"),(22,"Slash"),
              (36,"Flamethrower"),(44,"Fire Blast"),(50,"Wing Attack")],
    egg_groups=["Monster","Dragon"]))

_sp(SpeciesData(7, "Squirtle",
    [PokemonType.WATER],
    44, 48, 65, 50, 64, 43, 45, 63, "medium_slow",
    learnset=[(1,"Tackle"),(1,"Tail Whip"),(3,"Bubble"),(6,"Withdraw"),(9,"Water Gun"),(15,"Bite"),
              (18,"Rapid Spin"),(22,"Protect"),(28,"Rain Dance"),(34,"Skull Bash"),(40,"Hydro Pump")],
    evolutions=[EvolutionCondition("Wartortle", min_level=16)],
    egg_groups=["Monster","Water 1"],
    pokedex_entry="After birth, its back swells and hardens into a shell. Powerfully sprays foam from its mouth.",
    base_friendship=70))

_sp(SpeciesData(8, "Wartortle",
    [PokemonType.WATER],
    59, 63, 80, 65, 80, 58, 45, 142, "medium_slow",
    learnset=[(1,"Tackle"),(1,"Tail Whip"),(1,"Bubble"),(3,"Bubble"),(6,"Withdraw"),(9,"Water Gun"),
              (15,"Bite"),(18,"Rapid Spin"),(22,"Protect"),(28,"Rain Dance"),(34,"Skull Bash"),(40,"Hydro Pump")],
    evolutions=[EvolutionCondition("Blastoise", min_level=36)],
    egg_groups=["Monster","Water 1"]))

_sp(SpeciesData(9, "Blastoise",
    [PokemonType.WATER],
    79, 83, 100, 85, 105, 78, 45, 239, "medium_slow",
    learnset=[(1,"Tackle"),(1,"Tail Whip"),(1,"Bubble"),(1,"Withdraw"),(9,"Water Gun"),(15,"Bite"),
              (18,"Rapid Spin"),(22,"Protect"),(28,"Rain Dance"),(34,"Skull Bash"),(36,"Hydro Pump")],
    egg_groups=["Monster","Water 1"]))

_sp(SpeciesData(10, "Caterpie",
    [PokemonType.BUG],
    45, 30, 35, 20, 20, 45, 255, 53, "medium_fast",
    learnset=[(1,"Tackle"),(1,"String Shot")],
    evolutions=[EvolutionCondition("Metapod", min_level=7)],
    egg_groups=["Bug"],
    pokedex_entry="Its short feet are tipped with suction pads that enable it to tirelessly climb slopes and walls."))

_sp(SpeciesData(11, "Metapod",
    [PokemonType.BUG],
    50, 20, 55, 25, 25, 30, 120, 72, "medium_fast",
    learnset=[(1,"Harden")],
    evolutions=[EvolutionCondition("Butterfree", min_level=10)],
    egg_groups=["Bug"]))

_sp(SpeciesData(12, "Butterfree",
    [PokemonType.BUG, PokemonType.FLYING],
    60, 45, 50, 90, 80, 70, 45, 178, "medium_fast",
    learnset=[(1,"Confusion"),(12,"Confusion"),(15,"Poison Powder"),(16,"Stun Spore"),(17,"Sleep Powder"),
              (21,"Gust"),(24,"Supersonic"),(27,"Psybeam"),(30,"Wing Attack"),(33,"Whirlwind"),
              (36,"Psychic"),(39,"Silver Wind")],
    egg_groups=["Bug"]))

_sp(SpeciesData(13, "Weedle",
    [PokemonType.BUG, PokemonType.POISON],
    40, 35, 30, 20, 20, 50, 255, 52, "medium_fast",
    learnset=[(1,"Poison Sting"),(1,"String Shot")],
    evolutions=[EvolutionCondition("Kakuna", min_level=7)],
    egg_groups=["Bug"]))

_sp(SpeciesData(14, "Kakuna",
    [PokemonType.BUG, PokemonType.POISON],
    45, 25, 50, 25, 25, 35, 120, 71, "medium_fast",
    learnset=[(1,"Harden")],
    evolutions=[EvolutionCondition("Beedrill", min_level=10)],
    egg_groups=["Bug"]))

_sp(SpeciesData(15, "Beedrill",
    [PokemonType.BUG, PokemonType.POISON],
    65, 90, 40, 45, 80, 75, 45, 178, "medium_fast",
    learnset=[(1,"Fury Attack"),(1,"Twineedle"),(20,"Focus Energy"),(25,"Fury Swipes"),
              (30,"Toxic"),(35,"Agility"),(40,"Pin Missile")],
    egg_groups=["Bug"]))

_sp(SpeciesData(16, "Pidgey",
    [PokemonType.NORMAL, PokemonType.FLYING],
    40, 45, 40, 35, 35, 56, 255, 50, "medium_slow",
    learnset=[(1,"Tackle"),(5,"Sand Attack"),(9,"Gust"),(13,"Quick Attack"),(19,"Whirlwind"),
              (25,"Twister"),(31,"Feather Dance"),(39,"Agility"),(45,"Wing Attack"),(51,"Mirror Move")],
    evolutions=[EvolutionCondition("Pidgeotto", min_level=18)],
    egg_groups=["Flying"]))

_sp(SpeciesData(17, "Pidgeotto",
    [PokemonType.NORMAL, PokemonType.FLYING],
    63, 60, 55, 50, 50, 71, 120, 122, "medium_slow",
    learnset=[(1,"Tackle"),(1,"Sand Attack"),(5,"Sand Attack"),(9,"Gust"),(13,"Quick Attack"),
              (21,"Whirlwind"),(28,"Agility"),(36,"Wing Attack"),(42,"Mirror Move")],
    evolutions=[EvolutionCondition("Pidgeot", min_level=36)],
    egg_groups=["Flying"]))

_sp(SpeciesData(18, "Pidgeot",
    [PokemonType.NORMAL, PokemonType.FLYING],
    83, 80, 75, 70, 70, 101, 45, 216, "medium_slow",
    learnset=[(1,"Tackle"),(1,"Sand Attack"),(1,"Gust"),(1,"Quick Attack"),(21,"Whirlwind"),
              (28,"Agility"),(38,"Wing Attack"),(44,"Mirror Move")],
    egg_groups=["Flying"]))

_sp(SpeciesData(19, "Rattata",
    [PokemonType.NORMAL],
    30, 56, 35, 25, 35, 72, 255, 51, "medium_fast",
    learnset=[(1,"Tackle"),(1,"Tail Whip"),(4,"Quick Attack"),(7,"Focus Energy"),(10,"Bite"),
              (13,"Pursuit"),(16,"Hyper Fang"),(19,"Sucker Punch"),(22,"Super Fang"),(25,"Double-Edge")],
    evolutions=[EvolutionCondition("Raticate", min_level=20)],
    egg_groups=["Field"]))

_sp(SpeciesData(20, "Raticate",
    [PokemonType.NORMAL],
    55, 81, 60, 50, 70, 97, 90, 145, "medium_fast",
    learnset=[(1,"Tackle"),(1,"Tail Whip"),(1,"Quick Attack"),(1,"Focus Energy"),(10,"Bite"),
              (14,"Pursuit"),(19,"Hyper Fang"),(24,"Sucker Punch"),(27,"Super Fang"),(32,"Double-Edge")],
    egg_groups=["Field"]))

_sp(SpeciesData(21, "Spearow",
    [PokemonType.NORMAL, PokemonType.FLYING],
    40, 60, 30, 31, 31, 70, 255, 52, "medium_fast",
    learnset=[(1,"Peck"),(1,"Growl"),(7,"Leer"),(13,"Fury Attack"),(19,"Mirror Move"),
              (25,"Aerial Ace"),(31,"Agility"),(37,"Drill Peck")],
    evolutions=[EvolutionCondition("Fearow", min_level=20)],
    egg_groups=["Flying"]))

_sp(SpeciesData(22, "Fearow",
    [PokemonType.NORMAL, PokemonType.FLYING],
    65, 90, 65, 61, 61, 100, 90, 155, "medium_fast",
    learnset=[(1,"Peck"),(1,"Growl"),(1,"Leer"),(7,"Leer"),(13,"Fury Attack"),(19,"Mirror Move"),
              (25,"Agility"),(31,"Aerial Ace"),(37,"Drill Peck")],
    egg_groups=["Flying"]))

_sp(SpeciesData(23, "Ekans",
    [PokemonType.POISON],
    35, 60, 44, 40, 54, 55, 255, 58, "medium_fast",
    learnset=[(1,"Wrap"),(1,"Leer"),(9,"Poison Sting"),(12,"Bite"),(17,"Glare"),(20,"Screech"),
              (25,"Acid"),(28,"Stockpile"),(33,"Swallow"),(36,"Spit Up"),(41,"Haze")],
    evolutions=[EvolutionCondition("Arbok", min_level=22)],
    egg_groups=["Field","Dragon"]))

_sp(SpeciesData(24, "Arbok",
    [PokemonType.POISON],
    60, 95, 69, 65, 79, 80, 90, 153, "medium_fast",
    learnset=[(1,"Wrap"),(1,"Leer"),(1,"Poison Sting"),(9,"Poison Sting"),(12,"Bite"),
              (17,"Glare"),(20,"Screech"),(27,"Acid"),(33,"Stockpile"),(38,"Swallow"),(43,"Haze")],
    egg_groups=["Field","Dragon"]))

_sp(SpeciesData(25, "Pikachu",
    [PokemonType.ELECTRIC],
    35, 55, 40, 50, 50, 90, 190, 112, "medium_fast",
    learnset=[(1,"Thundershock"),(1,"Growl"),(1,"Tail Whip"),(5,"Tail Whip"),(9,"Quick Attack"),
              (13,"Thunder Wave"),(18,"Electro Ball"),(21,"Double Team"),(25,"Slam"),(29,"Thunderbolt"),
              (33,"Feint"),(37,"Agility"),(42,"Discharge"),(45,"Light Screen"),(50,"Thunder")],
    evolutions=[EvolutionCondition("Raichu", item="Thunder Stone")],
    egg_groups=["Field","Fairy"],
    base_friendship=70,
    pokedex_entry="When several of these Pokémon gather, their electricity could build and cause lightning storms.",
    gender_ratio=0.5))

_sp(SpeciesData(26, "Raichu",
    [PokemonType.ELECTRIC],
    60, 90, 55, 90, 80, 110, 75, 218, "medium_fast",
    learnset=[(1,"Thundershock"),(1,"Tail Whip"),(1,"Quick Attack"),(1,"Thunderbolt")],
    egg_groups=["Field","Fairy"]))

_sp(SpeciesData(27, "Sandshrew",
    [PokemonType.GROUND],
    50, 75, 85, 20, 30, 40, 255, 60, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Defense Curl"),(6,"Sand Attack"),(11,"Poison Sting"),(17,"Swift"),
              (23,"Fury Swipes"),(29,"Rollout"),(35,"Slash"),(41,"Sand Tomb"),(47,"Gyro Ball")],
    evolutions=[EvolutionCondition("Sandslash", min_level=22)],
    egg_groups=["Field"]))

_sp(SpeciesData(28, "Sandslash",
    [PokemonType.GROUND],
    75, 100, 110, 45, 55, 65, 90, 158, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Defense Curl"),(1,"Sand Attack"),(6,"Sand Attack"),(11,"Poison Sting"),
              (17,"Swift"),(23,"Fury Swipes"),(29,"Rollout"),(35,"Slash"),(41,"Sand Tomb")],
    egg_groups=["Field"]))

_sp(SpeciesData(29, "Nidoran♀",
    [PokemonType.POISON],
    55, 47, 52, 40, 40, 41, 235, 55, "medium_slow",
    learnset=[(1,"Growl"),(1,"Scratch"),(7,"Tail Whip"),(9,"Double Kick"),(12,"Poison Sting"),
              (17,"Fury Swipes"),(20,"Bite"),(23,"Helping Hand"),(29,"Toxic"),(36,"Flatter"),(40,"Crunch")],
    evolutions=[EvolutionCondition("Nidorina", min_level=16)],
    egg_groups=["Monster","Field"],
    gender_ratio=1.0))

_sp(SpeciesData(30, "Nidorina",
    [PokemonType.POISON],
    70, 62, 67, 55, 55, 56, 120, 128, "medium_slow",
    learnset=[(1,"Growl"),(1,"Scratch"),(1,"Tail Whip"),(7,"Tail Whip"),(9,"Double Kick"),
              (12,"Poison Sting"),(17,"Fury Swipes"),(20,"Bite"),(23,"Helping Hand"),(29,"Toxic")],
    evolutions=[EvolutionCondition("Nidoqueen", item="Moon Stone")],
    egg_groups=["Undiscovered"],
    gender_ratio=1.0))

_sp(SpeciesData(31, "Nidoqueen",
    [PokemonType.POISON, PokemonType.GROUND],
    90, 92, 87, 75, 85, 76, 45, 223, "medium_slow",
    learnset=[(1,"Scratch"),(1,"Tail Whip"),(1,"Double Kick"),(1,"Poison Sting"),(23,"Helping Hand"),
              (29,"Toxic"),(36,"Flatter"),(40,"Crunch"),(44,"Earth Power"),(48,"Superpower")],
    egg_groups=["Undiscovered"],
    gender_ratio=1.0))

_sp(SpeciesData(32, "Nidoran♂",
    [PokemonType.POISON],
    46, 57, 40, 40, 40, 50, 235, 55, "medium_slow",
    learnset=[(1,"Leer"),(1,"Peck"),(7,"Focus Energy"),(9,"Double Kick"),(12,"Poison Sting"),
              (17,"Fury Attack"),(20,"Horn Attack"),(23,"Helping Hand"),(29,"Toxic"),(36,"Flatter")],
    evolutions=[EvolutionCondition("Nidorino", min_level=16)],
    egg_groups=["Monster","Field"],
    gender_ratio=0.0))

_sp(SpeciesData(33, "Nidorino",
    [PokemonType.POISON],
    61, 72, 57, 55, 55, 65, 120, 128, "medium_slow",
    learnset=[(1,"Leer"),(1,"Peck"),(1,"Focus Energy"),(7,"Focus Energy"),(9,"Double Kick"),
              (12,"Poison Sting"),(17,"Fury Attack"),(20,"Horn Attack"),(23,"Helping Hand"),(29,"Toxic")],
    evolutions=[EvolutionCondition("Nidoking", item="Moon Stone")],
    egg_groups=["Monster","Field"],
    gender_ratio=0.0))

_sp(SpeciesData(34, "Nidoking",
    [PokemonType.POISON, PokemonType.GROUND],
    81, 102, 77, 85, 75, 85, 45, 223, "medium_slow",
    learnset=[(1,"Peck"),(1,"Focus Energy"),(1,"Double Kick"),(1,"Poison Sting"),(23,"Helping Hand"),
              (29,"Toxic"),(36,"Flatter"),(40,"Crunch"),(44,"Earth Power"),(48,"Megahorn")],
    egg_groups=["Monster","Field"],
    gender_ratio=0.0))

_sp(SpeciesData(35, "Clefairy",
    [PokemonType.NORMAL],
    70, 45, 48, 60, 65, 35, 150, 113, "fast",
    learnset=[(1,"Pound"),(1,"Growl"),(4,"Encore"),(8,"Sing"),(11,"DoubleSlap"),(15,"Defense Curl"),
              (18,"Follow Me"),(22,"Minimize"),(25,"Wake-Up Slap"),(29,"Metronome"),(32,"Moonblast"),
              (36,"Gravity"),(39,"Moonlight"),(43,"Stored Power"),(46,"Light Screen"),(50,"Cosmic Power")],
    evolutions=[EvolutionCondition("Clefable", item="Moon Stone")],
    egg_groups=["Fairy"],
    gender_ratio=0.75))

_sp(SpeciesData(36, "Clefable",
    [PokemonType.NORMAL],
    95, 70, 73, 95, 90, 60, 25, 217, "fast",
    learnset=[(1,"Pound"),(1,"Growl"),(1,"Sing"),(1,"DoubleSlap"),(1,"Metronome")],
    egg_groups=["Fairy"],
    gender_ratio=0.75))

_sp(SpeciesData(37, "Vulpix",
    [PokemonType.FIRE],
    38, 41, 40, 50, 65, 65, 190, 60, "medium_fast",
    learnset=[(1,"Ember"),(1,"Tail Whip"),(5,"Roar"),(9,"Quick Attack"),(13,"Fire Spin"),(17,"Confuse Ray"),
              (21,"Imprison"),(25,"Faint Attack"),(29,"Flamethrower"),(33,"Safeguard"),(37,"Will-O-Wisp"),
              (41,"Extrasensory"),(45,"Fire Blast")],
    evolutions=[EvolutionCondition("Ninetales", item="Fire Stone")],
    egg_groups=["Field"],
    gender_ratio=0.75))

_sp(SpeciesData(38, "Ninetales",
    [PokemonType.FIRE],
    73, 76, 75, 81, 100, 100, 75, 177, "medium_fast",
    learnset=[(1,"Ember"),(1,"Quick Attack"),(1,"Confuse Ray"),(1,"Fire Spin")],
    egg_groups=["Field"],
    gender_ratio=0.75))

_sp(SpeciesData(39, "Jigglypuff",
    [PokemonType.NORMAL],
    115, 45, 20, 45, 25, 20, 170, 76, "fast",
    learnset=[(1,"Sing"),(1,"Defense Curl"),(4,"Pound"),(9,"Disable"),(13,"Defense Curl"),
              (17,"DoubleSlap"),(25,"Rest"),(29,"Body Slam"),(33,"Gyro Ball"),(41,"Wake-Up Slap"),
              (45,"Mimic"),(49,"Hyper Voice")],
    evolutions=[EvolutionCondition("Wigglytuff", item="Moon Stone")],
    egg_groups=["Fairy"],
    gender_ratio=0.75))

_sp(SpeciesData(40, "Wigglytuff",
    [PokemonType.NORMAL],
    140, 70, 45, 85, 50, 45, 50, 173, "fast",
    learnset=[(1,"Sing"),(1,"Defense Curl"),(1,"Pound"),(1,"Disable")],
    egg_groups=["Fairy"],
    gender_ratio=0.75))

_sp(SpeciesData(41, "Zubat",
    [PokemonType.POISON, PokemonType.FLYING],
    40, 45, 35, 30, 40, 55, 255, 54, "medium_fast",
    learnset=[(1,"Leech Life"),(5,"Supersonic"),(9,"Astonish"),(13,"Bite"),(17,"Wing Attack"),
              (21,"Confuse Ray"),(25,"Air Cutter"),(29,"Mean Look"),(33,"Acrobatics"),(37,"Haze"),
              (41,"Air Slash")],
    evolutions=[EvolutionCondition("Golbat", min_level=22)],
    egg_groups=["Flying"],
    gender_ratio=0.5))

_sp(SpeciesData(42, "Golbat",
    [PokemonType.POISON, PokemonType.FLYING],
    75, 80, 70, 65, 75, 90, 90, 159, "medium_fast",
    learnset=[(1,"Screech"),(1,"Leech Life"),(5,"Supersonic"),(9,"Astonish"),(13,"Bite"),
              (17,"Wing Attack"),(21,"Confuse Ray"),(25,"Air Cutter"),(29,"Mean Look"),(33,"Acrobatics"),
              (37,"Haze"),(41,"Air Slash")],
    egg_groups=["Flying"],
    gender_ratio=0.5))

_sp(SpeciesData(43, "Oddish",
    [PokemonType.GRASS, PokemonType.POISON],
    45, 50, 55, 75, 65, 30, 255, 64, "medium_slow",
    learnset=[(1,"Absorb"),(5,"Sweet Scent"),(9,"Acid"),(13,"Poison Powder"),(15,"Stun Spore"),
              (17,"Sleep Powder"),(21,"Mega Drain"),(25,"Lucky Chant"),(29,"Moonblast"),(33,"Giga Drain"),
              (37,"Petal Dance"),(41,"Solar Beam")],
    evolutions=[EvolutionCondition("Gloom", min_level=21)],
    egg_groups=["Grass"]))

_sp(SpeciesData(44, "Gloom",
    [PokemonType.GRASS, PokemonType.POISON],
    60, 65, 70, 85, 75, 40, 120, 138, "medium_slow",
    learnset=[(1,"Absorb"),(1,"Sweet Scent"),(5,"Sweet Scent"),(9,"Acid"),(13,"Poison Powder"),
              (15,"Stun Spore"),(17,"Sleep Powder"),(21,"Mega Drain"),(25,"Lucky Chant"),
              (29,"Moonblast"),(33,"Giga Drain"),(37,"Petal Dance")],
    evolutions=[EvolutionCondition("Vileplume", item="Leaf Stone"),
                EvolutionCondition("Bellossom", item="Sun Stone")],
    egg_groups=["Grass"]))

_sp(SpeciesData(45, "Vileplume",
    [PokemonType.GRASS, PokemonType.POISON],
    75, 80, 85, 110, 90, 50, 45, 221, "medium_slow",
    learnset=[(1,"Absorb"),(1,"Acid"),(1,"Poison Powder"),(1,"Stun Spore"),(1,"Sleep Powder"),
              (1,"Mega Drain"),(1,"Moonblast"),(1,"Petal Dance"),(1,"Solar Beam")],
    egg_groups=["Grass"]))

_sp(SpeciesData(46, "Paras",
    [PokemonType.BUG, PokemonType.GRASS],
    35, 70, 55, 45, 55, 25, 190, 57, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Stun Spore"),(6,"PoisonPowder"),(11,"Leech Life"),(17,"Spore"),
              (22,"Slash"),(27,"Growth"),(32,"Giga Drain"),(37,"Aromatherapy")],
    evolutions=[EvolutionCondition("Parasect", min_level=24)],
    egg_groups=["Bug","Grass"]))

_sp(SpeciesData(47, "Parasect",
    [PokemonType.BUG, PokemonType.GRASS],
    60, 95, 80, 60, 80, 30, 75, 142, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Stun Spore"),(1,"PoisonPowder"),(6,"PoisonPowder"),(11,"Leech Life"),
              (17,"Spore"),(22,"Slash"),(27,"Growth"),(32,"Giga Drain")],
    egg_groups=["Bug","Grass"]))

_sp(SpeciesData(48, "Venonat",
    [PokemonType.BUG, PokemonType.POISON],
    60, 55, 50, 40, 55, 45, 190, 61, "medium_fast",
    learnset=[(1,"Tackle"),(1,"Disable"),(5,"Foresight"),(9,"Supersonic"),(13,"Confusion"),
              (17,"Poison Powder"),(21,"Leech Life"),(25,"Stun Spore"),(29,"Psybeam"),
              (33,"Sleep Powder"),(37,"Zen Headbutt"),(41,"Psychic")],
    evolutions=[EvolutionCondition("Venomoth", min_level=31)],
    egg_groups=["Bug"]))

_sp(SpeciesData(49, "Venomoth",
    [PokemonType.BUG, PokemonType.POISON],
    70, 65, 60, 90, 75, 90, 75, 158, "medium_fast",
    learnset=[(1,"Tackle"),(1,"Disable"),(1,"Foresight"),(1,"Supersonic"),(13,"Confusion"),
              (17,"Poison Powder"),(21,"Leech Life"),(25,"Stun Spore"),(29,"Psybeam"),
              (33,"Sleep Powder"),(37,"Zen Headbutt"),(41,"Psychic")],
    egg_groups=["Bug"]))

_sp(SpeciesData(50, "Diglett",
    [PokemonType.GROUND],
    10, 55, 25, 35, 45, 95, 255, 53, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Sand Attack"),(4,"Growl"),(7,"Astonish"),(12,"Mud Slap"),
              (15,"Magnitude"),(19,"Bulldoze"),(22,"Sucker Punch"),(26,"Mud Bomb"),(29,"Slash"),
              (33,"Earthquake"),(36,"Fissure"),(40,"Sandstorm")],
    evolutions=[EvolutionCondition("Dugtrio", min_level=26)],
    egg_groups=["Field"]))

_sp(SpeciesData(51, "Dugtrio",
    [PokemonType.GROUND],
    35, 100, 50, 50, 70, 120, 50, 149, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Sand Attack"),(1,"Growl"),(1,"Astonish"),(12,"Mud Slap"),
              (15,"Magnitude"),(19,"Bulldoze"),(22,"Sucker Punch"),(26,"Mud Bomb"),
              (29,"Slash"),(33,"Earthquake"),(36,"Fissure")],
    egg_groups=["Field"]))

_sp(SpeciesData(52, "Meowth",
    [PokemonType.NORMAL],
    40, 45, 35, 40, 40, 90, 255, 58, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Growl"),(4,"Bite"),(7,"Pay Day"),(10,"Screech"),(14,"Fury Swipes"),
              (17,"Faint Attack"),(20,"Taunt"),(24,"Slash"),(27,"Nasty Plot"),(30,"Assurance"),(33,"Captivate")],
    evolutions=[EvolutionCondition("Persian", min_level=28)],
    egg_groups=["Field"],
    gender_ratio=0.5))

_sp(SpeciesData(53, "Persian",
    [PokemonType.NORMAL],
    65, 70, 60, 65, 65, 115, 90, 154, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Growl"),(1,"Bite"),(1,"Pay Day"),(10,"Screech"),
              (14,"Fury Swipes"),(17,"Faint Attack"),(20,"Taunt"),(24,"Slash"),(27,"Nasty Plot")],
    egg_groups=["Field"],
    gender_ratio=0.5))

_sp(SpeciesData(54, "Psyduck",
    [PokemonType.WATER],
    50, 52, 48, 65, 50, 55, 190, 64, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Tail Whip"),(4,"Water Sport"),(8,"Confusion"),(11,"Disable"),
              (15,"Scratching"),(18,"Water Pulse"),(22,"Screech"),(25,"Psych Up"),(29,"Fury Swipes"),
              (32,"Zen Headbutt"),(36,"Amnesia"),(39,"Aqua Tail"),(43,"Psychic")],
    evolutions=[EvolutionCondition("Golduck", min_level=33)],
    egg_groups=["Water 1","Field"]))

_sp(SpeciesData(55, "Golduck",
    [PokemonType.WATER],
    80, 82, 78, 95, 80, 85, 75, 175, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Tail Whip"),(1,"Water Sport"),(1,"Confusion"),(1,"Disable"),
              (18,"Water Pulse"),(22,"Screech"),(25,"Psych Up"),(29,"Fury Swipes"),
              (32,"Zen Headbutt"),(36,"Amnesia"),(39,"Aqua Tail"),(43,"Psychic")],
    egg_groups=["Water 1","Field"]))

_sp(SpeciesData(56, "Mankey",
    [PokemonType.FIGHTING],
    40, 80, 35, 35, 45, 70, 190, 61, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Leer"),(1,"Low Kick"),(6,"Fury Swipes"),(11,"Focus Energy"),
              (16,"Karate Chop"),(21,"Seismic Toss"),(26,"Screech"),(31,"Assurance"),
              (36,"Swagger"),(41,"Cross Chop"),(46,"Thrash"),(51,"Close Combat")],
    evolutions=[EvolutionCondition("Primeape", min_level=28)],
    egg_groups=["Field"]))

_sp(SpeciesData(57, "Primeape",
    [PokemonType.FIGHTING],
    65, 105, 60, 60, 70, 95, 75, 159, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Leer"),(1,"Low Kick"),(1,"Fury Swipes"),(11,"Focus Energy"),
              (16,"Karate Chop"),(21,"Seismic Toss"),(26,"Screech"),(31,"Assurance"),
              (36,"Swagger"),(41,"Cross Chop"),(46,"Thrash"),(51,"Close Combat")],
    egg_groups=["Field"]))

_sp(SpeciesData(58, "Growlithe",
    [PokemonType.FIRE],
    55, 70, 45, 70, 50, 60, 190, 65, "slow",
    learnset=[(1,"Bite"),(1,"Roar"),(6,"Ember"),(9,"Leer"),(14,"Odor Sleuth"),(17,"Helping Hand"),
              (22,"Flame Wheel"),(25,"Reversal"),(30,"Fire Fang"),(33,"Flamethrower"),
              (39,"Agility"),(42,"Retaliate"),(47,"Flare Blitz"),(50,"Outrage")],
    evolutions=[EvolutionCondition("Arcanine", item="Fire Stone")],
    egg_groups=["Field"]))

_sp(SpeciesData(59, "Arcanine",
    [PokemonType.FIRE],
    90, 110, 80, 100, 80, 95, 75, 194, "slow",
    learnset=[(1,"Bite"),(1,"Roar"),(1,"Odor Sleuth"),(1,"Helping Hand"),(1,"Extreme Speed"),
              (39,"Agility"),(42,"Retaliate"),(47,"Flare Blitz"),(50,"Outrage")],
    egg_groups=["Field"]))

_sp(SpeciesData(60, "Poliwag",
    [PokemonType.WATER],
    40, 50, 40, 40, 40, 90, 255, 60, "medium_slow",
    learnset=[(1,"Bubble"),(4,"Hypnosis"),(8,"Water Sport"),(11,"Rain Dance"),(15,"Body Slam"),
              (18,"Bubble Beam"),(22,"Mud Shot"),(25,"Belly Drum"),(29,"Wake-Up Slap"),
              (32,"Hydro Pump"),(36,"Mud Bomb")],
    evolutions=[EvolutionCondition("Poliwhirl", min_level=25)],
    egg_groups=["Water 1"]))

_sp(SpeciesData(61, "Poliwhirl",
    [PokemonType.WATER],
    65, 65, 65, 50, 50, 90, 120, 135, "medium_slow",
    learnset=[(1,"Bubble"),(1,"Hypnosis"),(1,"Water Sport"),(1,"Rain Dance"),(15,"Body Slam"),
              (18,"Bubble Beam"),(22,"Mud Shot"),(25,"Belly Drum"),(29,"Wake-Up Slap"),(32,"Hydro Pump")],
    evolutions=[EvolutionCondition("Poliwrath", item="Water Stone"),
                EvolutionCondition("Politoed", trade=True, held_item="King's Rock")],
    egg_groups=["Water 1"]))

_sp(SpeciesData(62, "Poliwrath",
    [PokemonType.WATER, PokemonType.FIGHTING],
    90, 95, 95, 70, 90, 70, 45, 230, "medium_slow",
    learnset=[(1,"Bubble"),(1,"Hypnosis"),(1,"Double Slap"),(1,"Rain Dance"),(1,"Body Slam"),
              (1,"Bubble Beam"),(1,"Mind Reader"),(1,"Dynamic Punch")],
    egg_groups=["Water 1"]))

_sp(SpeciesData(63, "Abra",
    [PokemonType.PSYCHIC],
    25, 20, 15, 105, 55, 90, 200, 62, "medium_slow",
    learnset=[(1,"Teleport")],
    evolutions=[EvolutionCondition("Kadabra", min_level=16)],
    egg_groups=["Human-Like"],
    gender_ratio=0.25))

_sp(SpeciesData(64, "Kadabra",
    [PokemonType.PSYCHIC],
    40, 35, 30, 120, 70, 105, 100, 140, "medium_slow",
    learnset=[(1,"Teleport"),(1,"Kinesis"),(16,"Confusion"),(18,"Disable"),(21,"Psybeam"),
              (23,"Reflect"),(25,"Recover"),(30,"Psych Up"),(33,"Calm Mind"),(38,"Future Sight"),
              (43,"Trick"),(48,"Psychic")],
    evolutions=[EvolutionCondition("Alakazam", trade=True)],
    egg_groups=["Human-Like"],
    gender_ratio=0.25))

_sp(SpeciesData(65, "Alakazam",
    [PokemonType.PSYCHIC],
    55, 50, 45, 135, 95, 120, 50, 225, "medium_slow",
    learnset=[(1,"Teleport"),(1,"Kinesis"),(1,"Confusion"),(1,"Disable"),(1,"Psybeam"),
              (1,"Reflect"),(1,"Recover"),(1,"Psych Up"),(1,"Calm Mind"),(1,"Future Sight"),
              (1,"Trick"),(1,"Psychic")],
    egg_groups=["Human-Like"],
    gender_ratio=0.25))

_sp(SpeciesData(66, "Machop",
    [PokemonType.FIGHTING],
    70, 80, 50, 35, 35, 35, 180, 61, "medium_slow",
    learnset=[(1,"Low Kick"),(1,"Leer"),(4,"Focus Energy"),(8,"Karate Chop"),(12,"Foresight"),
              (15,"Seismic Toss"),(19,"Revenge"),(22,"Vital Throw"),(26,"Submission"),(29,"Wake-Up Slap"),
              (33,"Cross Chop"),(36,"Scary Face"),(40,"Dynamic Punch")],
    evolutions=[EvolutionCondition("Machoke", min_level=28)],
    egg_groups=["Human-Like"]))

_sp(SpeciesData(67, "Machoke",
    [PokemonType.FIGHTING],
    80, 100, 70, 50, 60, 45, 90, 142, "medium_slow",
    learnset=[(1,"Low Kick"),(1,"Leer"),(1,"Focus Energy"),(1,"Karate Chop"),(12,"Foresight"),
              (15,"Seismic Toss"),(19,"Revenge"),(22,"Vital Throw"),(26,"Submission"),
              (29,"Wake-Up Slap"),(33,"Cross Chop"),(36,"Scary Face"),(40,"Dynamic Punch")],
    evolutions=[EvolutionCondition("Machamp", trade=True)],
    egg_groups=["Human-Like"]))

_sp(SpeciesData(68, "Machamp",
    [PokemonType.FIGHTING],
    90, 130, 80, 65, 85, 55, 45, 227, "medium_slow",
    learnset=[(1,"Low Kick"),(1,"Leer"),(1,"Focus Energy"),(1,"Karate Chop"),(1,"Foresight"),
              (15,"Seismic Toss"),(19,"Revenge"),(22,"Vital Throw"),(26,"Submission"),
              (33,"Cross Chop"),(40,"Dynamic Punch")],
    egg_groups=["Human-Like"]))

_sp(SpeciesData(69, "Bellsprout",
    [PokemonType.GRASS, PokemonType.POISON],
    50, 75, 35, 70, 30, 40, 255, 60, "medium_slow",
    learnset=[(1,"Vine Whip"),(1,"Growth"),(7,"Wrap"),(11,"Sleep Powder"),(15,"Poison Powder"),
              (19,"Stun Spore"),(23,"Acid"),(27,"Knock Off"),(33,"Sweet Scent"),(37,"Gastro Acid"),
              (41,"Power Whip"),(45,"Wring Out")],
    evolutions=[EvolutionCondition("Weepinbell", min_level=21)],
    egg_groups=["Grass"]))

_sp(SpeciesData(70, "Weepinbell",
    [PokemonType.GRASS, PokemonType.POISON],
    65, 90, 50, 85, 45, 55, 120, 137, "medium_slow",
    learnset=[(1,"Vine Whip"),(1,"Growth"),(1,"Wrap"),(7,"Wrap"),(11,"Sleep Powder"),
              (15,"Poison Powder"),(19,"Stun Spore"),(23,"Acid"),(27,"Knock Off"),
              (33,"Sweet Scent"),(37,"Gastro Acid"),(41,"Power Whip")],
    evolutions=[EvolutionCondition("Victreebel", item="Leaf Stone")],
    egg_groups=["Grass"]))

_sp(SpeciesData(71, "Victreebel",
    [PokemonType.GRASS, PokemonType.POISON],
    80, 105, 65, 100, 70, 70, 45, 221, "medium_slow",
    learnset=[(1,"Vine Whip"),(1,"Growth"),(1,"Wrap"),(1,"Sleep Powder"),(1,"Poison Powder"),
              (1,"Stun Spore"),(1,"Acid"),(1,"Sweet Scent"),(1,"Power Whip"),(1,"Leaf Storm")],
    egg_groups=["Grass"]))

_sp(SpeciesData(72, "Tentacool",
    [PokemonType.WATER, PokemonType.POISON],
    40, 40, 35, 50, 100, 70, 190, 67, "slow",
    learnset=[(1,"Poison Sting"),(1,"Supersonic"),(4,"Constrict"),(9,"Acid"),(12,"Toxic Spikes"),
              (17,"BubbleBeam"),(20,"Wrap"),(25,"Acid Spray"),(28,"Barrier"),(33,"Water Pulse"),
              (36,"Poison Jab"),(41,"Screech"),(44,"Hydro Pump")],
    evolutions=[EvolutionCondition("Tentacruel", min_level=30)],
    egg_groups=["Water 3"]))

_sp(SpeciesData(73, "Tentacruel",
    [PokemonType.WATER, PokemonType.POISON],
    80, 70, 65, 80, 120, 100, 60, 166, "slow",
    learnset=[(1,"Poison Sting"),(1,"Supersonic"),(1,"Constrict"),(1,"Acid"),(1,"Toxic Spikes"),
              (17,"BubbleBeam"),(20,"Wrap"),(25,"Acid Spray"),(28,"Barrier"),(33,"Water Pulse"),
              (36,"Poison Jab"),(41,"Screech"),(44,"Hydro Pump")],
    egg_groups=["Water 3"]))

_sp(SpeciesData(74, "Geodude",
    [PokemonType.ROCK, PokemonType.GROUND],
    40, 80, 100, 30, 30, 20, 255, 60, "medium_slow",
    learnset=[(1,"Tackle"),(1,"Defense Curl"),(4,"Mud Sport"),(8,"Rock Polish"),(11,"Rock Throw"),
              (15,"Magnitude"),(17,"Steamroller"),(19,"Rock Blast"),(22,"Smack Down"),(25,"Selfdestruct"),
              (29,"Stealth Rock"),(32,"Rock Slide"),(36,"Earthquake"),(42,"Explosion")],
    evolutions=[EvolutionCondition("Graveler", min_level=25)],
    egg_groups=["Mineral"]))

_sp(SpeciesData(75, "Graveler",
    [PokemonType.ROCK, PokemonType.GROUND],
    55, 95, 115, 45, 45, 35, 120, 137, "medium_slow",
    learnset=[(1,"Tackle"),(1,"Defense Curl"),(1,"Mud Sport"),(1,"Rock Polish"),(11,"Rock Throw"),
              (15,"Magnitude"),(17,"Steamroller"),(19,"Rock Blast"),(22,"Smack Down"),(25,"Selfdestruct"),
              (29,"Stealth Rock"),(32,"Rock Slide"),(36,"Earthquake"),(42,"Explosion")],
    evolutions=[EvolutionCondition("Golem", trade=True)],
    egg_groups=["Mineral"]))

_sp(SpeciesData(76, "Golem",
    [PokemonType.ROCK, PokemonType.GROUND],
    80, 120, 130, 55, 65, 45, 45, 223, "medium_slow",
    learnset=[(1,"Tackle"),(1,"Defense Curl"),(1,"Mud Sport"),(1,"Rock Polish"),(1,"Rock Throw"),
              (1,"Magnitude"),(25,"Selfdestruct"),(29,"Stealth Rock"),(32,"Rock Slide"),
              (36,"Earthquake"),(42,"Explosion")],
    egg_groups=["Mineral"]))

_sp(SpeciesData(77, "Ponyta",
    [PokemonType.FIRE],
    50, 85, 55, 65, 65, 90, 190, 60, "medium_fast",
    learnset=[(1,"Tackle"),(1,"Growl"),(4,"Tail Whip"),(9,"Ember"),(14,"Flame Wheel"),
              (19,"Stomp"),(24,"Flame Charge"),(29,"Fire Spin"),(34,"Take Down"),
              (39,"Inferno"),(44,"Agility"),(49,"Bounce"),(54,"Flare Blitz")],
    evolutions=[EvolutionCondition("Rapidash", min_level=40)],
    egg_groups=["Field"]))

_sp(SpeciesData(78, "Rapidash",
    [PokemonType.FIRE],
    65, 100, 70, 80, 80, 105, 60, 175, "medium_fast",
    learnset=[(1,"Tackle"),(1,"Growl"),(1,"Tail Whip"),(1,"Ember"),(1,"Flame Wheel"),
              (1,"Stomp"),(1,"Flame Charge"),(1,"Fire Spin"),(1,"Take Down"),
              (40,"Inferno"),(44,"Agility"),(49,"Bounce"),(54,"Flare Blitz")],
    egg_groups=["Field"]))

_sp(SpeciesData(79, "Slowpoke",
    [PokemonType.WATER, PokemonType.PSYCHIC],
    90, 65, 65, 40, 40, 15, 190, 63, "medium_fast",
    learnset=[(1,"Curse"),(1,"Yawn"),(1,"Tackle"),(5,"Growl"),(9,"Water Gun"),(13,"Confusion"),
              (17,"Disable"),(21,"Headbutt"),(25,"Water Pulse"),(29,"Zen Headbutt"),
              (33,"Slack Off"),(37,"Amnesia"),(41,"Psychic"),(45,"Rain Dance"),(49,"Psych Up")],
    evolutions=[EvolutionCondition("Slowbro", min_level=37),
                EvolutionCondition("Slowking", trade=True, held_item="King's Rock")],
    egg_groups=["Monster","Water 1"]))

_sp(SpeciesData(80, "Slowbro",
    [PokemonType.WATER, PokemonType.PSYCHIC],
    95, 75, 110, 100, 80, 30, 75, 172, "medium_fast",
    learnset=[(1,"Curse"),(1,"Yawn"),(1,"Tackle"),(1,"Growl"),(1,"Water Gun"),(1,"Confusion"),
              (1,"Disable"),(1,"Headbutt"),(1,"Water Pulse"),(1,"Zen Headbutt"),
              (33,"Slack Off"),(37,"Amnesia"),(41,"Psychic"),(45,"Rain Dance")],
    egg_groups=["Monster","Water 1"]))

_sp(SpeciesData(81, "Magnemite",
    [PokemonType.ELECTRIC],
    25, 35, 70, 95, 55, 45, 190, 65, "medium_fast",
    learnset=[(1,"Metal Sound"),(1,"Tackle"),(6,"Thundershock"),(9,"Supersonic"),(12,"Sonicboom"),
              (15,"Thunder Wave"),(20,"Magnet Bomb"),(23,"Spark"),(26,"Mirror Shot"),
              (29,"Metal Sound"),(33,"Electro Ball"),(36,"Flash Cannon"),(40,"Screech"),
              (43,"Discharge"),(46,"Lock-On"),(50,"Zap Cannon")],
    evolutions=[EvolutionCondition("Magneton", min_level=30)],
    egg_groups=["Mineral"],
    gender_ratio=-1.0))

_sp(SpeciesData(82, "Magneton",
    [PokemonType.ELECTRIC],
    50, 60, 95, 120, 70, 70, 60, 163, "medium_fast",
    learnset=[(1,"Metal Sound"),(1,"Tackle"),(1,"Thundershock"),(1,"Supersonic"),(1,"Sonicboom"),
              (1,"Thunder Wave"),(20,"Magnet Bomb"),(23,"Spark"),(26,"Mirror Shot"),
              (29,"Metal Sound"),(33,"Electro Ball"),(36,"Flash Cannon"),(40,"Screech"),(43,"Discharge")],
    egg_groups=["Mineral"],
    gender_ratio=-1.0))

_sp(SpeciesData(83, "Farfetch'd",
    [PokemonType.NORMAL, PokemonType.FLYING],
    52, 90, 55, 58, 62, 60, 45, 94, "medium_fast",
    learnset=[(1,"Peck"),(1,"Sand Attack"),(5,"Leer"),(9,"Fury Cutter"),(13,"Cut"),(17,"Aerial Ace"),
              (21,"Knock Off"),(25,"Slash"),(29,"Air Cutter"),(33,"Swords Dance"),
              (37,"Agility"),(41,"Night Slash"),(45,"Brave Bird")],
    egg_groups=["Flying","Field"]))

_sp(SpeciesData(84, "Doduo",
    [PokemonType.NORMAL, PokemonType.FLYING],
    35, 85, 45, 35, 35, 75, 190, 62, "medium_fast",
    learnset=[(1,"Peck"),(1,"Growl"),(7,"Quick Attack"),(13,"Rage"),(19,"Fury Attack"),
              (25,"Pursuit"),(31,"Uproar"),(37,"Acupressure"),(43,"Swords Dance"),(49,"Thrash")],
    evolutions=[EvolutionCondition("Dodrio", min_level=31)],
    egg_groups=["Flying","Field"]))

_sp(SpeciesData(85, "Dodrio",
    [PokemonType.NORMAL, PokemonType.FLYING],
    60, 110, 70, 60, 60, 100, 45, 161, "medium_fast",
    learnset=[(1,"Peck"),(1,"Growl"),(1,"Quick Attack"),(1,"Rage"),(19,"Fury Attack"),
              (25,"Pursuit"),(31,"Uproar"),(37,"Acupressure"),(43,"Swords Dance"),(49,"Thrash")],
    egg_groups=["Flying","Field"]))

_sp(SpeciesData(86, "Seel",
    [PokemonType.WATER],
    65, 45, 55, 45, 70, 45, 190, 65, "medium_fast",
    learnset=[(1,"Headbutt"),(1,"Growl"),(3,"Water Sport"),(7,"Icy Wind"),(13,"Encore"),
              (19,"Ice Shard"),(25,"Rest"),(31,"Aqua Ring"),(37,"Aurora Beam"),(43,"Aqua Tail"),
              (49,"Ice Beam"),(55,"Safeguard"),(61,"Hail")],
    evolutions=[EvolutionCondition("Dewgong", min_level=34)],
    egg_groups=["Water 1","Field"]))

_sp(SpeciesData(87, "Dewgong",
    [PokemonType.WATER, PokemonType.ICE],
    90, 70, 80, 70, 95, 70, 75, 166, "medium_fast",
    learnset=[(1,"Headbutt"),(1,"Growl"),(1,"Water Sport"),(1,"Icy Wind"),(1,"Encore"),
              (19,"Ice Shard"),(25,"Rest"),(31,"Aqua Ring"),(37,"Aurora Beam"),(43,"Aqua Tail"),
              (49,"Ice Beam"),(55,"Safeguard"),(61,"Hail")],
    egg_groups=["Water 1","Field"]))

_sp(SpeciesData(88, "Grimer",
    [PokemonType.POISON],
    80, 80, 50, 40, 50, 25, 190, 65, "medium_fast",
    learnset=[(1,"Poison Gas"),(1,"Pound"),(4,"Harden"),(7,"Disable"),(14,"Sludge"),
              (17,"Mud Bomb"),(20,"Minimize"),(25,"Faint Attack"),(28,"Screech"),
              (31,"Sludge Bomb"),(38,"Acid Armor"),(41,"Sludge Wave"),(44,"Gunk Shot")],
    evolutions=[EvolutionCondition("Muk", min_level=38)],
    egg_groups=["Amorphous"],
    gender_ratio=0.5))

_sp(SpeciesData(89, "Muk",
    [PokemonType.POISON],
    105, 105, 75, 65, 100, 50, 75, 157, "medium_fast",
    learnset=[(1,"Poison Gas"),(1,"Pound"),(1,"Harden"),(1,"Disable"),(1,"Sludge"),
              (17,"Mud Bomb"),(20,"Minimize"),(25,"Faint Attack"),(28,"Screech"),
              (31,"Sludge Bomb"),(38,"Acid Armor"),(41,"Sludge Wave"),(44,"Gunk Shot")],
    egg_groups=["Amorphous"],
    gender_ratio=0.5))

_sp(SpeciesData(90, "Shellder",
    [PokemonType.WATER],
    30, 65, 100, 45, 25, 40, 190, 61, "slow",
    learnset=[(1,"Tackle"),(1,"Withdraw"),(6,"Supersonic"),(11,"Icicle Spear"),(16,"Protect"),
              (21,"Leer"),(26,"Clamp"),(31,"Ice Shard"),(36,"Razor Shell"),(41,"Aurora Beam"),
              (46,"Whirlpool"),(51,"Iron Defense"),(56,"Ice Beam"),(61,"Shell Smash")],
    evolutions=[EvolutionCondition("Cloyster", item="Water Stone")],
    egg_groups=["Water 3"]))

_sp(SpeciesData(91, "Cloyster",
    [PokemonType.WATER, PokemonType.ICE],
    50, 95, 180, 85, 45, 70, 60, 184, "slow",
    learnset=[(1,"Tackle"),(1,"Withdraw"),(1,"Supersonic"),(1,"Icicle Spear"),(1,"Protect"),
              (1,"Leer"),(26,"Clamp"),(31,"Ice Shard"),(36,"Razor Shell"),(41,"Aurora Beam"),
              (51,"Iron Defense"),(56,"Ice Beam"),(61,"Shell Smash")],
    egg_groups=["Water 3"]))

_sp(SpeciesData(92, "Gastly",
    [PokemonType.GHOST, PokemonType.POISON],
    30, 35, 30, 100, 35, 80, 190, 62, "medium_slow",
    learnset=[(1,"Hypnosis"),(1,"Lick"),(4,"Spite"),(8,"Mean Look"),(11,"Curse"),
              (15,"Night Shade"),(20,"Confuse Ray"),(23,"Sucker Punch"),(27,"Payback"),
              (31,"Shadow Ball"),(35,"Dream Eater"),(39,"Dark Pulse"),(43,"Destiny Bond"),
              (47,"Hex")],
    evolutions=[EvolutionCondition("Haunter", min_level=25)],
    egg_groups=["Amorphous"],
    gender_ratio=0.5))

_sp(SpeciesData(93, "Haunter",
    [PokemonType.GHOST, PokemonType.POISON],
    45, 50, 45, 115, 55, 95, 90, 142, "medium_slow",
    learnset=[(1,"Hypnosis"),(1,"Lick"),(1,"Spite"),(1,"Mean Look"),(11,"Curse"),
              (15,"Night Shade"),(20,"Confuse Ray"),(23,"Sucker Punch"),(27,"Payback"),
              (31,"Shadow Ball"),(35,"Dream Eater"),(39,"Dark Pulse"),(43,"Destiny Bond"),(47,"Hex")],
    evolutions=[EvolutionCondition("Gengar", trade=True)],
    egg_groups=["Amorphous"],
    gender_ratio=0.5))

_sp(SpeciesData(94, "Gengar",
    [PokemonType.GHOST, PokemonType.POISON],
    60, 65, 60, 130, 75, 110, 45, 225, "medium_slow",
    learnset=[(1,"Hypnosis"),(1,"Lick"),(1,"Spite"),(1,"Mean Look"),(1,"Curse"),
              (15,"Night Shade"),(20,"Confuse Ray"),(23,"Sucker Punch"),(27,"Payback"),
              (31,"Shadow Ball"),(35,"Dream Eater"),(39,"Dark Pulse"),(43,"Destiny Bond"),(47,"Hex")],
    egg_groups=["Amorphous"],
    gender_ratio=0.5))

_sp(SpeciesData(95, "Onix",
    [PokemonType.ROCK, PokemonType.GROUND],
    35, 45, 160, 30, 45, 70, 45, 77, "medium_fast",
    learnset=[(1,"Mud Sport"),(1,"Tackle"),(1,"Harden"),(6,"Bind"),(11,"Screech"),
              (14,"Rock Throw"),(18,"Rock Tomb"),(21,"Rage"),(25,"Stealth Rock"),(28,"Slam"),
              (32,"Dragon Breath"),(35,"Sandstorm"),(39,"Iron Tail"),(42,"Sand Tomb"),
              (46,"Stone Edge"),(49,"Double-Edge")],
    evolutions=[EvolutionCondition("Steelix", trade=True, held_item="Metal Coat")],
    egg_groups=["Mineral"]))

_sp(SpeciesData(96, "Drowzee",
    [PokemonType.PSYCHIC],
    60, 48, 45, 43, 90, 42, 190, 66, "medium_fast",
    learnset=[(1,"Pound"),(1,"Hypnosis"),(5,"Disable"),(9,"Confusion"),(13,"Headbutt"),
              (17,"Poison Gas"),(21,"Meditate"),(25,"Psybeam"),(29,"Psych Up"),(33,"Psychic"),
              (37,"Swagger"),(41,"Future Sight"),(45,"Wake-Up Slap"),(49,"Nasty Plot"),(53,"Zen Headbutt")],
    evolutions=[EvolutionCondition("Hypno", min_level=26)],
    egg_groups=["Human-Like"]))

_sp(SpeciesData(97, "Hypno",
    [PokemonType.PSYCHIC],
    85, 73, 70, 73, 115, 67, 75, 169, "medium_fast",
    learnset=[(1,"Pound"),(1,"Hypnosis"),(1,"Disable"),(1,"Confusion"),(1,"Headbutt"),
              (1,"Poison Gas"),(21,"Meditate"),(25,"Psybeam"),(29,"Psych Up"),(33,"Psychic"),
              (37,"Swagger"),(41,"Future Sight"),(45,"Wake-Up Slap"),(49,"Nasty Plot"),(53,"Zen Headbutt")],
    egg_groups=["Human-Like"]))

_sp(SpeciesData(98, "Krabby",
    [PokemonType.WATER],
    30, 105, 90, 25, 25, 50, 225, 65, "medium_fast",
    learnset=[(1,"Mud Sport"),(1,"Bubble"),(1,"Vice Grip"),(5,"Leer"),(9,"Harden"),(13,"BubbleBeam"),
              (17,"Mud Shot"),(21,"Metal Claw"),(25,"Stomp"),(29,"Protect"),(33,"Guillotine"),
              (37,"Slam"),(41,"Brine"),(45,"Crabhammer")],
    evolutions=[EvolutionCondition("Kingler", min_level=28)],
    egg_groups=["Water 3"]))

_sp(SpeciesData(99, "Kingler",
    [PokemonType.WATER],
    55, 130, 115, 50, 50, 75, 60, 166, "medium_fast",
    learnset=[(1,"Mud Sport"),(1,"Bubble"),(1,"Vice Grip"),(1,"Leer"),(1,"Harden"),(1,"BubbleBeam"),
              (17,"Mud Shot"),(21,"Metal Claw"),(25,"Stomp"),(29,"Protect"),(33,"Guillotine"),
              (37,"Slam"),(41,"Brine"),(45,"Crabhammer")],
    egg_groups=["Water 3"]))

_sp(SpeciesData(100, "Voltorb",
    [PokemonType.ELECTRIC],
    40, 30, 50, 55, 55, 100, 190, 66, "medium_fast",
    learnset=[(1,"Charge"),(1,"Tackle"),(5,"Sonic Boom"),(9,"Spark"),(13,"Eerie Impulse"),
              (17,"Rollout"),(21,"Screech"),(25,"Charge Beam"),(29,"Light Screen"),
              (33,"Electro Ball"),(37,"Self-Destruct"),(41,"Swift"),(45,"Discharge"),
              (49,"Mirror Coat"),(53,"Explosion")],
    evolutions=[EvolutionCondition("Electrode", min_level=30)],
    egg_groups=["Mineral"],
    gender_ratio=-1.0))

_sp(SpeciesData(101, "Electrode",
    [PokemonType.ELECTRIC],
    60, 50, 70, 80, 80, 150, 60, 168, "medium_fast",
    learnset=[(1,"Charge"),(1,"Tackle"),(1,"Sonic Boom"),(1,"Spark"),(1,"Eerie Impulse"),
              (1,"Rollout"),(21,"Screech"),(25,"Charge Beam"),(29,"Light Screen"),
              (33,"Electro Ball"),(37,"Explosion"),(41,"Swift"),(45,"Discharge"),(53,"Mirror Coat")],
    egg_groups=["Mineral"],
    gender_ratio=-1.0))

_sp(SpeciesData(102, "Exeggcute",
    [PokemonType.GRASS, PokemonType.PSYCHIC],
    60, 40, 80, 60, 45, 40, 90, 65, "slow",
    learnset=[(1,"Barrage"),(1,"Uproar"),(1,"Hypnosis"),(7,"Reflect"),(11,"Leech Seed"),
              (15,"Bullet Seed"),(19,"Stun Spore"),(23,"Poison Powder"),(27,"Sleep Powder"),
              (31,"Confusion"),(35,"Worry Seed"),(39,"Natural Gift"),(43,"Solar Beam"),
              (47,"Egg Bomb")],
    evolutions=[EvolutionCondition("Exeggutor", item="Leaf Stone")],
    egg_groups=["Grass"]))

_sp(SpeciesData(103, "Exeggutor",
    [PokemonType.GRASS, PokemonType.PSYCHIC],
    95, 95, 85, 125, 75, 55, 45, 212, "slow",
    learnset=[(1,"Barrage"),(1,"Hypnosis"),(1,"Confusion"),(1,"Egg Bomb"),
              (1,"Stomp"),(1,"Psychic"),(1,"Solar Beam")],
    egg_groups=["Grass"]))

_sp(SpeciesData(104, "Cubone",
    [PokemonType.GROUND],
    50, 50, 95, 40, 50, 35, 190, 64, "medium_fast",
    learnset=[(1,"Growl"),(1,"Tackle"),(5,"Bone Club"),(9,"Headbutt"),(13,"Leer"),
              (17,"Focus Energy"),(21,"Bonemerang"),(25,"Rage"),(29,"False Swipe"),
              (33,"Thrash"),(37,"Fling"),(41,"Bone Rush"),(45,"Endeavor"),(49,"Double-Edge")],
    evolutions=[EvolutionCondition("Marowak", min_level=28)],
    egg_groups=["Monster","Field"]))

_sp(SpeciesData(105, "Marowak",
    [PokemonType.GROUND],
    60, 80, 110, 50, 80, 45, 75, 149, "medium_fast",
    learnset=[(1,"Growl"),(1,"Tackle"),(1,"Bone Club"),(1,"Headbutt"),(1,"Leer"),
              (1,"Focus Energy"),(1,"Bonemerang"),(1,"Rage"),(1,"False Swipe"),
              (1,"Thrash"),(37,"Fling"),(41,"Bone Rush"),(45,"Endeavor"),(49,"Double-Edge")],
    egg_groups=["Monster","Field"]))

_sp(SpeciesData(106, "Hitmonlee",
    [PokemonType.FIGHTING],
    50, 120, 53, 35, 110, 87, 45, 159, "medium_fast",
    learnset=[(1,"Tackle"),(1,"Double Kick"),(5,"Meditate"),(9,"Rolling Kick"),(13,"Jump Kick"),
              (17,"Brick Break"),(21,"Focus Energy"),(25,"Hi Jump Kick"),(29,"Mind Reader"),
              (33,"Foresight"),(37,"Wide Guard"),(41,"Blaze Kick"),(45,"Endure"),(49,"Mega Kick")],
    egg_groups=["Human-Like"],
    gender_ratio=0.0))

_sp(SpeciesData(107, "Hitmonchan",
    [PokemonType.FIGHTING],
    50, 105, 79, 35, 110, 76, 45, 159, "medium_fast",
    learnset=[(1,"Tackle"),(1,"Comet Punch"),(5,"Agility"),(9,"Pursuit"),(13,"Mach Punch"),
              (17,"Bullet Punch"),(21,"Thunderpunch"),(21,"Ice Punch"),(21,"Fire Punch"),
              (25,"Vacuum Wave"),(29,"Quick Guard"),(33,"Thunder Punch"),(37,"Sky Uppercut"),
              (41,"Mega Punch"),(45,"Detect"),(49,"Counter")],
    egg_groups=["Human-Like"],
    gender_ratio=0.0))

_sp(SpeciesData(108, "Lickitung",
    [PokemonType.NORMAL],
    90, 55, 75, 60, 75, 30, 45, 77, "medium_fast",
    learnset=[(1,"Lick"),(1,"Supersonic"),(7,"Defense Curl"),(13,"Knock Off"),(19,"Wrap"),
              (25,"Stomp"),(31,"Disable"),(37,"Slam"),(43,"Rollout"),(49,"Body Slam"),
              (55,"Screech"),(61,"Power Whip")],
    egg_groups=["Monster"]))

_sp(SpeciesData(109, "Koffing",
    [PokemonType.POISON],
    40, 65, 95, 60, 45, 35, 190, 68, "medium_fast",
    learnset=[(1,"Poison Gas"),(1,"Tackle"),(4,"Smog"),(7,"Smokescreen"),(12,"Assurance"),
              (15,"Sludge"),(20,"Selfdestruct"),(25,"Haze"),(30,"Gyro Ball"),(35,"Sludge Bomb"),
              (40,"Explosion"),(45,"Destiny Bond"),(50,"Memento")],
    evolutions=[EvolutionCondition("Weezing", min_level=35)],
    egg_groups=["Amorphous"],
    gender_ratio=0.5))

_sp(SpeciesData(110, "Weezing",
    [PokemonType.POISON],
    65, 90, 120, 85, 70, 60, 60, 172, "medium_fast",
    learnset=[(1,"Poison Gas"),(1,"Tackle"),(1,"Smog"),(1,"Smokescreen"),(1,"Assurance"),
              (1,"Sludge"),(20,"Selfdestruct"),(25,"Haze"),(30,"Gyro Ball"),(35,"Sludge Bomb"),
              (40,"Explosion"),(45,"Destiny Bond"),(50,"Memento")],
    egg_groups=["Amorphous"],
    gender_ratio=0.5))

_sp(SpeciesData(111, "Rhyhorn",
    [PokemonType.GROUND, PokemonType.ROCK],
    80, 85, 95, 30, 30, 25, 120, 69, "slow",
    learnset=[(1,"Horn Attack"),(1,"Tail Whip"),(5,"Fury Attack"),(10,"Scary Face"),
              (14,"Smack Down"),(18,"Stomp"),(23,"Rock Blast"),(27,"Bulldoze"),(32,"Chip Away"),
              (36,"Take Down"),(40,"Drill Run"),(45,"Stone Edge"),(49,"Earthquake"),
              (54,"Horn Drill"),(58,"Megahorn")],
    evolutions=[EvolutionCondition("Rhydon", min_level=42)],
    egg_groups=["Monster","Field"]))

_sp(SpeciesData(112, "Rhydon",
    [PokemonType.GROUND, PokemonType.ROCK],
    105, 130, 120, 45, 45, 40, 60, 170, "slow",
    learnset=[(1,"Horn Attack"),(1,"Tail Whip"),(1,"Fury Attack"),(1,"Scary Face"),
              (1,"Smack Down"),(1,"Stomp"),(1,"Rock Blast"),(1,"Bulldoze"),
              (36,"Take Down"),(40,"Drill Run"),(45,"Stone Edge"),(49,"Earthquake"),
              (54,"Horn Drill"),(58,"Megahorn")],
    evolutions=[EvolutionCondition("Rhyperior", trade=True, held_item="Protector")],
    egg_groups=["Monster","Field"]))

_sp(SpeciesData(113, "Chansey",
    [PokemonType.NORMAL],
    250, 5, 5, 35, 105, 50, 30, 395, "fast",
    learnset=[(1,"Pound"),(1,"Growl"),(5,"Tail Whip"),(9,"Refresh"),(13,"Softboiled"),
              (17,"DoubleSlap"),(23,"Minimize"),(27,"Sing"),(33,"Egg Bomb"),(39,"Defense Curl"),
              (45,"Light Screen"),(51,"Double-Edge")],
    evolutions=[EvolutionCondition("Blissey", friendship=220)],
    egg_groups=["Fairy"],
    gender_ratio=1.0,
    base_friendship=140))

_sp(SpeciesData(114, "Tangela",
    [PokemonType.GRASS],
    65, 55, 115, 100, 40, 60, 45, 87, "medium_fast",
    learnset=[(1,"Ingrain"),(1,"Constrict"),(4,"Sleep Powder"),(7,"Absorb"),(10,"Vine Whip"),
              (15,"Bind"),(20,"Mega Drain"),(25,"Stun Spore"),(28,"Ancient Power"),(31,"Knock Off"),
              (36,"Natural Gift"),(39,"Slam"),(44,"Tickle"),(47,"Wring Out"),(52,"Power Whip")],
    egg_groups=["Grass"]))

_sp(SpeciesData(115, "Kangaskhan",
    [PokemonType.NORMAL],
    105, 95, 80, 40, 80, 90, 45, 172, "medium_fast",
    learnset=[(1,"Comet Punch"),(1,"Leer"),(1,"Fake Out"),(9,"Bite"),(13,"Double Hit"),
              (17,"Tail Whip"),(21,"Mega Punch"),(25,"Chip Away"),(29,"Dizzy Punch"),(33,"Crunch"),
              (37,"Endure"),(41,"Outrage"),(45,"Sucker Punch"),(49,"Reversal")],
    egg_groups=["Monster"],
    gender_ratio=1.0))

_sp(SpeciesData(116, "Horsea",
    [PokemonType.WATER],
    30, 40, 70, 70, 25, 60, 225, 59, "medium_fast",
    learnset=[(1,"Water Gun"),(1,"Smokescreen"),(4,"Leer"),(8,"BubbleBeam"),(13,"Focus Energy"),
              (19,"BubbleBeam"),(24,"Agility"),(30,"Twister"),(35,"Brine"),(41,"Hydro Pump"),
              (46,"Dragon Dance"),(52,"Dragon Pulse")],
    evolutions=[EvolutionCondition("Seadra", min_level=32)],
    egg_groups=["Water 1","Dragon"]))

_sp(SpeciesData(117, "Seadra",
    [PokemonType.WATER],
    55, 65, 95, 95, 45, 85, 75, 154, "medium_fast",
    learnset=[(1,"Water Gun"),(1,"Smokescreen"),(1,"Leer"),(1,"BubbleBeam"),(1,"Focus Energy"),
              (24,"Agility"),(30,"Twister"),(35,"Brine"),(41,"Hydro Pump"),
              (46,"Dragon Dance"),(52,"Dragon Pulse")],
    evolutions=[EvolutionCondition("Kingdra", trade=True, held_item="Dragon Scale")],
    egg_groups=["Water 1","Dragon"]))

_sp(SpeciesData(118, "Goldeen",
    [PokemonType.WATER],
    45, 67, 60, 35, 50, 63, 225, 64, "medium_fast",
    learnset=[(1,"Peck"),(1,"Tail Whip"),(9,"Water Sport"),(17,"Supersonic"),(21,"Horn Attack"),
              (25,"Flail"),(29,"Water Pulse"),(33,"Aqua Ring"),(37,"Fury Attack"),(41,"Waterfall"),
              (45,"Horn Drill"),(49,"Agility"),(53,"Soak")],
    evolutions=[EvolutionCondition("Seaking", min_level=33)],
    egg_groups=["Water 2"]))

_sp(SpeciesData(119, "Seaking",
    [PokemonType.WATER],
    80, 92, 65, 65, 80, 68, 60, 158, "medium_fast",
    learnset=[(1,"Peck"),(1,"Tail Whip"),(1,"Water Sport"),(1,"Supersonic"),(1,"Horn Attack"),
              (25,"Flail"),(29,"Water Pulse"),(33,"Aqua Ring"),(37,"Fury Attack"),(41,"Waterfall"),
              (45,"Horn Drill"),(49,"Agility"),(53,"Soak")],
    egg_groups=["Water 2"]))

_sp(SpeciesData(120, "Staryu",
    [PokemonType.WATER],
    30, 45, 55, 70, 55, 85, 225, 68, "slow",
    learnset=[(1,"Tackle"),(1,"Harden"),(6,"Water Gun"),(11,"Rapid Spin"),(16,"Recover"),
              (21,"Camouflage"),(26,"Swift"),(31,"BubbleBeam"),(36,"Minimize"),(41,"Gyro Ball"),
              (46,"Light Screen"),(51,"Cosmic Power"),(56,"Hydro Pump")],
    evolutions=[EvolutionCondition("Starmie", item="Water Stone")],
    egg_groups=["Water 3"],
    gender_ratio=-1.0))

_sp(SpeciesData(121, "Starmie",
    [PokemonType.WATER, PokemonType.PSYCHIC],
    60, 75, 85, 100, 85, 115, 60, 182, "slow",
    learnset=[(1,"Tackle"),(1,"Harden"),(1,"Water Gun"),(1,"Rapid Spin"),(1,"Recover"),
              (1,"Swift"),(1,"BubbleBeam"),(1,"Minimize"),(1,"Psychic"),(1,"Hydro Pump")],
    egg_groups=["Water 3"],
    gender_ratio=-1.0))

_sp(SpeciesData(122, "Mr. Mime",
    [PokemonType.PSYCHIC],
    40, 45, 65, 100, 120, 90, 45, 136, "medium_fast",
    learnset=[(1,"Pound"),(1,"Confusion"),(1,"Tickle"),(4,"Barrier"),(8,"Encore"),(11,"Doubleslap"),
              (15,"Meditate"),(18,"Magic Coat"),(22,"Light Screen"),(25,"Psybeam"),(29,"Substitute"),
              (32,"Reflect"),(36,"Psych Up"),(39,"Recycle"),(43,"Trick"),(46,"Psychic"),
              (50,"Role Play"),(53,"Baton Pass"),(57,"Safeguard")],
    egg_groups=["Human-Like"]))

_sp(SpeciesData(123, "Scyther",
    [PokemonType.BUG, PokemonType.FLYING],
    70, 110, 80, 55, 80, 105, 45, 187, "medium_fast",
    learnset=[(1,"Vacuum Wave"),(1,"Quick Attack"),(1,"Leer"),(5,"Focus Energy"),(9,"Pursuit"),
              (13,"False Swipe"),(17,"Agility"),(21,"Wing Attack"),(25,"Fury Cutter"),
              (29,"Slash"),(33,"Razor Wind"),(37,"Double Team"),(41,"X-Scissor"),(45,"Night Slash"),
              (49,"Double Hit"),(53,"Air Slash"),(57,"Swords Dance")],
    evolutions=[EvolutionCondition("Scizor", trade=True, held_item="Metal Coat")],
    egg_groups=["Bug"]))

_sp(SpeciesData(124, "Jynx",
    [PokemonType.ICE, PokemonType.PSYCHIC],
    65, 50, 35, 115, 95, 95, 45, 137, "medium_fast",
    learnset=[(1,"Pound"),(1,"Lick"),(4,"Lovely Kiss"),(8,"Powder Snow"),(11,"DoubleSlap"),
              (15,"Ice Punch"),(18,"Mean Look"),(22,"Fake Tears"),(25,"Blizzard"),
              (29,"Nasty Plot"),(32,"Perish Song"),(36,"Psychic"),(39,"Blizzard")],
    egg_groups=["Human-Like"],
    gender_ratio=1.0))

_sp(SpeciesData(125, "Electabuzz",
    [PokemonType.ELECTRIC],
    65, 83, 57, 95, 85, 105, 45, 156, "medium_fast",
    learnset=[(1,"Quick Attack"),(1,"Leer"),(4,"Thunderpunch"),(8,"Low Kick"),(11,"Swift"),
              (15,"Shock Wave"),(18,"Light Screen"),(22,"Thunder Wave"),(25,"Electro Ball"),
              (29,"Thunder"),(32,"Discharge"),(36,"Screech"),(39,"Thunderbolt"),(43,"Flamethrower")],
    evolutions=[EvolutionCondition("Electivire", trade=True, held_item="Electirizer")],
    egg_groups=["Human-Like"]))

_sp(SpeciesData(126, "Magmar",
    [PokemonType.FIRE],
    65, 95, 57, 100, 85, 93, 45, 156, "medium_fast",
    learnset=[(1,"Smog"),(1,"Leer"),(4,"Ember"),(8,"Smokescreen"),(11,"Faint Attack"),
              (15,"Fire Spin"),(18,"Clear Smog"),(22,"Flame Burst"),(25,"Fire Punch"),
              (29,"Lava Plume"),(32,"Sunny Day"),(36,"Flamethrower"),(39,"Fire Blast"),
              (43,"Flare Blitz")],
    evolutions=[EvolutionCondition("Magmortar", trade=True, held_item="Magmarizer")],
    egg_groups=["Human-Like"]))

_sp(SpeciesData(127, "Pinsir",
    [PokemonType.BUG],
    65, 125, 100, 55, 70, 85, 45, 175, "slow",
    learnset=[(1,"Vice Grip"),(1,"Focus Energy"),(7,"Bind"),(11,"Seismic Toss"),(17,"Harden"),
              (21,"Revenge"),(27,"Brick Break"),(31,"Vital Throw"),(37,"Slash"),(41,"Swords Dance"),
              (47,"X-Scissor"),(51,"Submission"),(57,"Storm Throw"),(61,"Superpower")],
    egg_groups=["Bug"]))

_sp(SpeciesData(128, "Tauros",
    [PokemonType.NORMAL],
    75, 100, 95, 40, 70, 110, 45, 172, "slow",
    learnset=[(1,"Tackle"),(1,"Tail Whip"),(4,"Rage"),(10,"Horn Attack"),(14,"Scary Face"),
              (19,"Pursuit"),(25,"Rest"),(31,"Payback"),(36,"Work Up"),(42,"Zen Headbutt"),
              (47,"Take Down"),(53,"Double-Edge"),(58,"Giga Impact")],
    egg_groups=["Field"],
    gender_ratio=0.0))

_sp(SpeciesData(129, "Magikarp",
    [PokemonType.WATER],
    20, 10, 55, 15, 20, 80, 255, 40, "slow",
    learnset=[(1,"Splash"),(15,"Tackle"),(30,"Flail")],
    evolutions=[EvolutionCondition("Gyarados", min_level=20)],
    egg_groups=["Water 2","Dragon"],
    pokedex_entry="In the distant past, it was somewhat stronger than the horribly weak Pokémon it is today.",
    base_friendship=70))

_sp(SpeciesData(130, "Gyarados",
    [PokemonType.WATER, PokemonType.FLYING],
    95, 125, 79, 60, 100, 81, 45, 189, "slow",
    learnset=[(1,"Thrash"),(1,"Bite"),(20,"Dragon Rage"),(25,"Leer"),(30,"Twister"),
              (35,"Ice Fang"),(40,"Aqua Tail"),(45,"Rain Dance"),(50,"Hyper Beam"),(55,"Dragon Dance")],
    egg_groups=["Water 2","Dragon"]))

_sp(SpeciesData(131, "Lapras",
    [PokemonType.WATER, PokemonType.ICE],
    130, 85, 80, 85, 95, 60, 45, 187, "slow",
    learnset=[(1,"Water Gun"),(1,"Growl"),(5,"Sing"),(9,"Mist"),(13,"Confuse Ray"),
              (17,"Ice Shard"),(21,"Body Slam"),(25,"Rain Dance"),(29,"Perish Song"),
              (33,"Ice Beam"),(37,"Blizzard"),(41,"Sheer Cold"),(45,"Safeguard"),(49,"Hydro Pump")],
    egg_groups=["Monster","Water 1"],
    base_friendship=70))

_sp(SpeciesData(132, "Ditto",
    [PokemonType.NORMAL],
    48, 48, 48, 48, 48, 48, 35, 101, "medium_fast",
    learnset=[(1,"Transform")],
    egg_groups=["Ditto"],
    gender_ratio=-1.0,
    pokedex_entry="Capable of copying an enemy's genetic code to instantly transform itself into a duplicate of the enemy."))

_sp(SpeciesData(133, "Eevee",
    [PokemonType.NORMAL],
    55, 55, 50, 45, 65, 55, 45, 65, "medium_fast",
    learnset=[(1,"Tackle"),(1,"Tail Whip"),(4,"Sand Attack"),(8,"Growl"),(11,"Quick Attack"),
              (15,"Bite"),(19,"Refresh"),(23,"Covet"),(27,"Take Down"),(31,"Charm"),
              (35,"Baton Pass"),(39,"Double-Edge"),(43,"Last Resort")],
    evolutions=[
        EvolutionCondition("Vaporeon", item="Water Stone"),
        EvolutionCondition("Jolteon", item="Thunder Stone"),
        EvolutionCondition("Flareon", item="Fire Stone"),
        EvolutionCondition("Espeon", friendship=220, time_of_day="day"),
        EvolutionCondition("Umbreon", friendship=220, time_of_day="night"),
        EvolutionCondition("Leafeon", item="Leaf Stone"),
        EvolutionCondition("Glaceon", item="Ice Stone"),
    ],
    egg_groups=["Field"],
    base_friendship=70))

_sp(SpeciesData(134, "Vaporeon",
    [PokemonType.WATER],
    130, 65, 60, 110, 95, 65, 45, 184, "medium_fast",
    learnset=[(1,"Water Gun"),(1,"Tackle"),(1,"Tail Whip"),(1,"Sand Attack"),
              (1,"Quick Attack"),(1,"Water Pulse"),(1,"Aurora Beam"),(1,"Aqua Ring"),
              (1,"Last Resort"),(1,"Hydro Pump")],
    egg_groups=["Field"]))

_sp(SpeciesData(135, "Jolteon",
    [PokemonType.ELECTRIC],
    65, 65, 60, 110, 95, 130, 45, 184, "medium_fast",
    learnset=[(1,"Thundershock"),(1,"Tackle"),(1,"Tail Whip"),(1,"Sand Attack"),
              (1,"Quick Attack"),(1,"Thunder Wave"),(1,"Thunder Fang"),(1,"Double Kick"),
              (1,"Pin Missile"),(1,"Last Resort"),(1,"Thunder")],
    egg_groups=["Field"]))

_sp(SpeciesData(136, "Flareon",
    [PokemonType.FIRE],
    65, 130, 60, 95, 110, 65, 45, 184, "medium_fast",
    learnset=[(1,"Ember"),(1,"Tackle"),(1,"Tail Whip"),(1,"Sand Attack"),
              (1,"Quick Attack"),(1,"Bite"),(1,"Fire Fang"),(1,"Smog"),
              (1,"Lava Plume"),(1,"Last Resort"),(1,"Flare Blitz")],
    egg_groups=["Field"]))

_sp(SpeciesData(137, "Porygon",
    [PokemonType.NORMAL],
    65, 60, 70, 85, 75, 40, 45, 130, "medium_fast",
    learnset=[(1,"Tackle"),(1,"Conversion"),(1,"Sharpen"),(4,"Psybeam"),(12,"Agility"),
              (19,"Recover"),(26,"Discharge"),(33,"Lock-On"),(40,"Tri Attack"),(47,"Magic Coat"),
              (54,"Zap Cannon"),(61,"Hyper Beam")],
    evolutions=[EvolutionCondition("Porygon2", trade=True, held_item="Upgrade")],
    egg_groups=["Mineral"],
    gender_ratio=-1.0))

_sp(SpeciesData(138, "Omanyte",
    [PokemonType.ROCK, PokemonType.WATER],
    35, 40, 100, 90, 55, 35, 45, 71, "medium_fast",
    learnset=[(1,"Constrict"),(1,"Withdraw"),(7,"Bite"),(13,"Water Gun"),(19,"Rollout"),
              (25,"Leer"),(31,"Ancient Power"),(37,"BubbleBeam"),(43,"Protect"),(49,"Brine"),
              (55,"Hydro Pump"),(61,"Shell Smash")],
    evolutions=[EvolutionCondition("Omastar", min_level=40)],
    egg_groups=["Water 1","Water 3"],
    is_fossil=True))

_sp(SpeciesData(139, "Omastar",
    [PokemonType.ROCK, PokemonType.WATER],
    70, 60, 125, 115, 70, 55, 45, 173, "medium_fast",
    learnset=[(1,"Constrict"),(1,"Withdraw"),(1,"Bite"),(1,"Water Gun"),(1,"Rollout"),
              (1,"Leer"),(1,"Ancient Power"),(1,"BubbleBeam"),(1,"Protect"),
              (1,"Brine"),(1,"Hydro Pump"),(1,"Shell Smash")],
    egg_groups=["Water 1","Water 3"],
    is_fossil=True))

_sp(SpeciesData(140, "Kabuto",
    [PokemonType.ROCK, PokemonType.WATER],
    30, 80, 90, 55, 45, 55, 45, 71, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Harden"),(7,"Absorb"),(13,"Leer"),(19,"Mud Shot"),
              (25,"Sand Attack"),(31,"Ancient Power"),(37,"Mega Drain"),(43,"Aqua Jet"),
              (49,"Slash"),(55,"Rock Slide"),(61,"Wring Out")],
    evolutions=[EvolutionCondition("Kabutops", min_level=40)],
    egg_groups=["Water 1","Water 3"],
    is_fossil=True))

_sp(SpeciesData(141, "Kabutops",
    [PokemonType.ROCK, PokemonType.WATER],
    60, 115, 105, 65, 70, 80, 45, 173, "medium_fast",
    learnset=[(1,"Scratch"),(1,"Harden"),(1,"Absorb"),(1,"Leer"),(1,"Mud Shot"),
              (1,"Sand Attack"),(1,"Ancient Power"),(1,"Mega Drain"),(1,"Aqua Jet"),
              (1,"Slash"),(1,"Rock Slide"),(1,"Wring Out")],
    egg_groups=["Water 1","Water 3"],
    is_fossil=True))

_sp(SpeciesData(142, "Aerodactyl",
    [PokemonType.ROCK, PokemonType.FLYING],
    80, 105, 65, 60, 75, 130, 45, 180, "slow",
    learnset=[(1,"Ice Fang"),(1,"Fire Fang"),(1,"Thunder Fang"),(1,"Wing Attack"),
              (1,"Supersonic"),(1,"Bite"),(9,"Ancient Power"),(17,"Scary Face"),
              (25,"Roost"),(33,"Agility"),(41,"Rock Slide"),(49,"Take Down"),
              (57,"Stone Edge"),(65,"Hyper Beam")],
    egg_groups=["Flying"],
    is_fossil=True))

_sp(SpeciesData(143, "Snorlax",
    [PokemonType.NORMAL],
    160, 110, 65, 65, 110, 30, 25, 189, "slow",
    learnset=[(1,"Tackle"),(1,"Defense Curl"),(1,"Amnesia"),(4,"Lick"),(9,"Belly Drum"),
              (12,"Yawn"),(17,"Rest"),(20,"Snore"),(25,"Sleep Talk"),(28,"Body Slam"),
              (33,"Block"),(36,"Rollout"),(41,"Crunch"),(44,"Heavy Slam"),(49,"Giga Impact")],
    evolutions=[],
    egg_groups=["Monster"],
    base_friendship=70))

_sp(SpeciesData(144, "Articuno",
    [PokemonType.ICE, PokemonType.FLYING],
    90, 85, 100, 95, 125, 85, 3, 261, "slow",
    learnset=[(1,"Gust"),(1,"Powder Snow"),(1,"Mist"),(1,"Ice Shard"),(5,"Tailwind"),
              (11,"Roost"),(17,"Ice Beam"),(23,"Reflect"),(29,"Hail"),(35,"Blizzard"),
              (41,"Agility"),(47,"Sheer Cold"),(53,"Hurricane")],
    is_legendary=True,
    gender_ratio=-1.0,
    pokedex_entry="A legendary bird Pokémon that can control ice. The flapping of its wings chills the air.",
    base_friendship=35))

_sp(SpeciesData(145, "Zapdos",
    [PokemonType.ELECTRIC, PokemonType.FLYING],
    90, 90, 85, 125, 90, 100, 3, 261, "slow",
    learnset=[(1,"Peck"),(1,"ThunderShock"),(1,"Thunder Wave"),(1,"Detect"),(5,"Pluck"),
              (11,"Ancient Power"),(17,"Charge"),(23,"Agility"),(29,"Discharge"),(35,"Rain Dance"),
              (41,"Light Screen"),(47,"Drill Peck"),(53,"Thunder")],
    is_legendary=True,
    gender_ratio=-1.0,
    pokedex_entry="A legendary bird Pokémon that is said to appear from clouds while dropping enormous lightning bolts.",
    base_friendship=35))

_sp(SpeciesData(146, "Moltres",
    [PokemonType.FIRE, PokemonType.FLYING],
    90, 100, 90, 125, 85, 90, 3, 261, "slow",
    learnset=[(1,"Wing Attack"),(1,"Ember"),(1,"Fire Spin"),(1,"Agility"),(5,"Endure"),
              (11,"Ancient Power"),(17,"Flamethrower"),(23,"Safeguard"),(29,"Air Slash"),
              (35,"Sunny Day"),(41,"Heat Wave"),(47,"Sky Attack"),(53,"Hurricane")],
    is_legendary=True,
    gender_ratio=-1.0,
    pokedex_entry="Known as the legendary bird of fire. Every flap of its wings creates a dazzling flash of flames.",
    base_friendship=35))

_sp(SpeciesData(147, "Dratini",
    [PokemonType.DRAGON],
    41, 64, 45, 50, 50, 50, 45, 67, "slow",
    learnset=[(1,"Wrap"),(1,"Leer"),(5,"Thunder Wave"),(11,"Twister"),(15,"Dragon Rage"),
              (21,"Slam"),(25,"Agility"),(31,"Dragon Tail"),(35,"Aqua Tail"),(41,"Dragon Rush"),
              (45,"ExtremeSpeed"),(51,"Hyper Beam"),(55,"Dragon Dance")],
    evolutions=[EvolutionCondition("Dragonair", min_level=30)],
    egg_groups=["Water 1","Dragon"]))

_sp(SpeciesData(148, "Dragonair",
    [PokemonType.DRAGON],
    61, 84, 65, 70, 70, 70, 45, 144, "slow",
    learnset=[(1,"Wrap"),(1,"Leer"),(1,"Thunder Wave"),(1,"Twister"),(15,"Dragon Rage"),
              (21,"Slam"),(25,"Agility"),(31,"Dragon Tail"),(35,"Aqua Tail"),(41,"Dragon Rush"),
              (45,"ExtremeSpeed"),(51,"Hyper Beam"),(55,"Dragon Dance")],
    evolutions=[EvolutionCondition("Dragonite", min_level=55)],
    egg_groups=["Water 1","Dragon"]))

_sp(SpeciesData(149, "Dragonite",
    [PokemonType.DRAGON, PokemonType.FLYING],
    91, 134, 95, 100, 100, 80, 45, 270, "slow",
    learnset=[(1,"Wrap"),(1,"Leer"),(1,"Thunder Wave"),(1,"Twister"),(1,"Dragon Rage"),
              (1,"Slam"),(1,"Agility"),(1,"Dragon Tail"),(1,"Aqua Tail"),(1,"Dragon Rush"),
              (1,"ExtremeSpeed"),(1,"Hyper Beam"),(1,"Dragon Dance"),(55,"Hurricane")],
    egg_groups=["Water 1","Dragon"]))

_sp(SpeciesData(150, "Mewtwo",
    [PokemonType.PSYCHIC],
    106, 110, 90, 154, 90, 130, 3, 306, "slow",
    learnset=[(1,"Confusion"),(1,"Disable"),(1,"Psych Up"),(8,"Mist"),(15,"Psybeam"),
              (22,"Swift"),(29,"Future Sight"),(36,"Recover"),(43,"Psychic"),(50,"Barrier"),
              (57,"Aura Sphere"),(64,"Amnesia"),(71,"Me First"),(78,"Safeguard"),(85,"Hyper Beam")],
    is_legendary=True,
    gender_ratio=-1.0,
    pokedex_entry="A Pokémon that was created by genetic manipulation. However, even the power of the greatest humans could not create a perfect copy of Mew.",
    base_friendship=0))

_sp(SpeciesData(151, "Mew",
    [PokemonType.PSYCHIC],
    100, 100, 100, 100, 100, 100, 45, 270, "medium_slow",
    learnset=[(1,"Pound"),(10,"Transform"),(20,"Metronome"),(30,"Psychic"),(40,"Barrier"),
              (50,"Ancient Power"),(60,"Amnesia"),(70,"Me First"),(80,"Baton Pass"),(90,"Nasty Plot"),
              (100,"Aura Sphere")],
    is_legendary=True,
    gender_ratio=-1.0,
    pokedex_entry="So rare that it is still said to be a mirage by many experts. Only a few people have seen it worldwide.",
    base_friendship=100))
