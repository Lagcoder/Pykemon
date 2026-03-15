"""
Gym system — manages Gym Leaders, badges, and the Gym challenge flow.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..core.trainer import Trainer

from ..core.trainer import GYMS, GymData, build_gym_leader, build_elite_four_member, ELITE_FOUR


class GymChallenge:
    """
    Represents a single Gym challenge attempt.
    """

    def __init__(self, gym: GymData):
        self.gym = gym
        self.leader = build_gym_leader(gym)

    def can_challenge(self, trainer: "Trainer") -> bool:
        """Return True if the player has enough badges to challenge this gym."""
        return len(trainer.badges) >= self.gym.required_badges

    def challenge_refused_message(self) -> str:
        return (
            f"Gym Leader {self.gym.leader_name}: "
            f"Come back when you have {self.gym.required_badges} badge(s)."
        )

    def award_badge(self, trainer: "Trainer") -> list[str]:
        """Award the badge to the player and return messages."""
        badge = self.gym.badge_name
        msgs = []
        if trainer.has_badge(badge):
            msgs.append(f"You already have the {badge}.")
        else:
            trainer.award_badge(badge)
            msgs.append(f"{self.gym.leader_name}: You've proven your worth! Take the {badge}!")
            msgs.append(f"You received the {badge}!")
            # Badge stat boosts (Gen I style)
            msgs.extend(self._badge_effects(badge, trainer))
        return msgs

    def _badge_effects(self, badge: str, trainer: "Trainer") -> list[str]:
        """Return flavour messages for badge effects (stat boosts for owned Pokémon)."""
        effects = {
            "Boulder Badge": "Pokémon up to level 20 will obey you.",
            "Cascade Badge": "Pokémon up to level 30 will obey you.",
            "Thunder Badge": "Pokémon up to level 40 will obey you.",
            "Rainbow Badge": "Pokémon up to level 50 will obey you.",
            "Soul Badge":    "Pokémon up to level 60 will obey you.",
            "Marsh Badge":   "Pokémon up to level 70 will obey you.",
            "Volcano Badge": "Pokémon up to level 80 will obey you.",
            "Earth Badge":   "All Pokémon will obey you.",
        }
        msg = effects.get(badge, "")
        return [msg] if msg else []


class PokemonLeague:
    """
    Manages the Elite Four and Champion challenge.
    """

    def __init__(self):
        self.members = [build_elite_four_member(m) for m in ELITE_FOUR]
        self.current_member_idx = 0

    def can_challenge(self, trainer: "Trainer") -> bool:
        """Player must have all 8 badges."""
        return len(trainer.badges) >= 8

    def next_opponent(self):
        """Return the next Elite Four member (or Champion)."""
        if self.current_member_idx < len(self.members):
            return self.members[self.current_member_idx]
        return None

    def advance(self) -> bool:
        """Move to the next member. Returns True if there are more."""
        self.current_member_idx += 1
        return self.current_member_idx < len(self.members)

    def is_complete(self) -> bool:
        return self.current_member_idx >= len(self.members)

    def reset(self) -> None:
        """Reset to the beginning of the Elite Four."""
        self.current_member_idx = 0
        # Re-build all parties at full health
        self.members = [build_elite_four_member(m) for m in ELITE_FOUR]

    @property
    def champion(self):
        """Return the Champion (last member)."""
        return self.members[-1] if self.members else None

    def victory_message(self) -> str:
        return (
            "Congratulations! You have defeated the Pokémon League Champion!\n"
            "You are entered into the Hall of Fame!\n"
            "Your name will be remembered forever!"
        )


class GymBadgeSystem:
    """
    Tracks all gym challenges and the player's badge progress.
    """

    def __init__(self):
        self.challenges = [GymChallenge(gym) for gym in GYMS]
        self.league = PokemonLeague()

    def get_gym(self, number: int) -> Optional[GymChallenge]:
        """Get a gym by its 1-indexed number."""
        if 1 <= number <= len(self.challenges):
            return self.challenges[number - 1]
        return None

    def next_gym(self, trainer: "Trainer") -> Optional[GymChallenge]:
        """Return the next gym the player hasn't defeated yet."""
        for ch in self.challenges:
            if ch.gym.badge_name not in trainer.badges:
                return ch
        return None

    def all_badges_summary(self, trainer: "Trainer") -> str:
        lines = ["=== BADGES ==="]
        for gym in GYMS:
            has = "✓" if gym.badge_name in trainer.badges else "✗"
            lines.append(f"  [{has}] {gym.badge_name:<18} — {gym.leader_name} ({gym.city})")
        return "\n".join(lines)

    def display_gyms(self) -> str:
        lines = ["=== GYM ROSTER ==="]
        for gym in GYMS:
            lines.append(
                f"  Gym {gym.number}: {gym.city:<20} "
                f"Leader: {gym.leader_name:<12} "
                f"Type: {gym.specialty_type}"
            )
        return "\n".join(lines)
