"""
Tests for the Pykemon game engine.

Run with:
    python -m pytest tests/ -v
    python tests/test_pykemon.py
"""

from __future__ import annotations
import random
import sys
import os

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pykemon as pk
from pykemon.data.types import PokemonType, get_effectiveness, effectiveness_text, TYPE_CHART
from pykemon.data.moves import MOVES, TM_MOVES, HM_MOVES, StatusEffect, WeatherEffect
from pykemon.data.pokemon_data import SPECIES, SPECIES_BY_NUM
from pykemon.data.items import ITEMS, ItemCategory
from pykemon.core.pokemon import Pokemon, create_pokemon, Move
from pykemon.core.trainer import Trainer, GYMS, ELITE_FOUR, build_gym_leader, build_elite_four_member
from pykemon.core.battle import Battle, BattleResult
from pykemon.core.bag import Bag
from pykemon.core.pokedex import Pokedex
from pykemon.systems.evolution import check_evolution, evolve, can_evolve_with_item
from pykemon.systems.friendship import update_friendship, friendship_tier, return_power, frustration_power
from pykemon.systems.day_night import get_time_of_day, is_nighttime, is_daytime
from pykemon.systems.ride import RideSystem, RIDE_POKEMON
from pykemon.world.pokemon_center import PokemonCenter, PC
from pykemon.world.poke_mart import PokeMart
from pykemon.world.gym import GymBadgeSystem, GymChallenge, PokemonLeague
from pykemon.world.fossils import FossilLab, FOSSIL_REVIVALS


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def bulbasaur():
    return create_pokemon("Bulbasaur", 10, trainer_name="Test")

@pytest.fixture
def charmander():
    return create_pokemon("Charmander", 10, trainer_name="Test")

@pytest.fixture
def player():
    p = Trainer("Ash", money=5000, is_player=True)
    p.bag.add_item("Poké Ball", 10)
    p.bag.add_item("Potion", 5)
    p.bag.add_item("Ultra Ball", 3)
    return p

@pytest.fixture
def player_with_party():
    p = Trainer("Ash", money=5000, is_player=True)
    p.bag.add_item("Poké Ball", 10)
    p.add_pokemon(create_pokemon("Charizard", 50, trainer_name="Ash"))
    p.add_pokemon(create_pokemon("Blastoise", 50, trainer_name="Ash"))
    return p


# ── 1. Type system ─────────────────────────────────────────────────────────────

class TestTypeSystem:
    def test_15_types_exist(self):
        """The game has exactly 15 Gen I types."""
        gen1_types = [
            PokemonType.NORMAL, PokemonType.FIRE, PokemonType.WATER,
            PokemonType.GRASS, PokemonType.ELECTRIC, PokemonType.ICE,
            PokemonType.FIGHTING, PokemonType.POISON, PokemonType.GROUND,
            PokemonType.FLYING, PokemonType.PSYCHIC, PokemonType.BUG,
            PokemonType.ROCK, PokemonType.GHOST, PokemonType.DRAGON,
        ]
        for t in gen1_types:
            assert t in PokemonType

    def test_type_chart_covers_all_types(self):
        """Every type in the chart has entries for all defenders."""
        for atk_type in TYPE_CHART:
            assert isinstance(TYPE_CHART[atk_type], dict)

    def test_fire_super_effective_vs_grass(self):
        assert get_effectiveness(PokemonType.FIRE, [PokemonType.GRASS]) == 2.0

    def test_water_super_effective_vs_fire(self):
        assert get_effectiveness(PokemonType.WATER, [PokemonType.FIRE]) == 2.0

    def test_electric_immune_to_ground(self):
        assert get_effectiveness(PokemonType.GROUND, [PokemonType.FLYING]) == 0.0

    def test_dual_type_multiplication(self):
        # Water vs Water/Ground = 0.5 * 2.0 = 1.0
        mult = get_effectiveness(PokemonType.WATER, [PokemonType.WATER, PokemonType.GROUND])
        assert mult == 1.0

    def test_effectiveness_text_super(self):
        assert "super effective" in effectiveness_text(2.0)

    def test_effectiveness_text_immune(self):
        assert "no effect" in effectiveness_text(0.0)

    def test_effectiveness_text_normal(self):
        assert effectiveness_text(1.0) == ""


# ── 2. Pokémon species data ────────────────────────────────────────────────────

