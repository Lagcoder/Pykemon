"""
Fossil system — revives fossil items into Pokémon.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..core.trainer import Trainer

from ..data.items import ITEMS
from ..core.pokemon import create_pokemon


# Mapping of fossil item -> Pokémon species that it revives
FOSSIL_REVIVALS: dict[str, str] = {
    "Old Amber":       "Aerodactyl",
    "Dome Fossil":     "Kabuto",
    "Helix Fossil":    "Omanyte",
    "Root Fossil":     "Lileep",
    "Claw Fossil":     "Anorith",
    "Skull Fossil":    "Cranidos",
    "Armor Fossil":    "Shieldon",
    "Cover Fossil":    "Tirtouga",
    "Plume Fossil":    "Archen",
    "Jaw Fossil":      "Tyrunt",
    "Sail Fossil":     "Amaura",
}


class FossilLab:
    """
    Fossil revival laboratory.
    """

    def __init__(self, location: str = "Cinnabar Island"):
        self.location = location

    def can_revive(self, fossil_name: str) -> bool:
        return fossil_name in FOSSIL_REVIVALS

    def revive(
        self,
        trainer: "Trainer",
        fossil_name: str,
        revival_level: int = 5,
    ) -> tuple[Optional["Pokemon"], list[str]]:  # type: ignore[name-defined]
        """
        Revive a fossil Pokémon from the trainer's bag.

        Returns (pokemon, messages). If revival fails, pokemon is None.
        """
        msgs: list[str] = []
        if not trainer.bag.has_item(fossil_name):
            msgs.append(f"You don't have a {fossil_name} to revive!")
            return None, msgs

        species_name = FOSSIL_REVIVALS.get(fossil_name)
        if not species_name:
            msgs.append(f"{fossil_name} is not a valid fossil.")
            return None, msgs

        msgs.append(f"Scientist: We can restore this {fossil_name}. Please wait...")
        msgs.append(f"Scientist: ...The restoration is complete!")

        pokemon = create_pokemon(
            species_name,
            revival_level,
            trainer_name=trainer.name,
        )
        trainer.bag.remove_item(fossil_name, 1)

        if trainer.add_pokemon(pokemon):
            msgs.append(f"{species_name} was added to your party!")
        else:
            # Party full — send to PC (handled externally)
            msgs.append(
                f"{species_name} was sent to your PC Storage "
                f"because your party is full!"
            )

        return pokemon, msgs

    def display(self) -> str:
        lines = ["=== FOSSIL LAB ===", f"Location: {self.location}", ""]
        lines.append("We can revive the following fossils:")
        for fossil, pokemon in sorted(FOSSIL_REVIVALS.items()):
            lines.append(f"  {fossil:<20} → {pokemon}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<FossilLab {self.location}>"
