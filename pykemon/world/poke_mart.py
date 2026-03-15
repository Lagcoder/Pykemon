"""
Poké Mart — sells items to the player.
Inventory varies by number of badges earned.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from ..data.items import ITEMS, ItemCategory

if TYPE_CHECKING:
    from ..core.trainer import Trainer


# Mart inventory unlocked at each badge count threshold
_BADGE_STOCK: list[tuple[int, list[str]]] = [
    (0, ["Poké Ball", "Antidote", "Potion", "Escape Rope", "Repel"]),
    (1, ["Super Potion", "Paralyze Heal", "Burn Heal", "Ice Heal", "Awakening",
         "Full Heal"]),
    (2, ["Great Ball", "Super Repel"]),
    (3, ["Hyper Potion", "Revive"]),
    (5, ["Ultra Ball", "Max Repel", "Full Restore"]),
    (7, ["Max Potion"]),
    (8, ["Max Revive"]),
]


class PokeMart:
    """
    A Poké Mart where the player can buy and sell items.
    """

    def __init__(self, city: str):
        self.city = city

    def get_stock(self, badge_count: int) -> list[str]:
        """Return a list of item names available based on badge count."""
        stock: list[str] = []
        for threshold, items in _BADGE_STOCK:
            if badge_count >= threshold:
                for item_name in items:
                    if item_name not in stock:
                        stock.append(item_name)
        return stock

    def display_stock(self, badge_count: int) -> str:
        stock = self.get_stock(badge_count)
        lines = [f"=== {self.city} Poké Mart ===", ""]
        for item_name in stock:
            item_data = ITEMS.get(item_name)
            if item_data and item_data.price > 0:
                lines.append(f"  {item_name:<25} ₽{item_data.price:,}")
        lines.append("")
        return "\n".join(lines)

    def buy(
        self,
        trainer: "Trainer",
        item_name: str,
        count: int = 1,
        badge_count: int = 0,
    ) -> tuple[bool, str]:
        """
        Purchase items.
        Returns (success: bool, message: str).
        """
        if item_name not in self.get_stock(badge_count):
            return False, f"Sorry, we don't carry {item_name} here."
        item_data = ITEMS.get(item_name)
        if not item_data:
            return False, f"Unknown item: {item_name}"
        total_cost = item_data.price * count
        if trainer.money < total_cost:
            return False, (
                f"You need ₽{total_cost:,} to buy {count}× {item_name}, "
                f"but you only have ₽{trainer.money:,}."
            )
        trainer.money -= total_cost
        trainer.bag.add_item(item_name, count)
        return True, (
            f"Bought {count}× {item_name} for ₽{total_cost:,}. "
            f"Remaining: ₽{trainer.money:,}"
        )

    def sell(
        self,
        trainer: "Trainer",
        item_name: str,
        count: int = 1,
    ) -> tuple[bool, str]:
        """
        Sell items at half price.
        Returns (success: bool, message: str).
        """
        item_data = ITEMS.get(item_name)
        if not item_data:
            return False, f"Unknown item: {item_name}"
        if item_data.price == 0:
            return False, f"{item_name} cannot be sold."
        if not trainer.bag.has_item(item_name, count):
            return False, f"You don't have {count}× {item_name} in your bag."
        sell_price = item_data.price // 2 * count
        trainer.bag.remove_item(item_name, count)
        trainer.money += sell_price
        return True, (
            f"Sold {count}× {item_name} for ₽{sell_price:,}. "
            f"Total money: ₽{trainer.money:,}"
        )

    def __repr__(self) -> str:
        return f"<PokéMart {self.city}>"