class TestPokemonData:
    def test_100_plus_pokemon(self):
        assert len(SPECIES) >= 100

    def test_original_151(self):
        assert len(SPECIES) >= 151

    def test_species_have_types(self):
        for sp in SPECIES.values():
            assert len(sp.types) >= 1

    def test_starters_exist(self):
        for starter in ["Bulbasaur", "Charmander", "Squirtle"]:
            assert starter in SPECIES

    def test_legendary_pokemon(self):
        legendaries = [s for s in SPECIES.values() if s.is_legendary]
        assert len(legendaries) >= 3

    def test_fossil_pokemon(self):
        fossil_pkmn = [s for s in SPECIES.values() if s.is_fossil]
        assert len(fossil_pkmn) >= 2

    def test_evolutions_exist(self):
        assert len(SPECIES["Bulbasaur"].evolutions) > 0
        assert SPECIES["Bulbasaur"].evolutions[0].evolves_to == "Ivysaur"

    def test_caterpie_evolves_at_7(self):
        evos = SPECIES["Caterpie"].evolutions
        assert any(e.min_level == 7 for e in evos)

    def test_pokemon_have_learnsets(self):
        for name in ["Bulbasaur", "Charmander", "Squirtle"]:
            assert len(SPECIES[name].learnset) > 0

    def test_all_species_have_valid_numbers(self):
        for num, sp in SPECIES_BY_NUM.items():
            assert 1 <= num <= 9999
            assert sp.number == num


# ── 3. Pokémon instances ───────────────────────────────────────────────────────

class TestPokemonInstance:
    def test_create_pokemon(self, bulbasaur):
        assert bulbasaur.species.name == "Bulbasaur"
        assert bulbasaur.level == 10
        assert bulbasaur.current_hp == bulbasaur.max_hp

    def test_has_4_moves_max(self, bulbasaur):
        assert len(bulbasaur.moves) <= 4

    def test_stats_are_positive(self, bulbasaur):
        assert bulbasaur.max_hp > 0
        assert bulbasaur.base_atk > 0
        assert bulbasaur.base_def > 0
        assert bulbasaur.base_spe > 0

    def test_gender_set(self, bulbasaur):
        assert bulbasaur.gender in ("M", "F", None)

    def test_shiny_flag(self):
        shiny = create_pokemon("Pikachu", 10, is_shiny=True, trainer_name="Red")
        assert shiny.is_shiny is True

    def test_friendship_default(self, bulbasaur):
        assert bulbasaur.friendship == SPECIES["Bulbasaur"].base_friendship

    def test_heal(self, bulbasaur):
        bulbasaur.current_hp = 5
        bulbasaur.heal(100)
        assert bulbasaur.current_hp <= bulbasaur.max_hp
        assert bulbasaur.current_hp > 5

    def test_full_heal(self, bulbasaur):
        bulbasaur.current_hp = 1
        bulbasaur.full_heal()
        assert bulbasaur.current_hp == bulbasaur.max_hp
        assert bulbasaur.status is None

    def test_take_damage(self, bulbasaur):
        original_hp = bulbasaur.current_hp
        bulbasaur.take_damage(5)
        assert bulbasaur.current_hp == original_hp - 5

    def test_faint_on_zero_hp(self, bulbasaur):
        bulbasaur.take_damage(9999)
        assert bulbasaur.fainted

    def test_learn_move(self, bulbasaur):
        bulbasaur.moves = []
        bulbasaur.learn_move("Tackle")
        assert any(m.data.name == "Tackle" for m in bulbasaur.moves)

    def test_summary(self, bulbasaur):
        s = bulbasaur.summary()
        assert "Bulbasaur" in s
        assert "HP" in s

    def test_held_item(self, bulbasaur):
        bulbasaur.held_item = "Leftovers"
        assert bulbasaur.held_item == "Leftovers"

    def test_ivs_in_valid_range(self, bulbasaur):
        for stat, val in bulbasaur.ivs.items():
            assert 0 <= val <= 31, f"{stat} IV out of range: {val}"

    def test_stat_stages_start_at_zero(self, bulbasaur):
        for stat, val in bulbasaur.stat_stages.items():
            assert val == 0


# ── 4. Moves ──────────────────────────────────────────────────────────────────

class TestMoves:
    def test_moves_registered(self):
        assert len(MOVES) >= 100

    def test_tms_registered(self):
        assert len(TM_MOVES) >= 20

    def test_hms_registered(self):
        assert len(HM_MOVES) >= 5

    def test_basic_move_attributes(self):
        tackle = MOVES["Tackle"]
        assert tackle.power == 40
        assert tackle.accuracy == 100
        assert tackle.pp == 35

    def test_status_move_power_zero(self):
        growl = MOVES["Growl"]
        assert growl.power == 0

    def test_move_has_type(self):
        ember = MOVES["Ember"]
        assert ember.move_type == PokemonType.FIRE

    def test_hm_surf(self):
        surf = MOVES["Surf"]
        assert surf.hm_number == 3

    def test_tm_thunderbolt(self):
        assert 24 in TM_MOVES
        assert TM_MOVES[24].name == "Thunderbolt"


# ── 5. Items ──────────────────────────────────────────────────────────────────

