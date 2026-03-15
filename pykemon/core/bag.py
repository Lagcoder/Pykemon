"""
Bag / inventory system for Pykemon.
"""

from __future__ import annotations
from collections import defaultdict
from typing import Optional
from ..data.items import ITEMS, ItemCategory, ItemData
from ..data.moves import TM_MOVES, HM_MOVES


class Bag:
    """
    Manages the player's item inventory.
    Organised into pockets by ItemCategory.
    """

    def __init__(self):
        # pocket -> {item_name: count}
        self._pockets: dict[ItemCategory, dict[str, int]] = {
            cat: {} for cat in ItemCategory
        }

    # ── Modification ─────────────────────────────────────────────────────────

    def add_item(self, item_name: str, count: int = 1) -> None:
        """Add items to the bag."""
        item = ITEMS.get(item_name)
        if not item:
            raise ValueError(f"Unknown item: {item_name}")
        pocket = self._pockets[item.category]
        pocket[item_name] = pocket.get(item_name, 0) + count

    def remove_item(self, item_name: str, count: int = 1) -> bool:
        """Remove items from the bag. Returns True if successful."""
        item = ITEMS.get(item_name)
        if not item:
            return False
        pocket = self._pockets[item.category]
        if pocket.get(item_name, 0) < count:
            return False
        pocket[item_name] -= count
        if pocket[item_name] <= 0:
            del pocket[item_name]
        return True

    def has_item(self, item_name: str, count: int = 1) -> bool:
        item = ITEMS.get(item_name)
        if not item:
            return False
        return self._pockets[item.category].get(item_name, 0) >= count

    def item_count(self, item_name: str) -> int:
        item = ITEMS.get(item_name)
        if not item:
            return 0
        return self._pockets[item.category].get(item_name, 0)

    # ── Queries ───────────────────────────────────────────────────────────────

    def get_pocket(self, category: ItemCategory) -> dict[str, int]:
        return dict(self._pockets[category])

    def all_items(self) -> dict[str, int]:
        result: dict[str, int] = {}
        for pocket in self._pockets.values():
            result.update(pocket)
        return result

    def pokeballs(self) -> dict[str, int]:
        return self.get_pocket(ItemCategory.POKEBALL)

    def medicine(self) -> dict[str, int]:
        return self.get_pocket(ItemCategory.MEDICINE)

    def tms_hms(self) -> dict[str, int]:
        result = {}
        result.update(self.get_pocket(ItemCategory.TM))
        result.update(self.get_pocket(ItemCategory.HM))
        return result

    def key_items(self) -> dict[str, int]:
        return self.get_pocket(ItemCategory.KEY)

    def held_items(self) -> dict[str, int]:
        return self.get_pocket(ItemCategory.HELD)

    def fossils(self) -> dict[str, int]:
        return self.get_pocket(ItemCategory.FOSSIL)

    # ── TM/HM teaching ────────────────────────────────────────────────────────

    def can_teach_tm(self, tm_number: int, pokemon_name: str) -> bool:
        """Check if a TM can be taught to a Pokémon (permissive - all can learn)."""
        return tm_number in TM_MOVES and self.has_item(f"TM{tm_number:02d}")

    def teach_tm(self, tm_number: int, pokemon: "Pokemon") -> bool:  # type: ignore[name-defined]
        """Teach a TM move to a Pokémon. Returns True if successful."""
        if tm_number not in TM_MOVES:
            return False
        move_data = TM_MOVES[tm_number]
        item_name = f"TM{tm_number:02d}"
        if not self.has_item(item_name):
            return False
        if len(pokemon.moves) < 4:
            pokemon.learn_move(move_data.name)
        else:
            # Replace oldest move
            pokemon.learn_move(move_data.name, slot=0)
        # TMs are consumed (Gen I/II style); set to infinite use in newer games
        # We'll keep TMs and not consume them (Gen V+ style)
        return True

    def teach_hm(self, hm_number: int, pokemon: "Pokemon") -> bool:  # type: ignore[name-defined]
        """Teach an HM move. HMs are not consumed and cannot be forgotten."""
        if hm_number not in HM_MOVES:
            return False
        move_data = HM_MOVES[hm_number]
        item_name = f"HM{hm_number:02d}"
        if not self.has_item(item_name):
            return False
        if len(pokemon.moves) < 4:
            pokemon.learn_move(move_data.name)
        else:
            pokemon.learn_move(move_data.name, slot=0)
        return True

    # ── Display ───────────────────────────────────────────────────────────────

    def display(self) -> str:
        lines = ["=== BAG ==="]
        for cat in ItemCategory:
            pocket = self._pockets[cat]
            if not pocket:
                continue
            lines.append(f"\n[{cat.value}]")
            for item_name, count in sorted(pocket.items()):
                item_data = ITEMS.get(item_name)
                lines.append(f"  {item_name:<25} x{count:<4}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        total = sum(sum(p.values()) for p in self._pockets.values())
        return f"<Bag {total} items>"
