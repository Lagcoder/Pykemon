"""
Friendship and Affection system.

Friendship (0-255):
  - Affects certain evolutions (e.g. Eevee -> Espeon/Umbreon, Chansey -> Blissey)
  - Some moves become more powerful with high friendship (Return)
  - Low friendship powers up moves like Frustration

Affection (0-255, Pokemon-Amie/Refresh mechanic):
  - Boosts EXP gain (already handled in Pokemon.gain_exp)
  - Occasional blocking of status effects / KO prevention
  - In-battle messages at high affection
"""

from __future__ import annotations
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.pokemon import Pokemon


# ── Friendship changes ────────────────────────────────────────────────────────

FRIENDSHIP_EVENTS = {
    "level_up":         4,
    "level_up_luxury":  9,   # Luxury Ball bonus
    "battle_win":       1,
    "medicine":         1,
    "poffin":           5,
    "grooming":        10,
    "fainted":         -1,
    "bitter_medicine": -5,
    "rare_candy":       3,
    "walk":             1,
}


def update_friendship(
    pokemon: "Pokemon",
    event: str,
) -> int:
    """
    Update a Pokémon's friendship based on an event.
    Returns the new friendship value.
    """
    base_delta = FRIENDSHIP_EVENTS.get(event, 0)
    if base_delta == 0:
        return pokemon.friendship

    # Luxury Ball gives extra friendship
    if event in ("level_up",) and pokemon.caught_in == "Luxury Ball":
        base_delta = FRIENDSHIP_EVENTS["level_up_luxury"]

    # Soothe Bell doubles positive friendship gains
    if base_delta > 0 and pokemon.held_item == "Soothe Bell":
        base_delta = base_delta * 2

    pokemon.friendship = max(0, min(255, pokemon.friendship + base_delta))
    return pokemon.friendship


def friendship_tier(pokemon: "Pokemon") -> str:
    """Describe the friendship level in human terms."""
    f = pokemon.friendship
    if f >= 250:
        return "overflowing — it absolutely adores you!"
    elif f >= 200:
        return "very high — it loves you dearly."
    elif f >= 150:
        return "high — it trusts you greatly."
    elif f >= 100:
        return "moderate — it likes you."
    elif f >= 50:
        return "low — it's still getting used to you."
    else:
        return "very low — it doesn't trust you yet."


# ── Affection changes ─────────────────────────────────────────────────────────

def update_affection(
    pokemon: "Pokemon",
    delta: int,
) -> int:
    """
    Update a Pokémon's affection (Pokémon-Amie style).
    Returns the new affection value.
    """
    pokemon.affection = max(0, min(255, pokemon.affection + delta))
    return pokemon.affection


# ── Return / Frustration power ────────────────────────────────────────────────

def return_power(pokemon: "Pokemon") -> int:
    """Power of the Return move (max 102 at 255 friendship)."""
    return max(1, pokemon.friendship * 2 // 5)


def frustration_power(pokemon: "Pokemon") -> int:
    """Power of the Frustration move (max 102 at 0 friendship)."""
    return max(1, (255 - pokemon.friendship) * 2 // 5)


# ── In-battle affection effects ───────────────────────────────────────────────

def affection_endure(pokemon: "Pokemon") -> bool:
    """
    High affection (160+) gives a chance to endure a KO hit with 1 HP.
    Returns True if the effect triggers.
    """
    if pokemon.affection >= 160 and pokemon.current_hp > 0:
        threshold = (pokemon.affection - 160) / 95  # up to 100% at 255
        return random.random() < threshold * 0.15   # up to ~15% chance
    return False


def affection_status_block(pokemon: "Pokemon") -> bool:
    """
    High affection (120+) gives a chance to shake off status conditions.
    Returns True if the block triggers.
    """
    if pokemon.affection >= 120:
        return random.random() < 0.1
    return False


def affection_battle_messages(pokemon: "Pokemon") -> list[str]:
    """
    Return in-battle affection messages based on current affection level.
    These are purely flavour messages.
    """
    msgs: list[str] = []
    if pokemon.affection >= 255:
        msgs.append(f"{pokemon.nickname} is giving its all for you!")
    elif pokemon.affection >= 200:
        msgs.append(f"{pokemon.nickname} is trying its hardest for you!")
    elif pokemon.affection >= 150:
        msgs.append(f"{pokemon.nickname} is looking at you with trust.")
    return msgs