class TestItems:
    def test_pokeballs_exist(self):
        balls = [i for i in ITEMS.values() if i.category == ItemCategory.POKEBALL]
        assert len(balls) >= 5

    def test_master_ball_catch_rate(self):
        assert ITEMS["Master Ball"].catch_rate_modifier >= 100

    def test_medicine_restores_hp(self):
        potion = ITEMS["Potion"]
        assert potion.hp_restore > 0

    def test_full_restore(self):
        fr = ITEMS["Full Restore"]
        assert fr.hp_restore == -1

    def test_fossils_in_items(self):
        fossils = [i for i in ITEMS.values() if i.category == ItemCategory.FOSSIL]
        assert len(fossils) >= 3

    def test_held_items_exist(self):
        held = [i for i in ITEMS.values() if i.category == ItemCategory.HELD]
        assert len(held) >= 5

    def test_tms_in_items(self):
        tms = [i for i in ITEMS.values() if i.category == ItemCategory.TM]
        assert len(tms) >= 10


# ── 6. Bag ────────────────────────────────────────────────────────────────────

class TestBag:
    def test_add_and_count(self):
        bag = Bag()
        bag.add_item("Potion", 3)
        assert bag.item_count("Potion") == 3

    def test_remove_item(self):
        bag = Bag()
        bag.add_item("Potion", 3)
        result = bag.remove_item("Potion", 2)
        assert result
        assert bag.item_count("Potion") == 1

    def test_remove_insufficient(self):
        bag = Bag()
        bag.add_item("Potion", 1)
        result = bag.remove_item("Potion", 5)
        assert not result

    def test_has_item(self):
        bag = Bag()
        bag.add_item("Poké Ball", 5)
        assert bag.has_item("Poké Ball")
        assert not bag.has_item("Ultra Ball")

    def test_pokeballs_pocket(self):
        bag = Bag()
        bag.add_item("Poké Ball", 3)
        bag.add_item("Great Ball", 2)
        assert "Poké Ball" in bag.pokeballs()
        assert "Great Ball" in bag.pokeballs()

    def test_display(self):
        bag = Bag()
        bag.add_item("Potion", 1)
        disp = bag.display()
        assert "Potion" in disp


# ── 7. Trainer ────────────────────────────────────────────────────────────────

class TestTrainer:
    def test_add_pokemon(self, player, bulbasaur):
        player.add_pokemon(bulbasaur)
        assert bulbasaur in player.party

    def test_party_max_6(self, player):
        for i in range(7):
            mon = create_pokemon("Rattata", 5, trainer_name="Test")
            player.add_pokemon(mon)
        assert len(player.party) == 6

    def test_has_usable_pokemon(self, player_with_party):
        assert player_with_party.has_usable_pokemon()

    def test_heal_party(self, player_with_party):
        player_with_party.party[0].current_hp = 1
        player_with_party.heal_party()
        assert player_with_party.party[0].current_hp == player_with_party.party[0].max_hp

    def test_badge_award(self, player):
        player.award_badge("Boulder Badge")
        assert player.has_badge("Boulder Badge")
        assert "Boulder Badge" in player.badges

    def test_money(self, player):
        assert player.money == 5000


# ── 8. Battle ─────────────────────────────────────────────────────────────────

class TestBattle:
    def test_basic_battle_turn(self):
        p = Trainer("P", party=[create_pokemon("Charmander", 10, trainer_name="P")])
        o = Trainer("O", party=[create_pokemon("Squirtle", 10, is_wild=True)])
        b = Battle(p, o, is_wild=True)
        msgs = b.run_turn(("move", 0))
        assert isinstance(msgs, list)

    def test_weather_sets(self):
        p = Trainer("P", party=[create_pokemon("Charizard", 40, trainer_name="P")])
        o = Trainer("O", party=[create_pokemon("Blastoise", 40)])
        b = Battle(p, o)
        b.apply_weather(WeatherEffect.RAIN)
        assert b.weather == WeatherEffect.RAIN

    def test_wild_battle_can_catch(self):
        p = Trainer("P", party=[create_pokemon("Charizard", 50, trainer_name="P")])
        p.bag.add_item("Master Ball", 1)
        o = Trainer("O", party=[create_pokemon("Pidgey", 5, is_wild=True)])
        b = Battle(p, o, is_wild=True)
        success, msgs = b.attempt_catch("Master Ball")
        assert success is True

    def test_non_wild_cannot_catch(self):
        p = Trainer("P", party=[create_pokemon("Pikachu", 20, trainer_name="P")])
        p.bag.add_item("Poké Ball", 5)
        o = Trainer("O", party=[create_pokemon("Geodude", 12)])
        b = Battle(p, o, is_wild=False)
        success, msgs = b.attempt_catch("Poké Ball")
        assert success is False

    def test_double_battle_slots(self):
        t1 = Trainer("T1", party=[create_pokemon("Pikachu", 20),
                                   create_pokemon("Eevee", 18)])
        t2 = Trainer("T2", party=[create_pokemon("Geodude", 20),
                                   create_pokemon("Onix", 22)])
        b = Battle(t1, t2, is_double=True)
        assert b.player_active_idx == 0
        assert b.player_active_idx2 == 1

    def test_run_action(self):
        p = Trainer("P", party=[create_pokemon("Rapidash", 40, trainer_name="P")])
        o = Trainer("O", party=[create_pokemon("Raticate", 30, is_wild=True)])
        b = Battle(p, o, is_wild=True)
        msgs = b.run_turn("run")
        assert b.result == BattleResult.RUN

    def test_battle_result_win_on_ko(self):
        p_mon = create_pokemon("Mewtwo", 100, trainer_name="P")
        o_mon = create_pokemon("Magikarp", 5, is_wild=True)
        p = Trainer("P", party=[p_mon])
        o = Trainer("O", party=[o_mon])
        b = Battle(p, o, is_wild=True)
        for _ in range(10):
            if b.result is not None:
                break
            b.run_turn(("move", 0))
        assert b.result in (BattleResult.WIN, None)


