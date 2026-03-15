"""
Ride Pokémon system — lets the player mount certain Pokémon to traverse terrain.
Acts like a field HM replacement (Gen VII style).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.pokemon import Pokemon


@dataclass
class RideAbility:
    name: str            # e.g. "Tauros Charge"
    terrain: str         # e.g. "land", "water", "air", "cave"
    description: str
    replaces_hm: Optional[int] = None   # HM number this replaces (e.g. 3 = Surf)


# Ride Pokémon registry
RIDE_POKEMON: dict[str, RideAbility] = {
    "Tauros":   RideAbility("Tauros Charge",  "land",  "Dash and smash cracked boulders.", replaces_hm=None),
    "Lapras":   RideAbility("Lapras Paddle",   "water", "Surf on water bodies.",             replaces_hm=3),
    "Charizard":RideAbility("Charizard Glide", "air",   "Soar over terrain to distant areas.", replaces_hm=2),
    "Stoutland":RideAbility("Stoutland Search","land",  "Detect hidden items.",               replaces_hm=None),
    "Sharpedo": RideAbility("Sharpedo Jet",    "water", "Jet through water and smash rocks.", replaces_hm=None),
    "Mudsdale": RideAbility("Mudsdale Gallop", "land",  "Traverse rough terrain effortlessly.",replaces_hm=None),
    "Flygon":   RideAbility("Flygon Hover",    "air",   "Hover above ground and fly.",         replaces_hm=2),
    "Noivern":  RideAbility("Noivern Soar",    "air",   "Soar at great speed.",                replaces_hm=2),
    "Rhyhorn":  RideAbility("Rhyhorn Crag",    "land",  "Smash rock formations and boulders.", replaces_hm=None),
    "Wailord":  RideAbility("Wailord Float",   "water", "Surf on the ocean on this massive Pokémon.", replaces_hm=3),
}


class RideSystem:
    """
    Manages which Pokémon the player can ride and what abilities are available.
    """

    def __init__(self):
        self._unlocked: set[str] = set()

    def unlock(self, pokemon_name: str) -> bool:
        """Unlock a Ride Pokémon. Returns True if it exists."""
        if pokemon_name in RIDE_POKEMON:
            self._unlocked.add(pokemon_name)
            return True
        return False

    def can_ride(self, pokemon_name: str) -> bool:
        return pokemon_name in self._unlocked

    def get_available(self) -> list[tuple[str, RideAbility]]:
        return [(name, ability) for name, ability in RIDE_POKEMON.items()
                if name in self._unlocked]

    def can_use_terrain(self, terrain: str) -> bool:
        """Return True if any unlocked Ride Pokémon supports the given terrain."""
        for name in self._unlocked:
            if RIDE_POKEMON[name].terrain == terrain:
                return True
        return False

    def use(self, pokemon_name: str) -> Optional[str]:
        """
        Use a Ride Pokémon.
        Returns a description of the action, or None if unavailable.
        """
        if not self.can_ride(pokemon_name):
            return None
        ability = RIDE_POKEMON[pokemon_name]
        return f"You mount {pokemon_name}! {ability.description}"

    def display(self) -> str:
        lines = ["=== RIDE POKÉMON ==="]
        for name, ability in RIDE_POKEMON.items():
            status = "✓" if name in self._unlocked else "✗"
            lines.append(f"  [{status}] {name:<12} {ability.name:<20} ({ability.terrain})")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<RideSystem unlocked={sorted(self._unlocked)}>"
