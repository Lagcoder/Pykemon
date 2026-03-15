"""
Pokédex — tracks seen and caught Pokémon, and provides species information.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from ..data.pokemon_data import SPECIES, SPECIES_BY_NUM

if TYPE_CHECKING:
    from .pokemon import Pokemon


class Pokedex:
    """
    Tracks which Pokémon the player has seen and caught.
    """

    def __init__(self):
        self._seen: set[int] = set()
        self._caught: set[int] = set()

    # ── Registration ──────────────────────────────────────────────────────────

    def register_seen(self, pokemon: "Pokemon") -> None:
        """Mark a Pokémon as seen."""
        self._seen.add(pokemon.species.number)

    def register_caught(self, pokemon: "Pokemon") -> None:
        """Mark a Pokémon as both seen and caught."""
        num = pokemon.species.number
        self._seen.add(num)
        self._caught.add(num)

    # ── Queries ───────────────────────────────────────────────────────────────

    def is_seen(self, number: int) -> bool:
        return number in self._seen

    def is_caught(self, number: int) -> bool:
        return number in self._caught

    @property
    def seen_count(self) -> int:
        return len(self._seen)

    @property
    def caught_count(self) -> int:
        return len(self._caught)

    @property
    def completion_pct(self) -> float:
        total = len(SPECIES)
        if total == 0:
            return 0.0
        return self._caught.__len__() / total * 100

    # ── Display ───────────────────────────────────────────────────────────────

    def lookup(self, name_or_number: "str | int") -> Optional[str]:
        """
        Return a Pokédex entry string for the given species.
        Only returns data for seen/caught Pokémon.
        """
        if isinstance(name_or_number, int):
            species = SPECIES_BY_NUM.get(name_or_number)
        else:
            species = SPECIES.get(name_or_number)
        if not species:
            return f"No data found for: {name_or_number}"

        if not self.is_seen(species.number):
            return f"#{species.number:03d} ???\nNot yet encountered."

        types_str = "/".join(t.value for t in species.types)
        caught_marker = "✓ CAUGHT" if self.is_caught(species.number) else "○ Seen"
        entry = (
            f"#{species.number:03d} {species.name}  [{caught_marker}]\n"
            f"Type: {types_str}\n"
            f"HP:{species.base_hp}  ATK:{species.base_atk}  DEF:{species.base_def}  "
            f"SpA:{species.base_spa}  SpD:{species.base_spd}  Spe:{species.base_spe}\n"
            f"{species.pokedex_entry or '(No entry available.)'}"
        )
        return entry

    def list_all(self, only_caught: bool = False) -> str:
        """Return a formatted Pokédex list."""
        lines = [f"{'='*50}", f"{'POKÉDEX':^50}", f"{'='*50}",
                 f"Seen: {self.seen_count}  Caught: {self.caught_count}  "
                 f"Completion: {self.completion_pct:.1f}%", ""]
        for num in sorted(SPECIES_BY_NUM.keys()):
            sp = SPECIES_BY_NUM[num]
            if num in self._caught:
                marker = "✓"
            elif num in self._seen:
                marker = "○"
            else:
                if only_caught:
                    continue
                marker = " "
            name = sp.name if num in self._seen else "???"
            lines.append(f"  {marker} #{num:03d}  {name}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<Pokédex seen={self.seen_count} caught={self.caught_count}>"