# ── 9. Evolution ──────────────────────────────────────────────────────────────

class TestEvolution:
    def test_caterpie_evolves_to_metapod(self):
        cat = create_pokemon("Caterpie", 7, trainer_name="T")
        cond = check_evolution(cat)
        assert cond is not None
        assert cond.evolves_to == "Metapod"

    def test_caterpie_no_evo_before_7(self):
        cat = create_pokemon("Caterpie", 6, trainer_name="T")
        cond = check_evolution(cat)
        assert cond is None

    def test_evolve_mutates_species(self):
        cat = create_pokemon("Caterpie", 7, trainer_name="T")
        cond = check_evolution(cat)
        evolve(cat, cond)
        assert cat.species.name == "Metapod"

    def test_friendship_evolution(self):
        chansey = create_pokemon("Chansey", 40, trainer_name="T")
        chansey.friendship = 220
        cond = check_evolution(chansey)
        assert cond is not None
        assert cond.evolves_to == "Blissey"

    def test_item_evolution_eevee_fire_stone(self):
        eevee = create_pokemon("Eevee", 1, trainer_name="T")
        assert can_evolve_with_item(eevee, "Fire Stone")

    def test_no_evolution_for_venusaur(self):
        ven = create_pokemon("Venusaur", 100, trainer_name="T")
        cond = check_evolution(ven)
        assert cond is None

    def test_evolve_keeps_default_name_updated(self):
        cat = create_pokemon("Caterpie", 7, trainer_name="T")
        cond = check_evolution(cat)
        evolve(cat, cond)
        assert cat.nickname == "Metapod"

    def test_evolve_keeps_custom_nickname(self):
        cat = create_pokemon("Caterpie", 7, nickname="Worm", trainer_name="T")
        cond = check_evolution(cat)
        evolve(cat, cond)
        assert cat.nickname == "Worm"


# ── 10. Friendship / Affection ────────────────────────────────────────────────

class TestFriendship:
    def test_friendship_increases_on_level_up(self):
        mon = create_pokemon("Eevee", 5, trainer_name="T")
        before = mon.friendship
        update_friendship(mon, "level_up")
        assert mon.friendship > before

    def test_friendship_decreases_on_faint(self):
        mon = create_pokemon("Eevee", 5, trainer_name="T")
        before = mon.friendship
        update_friendship(mon, "fainted")
        assert mon.friendship < before

    def test_friendship_capped_at_255(self):
        mon = create_pokemon("Eevee", 5, trainer_name="T")
        mon.friendship = 254
        update_friendship(mon, "grooming")
        assert mon.friendship == 255

    def test_friendship_cannot_go_negative(self):
        mon = create_pokemon("Eevee", 5, trainer_name="T")
        mon.friendship = 0
        update_friendship(mon, "bitter_medicine")
        assert mon.friendship == 0

    def test_return_power(self):
        mon = create_pokemon("Eevee", 5, trainer_name="T")
        mon.friendship = 255
        assert return_power(mon) == 102

    def test_frustration_power(self):
        mon = create_pokemon("Eevee", 5, trainer_name="T")
        mon.friendship = 0
        assert frustration_power(mon) == 102

    def test_friendship_tier(self):
        mon = create_pokemon("Eevee", 5, trainer_name="T")
        mon.friendship = 255
        tier = friendship_tier(mon)
        assert "adores" in tier or "loves" in tier


# ── 11. Day/Night ─────────────────────────────────────────────────────────────

class TestDayNight:
    def test_morning_hour(self):
        assert get_time_of_day(7) == "morning"

    def test_day_hour(self):
        assert get_time_of_day(12) == "day"

    def test_evening_hour(self):
        assert get_time_of_day(19) == "evening"

    def test_night_hour(self):
        assert get_time_of_day(23) == "night"

    def test_is_nighttime(self):
        assert is_nighttime(23) is True
        assert is_nighttime(2) is True
        assert is_nighttime(12) is False

    def test_is_daytime(self):
        assert is_daytime(12) is True
        assert is_daytime(23) is False

    def test_eevee_espeon_day_evo(self):
        eevee = create_pokemon("Eevee", 5, trainer_name="T")
        eevee.friendship = 220
        cond = check_evolution(eevee, time_of_day="day")
        assert cond is not None
        assert cond.evolves_to == "Espeon"

    def test_eevee_umbreon_night_evo(self):
        eevee = create_pokemon("Eevee", 5, trainer_name="T")
        eevee.friendship = 220
        cond = check_evolution(eevee, time_of_day="night")
        assert cond is not None
        assert cond.evolves_to == "Umbreon"


