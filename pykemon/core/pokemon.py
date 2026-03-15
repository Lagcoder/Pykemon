"""
Core Pokémon class representing an individual Pokémon instance.
"""

from __future__ import annotations
import random
from typing import Optional
from ..data.types import PokemonType
from ..data.pokemon_data import SpeciesData, SPECIES
from ..data.moves import MoveData, MOVES, StatusEffect


class Move:
    """An individual move slot in a Pokémon's moveset."""

    def __init__(self, move_data: MoveData):
        self.data = move_data
        self.pp_max = move_data.pp
        self.pp = move_data.pp

    def use(self) -> bool:
        """Use one PP. Returns True if successful."""
        if self.pp <= 0:
            return False
        self.pp -= 1
        return True

    def restore_pp(self, amount: int = -1) -> None:
        """Restore PP. amount=-1 restores to max."""
        if amount < 0:
            self.pp = self.pp_max
        else:
            self.pp = min(self.pp_max, self.pp + amount)

    def __repr__(self) -> str:
        return f"<Move {self.data.name} {self.pp}/{self.pp_max}>"


class Pokemon:
    """
    A fully instantiated Pokémon with individual stats, moves,
    status conditions, friendship, held item, etc.
    """

    STAT_STAGE_MULTIPLIERS = {
        -6: 2/8, -5: 2/7, -4: 2/6, -3: 2/5, -2: 2/4, -1: 2/3,
         0: 1.0,
         1: 3/2,  2: 4/2,  3: 5/2,  4: 6/2,  5: 7/2,  6: 8/2,
    }
    ACC_EVA_STAGE_MULTIPLIERS = {
        -6: 3/9, -5: 3/8, -4: 3/7, -3: 3/6, -2: 3/5, -1: 3/4,
         0: 1.0,
         1: 4/3,  2: 5/3,  3: 6/3,  4: 7/3,  5: 8/3,  6: 9/3,
    }

    def __init__(
        self,
        species: SpeciesData,
        level: int,
        nickname: Optional[str] = None,
        is_shiny: bool = False,
        is_wild: bool = False,
        trainer_name: str = "Wild",
        ivs: Optional[dict] = None,
        evs: Optional[dict] = None,
    ):
        self.species = species
        self.level = level
        self.nickname = nickname or species.name
        self.is_shiny = is_shiny
        self.trainer_name = trainer_name
        self.is_wild = is_wild
        self.experience = self._level_to_exp(level)
        self.friendship = species.base_friendship
        self.affection = 0         # 0-255
        self.held_item: Optional[str] = None

        # IVs (0-31 each) and EVs (0-255 each, max 510 total)
        self.ivs = ivs or {stat: random.randint(0, 31) for stat in ["hp","atk","def","spa","spd","spe"]}
        self.evs = evs or {stat: 0 for stat in ["hp","atk","def","spa","spd","spe"]}

        # Determine gender
        if species.gender_ratio < 0:
            self.gender = None
        elif random.random() < species.gender_ratio:
            self.gender = "F"
        else:
            self.gender = "M"

        # Calculate stats
        self._calc_stats()
        self.current_hp = self.max_hp

        # Status conditions
        self.status: Optional[StatusEffect] = None
        self.status_turns = 0        # turns remaining (sleep etc.)
        self.toxic_counter = 0       # for TOX damage

        # Volatile status (resets between battles)
        self.confused = False
        self.confusion_turns = 0
        self.flinched = False
        self.fainted = False
        self.is_charging = False     # charging a two-turn move
        self.charging_move: Optional[Move] = None
        self.is_underground = False  # for Dig
        self.is_airborne = False     # for Fly/Bounce
        self.substitute_hp = 0
        self.locked_move: Optional[Move] = None  # choice item lock or outrage etc.
        self.choice_locked = False
        self.protect_active = False
        self.last_move_used: Optional[Move] = None

        # In-battle stat stages (-6 to +6)
        self.stat_stages: dict[str, int] = {
            "atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0,
            "acc": 0, "eva": 0,
        }

        # Build moveset (up to 4 moves from learnset)
        self.moves: list[Move] = self._build_moveset()

        # Pokédex flags
        self.caught_in: Optional[str] = None    # ball type
        self.original_trainer = trainer_name

    # ── Stats ────────────────────────────────────────────────────────────────

    def _calc_stats(self) -> None:
        sp = self.species
        lvl = self.level
        iv = self.ivs
        ev = self.evs

        def calc(base: int, iv_val: int, ev_val: int, is_hp: bool = False) -> int:
            if is_hp:
                return int(((2 * base + iv_val + ev_val // 4) * lvl) / 100) + lvl + 10
            else:
                return int((int(((2 * base + iv_val + ev_val // 4) * lvl) / 100) + 5))

        self.max_hp = calc(sp.base_hp, iv["hp"], ev["hp"], is_hp=True)
        self.base_atk = calc(sp.base_atk, iv["atk"], ev["atk"])
        self.base_def = calc(sp.base_def, iv["def"], ev["def"])
        self.base_spa = calc(sp.base_spa, iv["spa"], ev["spa"])
        self.base_spd = calc(sp.base_spd, iv["spd"], ev["spd"])
        self.base_spe = calc(sp.base_spe, iv["spe"], ev["spe"])

    def get_stat(self, stat: str) -> int:
        """Get battle-effective stat considering stages and held items."""
        base = {
            "atk": self.base_atk, "def": self.base_def,
            "spa": self.base_spa, "spd": self.base_spd, "spe": self.base_spe,
        }[stat]
        stage = self.stat_stages.get(stat, 0)
        mult = self.STAT_STAGE_MULTIPLIERS[max(-6, min(6, stage))]
        val = int(base * mult)
        # Held item boost
        if self.held_item:
            from ..data.items import ITEMS
            item_data = ITEMS.get(self.held_item)
            if item_data:
                if item_data.held_choice_band and stat == "atk":
                    val = int(val * 1.5)
                if item_data.held_choice_specs and stat == "spa":
                    val = int(val * 1.5)
                if item_data.held_choice_scarf and stat == "spe":
                    val = int(val * 1.5)
        # Paralysis halves speed
        if self.status == StatusEffect.PARALYSIS and stat == "spe":
            val = val // 2
        # Burn halves attack
        if self.status == StatusEffect.BURN and stat == "atk":
            val = val // 2
        return max(1, val)

    def get_accuracy_multiplier(self) -> float:
        stage = self.stat_stages.get("acc", 0)
        return self.ACC_EVA_STAGE_MULTIPLIERS[max(-6, min(6, stage))]

    def get_evasion_multiplier(self) -> float:
        stage = self.stat_stages.get("eva", 0)
        return self.ACC_EVA_STAGE_MULTIPLIERS[max(-6, min(6, stage))]

    # ── Learnset ──────────────────────────────────────────────────────────────

    def _build_moveset(self) -> list[Move]:
        """Build up to 4 moves from the learnset at or below current level."""
        learnable = [
            move_name for (lvl, move_name) in self.species.learnset
            if lvl <= self.level and move_name in MOVES
        ]
        # Take the last 4 unique moves
        seen: list[str] = []
        for m in learnable:
            if m not in seen:
                seen.append(m)
        slots = seen[-4:] if len(seen) >= 4 else seen
        return [Move(MOVES[m]) for m in slots]

    def can_learn_move(self) -> list[str]:
        """Return a list of moves learnable at exactly the current level."""
        return [
            move_name for (lvl, move_name) in self.species.learnset
            if lvl == self.level and move_name in MOVES
        ]

    def learn_move(self, move_name: str, slot: int = -1) -> None:
        """
        Add a move to the moveset.
        slot = -1 means replace the oldest move if full.
        """
        if move_name not in MOVES:
            raise ValueError(f"Unknown move: {move_name}")
        move_obj = Move(MOVES[move_name])
        if len(self.moves) < 4:
            self.moves.append(move_obj)
        elif 0 <= slot < 4:
            self.moves[slot] = move_obj
        else:
            self.moves.pop(0)
            self.moves.append(move_obj)

    # ── Experience & Leveling ─────────────────────────────────────────────────

    def _level_to_exp(self, level: int) -> int:
        gr = self.species.growth_rate
        n = level
        if gr == "fast":
            return int(4 * n ** 3 / 5)
        elif gr == "medium_fast":
            return n ** 3
        elif gr == "medium_slow":
            return max(0, int(6 / 5 * n ** 3 - 15 * n ** 2 + 100 * n - 140))
        elif gr == "slow":
            return int(5 * n ** 3 / 4)
        elif gr == "erratic":
            if n <= 50:
                return int(n ** 3 * (100 - n) / 50)
            elif n <= 68:
                return int(n ** 3 * (150 - n) / 100)
            elif n <= 98:
                return int(n ** 3 * ((1911 - 10 * n) / 3) / 500)
            else:
                return int(n ** 3 * (160 - n) / 100)
        elif gr == "fluctuating":
            if n <= 15:
                return int(n ** 3 * ((n + 1) / 3 + 24) / 50)
            elif n <= 35:
                return int(n ** 3 * (n + 14) / 50)
            else:
                return int(n ** 3 * (n / 2 + 32) / 50)
        return n ** 3

    def exp_needed_for_next_level(self) -> int:
        if self.level >= 100:
            return 0
        return self._level_to_exp(self.level + 1) - self.experience

    def gain_exp(self, amount: int) -> list[str]:
        """Grant experience. Returns list of event messages (level ups, etc.)."""
        if self.level >= 100:
            return []
        messages = []
        # Affection / friendship bonus
        if self.affection >= 255:
            amount = int(amount * 1.2)
        self.experience += amount
        messages.append(f"{self.nickname} gained {amount} EXP.")
        while self.level < 100 and self.experience >= self._level_to_exp(self.level + 1):
            self.level += 1
            old_max = self.max_hp
            self._calc_stats()
            self.current_hp += (self.max_hp - old_max)
            self.current_hp = min(self.current_hp, self.max_hp)
            messages.append(f"{self.nickname} grew to level {self.level}!")
            # Learn moves
            for move_name in self.can_learn_move():
                if len(self.moves) < 4:
                    self.learn_move(move_name)
                    messages.append(f"{self.nickname} learned {move_name}!")
                else:
                    messages.append(
                        f"{self.nickname} wants to learn {move_name}! But it already knows 4 moves."
                    )
        return messages

    # ── HP / Status ───────────────────────────────────────────────────────────

    def take_damage(self, amount: int) -> int:
        """Apply damage. Returns actual damage dealt."""
        amount = max(1, amount)
        if self.substitute_hp > 0:
            self.substitute_hp -= amount
            if self.substitute_hp <= 0:
                self.substitute_hp = 0
            return amount
        actual = min(self.current_hp, amount)
        self.current_hp -= actual
        if self.current_hp <= 0:
            self.current_hp = 0
            self.fainted = True
        return actual

    def heal(self, amount: int) -> int:
        """Restore HP. Returns actual HP restored."""
        if self.fainted:
            return 0
        before = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - before

    def full_heal(self) -> None:
        """Fully restore HP and cure all status."""
        self.current_hp = self.max_hp
        self.fainted = False
        self.cure_status()

    def revive(self, full: bool = False) -> None:
        """Revive a fainted Pokémon."""
        if not self.fainted:
            return
        self.fainted = False
        self.current_hp = self.max_hp if full else self.max_hp // 2
        self.cure_status()

    def cure_status(self, *effects: str) -> None:
        """
        Cure status conditions.
        If effects is provided, only cure those specific ones;
        otherwise cure all.
        """
        if not effects or (self.status and self.status.name in effects):
            self.status = None
            self.status_turns = 0
            self.toxic_counter = 0
        if not effects or "CONFUSION" in effects:
            self.confused = False
            self.confusion_turns = 0

    def apply_status(self, effect: StatusEffect) -> bool:
        """
        Attempt to apply a status condition.
        Returns True if successful.
        """
        if self.status is not None:
            return False  # already has a primary status
        # Type immunities
        if effect == StatusEffect.BURN and PokemonType.FIRE in self.species.types:
            return False
        if effect == StatusEffect.FREEZE and PokemonType.ICE in self.species.types:
            return False
        if effect in (StatusEffect.POISON, StatusEffect.BADLY_POISONED) and (
            PokemonType.POISON in self.species.types or PokemonType.STEEL in self.species.types
            if hasattr(PokemonType, 'STEEL') else PokemonType.POISON in self.species.types
        ):
            return False
        if effect == StatusEffect.PARALYSIS and PokemonType.ELECTRIC in self.species.types:
            return False
        self.status = effect
        if effect == StatusEffect.SLEEP:
            self.status_turns = random.randint(1, 3)
        return True

    def apply_end_of_turn_status(self) -> list[str]:
        """Process end-of-turn status damage. Returns event messages."""
        messages = []
        if self.fainted:
            return messages
        if self.status == StatusEffect.BURN:
            dmg = max(1, self.max_hp // 16)
            self.take_damage(dmg)
            messages.append(f"{self.nickname} is hurt by its burn! (-{dmg} HP)")
        elif self.status == StatusEffect.POISON:
            dmg = max(1, self.max_hp // 8)
            self.take_damage(dmg)
            messages.append(f"{self.nickname} is hurt by poison! (-{dmg} HP)")
        elif self.status == StatusEffect.BADLY_POISONED:
            self.toxic_counter += 1
            dmg = max(1, (self.max_hp * self.toxic_counter) // 16)
            self.take_damage(dmg)
            messages.append(f"{self.nickname} is badly poisoned! (-{dmg} HP)")
        elif self.status == StatusEffect.SLEEP:
            if self.status_turns > 0:
                self.status_turns -= 1
                messages.append(f"{self.nickname} is fast asleep.")
            if self.status_turns <= 0:
                self.cure_status("SLEEP")
                messages.append(f"{self.nickname} woke up!")
        # Leftovers
        if self.held_item == "Leftovers":
            restore = max(1, self.max_hp // 16)
            self.heal(restore)
            messages.append(f"{self.nickname} restored a little HP using Leftovers.")
        return messages

    # ── Battle resets ─────────────────────────────────────────────────────────

    def reset_volatile_status(self) -> None:
        """Reset volatile battle conditions (called when Pokémon is switched out)."""
        self.confused = False
        self.confusion_turns = 0
        self.flinched = False
        self.is_charging = False
        self.charging_move = None
        self.is_underground = False
        self.is_airborne = False
        self.substitute_hp = 0
        self.locked_move = None
        self.choice_locked = False
        self.protect_active = False
        self.stat_stages = {k: 0 for k in self.stat_stages}

    def reset_stages(self) -> None:
        """Reset all stat stages to 0."""
        self.stat_stages = {k: 0 for k in self.stat_stages}

    def change_stage(self, stat: str, delta: int) -> tuple[bool, str]:
        """
        Attempt to change a stat stage.
        Returns (changed: bool, message: str).
        """
        current = self.stat_stages.get(stat, 0)
        if delta > 0 and current >= 6:
            return False, f"{self.nickname}'s {stat} won't go any higher!"
        if delta < 0 and current <= -6:
            return False, f"{self.nickname}'s {stat} won't go any lower!"
        new = max(-6, min(6, current + delta))
        self.stat_stages[stat] = new
        if abs(delta) >= 3:
            adverb = "drastically" if delta > 0 else "severely"
        elif abs(delta) == 2:
            adverb = "sharply" if delta > 0 else "harshly"
        else:
            adverb = "rose" if delta > 0 else "fell"
        direction = "rose" if delta > 0 else "fell"
        if abs(delta) >= 2:
            return True, f"{self.nickname}'s {stat} {adverb} {direction}!"
        return True, f"{self.nickname}'s {stat} {direction}!"

    # ── Display ───────────────────────────────────────────────────────────────

    @property
    def hp_bar(self) -> str:
        filled = int(self.current_hp / self.max_hp * 20)
        bar = "█" * filled + "░" * (20 - filled)
        pct = self.current_hp / self.max_hp
        color = "low" if pct < 0.25 else ("mid" if pct < 0.5 else "ok")
        return f"[{bar}] {self.current_hp}/{self.max_hp}"

    @property
    def status_str(self) -> str:
        if self.status:
            return f"[{self.status.value}]"
        return ""

    @property
    def shiny_str(self) -> str:
        return " ✨" if self.is_shiny else ""

    def __repr__(self) -> str:
        shiny = "✨ " if self.is_shiny else ""
        gender = f" ({self.gender})" if self.gender else ""
        return (
            f"{shiny}{self.nickname}{gender} "
            f"Lv.{self.level} "
            f"{self.hp_bar} {self.status_str}"
        )

    def summary(self) -> str:
        types_str = "/".join(t.value for t in self.species.types)
        moves_str = ", ".join(f"{m.data.name}({m.pp}/{m.pp_max})" for m in self.moves)
        held = f" @ {self.held_item}" if self.held_item else ""
        shiny = " [SHINY]" if self.is_shiny else ""
        gender = f" ({self.gender})" if self.gender else ""
        return (
            f"{'='*50}\n"
            f"{self.nickname}{gender}{shiny}{held} | #{self.species.number} {self.species.name}\n"
            f"Type: {types_str} | Lv.{self.level}\n"
            f"HP: {self.current_hp}/{self.max_hp}  "
            f"ATK:{self.base_atk} DEF:{self.base_def} "
            f"SpA:{self.base_spa} SpD:{self.base_spd} Spe:{self.base_spe}\n"
            f"Friendship: {self.friendship}  Affection: {self.affection}\n"
            f"Moves: {moves_str}\n"
            f"{'='*50}"
        )


def create_pokemon(
    species_name: str,
    level: int,
    *,
    nickname: Optional[str] = None,
    is_shiny: bool = False,
    is_wild: bool = False,
    trainer_name: str = "Wild",
    held_item: Optional[str] = None,
    forced_moves: Optional[list[str]] = None,
) -> Pokemon:
    """Helper factory for creating a Pokémon instance."""
    if species_name not in SPECIES:
        raise ValueError(f"Unknown species: {species_name}")
    sp = SPECIES[species_name]
    # Shiny chance: 1/4096 for wild
    if is_wild and not is_shiny:
        is_shiny = random.randint(1, 4096) == 1
    mon = Pokemon(sp, level, nickname=nickname, is_shiny=is_shiny,
                  is_wild=is_wild, trainer_name=trainer_name)
    if held_item:
        mon.held_item = held_item
    if forced_moves:
        mon.moves = []
        for move_name in forced_moves[:4]:
            if move_name in MOVES:
                mon.moves.append(Move(MOVES[move_name]))
    return mon
