"""
Evolution system: handles level-up, item, trade, friendship, and time-based evolutions.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..core.pokemon import Pokemon
    from ..data.pokemon_data import EvolutionCondition


def check_evolution(
    pokemon: "Pokemon",
    time_of_day: str = "day",
    trade: bool = False,
    used_item: Optional[str] = None,
) -> Optional["EvolutionCondition"]:
    """
    Check whether a Pokémon should evolve.

    Returns the first matching EvolutionCondition, or None if no evolution triggers.
    """
    for cond in pokemon.species.evolutions:
        # Level-based
        if cond.min_level and pokemon.level >= cond.min_level:
            if not cond.item and not cond.trade and not cond.friendship:
                # May also require time of day
                if cond.time_of_day and cond.time_of_day != time_of_day:
                    continue
                if cond.move_known and not any(m.data.name == cond.move_known for m in pokemon.moves):
                    continue
                return cond

        # Friendship-based (also checks time of day)
        if cond.friendship and pokemon.friendship >= cond.friendship:
            if cond.time_of_day and cond.time_of_day != time_of_day:
                continue
            if cond.move_known and not any(m.data.name == cond.move_known for m in pokemon.moves):
                continue
            return cond

        # Item-based
        if cond.item and used_item and cond.item == used_item:
            return cond

        # Trade-based
        if cond.trade and trade:
            if cond.held_item and pokemon.held_item != cond.held_item:
                continue
            return cond

    return None


def evolve(pokemon: "Pokemon", cond: "EvolutionCondition") -> "Pokemon":
    """
    Evolve a Pokémon in-place: update its species, recalculate stats, and
    attempt to learn any moves available at the new form.

    Returns the mutated pokemon.
    """
    from ..data.pokemon_data import SPECIES
    from ..core.pokemon import Move
    from ..data.moves import MOVES

    new_species_name = cond.evolves_to
    if new_species_name not in SPECIES:
        raise ValueError(f"Unknown evolution target: {new_species_name}")

    old_name = pokemon.species.name
    new_species = SPECIES[new_species_name]

    pokemon.species = new_species

    # Preserve nickname: only update if it was the default (species name)
    if pokemon.nickname == old_name:
        pokemon.nickname = new_species.name

    # Recalculate stats (level stays the same)
    old_max = pokemon.max_hp
    pokemon._calc_stats()
    # Heal the difference in max HP
    pokemon.current_hp += pokemon.max_hp - old_max
    pokemon.current_hp = min(pokemon.current_hp, pokemon.max_hp)

    # Learn any moves available at the current level for the new species
    for (lvl, move_name) in new_species.learnset:
        if lvl <= pokemon.level and move_name in MOVES:
            if not any(m.data.name == move_name for m in pokemon.moves):
                if len(pokemon.moves) < 4:
                    pokemon.learn_move(move_name)

    return pokemon


def can_evolve_with_item(pokemon: "Pokemon", item_name: str) -> bool:
    """Return True if using the given item triggers an evolution."""
    from ..data.pokemon_data import SPECIES
    for cond in pokemon.species.evolutions:
        if cond.item and cond.item == item_name:
            return True
    return False


def item_evolutions_available(pokemon: "Pokemon") -> list[str]:
    """Return list of item names that can currently evolve this Pokémon."""
    return [cond.item for cond in pokemon.species.evolutions if cond.item]