# ── 12. Ride Pokémon ──────────────────────────────────────────────────────────

class TestRidePokemon:
    def test_unlock_lapras(self):
        ride = RideSystem()
        assert ride.unlock("Lapras")
        assert ride.can_ride("Lapras")

    def test_unknown_pokemon_not_unlockable(self):
        ride = RideSystem()
        assert not ride.unlock("Magikarp")

    def test_use_returns_message(self):
        ride = RideSystem()
        ride.unlock("Lapras")
        msg = ride.use("Lapras")
        assert msg is not None
        assert "Lapras" in msg

    def test_unlocked_terrain(self):
        ride = RideSystem()
        ride.unlock("Lapras")
        assert ride.can_use_terrain("water")

    def test_display(self):
        ride = RideSystem()
        disp = ride.display()
        assert "Lapras" in disp


# ── 13. Pokémon Center ────────────────────────────────────────────────────────

class TestPokemonCenter:
    def test_heals_party(self):
        center = PokemonCenter("Pallet Town")
        trainer = Trainer("T", party=[create_pokemon("Bulbasaur", 10, trainer_name="T")])
        trainer.party[0].current_hp = 1
        trainer.party[0].status = StatusEffect.POISON
        center.heal_party(trainer)
        assert trainer.party[0].current_hp == trainer.party[0].max_hp
        assert trainer.party[0].status is None

    def test_pc_deposit_withdraw(self):
        center = PokemonCenter("Cerulean City")
        mon = create_pokemon("Pidgey", 5, trainer_name="T")
        trainer = Trainer("T", party=[
            create_pokemon("Pikachu", 10, trainer_name="T"),
            mon,
        ])
        msgs = center.deposit_pokemon(trainer, 1)
        assert "Box" in msgs[0]
        assert len(trainer.party) == 1

    def test_pc_cannot_deposit_last_pokemon(self):
        center = PokemonCenter("Cerulean City")
        trainer = Trainer("T", party=[create_pokemon("Pikachu", 10, trainer_name="T")])
        msgs = center.deposit_pokemon(trainer, 0)
        assert "at least one" in msgs[0]


# ── 14. Poké Mart ─────────────────────────────────────────────────────────────

class TestPokeMart:
    def test_buy_item(self):
        mart = PokeMart("Viridian City")
        trainer = Trainer("T", money=1000)
        ok, msg = mart.buy(trainer, "Potion", 1, badge_count=0)
        assert ok
        assert trainer.bag.item_count("Potion") == 1
        assert trainer.money < 1000

    def test_buy_no_money(self):
        mart = PokeMart("Viridian City")
        trainer = Trainer("T", money=10)
        ok, msg = mart.buy(trainer, "Potion", 1, badge_count=0)
        assert not ok

    def test_sell_item(self):
        mart = PokeMart("Viridian City")
        trainer = Trainer("T", money=0)
        trainer.bag.add_item("Potion", 2)
        ok, msg = mart.sell(trainer, "Potion", 1)
        assert ok
        assert trainer.money > 0

    def test_stock_grows_with_badges(self):
        mart = PokeMart("Cerulean City")
        stock_0 = mart.get_stock(0)
        stock_5 = mart.get_stock(5)
        assert len(stock_5) > len(stock_0)


# ── 15. Gym System ────────────────────────────────────────────────────────────

class TestGymSystem:
    def test_8_gyms(self):
        assert len(GYMS) == 8

    def test_elite_four_5_members(self):
        assert len(ELITE_FOUR) == 5  # 4 Elite Four + Champion

    def test_gym_leaders_have_party(self):
        for gym in GYMS:
            leader = build_gym_leader(gym)
            assert len(leader.party) >= 1

    def test_gym_badge_system(self):
        gs = GymBadgeSystem()
        assert len(gs.challenges) == 8

    def test_challenge_requires_badges(self):
        gs = GymBadgeSystem()
        trainer = Trainer("T")
        gym2 = gs.get_gym(2)
        assert not gym2.can_challenge(trainer)
        trainer.award_badge("Boulder Badge")
        assert gym2.can_challenge(trainer)

    def test_award_badge(self):
        trainer = Trainer("T", money=3000, is_player=True)
        trainer.award_badge("Boulder Badge")
        assert trainer.has_badge("Boulder Badge")

    def test_league_requires_8_badges(self):
        gs = GymBadgeSystem()
        trainer = Trainer("T")
        assert not gs.league.can_challenge(trainer)
        for gym in GYMS:
            trainer.award_badge(gym.badge_name)
        assert gs.league.can_challenge(trainer)

    def test_display_gyms(self):
        gs = GymBadgeSystem()
        disp = gs.display_gyms()
        for gym in GYMS:
            assert gym.leader_name in disp


