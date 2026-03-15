"""
15 Pokémon Types and their effectiveness chart.
"""

from enum import Enum


class PokemonType(Enum):
    NORMAL = "Normal"
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"
    ELECTRIC = "Electric"
    ICE = "Ice"
    FIGHTING = "Fighting"
    POISON = "Poison"
    GROUND = "Ground"
    FLYING = "Flying"
    PSYCHIC = "Psychic"
    BUG = "Bug"
    ROCK = "Rock"
    GHOST = "Ghost"
    DRAGON = "Dragon"


# Type effectiveness chart: effectiveness[attacker][defender] = multiplier
# 2.0 = super effective, 0.5 = not very effective, 0.0 = immune
TYPE_CHART: dict[PokemonType, dict[PokemonType, float]] = {
    PokemonType.NORMAL: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 1.0, PokemonType.WATER: 1.0,
        PokemonType.GRASS: 1.0, PokemonType.ELECTRIC: 1.0, PokemonType.ICE: 1.0,
        PokemonType.FIGHTING: 1.0, PokemonType.POISON: 1.0, PokemonType.GROUND: 1.0,
        PokemonType.FLYING: 1.0, PokemonType.PSYCHIC: 1.0, PokemonType.BUG: 1.0,
        PokemonType.ROCK: 0.5, PokemonType.GHOST: 0.0, PokemonType.DRAGON: 1.0,
    },
    PokemonType.FIRE: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 0.5, PokemonType.WATER: 0.5,
        PokemonType.GRASS: 2.0, PokemonType.ELECTRIC: 1.0, PokemonType.ICE: 2.0,
        PokemonType.FIGHTING: 1.0, PokemonType.POISON: 1.0, PokemonType.GROUND: 1.0,
        PokemonType.FLYING: 1.0, PokemonType.PSYCHIC: 1.0, PokemonType.BUG: 2.0,
        PokemonType.ROCK: 0.5, PokemonType.GHOST: 1.0, PokemonType.DRAGON: 0.5,
    },
    PokemonType.WATER: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 2.0, PokemonType.WATER: 0.5,
        PokemonType.GRASS: 0.5, PokemonType.ELECTRIC: 1.0, PokemonType.ICE: 1.0,
        PokemonType.FIGHTING: 1.0, PokemonType.POISON: 1.0, PokemonType.GROUND: 2.0,
        PokemonType.FLYING: 1.0, PokemonType.PSYCHIC: 1.0, PokemonType.BUG: 1.0,
        PokemonType.ROCK: 2.0, PokemonType.GHOST: 1.0, PokemonType.DRAGON: 0.5,
    },
    PokemonType.GRASS: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 0.5, PokemonType.WATER: 2.0,
        PokemonType.GRASS: 0.5, PokemonType.ELECTRIC: 1.0, PokemonType.ICE: 1.0,
        PokemonType.FIGHTING: 1.0, PokemonType.POISON: 0.5, PokemonType.GROUND: 2.0,
        PokemonType.FLYING: 0.5, PokemonType.PSYCHIC: 1.0, PokemonType.BUG: 0.5,
        PokemonType.ROCK: 2.0, PokemonType.GHOST: 1.0, PokemonType.DRAGON: 0.5,
    },
    PokemonType.ELECTRIC: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 1.0, PokemonType.WATER: 2.0,
        PokemonType.GRASS: 0.5, PokemonType.ELECTRIC: 0.5, PokemonType.ICE: 1.0,
        PokemonType.FIGHTING: 1.0, PokemonType.POISON: 1.0, PokemonType.GROUND: 0.0,
        PokemonType.FLYING: 2.0, PokemonType.PSYCHIC: 1.0, PokemonType.BUG: 1.0,
        PokemonType.ROCK: 1.0, PokemonType.GHOST: 1.0, PokemonType.DRAGON: 0.5,
    },
    PokemonType.ICE: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 0.5, PokemonType.WATER: 0.5,
        PokemonType.GRASS: 2.0, PokemonType.ELECTRIC: 1.0, PokemonType.ICE: 0.5,
        PokemonType.FIGHTING: 1.0, PokemonType.POISON: 1.0, PokemonType.GROUND: 2.0,
        PokemonType.FLYING: 2.0, PokemonType.PSYCHIC: 1.0, PokemonType.BUG: 1.0,
        PokemonType.ROCK: 1.0, PokemonType.GHOST: 1.0, PokemonType.DRAGON: 2.0,
    },
    PokemonType.FIGHTING: {
        PokemonType.NORMAL: 2.0, PokemonType.FIRE: 1.0, PokemonType.WATER: 1.0,
        PokemonType.GRASS: 1.0, PokemonType.ELECTRIC: 1.0, PokemonType.ICE: 2.0,
        PokemonType.FIGHTING: 1.0, PokemonType.POISON: 0.5, PokemonType.GROUND: 1.0,
        PokemonType.FLYING: 0.5, PokemonType.PSYCHIC: 0.5, PokemonType.BUG: 0.5,
        PokemonType.ROCK: 2.0, PokemonType.GHOST: 0.0, PokemonType.DRAGON: 1.0,
    },
    PokemonType.POISON: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 1.0, PokemonType.WATER: 1.0,
        PokemonType.GRASS: 2.0, PokemonType.ELECTRIC: 1.0, PokemonType.ICE: 1.0,
        PokemonType.FIGHTING: 1.0, PokemonType.POISON: 0.5, PokemonType.GROUND: 0.5,
        PokemonType.FLYING: 1.0, PokemonType.PSYCHIC: 1.0, PokemonType.BUG: 1.0,
        PokemonType.ROCK: 0.5, PokemonType.GHOST: 0.5, PokemonType.DRAGON: 1.0,
    },
    PokemonType.GROUND: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 2.0, PokemonType.WATER: 1.0,
        PokemonType.GRASS: 0.5, PokemonType.ELECTRIC: 2.0, PokemonType.ICE: 1.0,
        PokemonType.FIGHTING: 1.0, PokemonType.POISON: 2.0, PokemonType.GROUND: 1.0,
        PokemonType.FLYING: 0.0, PokemonType.PSYCHIC: 1.0, PokemonType.BUG: 0.5,
        PokemonType.ROCK: 2.0, PokemonType.GHOST: 1.0, PokemonType.DRAGON: 1.0,
    },
    PokemonType.FLYING: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 1.0, PokemonType.WATER: 1.0,
        PokemonType.GRASS: 2.0, PokemonType.ELECTRIC: 0.5, PokemonType.ICE: 1.0,
        PokemonType.FIGHTING: 2.0, PokemonType.POISON: 1.0, PokemonType.GROUND: 1.0,
        PokemonType.FLYING: 1.0, PokemonType.PSYCHIC: 1.0, PokemonType.BUG: 2.0,
        PokemonType.ROCK: 0.5, PokemonType.GHOST: 1.0, PokemonType.DRAGON: 1.0,
    },
    PokemonType.PSYCHIC: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 1.0, PokemonType.WATER: 1.0,
        PokemonType.GRASS: 1.0, PokemonType.ELECTRIC: 1.0, PokemonType.ICE: 1.0,
        PokemonType.FIGHTING: 2.0, PokemonType.POISON: 2.0, PokemonType.GROUND: 1.0,
        PokemonType.FLYING: 1.0, PokemonType.PSYCHIC: 0.5, PokemonType.BUG: 1.0,
        PokemonType.ROCK: 1.0, PokemonType.GHOST: 0.0, PokemonType.DRAGON: 1.0,
    },
    PokemonType.BUG: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 0.5, PokemonType.WATER: 1.0,
        PokemonType.GRASS: 2.0, PokemonType.ELECTRIC: 1.0, PokemonType.ICE: 1.0,
        PokemonType.FIGHTING: 0.5, PokemonType.POISON: 0.5, PokemonType.GROUND: 1.0,
        PokemonType.FLYING: 0.5, PokemonType.PSYCHIC: 2.0, PokemonType.BUG: 1.0,
        PokemonType.ROCK: 1.0, PokemonType.GHOST: 0.5, PokemonType.DRAGON: 1.0,
    },
    PokemonType.ROCK: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 2.0, PokemonType.WATER: 1.0,
        PokemonType.GRASS: 1.0, PokemonType.ELECTRIC: 1.0, PokemonType.ICE: 2.0,
        PokemonType.FIGHTING: 0.5, PokemonType.POISON: 1.0, PokemonType.GROUND: 0.5,
        PokemonType.FLYING: 2.0, PokemonType.PSYCHIC: 1.0, PokemonType.BUG: 2.0,
        PokemonType.ROCK: 1.0, PokemonType.GHOST: 1.0, PokemonType.DRAGON: 1.0,
    },
    PokemonType.GHOST: {
        PokemonType.NORMAL: 0.0, PokemonType.FIRE: 1.0, PokemonType.WATER: 1.0,
        PokemonType.GRASS: 1.0, PokemonType.ELECTRIC: 1.0, PokemonType.ICE: 1.0,
        PokemonType.FIGHTING: 1.0, PokemonType.POISON: 1.0, PokemonType.GROUND: 1.0,
        PokemonType.FLYING: 1.0, PokemonType.PSYCHIC: 2.0, PokemonType.BUG: 1.0,
        PokemonType.ROCK: 1.0, PokemonType.GHOST: 2.0, PokemonType.DRAGON: 1.0,
    },
    PokemonType.DRAGON: {
        PokemonType.NORMAL: 1.0, PokemonType.FIRE: 1.0, PokemonType.WATER: 1.0,
        PokemonType.GRASS: 1.0, PokemonType.ELECTRIC: 1.0, PokemonType.ICE: 1.0,
        PokemonType.FIGHTING: 1.0, PokemonType.POISON: 1.0, PokemonType.GROUND: 1.0,
        PokemonType.FLYING: 1.0, PokemonType.PSYCHIC: 1.0, PokemonType.BUG: 1.0,
        PokemonType.ROCK: 1.0, PokemonType.GHOST: 1.0, PokemonType.DRAGON: 2.0,
    },
}


def get_effectiveness(attack_type: PokemonType, defense_types: list[PokemonType]) -> float:
    """Return the combined type effectiveness multiplier for an attack."""
    multiplier = 1.0
    for def_type in defense_types:
        multiplier *= TYPE_CHART[attack_type][def_type]
    return multiplier


def effectiveness_text(multiplier: float) -> str:
    """Return descriptive text for an effectiveness multiplier."""
    if multiplier == 0.0:
        return "It had no effect!"
    elif multiplier < 1.0:
        return "It's not very effective..."
    elif multiplier > 1.0:
        return "It's super effective!"
    return ""
