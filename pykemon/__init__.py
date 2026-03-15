"""
Pykemon — a Pokémon game engine written in Python.

Features:
  - 100+ Pokémon with stats, types, learnsets, and evolutions
  - 15 Pokémon types with full effectiveness chart
  - Turn-based combat with status effects, weather, double battles
  - Catching system with multiple Poké Balls
  - Evolution (level, item, trade, friendship, time)
  - 8 Gyms + Elite Four + Champion
  - Pokédex, TMs, HMs, Bag, Held Items, Fossils
  - Friendship / Affection system
  - Day/Night cycle
  - Shiny Pokémon
  - Ride Pokémon (HM replacement)
  - Pokémon Centers and Poké Marts
"""

from .core.pokemon import Pokemon, create_pokemon, Move
from .core.trainer import Trainer
from .core.battle import Battle, BattleResult
from .core.bag import Bag
from .core.pokedex import Pokedex
from .data.types import PokemonType, get_effectiveness
from .data.moves import MOVES, MoveData, StatusEffect, WeatherEffect
from .data.pokemon_data import SPECIES, SPECIES_BY_NUM, SpeciesData
from .data.items import ITEMS, ItemData, ItemCategory
from .systems.evolution import check_evolution, evolve
from .systems.friendship import update_friendship, friendship_tier
from .systems.day_night import get_time_of_day, describe_time
from .systems.ride import RideSystem
from .world.pokemon_center import PokemonCenter
from .world.poke_mart import PokeMart
from .world.gym import GymBadgeSystem
from .world.fossils import FossilLab

__version__ = "1.0.0"
__all__ = [
    "Pokemon", "create_pokemon", "Move",
    "Trainer",
    "Battle", "BattleResult",
    "Bag",
    "Pokedex",
    "PokemonType", "get_effectiveness",
    "MOVES", "MoveData", "StatusEffect", "WeatherEffect",
    "SPECIES", "SPECIES_BY_NUM", "SpeciesData",
    "ITEMS", "ItemData", "ItemCategory",
    "check_evolution", "evolve",
    "update_friendship", "friendship_tier",
    "get_time_of_day", "describe_time",
    "RideSystem",
    "PokemonCenter",
    "PokeMart",
    "GymBadgeSystem",
    "FossilLab",
]