# ── 16. Fossils ───────────────────────────────────────────────────────────────

class TestFossils:
    def test_fossil_revivals_exist(self):
        assert len(FOSSIL_REVIVALS) >= 3

    def test_revive_dome_fossil(self):
        lab = FossilLab()
        trainer = Trainer("T", party=[], money=3000, is_player=True)
        trainer.bag.add_item("Dome Fossil", 1)
        pokemon, msgs = lab.revive(trainer, "Dome Fossil")
        assert pokemon is not None
        assert pokemon.species.name == "Kabuto"
        assert not trainer.bag.has_item("Dome Fossil")

    def test_revive_without_fossil(self):
        lab = FossilLab()
        trainer = Trainer("T", party=[], money=3000)
        pokemon, msgs = lab.revive(trainer, "Dome Fossil")
        assert pokemon is None

    def test_old_amber_gives_aerodactyl(self):
        lab = FossilLab()
        trainer = Trainer("T", party=[], money=3000, is_player=True)
        trainer.bag.add_item("Old Amber", 1)
        pokemon, msgs = lab.revive(trainer, "Old Amber")
        assert pokemon is not None
        assert pokemon.species.name == "Aerodactyl"


# ── 17. Pokédex ───────────────────────────────────────────────────────────────

class TestPokedex:
    def test_register_seen(self, bulbasaur):
        dex = Pokedex()
        dex.register_seen(bulbasaur)
        assert dex.is_seen(1)
        assert not dex.is_caught(1)

    def test_register_caught(self, bulbasaur):
        dex = Pokedex()
        dex.register_caught(bulbasaur)
        assert dex.is_caught(1)
        assert dex.is_seen(1)

    def test_seen_count(self, bulbasaur, charmander):
        dex = Pokedex()
        dex.register_seen(bulbasaur)
        dex.register_seen(charmander)
        assert dex.seen_count == 2

    def test_lookup_unseen_returns_unknown(self):
        dex = Pokedex()
        result = dex.lookup("Pikachu")
        assert "???" in result or "Not yet" in result

    def test_lookup_seen(self, bulbasaur):
        dex = Pokedex()
        dex.register_seen(bulbasaur)
        result = dex.lookup("Bulbasaur")
        assert "Bulbasaur" in result

    def test_completion_pct(self):
        dex = Pokedex()
        assert dex.completion_pct == 0.0
        mon = create_pokemon("Bulbasaur", 5, trainer_name="T")
        dex.register_caught(mon)
        assert dex.completion_pct > 0


# ── 18. Shiny Pokémon ─────────────────────────────────────────────────────────

class TestShiny:
    def test_forced_shiny(self):
        mon = create_pokemon("Gyarados", 30, is_shiny=True, trainer_name="Red")
        assert mon.is_shiny

    def test_summary_shows_shiny(self):
        mon = create_pokemon("Gyarados", 30, is_shiny=True, trainer_name="Red")
        assert "[SHINY]" in mon.summary()

    def test_repr_shows_shiny_sparkle(self):
        mon = create_pokemon("Gyarados", 30, is_shiny=True, trainer_name="Red")
        assert "✨" in repr(mon)

    def test_wild_shiny_chance_is_bool(self):
        mon = create_pokemon("Rattata", 5, is_wild=False, trainer_name="T")
        assert isinstance(mon.is_shiny, bool)


# ── 19. Status effects ────────────────────────────────────────────────────────

class TestStatusEffects:
    def test_apply_burn(self, bulbasaur):
        bulbasaur.status = StatusEffect.BURN
        assert bulbasaur.status == StatusEffect.BURN

    def test_burn_status_str(self, bulbasaur):
        bulbasaur.status = StatusEffect.BURN
        assert "BRN" in bulbasaur.status_str

    def test_all_statuses_defined(self):
        for effect in StatusEffect:
            assert effect.value


# ── 20. TMs & HMs ────────────────────────────────────────────────────────────

class TestTMsHMs:
    def test_bag_contains_tm_items(self):
        bag = Bag()
        bag.add_item("TM24", 1)
        assert bag.item_count("TM24") == 1

    def test_hm_items_exist(self):
        assert "HM01" in ITEMS
        assert "HM02" in ITEMS
        assert "HM03" in ITEMS

    def test_teach_tm(self):
        bag = Bag()
        bag.add_item("TM24", 1)  # Thunderbolt
        mon = create_pokemon("Pikachu", 20, trainer_name="T")
        mon.moves = []
        result = bag.teach_tm(24, mon)
        assert result
        assert any(m.data.name == "Thunderbolt" for m in mon.moves)

    def test_teach_hm(self):
        bag = Bag()
        bag.add_item("HM03", 1)  # Surf
        mon = create_pokemon("Slowpoke", 20, trainer_name="T")
        mon.moves = []
        result = bag.teach_hm(3, mon)
        assert result
        assert any(m.data.name == "Surf" for m in mon.moves)


# ── 21. Story System ──────────────────────────────────────────────────────────

