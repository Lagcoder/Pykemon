"""
Pokémon Center — heals the player's party and stores Pokémon in the PC.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..core.trainer import Trainer
    from ..core.pokemon import Pokemon


class PC:
    """
    PC Storage system: up to 30 boxes, each holding up to 30 Pokémon.
    """

    BOXES = 30
    BOX_SIZE = 30

    def __init__(self):
        self._boxes: list[list[Optional["Pokemon"]]] = [
            [None] * self.BOX_SIZE for _ in range(self.BOXES)
        ]
        self.active_box = 0

    def deposit(self, pokemon: "Pokemon", box: Optional[int] = None) -> bool:
        """Deposit a Pokémon to a box. Returns True if successful."""
        box_idx = box if box is not None else self.active_box
        if box_idx < 0 or box_idx >= self.BOXES:
            return False
        for i, slot in enumerate(self._boxes[box_idx]):
            if slot is None:
                self._boxes[box_idx][i] = pokemon
                return True
        # Try next box
        for b in range(self.BOXES):
            for i, slot in enumerate(self._boxes[b]):
                if slot is None:
                    self._boxes[b][i] = pokemon
                    self.active_box = b
                    return True
        return False   # PC is full

    def withdraw(self, box: int, slot: int) -> Optional["Pokemon"]:
        """Withdraw a Pokémon from a box slot."""
        if box < 0 or box >= self.BOXES or slot < 0 or slot >= self.BOX_SIZE:
            return None
        pokemon = self._boxes[box][slot]
        if pokemon is not None:
            self._boxes[box][slot] = None
        return pokemon

    def list_box(self, box: int) -> list[tuple[int, "Pokemon"]]:
        """Return list of (slot_index, pokemon) for all filled slots in a box."""
        if box < 0 or box >= self.BOXES:
            return []
        return [(i, p) for i, p in enumerate(self._boxes[box]) if p is not None]

    def total_stored(self) -> int:
        return sum(1 for b in self._boxes for p in b if p is not None)

    def display_box(self, box: int) -> str:
        entries = self.list_box(box)
        if not entries:
            return f"Box {box + 1}: (empty)"
        lines = [f"Box {box + 1}:"]
        for slot, p in entries:
            shiny = "✨" if p.is_shiny else " "
            lines.append(f"  [{slot+1:2d}] {shiny}{p.nickname:<12} Lv.{p.level:3d}  {p.species.name}")
        return "\n".join(lines)


class PokemonCenter:
    """
    Pokémon Center — heals the party and provides PC access.
    """

    def __init__(self, city: str):
        self.city = city
        self.pc = PC()

    def heal_party(self, trainer: "Trainer") -> list[str]:
        """
        Fully restore all Pokémon in the party.
        Returns event messages.
        """
        msgs = [
            f"Nurse Joy: Welcome to the Pokémon Center in {self.city}!",
            "Nurse Joy: We'll restore your Pokémon to full health. Please wait...",
        ]
        trainer.heal_party()
        msgs.append("Nurse Joy: Your Pokémon have been restored to full health!")
        msgs.append(f"Nurse Joy: We hope to see you again!")
        return msgs

    def deposit_pokemon(self, trainer: "Trainer", party_idx: int) -> list[str]:
        """
        Deposit a Pokémon from the party into the PC.
        """
        if len(trainer.party) <= 1:
            return ["PC: You need to keep at least one Pokémon with you!"]
        if party_idx < 0 or party_idx >= len(trainer.party):
            return ["PC: Invalid Pokémon slot."]
        pokemon = trainer.party.pop(party_idx)
        if self.pc.deposit(pokemon):
            return [f"PC: {pokemon.nickname} was transferred to Box {self.pc.active_box + 1}."]
        # Put it back if PC is full
        trainer.party.insert(party_idx, pokemon)
        return ["PC: The PC is full! There's no room for any more Pokémon."]

    def withdraw_pokemon(self, trainer: "Trainer", box: int, slot: int) -> list[str]:
        """
        Withdraw a Pokémon from the PC into the party.
        """
        if len(trainer.party) >= 6:
            return ["PC: Your party is full! Deposit a Pokémon first."]
        pokemon = self.pc.withdraw(box, slot)
        if pokemon is None:
            return ["PC: There's no Pokémon in that slot."]
        trainer.party.append(pokemon)
        return [f"PC: {pokemon.nickname} was added to your party!"]

    def __repr__(self) -> str:
        return f"<PokémonCenter {self.city}>"
