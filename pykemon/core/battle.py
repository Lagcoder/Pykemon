"""
Turn-based battle engine with support for:
- Single and Double battles
- Weather effects
- Status conditions
- Stat stages
- Type effectiveness
- Catching mechanics
- Held items
- Complex move effects
"""

from __future__ import annotations
import random
from typing import Optional, TYPE_CHECKING

from ..data.types import PokemonType, get_effectiveness, effectiveness_text
from ..data.moves import MoveData, MoveCategory, StatusEffect, WeatherEffect, MoveEffect
from ..data.items import ITEMS, ItemData

if TYPE_CHECKING:
    from .pokemon import Pokemon, Move
    from .trainer import Trainer


class BattleResult:
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"
    RUN = "run"
    CATCH = "catch"
    CATCH_FAIL = "catch_fail"


class Battle:
    """
    Manages a single or double Pokémon battle.
    """

    def __init__(
        self,
        player_trainer: "Trainer",
        opponent: "Trainer",
        is_wild: bool = False,
        is_double: bool = False,
        weather: WeatherEffect = WeatherEffect.NONE,
        weather_turns: int = 0,
    ):
        self.player = player_trainer
        self.opponent = opponent
        self.is_wild = is_wild
        self.is_double = is_double
        self.weather = weather
        self.weather_turns = weather_turns
        self.turn = 0
        self.messages: list[str] = []
        self.result: Optional[str] = None

        # Active Pokémon indices
        self.player_active_idx = 0
        self.opponent_active_idx = 0
        # For doubles, we have a second slot
        self.player_active_idx2: Optional[int] = None
        self.opponent_active_idx2: Optional[int] = None

        if is_double:
            self._init_double()

    def _init_double(self) -> None:
        """Set up double battle second slots."""
        for i, mon in enumerate(self.player.party[1:], start=1):
            if not mon.fainted:
                self.player_active_idx2 = i
                break
        for i, mon in enumerate(self.opponent.party[1:], start=1):
            if not mon.fainted:
                self.opponent_active_idx2 = i
                break

    @property
    def player_pokemon(self) -> "Pokemon":
        return self.player.party[self.player_active_idx]

    @property
    def opponent_pokemon(self) -> "Pokemon":
        return self.opponent.party[self.opponent_active_idx]

    def log(self, *msgs: str) -> None:
        for msg in msgs:
            self.messages.append(msg)

    def get_log(self) -> list[str]:
        msgs = self.messages[:]
        self.messages.clear()
        return msgs

    # ── Move order ────────────────────────────────────────────────────────────

    def _move_first(
        self,
        mon1: "Pokemon",
        move1: "Move",
        mon2: "Pokemon",
        move2: Optional["Move"],
    ) -> bool:
        """Return True if mon1 goes first."""
        p1 = move1.data.effect.priority
        p2 = move2.data.effect.priority if move2 else 0
        if p1 != p2:
            return p1 > p2
        return mon1.get_stat("spe") >= mon2.get_stat("spe")

    # ── Weather ───────────────────────────────────────────────────────────────

    def apply_weather(self, new_weather: WeatherEffect) -> None:
        self.weather = new_weather
        self.weather_turns = 5
        msgs = {
            WeatherEffect.SUNNY: "The sunlight turned harsh!",
            WeatherEffect.RAIN: "It started to rain!",
            WeatherEffect.SANDSTORM: "A sandstorm kicked up!",
            WeatherEffect.HAIL: "It started to hail!",
        }
        self.log(msgs.get(new_weather, ""))

    def _process_weather_damage(self) -> None:
        """End-of-turn weather damage / heal."""
        if self.weather == WeatherEffect.SANDSTORM:
            for mon in [self.player_pokemon, self.opponent_pokemon]:
                if not mon.fainted:
                    immune_types = {PokemonType.ROCK, PokemonType.GROUND, PokemonType.STEEL}
                    if not any(t in mon.species.types for t in immune_types):
                        dmg = max(1, mon.max_hp // 16)
                        mon.take_damage(dmg)
                        self.log(f"{mon.nickname} is buffeted by the sandstorm! (-{dmg} HP)")
        elif self.weather == WeatherEffect.HAIL:
            for mon in [self.player_pokemon, self.opponent_pokemon]:
                if not mon.fainted and PokemonType.ICE not in mon.species.types:
                    dmg = max(1, mon.max_hp // 16)
                    mon.take_damage(dmg)
                    self.log(f"{mon.nickname} is buffeted by the hail! (-{dmg} HP)")

    def _tick_weather(self) -> None:
        if self.weather != WeatherEffect.NONE:
            if self.weather_turns > 0:
                self.weather_turns -= 1
            if self.weather_turns <= 0:
                self.log(f"The {self.weather.value} weather subsided.")
                self.weather = WeatherEffect.NONE

    # ── Accuracy ─────────────────────────────────────────────────────────────

    def _hits(self, attacker: "Pokemon", defender: "Pokemon", move: MoveData) -> bool:
        """Determine if a move hits."""
        if move.accuracy > 100:
            return True  # Always hits
        # Underground / airborne evasion
        if defender.is_underground and move.name not in ("Earthquake", "Magnitude", "Fissure"):
            return False
        if defender.is_airborne and move.name not in ("Thunder", "Hurricane", "Gust"):
            return False
        acc = move.accuracy / 100
        acc_stage = attacker.get_accuracy_multiplier()
        eva_stage = defender.get_evasion_multiplier()
        chance = acc * acc_stage / eva_stage
        return random.random() < chance

    # ── Damage calculation ────────────────────────────────────────────────────

    def _calc_damage(
        self,
        attacker: "Pokemon",
        defender: "Pokemon",
        move: MoveData,
    ) -> tuple[int, float, bool]:
        """
        Calculate damage dealt.
        Returns (damage, effectiveness_multiplier, is_critical).
        """
        if move.power == 0:
            return 0, 1.0, False

        # Critical hit
        crit_stage = 1 if move.effect.crits_always else 0
        if attacker.held_item == "Scope Lens":
            crit_stage += 1
        crit_thresholds = [1, 8, 2, 24]
        threshold = crit_thresholds[min(crit_stage, 3)]
        is_crit = random.randint(1, 24) <= threshold

        # Attack / Defense stats
        if move.category == MoveCategory.PHYSICAL:
            atk = attacker.get_stat("atk") if not is_crit else max(attacker.get_stat("atk"), attacker.base_atk)
            def_ = defender.get_stat("def") if not is_crit else min(defender.get_stat("def"), defender.base_def)
        else:
            atk = attacker.get_stat("spa") if not is_crit else max(attacker.get_stat("spa"), attacker.base_spa)
            def_ = defender.get_stat("spd") if not is_crit else min(defender.get_stat("spd"), defender.base_spd)

        # Base damage formula
        damage = int((((2 * attacker.level / 5 + 2) * move.power * atk) / def_) / 50 + 2)

        # STAB
        if move.move_type in attacker.species.types:
            damage = int(damage * 1.5)

        # Type effectiveness
        eff = get_effectiveness(move.move_type, defender.species.types)
        damage = int(damage * eff)

        # Weather bonuses
        if self.weather == WeatherEffect.SUNNY:
            if move.move_type == PokemonType.FIRE:
                damage = int(damage * 1.5)
            elif move.move_type == PokemonType.WATER:
                damage = int(damage * 0.5)
        elif self.weather == WeatherEffect.RAIN:
            if move.move_type == PokemonType.WATER:
                damage = int(damage * 1.5)
            elif move.move_type == PokemonType.FIRE:
                damage = int(damage * 0.5)

        # Critical hit multiplier
        if is_crit:
            damage = int(damage * 1.5)

        # Random factor (85-100%)
        damage = int(damage * random.randint(85, 100) / 100)

        # Held item type boosts
        if attacker.held_item:
            item_data = ITEMS.get(attacker.held_item)
            if item_data and item_data.held_boost_type == move.move_type.name:
                damage = int(damage * item_data.held_boost_factor)

        # Life Orb boost + recoil handled separately
        if attacker.held_item == "Life Orb":
            damage = int(damage * 1.3)

        return max(1, damage), eff, is_crit

    # ── Use a move ────────────────────────────────────────────────────────────

    def _apply_move(
        self,
        attacker: "Pokemon",
        move_obj: "Move",
        defender: "Pokemon",
        target_self: bool = False,
    ) -> None:
        """Execute a single move from attacker against defender."""
        move = move_obj.data
        effect = move.effect

        # Check PP
        if not move_obj.use():
            self.log(f"{attacker.nickname} has no PP left for {move.name}!")
            return

        attacker.last_move_used = move_obj

        # Set weather
        if effect.sets_weather:
            self.apply_weather(effect.sets_weather)

        # Status-only moves
        if move.category == MoveCategory.STATUS and move.power == 0:
            if move.accuracy <= 100 and not self._hits(attacker, defender, move):
                self.log(f"{attacker.nickname} used {move.name}... but it missed!")
                return

            # Stat changes on target
            if effect.stat_changes and not effect.target_self:
                if random.random() < effect.stat_change_chance:
                    for stat, delta in effect.stat_changes.items():
                        changed, msg = defender.change_stage(stat, delta)
                        self.log(msg)

            # Stat changes on self
            if effect.stat_changes and effect.target_self:
                for stat, delta in effect.stat_changes.items():
                    changed, msg = attacker.change_stage(stat, delta)
                    self.log(msg)

            # Apply status
            if effect.status and effect.target_self:
                if random.random() < effect.status_chance:
                    attacker.apply_status(effect.status)

            elif effect.status and not effect.target_self:
                if random.random() < effect.status_chance:
                    if defender.apply_status(effect.status):
                        self.log(f"{defender.nickname} was {effect.status.value}!")
                    else:
                        self.log(f"It didn't affect {defender.nickname}...")

            # Heal self (negative heals_user means self-heal)
            if effect.heals_user < 0:
                restore = int(attacker.max_hp * abs(effect.heals_user))
                restored = attacker.heal(restore)
                self.log(f"{attacker.nickname} restored {restored} HP!")

            return

        # Charging move (first turn)
        if effect.charges_turn and not attacker.is_charging:
            attacker.is_charging = True
            attacker.charging_move = move_obj
            if move.name == "Solar Beam" and self.weather == WeatherEffect.SUNNY:
                pass  # Skip charging in sun
            else:
                self.log(f"{attacker.nickname} is charging up {move.name}!")
                return

        if attacker.is_charging:
            attacker.is_charging = False
            attacker.charging_move = None

        # Accuracy check
        if not self._hits(attacker, defender, move):
            self.log(f"{attacker.nickname} used {move.name}... but it missed!")
            return

        # Multi-hit
        if effect.hits_twice:
            n_hits = random.choice([2, 2, 3, 3, 4, 5])
        else:
            n_hits = 1

        total_damage = 0
        for hit_num in range(n_hits):
            if defender.fainted:
                break
            damage, eff, is_crit = self._calc_damage(attacker, defender, move)
            if eff == 0.0:
                self.log(f"It had no effect on {defender.nickname}...")
                return

            actual = defender.take_damage(damage)
            total_damage += actual
            self.log(f"{attacker.nickname} used {move.name}!")
            eff_text = effectiveness_text(eff)
            if eff_text:
                self.log(eff_text)
            if is_crit:
                self.log("A critical hit!")
            self.log(f"{defender.nickname}: {defender.hp_bar}")

            if n_hits > 1 and hit_num == n_hits - 1:
                self.log(f"Hit {n_hits} time(s)!")

        # Recoil
        if effect.recoil > 0:
            recoil_dmg = max(1, int(total_damage * effect.recoil))
            attacker.take_damage(recoil_dmg)
            self.log(f"{attacker.nickname} was hurt by recoil! (-{recoil_dmg} HP)")

        # Life Orb recoil
        if attacker.held_item == "Life Orb":
            lo_recoil = max(1, attacker.max_hp // 10)
            attacker.take_damage(lo_recoil)

        # Drain / heal from damage
        if effect.heals_user > 0:
            heal_amt = max(1, int(total_damage * effect.heals_user))
            attacker.heal(heal_amt)
            self.log(f"{attacker.nickname} restored {heal_amt} HP!")

        # Shell Bell heal
        if attacker.held_item == "Shell Bell":
            sb_heal = max(1, total_damage // 8)
            attacker.heal(sb_heal)

        # Status effects on hit
        if effect.status and not effect.target_self:
            if random.random() < effect.status_chance:
                if not defender.fainted and defender.apply_status(effect.status):
                    self.log(f"{defender.nickname} was {effect.status.value}!")

        # Stat changes on defender
        if effect.stat_changes and not effect.target_self:
            if random.random() < effect.stat_change_chance:
                for stat, delta in effect.stat_changes.items():
                    _, msg = defender.change_stage(stat, delta)
                    self.log(msg)

        # Stat changes on self
        if effect.stat_changes and effect.target_self:
            for stat, delta in effect.stat_changes.items():
                _, msg = attacker.change_stage(stat, delta)
                self.log(msg)

        # Flinch
        if effect.flinch_chance > 0 and random.random() < effect.flinch_chance:
            defender.flinched = True

        if defender.fainted:
            self.log(f"{defender.nickname} fainted!")

    # ── Run a full turn ───────────────────────────────────────────────────────

    def run_turn(
        self,
        player_action: "str | tuple",
        opponent_action: Optional["str | tuple"] = None,
    ) -> list[str]:
        """
        Execute one battle turn.

        player_action / opponent_action can be:
          - ("move", move_index: int)
          - ("switch", party_index: int)
          - ("item", item_name: str, target_index: int)
          - "run"
        """
        self.turn += 1
        player = self.player_pokemon
        opponent = self.opponent_pokemon

        # Determine actions
        p_action = player_action
        o_action = opponent_action or self._ai_choose_action(self.opponent, player)

        # ── Switches resolve first ──────────────────────────────────────────
        if isinstance(p_action, tuple) and p_action[0] == "switch":
            self._do_switch(self.player, p_action[1], "player")
            player = self.player_pokemon
        if isinstance(o_action, tuple) and o_action[0] == "switch":
            self._do_switch(self.opponent, o_action[1], "opponent")
            opponent = self.opponent_pokemon

        # ── Items ───────────────────────────────────────────────────────────
        if isinstance(p_action, tuple) and p_action[0] == "item":
            self._use_item_in_battle(self.player, p_action[1], p_action[2])
        if isinstance(o_action, tuple) and o_action[0] == "item":
            self._use_item_in_battle(self.opponent, o_action[1], o_action[2])

        # ── Run ─────────────────────────────────────────────────────────────
        if p_action == "run":
            if self.is_wild:
                if self._attempt_run(player, opponent):
                    self.log(f"Got away safely!")
                    self.result = BattleResult.RUN
                else:
                    self.log(f"Can't escape!")
            else:
                self.log("Can't run from a trainer battle!")

        # ── Moves ───────────────────────────────────────────────────────────
        p_move_obj = None
        o_move_obj = None

        if isinstance(p_action, tuple) and p_action[0] == "move":
            idx = p_action[1]
            p_move_obj = player.moves[idx] if 0 <= idx < len(player.moves) else None

        if isinstance(o_action, tuple) and o_action[0] == "move":
            idx = o_action[1]
            o_move_obj = opponent.moves[idx] if 0 <= idx < len(opponent.moves) else None

        # Determine order
        if p_move_obj and o_move_obj:
            player_first = self._move_first(player, p_move_obj, opponent, o_move_obj)
        else:
            player_first = True

        def exec_player_move():
            if p_move_obj and not player.fainted:
                if player.flinched:
                    self.log(f"{player.nickname} flinched and couldn't move!")
                    player.flinched = False
                    return
                if not self._can_move(player):
                    return
                self._apply_move(player, p_move_obj, opponent)

        def exec_opponent_move():
            if o_move_obj and not opponent.fainted:
                if opponent.flinched:
                    self.log(f"{opponent.nickname} flinched and couldn't move!")
                    opponent.flinched = False
                    return
                if not self._can_move(opponent):
                    return
                self._apply_move(opponent, o_move_obj, player)

        if player_first:
            exec_player_move()
            exec_opponent_move()
        else:
            exec_opponent_move()
            exec_player_move()

        # ── End of turn ──────────────────────────────────────────────────────
        for msgs in [player.apply_end_of_turn_status(), opponent.apply_end_of_turn_status()]:
            self.messages.extend(msgs)
        self._process_weather_damage()
        self._tick_weather()

        # ── Check win/loss ───────────────────────────────────────────────────
        if self.result is None:
            if all(m.fainted for m in self.opponent.party):
                self.result = BattleResult.WIN
                prize = self.opponent.calculate_prize()
                self.log(f"{self.player.name} defeated {self.opponent.name}!")
                if prize > 0:
                    self.player.money += prize
                    self.log(f"{self.player.name} received ₽{prize}!")
            elif all(m.fainted for m in self.player.party):
                self.result = BattleResult.LOSE
                penalty = max(0, self.player.money // 2)
                self.player.money -= penalty
                self.log(f"{self.player.name} is out of usable Pokémon!")
                self.log(f"{self.player.name} blacked out and lost ₽{penalty}...")

        # Gain EXP for player's Pokémon
        if not player.fainted and (opponent.fainted or self.result == BattleResult.WIN):
            exp = self._calc_exp(opponent)
            for msg in player.gain_exp(exp):
                self.log(msg)

        return self.get_log()

    def _can_move(self, mon: "Pokemon") -> bool:
        """Return True if the Pokémon can execute its move this turn."""
        if mon.fainted:
            return False
        if mon.status == StatusEffect.SLEEP:
            self.log(f"{mon.nickname} is fast asleep.")
            return False
        if mon.status == StatusEffect.PARALYSIS:
            if random.random() < 0.25:
                self.log(f"{mon.nickname} is paralyzed! It can't move!")
                return False
        if mon.status == StatusEffect.FREEZE:
            if random.random() < 0.2:
                mon.cure_status("FREEZE")
                self.log(f"{mon.nickname} thawed out!")
            else:
                self.log(f"{mon.nickname} is frozen solid!")
                return False
        if mon.confused:
            mon.confusion_turns -= 1
            if mon.confusion_turns <= 0:
                mon.confused = False
                self.log(f"{mon.nickname} snapped out of confusion!")
            else:
                self.log(f"{mon.nickname} is confused!")
                if random.random() < 0.33:
                    # Hit self
                    self.log(f"It hurt itself in its confusion!")
                    dmg = int((((2 * mon.level / 5 + 2) * 40 * mon.get_stat("atk")) / mon.get_stat("def")) / 50 + 2)
                    mon.take_damage(dmg)
                    return False
        return True

    # ── Catching ─────────────────────────────────────────────────────────────

    def attempt_catch(self, ball_name: str) -> tuple[bool, list[str]]:
        """
        Attempt to catch the wild Pokémon.
        Returns (success: bool, messages: list[str]).
        """
        if not self.is_wild:
            return False, ["You can't catch a trainer's Pokémon!"]
        from ..data.items import ITEMS
        target = self.opponent_pokemon
        item_data = ITEMS.get(ball_name)
        if not item_data:
            return False, [f"Unknown ball: {ball_name}"]
        if ball_name == "Master Ball":
            self.result = BattleResult.CATCH
            return True, [f"The Master Ball worked perfectly! Caught {target.nickname}!"]

        modifier = item_data.catch_rate_modifier
        # Quick Ball bonus for turn 1
        if ball_name == "Quick Ball" and self.turn <= 1:
            modifier = 5.0
        # Timer Ball scales with turns
        if ball_name == "Timer Ball":
            modifier = min(4.0, 1.0 + self.turn * 0.3)
        # Status modifiers
        status_bonus = 1.0
        if target.status in (StatusEffect.SLEEP, StatusEffect.FREEZE):
            status_bonus = 2.5
        elif target.status in (StatusEffect.PARALYSIS, StatusEffect.BURN,
                                StatusEffect.POISON, StatusEffect.BADLY_POISONED):
            status_bonus = 1.5
        hp_fraction = target.current_hp / target.max_hp
        catch_value = int(
            ((3 * target.max_hp - 2 * target.current_hp) * target.species.catch_rate * modifier * status_bonus)
            / (3 * target.max_hp)
        )
        catch_value = max(1, catch_value)
        shake_check = int(1048560 / ((16711680 / catch_value) ** 0.25))
        shakes = 0
        msgs = [f"You throw a {ball_name}!"]
        for i in range(4):
            if random.randint(0, 65535) < shake_check:
                shakes += 1
                msgs.append("⬛" * (i + 1) + "..." if shakes < 4 else "")
            else:
                break
        if shakes == 4:
            # Use a heal ball to restore HP/status
            if ball_name == "Heal Ball":
                target.full_heal()
                msgs.append(f"Ding! {target.nickname} was caught!")
            else:
                msgs.append(f"Gotcha! {target.nickname} was caught!")
            target.caught_in = ball_name
            self.result = BattleResult.CATCH
            # Luxury ball = faster friendship gain
            if ball_name == "Luxury Ball":
                target.friendship = min(255, target.friendship + 10)
            return True, msgs
        else:
            msgs.append(f"Oh no! The Pokémon broke free! (shakes: {shakes})")
            return False, msgs

    # ── Escape ────────────────────────────────────────────────────────────────

    def _attempt_run(self, player_mon: "Pokemon", wild_mon: "Pokemon") -> bool:
        # Chance starts at -0.1 on turn 1 and increases by 0.1 each turn.
        # Turn 1: -0.1 (impossible), turn 2: 0.0 (impossible), turn 3: 0.1, …
        # turn 12: 1.0 (guaranteed).
        chance = -0.1 + 0.1 * (self.turn - 1)
        if chance <= 0:
            return False
        if chance >= 1.0:
            return True
        return random.random() < chance

    # ── Experience ───────────────────────────────────────────────────────────

    def _calc_exp(self, fainted_mon: "Pokemon") -> int:
        base = fainted_mon.species.base_exp
        bonus = 1.5 if not fainted_mon.is_wild else 1.0
        # Lucky Egg doubles EXP
        if self.player_pokemon.held_item == "Lucky Egg":
            bonus *= 2.0
        return max(1, int(base * fainted_mon.level * bonus / 7))

    # ── AI ────────────────────────────────────────────────────────────────────

    def _ai_choose_action(self, ai_trainer: "Trainer", target: "Pokemon") -> tuple:
        """Simple AI: pick highest-power available move."""
        mon = ai_trainer.party[self.opponent_active_idx]
        if mon.fainted:
            # Switch to next available
            for i, p in enumerate(ai_trainer.party):
                if not p.fainted and i != self.opponent_active_idx:
                    return ("switch", i)
        best_move_idx = 0
        best_score = -1
        for i, move_obj in enumerate(mon.moves):
            if move_obj.pp <= 0:
                continue
            move = move_obj.data
            if move.power == 0:
                continue
            eff = get_effectiveness(move.move_type, target.species.types)
            score = move.power * eff
            if move.move_type in mon.species.types:
                score *= 1.5
            if score > best_score:
                best_score = score
                best_move_idx = i
        return ("move", best_move_idx)

    # ── Switch ────────────────────────────────────────────────────────────────

    def _do_switch(self, trainer: "Trainer", idx: int, side: str) -> None:
        party = trainer.party
        if idx < 0 or idx >= len(party):
            return
        new_mon = party[idx]
        if new_mon.fainted:
            self.log(f"{new_mon.nickname} can't battle!")
            return
        if side == "player":
            old = self.player_pokemon
            old.reset_volatile_status()
            self.player_active_idx = idx
            self.log(f"{self.player.name} withdrew {old.nickname} and sent out {new_mon.nickname}!")
        else:
            old = self.opponent_pokemon
            old.reset_volatile_status()
            self.opponent_active_idx = idx
            self.log(f"{self.opponent.name} withdrew {old.nickname} and sent out {new_mon.nickname}!")

    # ── Item use in battle ────────────────────────────────────────────────────

    def _use_item_in_battle(self, trainer: "Trainer", item_name: str, target_idx: int) -> None:
        from ..data.items import ItemCategory
        item_data = ITEMS.get(item_name)
        if not item_data:
            return
        target = trainer.party[target_idx] if 0 <= target_idx < len(trainer.party) else None
        if not target:
            return
        if item_data.category in (ItemCategory.MEDICINE,):
            if item_data.revives and target.fainted:
                full = item_data.hp_restore == -1
                target.revive(full=full)
                self.log(f"{target.nickname} was revived!")
            elif not target.fainted:
                if item_data.hp_restore == -1:
                    target.heal(target.max_hp)
                    self.log(f"{target.nickname}'s HP was fully restored!")
                elif item_data.hp_restore == -2:
                    target.heal(target.max_hp // 2)
                    self.log(f"{target.nickname}'s HP was restored by half!")
                elif item_data.hp_restore > 0:
                    restored = target.heal(item_data.hp_restore)
                    self.log(f"{target.nickname} restored {restored} HP!")
                for status_name in item_data.cures_status:
                    target.cure_status(status_name)
                if item_data.cures_status:
                    self.log(f"{target.nickname}'s status was cured!")
        trainer.bag.remove_item(item_name, 1)