class TestStorySystem:
    """Tests for StoryFlag, GameState, save/load, and GameState helpers."""

    def test_story_flags_are_strings(self):
        from pykemon.story.events import StoryFlag
        flags = [v for k, v in vars(StoryFlag).items() if not k.startswith("_")]
        assert all(isinstance(f, str) for f in flags)

    def test_badge_to_flag_mapping(self):
        from pykemon.story.events import BADGE_TO_FLAG, StoryFlag
        assert BADGE_TO_FLAG["Boulder Badge"] == StoryFlag.BEAT_BROCK
        assert BADGE_TO_FLAG["Earth Badge"]   == StoryFlag.BEAT_GIOVANNI
        assert len(BADGE_TO_FLAG) == 8

    def test_gamestate_set_has_flag(self):
        from pykemon.story.events import GameState, StoryFlag
        player = Trainer("Red", money=3000, is_player=True)
        gs = GameState(player)
        assert not gs.has_flag(StoryFlag.BEAT_BROCK)
        gs.set_flag(StoryFlag.BEAT_BROCK)
        assert gs.has_flag(StoryFlag.BEAT_BROCK)

    def test_gamestate_travel_records_history(self):
        from pykemon.story.events import GameState
        player = Trainer("Red", money=3000, is_player=True)
        gs = GameState(player, "Pallet Town")
        gs.travel_to("Route 1")
        gs.travel_to("Viridian City")
        assert gs.current_location == "Viridian City"
        assert "Pallet Town" in gs.seen_locations
        assert "Route 1" in gs.seen_locations

    def test_gamestate_status_line(self):
        from pykemon.story.events import GameState
        player = Trainer("Red", money=1234, is_player=True)
        gs = GameState(player, "Pallet Town")
        line = gs.status_line()
        assert "Red" in line
        assert "1,234" in line
        assert "Pallet Town" in line

    def test_gamestate_badge_count(self):
        from pykemon.story.events import GameState
        player = Trainer("Red", money=5000, is_player=True)
        gs = GameState(player)
        assert gs.badge_count() == 0
        player.badges.append("Boulder Badge")
        assert gs.badge_count() == 1

    def test_gamestate_save_load(self, tmp_path):
        """Round-trip: save → load should restore key state."""
        import json
        from pykemon.story.events import GameState, StoryFlag
        save_file = str(tmp_path / "test_save.json")

        player = Trainer("Ash", money=2500, is_player=True)
        player.badges.append("Boulder Badge")
        player.bag.add_item("Potion", 3)
        player.add_pokemon(create_pokemon("Pikachu", 15, trainer_name="Ash"))

        gs = GameState(player, "Cerulean City")
        gs.set_flag(StoryFlag.BEAT_BROCK)
        gs.set_flag(StoryFlag.OAK_PARCEL_DELIVERED)

        gs.save(save_file)
        # Verify file exists and is valid JSON
        with open(save_file) as f:
            raw = json.load(f)
        assert raw["player_name"] == "Ash"
        assert raw["money"] == 2500
        assert "Boulder Badge" in raw["badges"]
        assert StoryFlag.BEAT_BROCK in raw["flags"]

        # Load and verify
        gs2 = GameState.load(save_file)
        assert gs2.player.name == "Ash"
        assert gs2.player.money == 2500
        assert "Boulder Badge" in gs2.player.badges
        assert gs2.has_flag(StoryFlag.BEAT_BROCK)
        assert gs2.has_flag(StoryFlag.OAK_PARCEL_DELIVERED)
        assert gs2.current_location == "Cerulean City"
        assert len(gs2.player.party) == 1
        assert gs2.player.party[0].species == "Pikachu"

    def test_gamestate_load_missing_file(self, tmp_path):
        from pykemon.story.events import GameState
        import pytest
        with pytest.raises(FileNotFoundError):
            GameState.load(str(tmp_path / "no_such_file.json"))


# ── 22. Locations & Story Path ────────────────────────────────────────────────

class TestLocations:
    """Tests for the Kanto location data."""

    def test_all_story_path_locations_exist(self):
        from pykemon.story.locations import LOCATIONS, STORY_PATH
        missing = [loc for loc in STORY_PATH if loc not in LOCATIONS]
        assert missing == [], f"Missing: {missing}"

    def test_story_path_starts_at_pallet(self):
        from pykemon.story.locations import STORY_PATH
        assert STORY_PATH[0] == "Pallet Town"

    def test_story_path_ends_at_indigo_plateau(self):
        from pykemon.story.locations import STORY_PATH
        assert STORY_PATH[-1] == "Indigo Plateau"

    def test_all_npc_trainer_classes_valid(self):
        from pykemon.story.locations import LOCATIONS
        from pykemon.core.trainer import TRAINER_CLASSES
        bad = []
        for loc_name, loc in LOCATIONS.items():
            for spec in loc.trainers:
                if spec.trainer_class not in TRAINER_CLASSES:
                    bad.append(f"{loc_name}/{spec.name}")
        assert bad == [], f"Invalid trainer classes: {bad}"

    def test_all_npc_party_species_valid(self):
        from pykemon.story.locations import LOCATIONS
        bad = []
        for loc_name, loc in LOCATIONS.items():
            for spec in loc.trainers:
                for species, lvl in spec.party:
                    try:
                        create_pokemon(species, lvl)
                    except Exception as e:
                        bad.append(f"{loc_name}/{spec.name}: {species}")
        assert bad == [], f"Invalid species: {bad}"

    def test_all_wild_encounter_species_valid(self):
        from pykemon.story.locations import LOCATIONS
        bad = []
        for loc_name, loc in LOCATIONS.items():
            for species, mn, mx in loc.wild_encounters:
                try:
                    create_pokemon(species, mn)
                except Exception as e:
                    bad.append(f"{loc_name}: {species}")
        assert bad == [], f"Invalid wild species: {bad}"

    def test_fish_encounters_valid(self):
        from pykemon.story.locations import LOCATIONS
        bad = []
        for loc_name, loc in LOCATIONS.items():
            for rod, pool in loc.fish_encounters.items():
                assert rod in ("Old Rod", "Good Rod", "Super Rod"), f"Unknown rod: {rod}"
                for species, mn, mx in pool:
                    try:
                        create_pokemon(species, mn)
                    except Exception as e:
                        bad.append(f"{loc_name}[{rod}]: {species}")
        assert bad == [], f"Invalid fish species: {bad}"

    def test_gym_locations_have_correct_gym_number(self):
        from pykemon.story.locations import LOCATIONS
        expected = {
            "Pewter City": 1, "Cerulean City": 2, "Vermilion City": 3,
            "Celadon City": 4, "Fuchsia City": 5, "Saffron City": 6,
            "Cinnabar Island": 7, "Viridian City (Return)": 8,
        }
        for city, num in expected.items():
            assert city in LOCATIONS, f"Missing location: {city}"
            assert LOCATIONS[city].gym_number == num, (
                f"{city} gym_number should be {num}"
            )

    def test_new_routes_present(self):
        from pykemon.story.locations import LOCATIONS
        for route in ("Route 5", "Route 7", "Route 8", "Route 22", "Route 24", "Route 25"):
            assert route in LOCATIONS, f"Missing: {route}"

    def test_pallet_has_fishing(self):
        from pykemon.story.locations import LOCATIONS
        loc = LOCATIONS["Pallet Town"]
        assert loc.fish_encounters
        assert "Old Rod" in loc.fish_encounters
        assert "Magikarp" in [s for s, *_ in loc.fish_encounters["Old Rod"]]

    def test_moltres_in_victory_road(self):
        from pykemon.story.locations import LOCATIONS
        loc = LOCATIONS["Victory Road"]
        species_names = [s for s, *_ in loc.wild_encounters]
        assert "Moltres" in species_names

    def test_bill_rescued_flag_exists(self):
        from pykemon.story.events import StoryFlag
        assert hasattr(StoryFlag, "BILL_RESCUED")
        assert StoryFlag.BILL_RESCUED == "BILL_RESCUED"

    def test_moltres_flag_exists(self):
        from pykemon.story.events import StoryFlag
        assert hasattr(StoryFlag, "MOLTRES_ENCOUNTERED")
        assert StoryFlag.MOLTRES_ENCOUNTERED == "MOLTRES_ENCOUNTERED"


# ── 23. Rival ─────────────────────────────────────────────────────────────────

class TestRival:
    def test_build_rival_returns_trainer(self):
        from pykemon.story.rival import build_rival, RIVAL_NAME
        rival = build_rival(0)
        assert rival is not None
        assert rival.name == RIVAL_NAME
        assert len(rival.party) >= 1

    def test_rival_escalates_over_encounters(self):
        from pykemon.story.rival import build_rival
        r0 = build_rival(0)
        r4 = build_rival(4)
        max_lv0 = max(p.level for p in r0.party)
        max_lv4 = max(p.level for p in r4.party)
        assert max_lv4 > max_lv0

    def test_rival_party_size_grows(self):
        from pykemon.story.rival import build_rival
        r0 = build_rival(0)
        r5 = build_rival(5)
        assert len(r5.party) >= len(r0.party)

    def test_rival_all_encounters_valid(self):
        from pykemon.story.rival import build_rival
        for i in range(6):
            rival = build_rival(i)
            assert len(rival.party) >= 1
            for mon in rival.party:
                assert mon.level >= 1


# ── 24. Bird Keeper trainer class ─────────────────────────────────────────────

class TestBirdKeeperClass:
    def test_bird_keeper_in_trainer_classes(self):
        from pykemon.core.trainer import TRAINER_CLASSES
        assert "Bird Keeper" in TRAINER_CLASSES

    def test_bird_keeper_payout(self):
        from pykemon.core.trainer import TRAINER_CLASSES
        tc = TRAINER_CLASSES["Bird Keeper"]
        assert tc.payout_multiplier > 0
