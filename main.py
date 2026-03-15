#!/usr/bin/env python3
"""
Pykemon — Main game entry point.
A text-based Pokémon RPG built in Python, following the Kanto story.

Usage:
    python main.py
"""

from __future__ import annotations
import sys
import random
from typing import Optional

from pykemon import (
    Pokemon, create_pokemon, Trainer, Battle, BattleResult,
    PokemonCenter, PokeMart, GymBadgeSystem, FossilLab, RideSystem,
    SPECIES, MOVES, ITEMS,
    check_evolution, evolve,
    update_friendship,
    get_time_of_day, describe_time,
    StoryFlag, GameState,
    build_rival, RIVAL_NAME,
    LOCATIONS, LocationService, STORY_PATH,
)
from pykemon.world.gym import GymChallenge


# ── Utility ───────────────────────────────────────────────────────────────────

def clear() -> None:
    print("\n" * 2)

def prompt(msg: str = "> ") -> str:
    try:
        return input(msg).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        sys.exit(0)

def press_enter(msg: str = "Press ENTER to continue...") -> None:
    prompt(msg)

def print_divider(char: str = "─", width: int = 50) -> None:
    print(char * width)

def say(text: str, player_name: str = "") -> None:
    print(text.replace("{player}", player_name))

def choose_from_list(options: list, title: str = "Choose:") -> int:
    print(f"\n{title}")
    print_divider()
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    print("  0. Back / Skip")
    print_divider()
    while True:
        raw = prompt("> ")
        if raw == "0":
            return -1
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return idx
        print(f"Please enter 0-{len(options)}.")


# ── Battle UI ─────────────────────────────────────────────────────────────────

def fight_menu(mon: Pokemon) -> tuple:
    print(f"\n  {mon.nickname}'s moves:")
    for i, move_obj in enumerate(mon.moves, 1):
        type_str = move_obj.data.move_type.value
        cat_str  = move_obj.data.category.value
        print(f"  {i}. {move_obj.data.name:<18} PP:{move_obj.pp}/{move_obj.pp_max}  [{type_str}]  [{cat_str}]  Pwr:{move_obj.data.power}")
    print("  0. Back")
    while True:
        raw = prompt("> ")
        if raw == "0":
            return ("move", 0)
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(mon.moves):
                return ("move", idx)
        print(f"Enter 1-{len(mon.moves)} or 0.")

def bag_menu_in_battle(player: Trainer, battle: Battle) -> tuple:
    medicine  = player.bag.medicine()
    pokeballs = player.bag.pokeballs()
    categories = []
    if medicine:
        categories.append("Medicine")
    if pokeballs and battle.is_wild:
        categories.append("Poké Balls")
    if not categories:
        print("  (Nothing useful in bag right now.)")
        return ("move", 0)
    choice = choose_from_list(categories, "Bag Pocket:")
    if choice < 0:
        return ("move", 0)
    pocket_name = categories[choice]
    items = list(medicine.items()) if pocket_name == "Medicine" else list(pokeballs.items())
    item_choices = [f"{name} x{qty}" for name, qty in items]
    item_idx = choose_from_list(item_choices, f"Select {pocket_name}:")
    if item_idx < 0:
        return ("move", 0)
    item_name, _ = items[item_idx]
    if pocket_name == "Poké Balls":
        success, msgs = battle.attempt_catch(item_name)
        player.bag.remove_item(item_name, 1)
        for msg in msgs:
            print(f"  {msg}")
        if success:
            player.add_pokemon(battle.opponent_pokemon)
            if player.pokedex:
                player.pokedex.register_caught(battle.opponent_pokemon)
        press_enter()
        return ("item", item_name, 0)
    party_choices = [f"{m.nickname} ({m.current_hp}/{m.max_hp} HP)" for m in player.party]
    target_idx = choose_from_list(party_choices, "Use on which Pokémon?")
    if target_idx < 0:
        return ("move", 0)
    return ("item", item_name, target_idx)

def switch_menu(trainer: Trainer):
    choices = []
    for mon in trainer.party:
        status = " [FAINTED]" if mon.fainted else f" {mon.hp_bar}"
        choices.append(f"{mon.nickname} Lv.{mon.level}{status}")
    idx = choose_from_list(choices, "Send out which Pokémon?")
    if idx < 0:
        return ("move", 0)
    if trainer.party[idx].fainted:
        print("  That Pokémon has fainted!")
        return switch_menu(trainer)
    return ("switch", idx)

def battle_menu(battle: Battle, player: Trainer):
    mon      = battle.player_pokemon
    opponent = battle.opponent_pokemon
    print()
    print_divider("═")
    print(f"  {opponent}")
    print_divider()
    print(f"  {mon}")
    print_divider("═")
    print()
    print("  1. Fight        2. Bag")
    print("  3. Pokémon      4. Run")
    print_divider()
    choice = prompt("> ")
    if choice == "1":
        return fight_menu(mon)
    elif choice == "2":
        return bag_menu_in_battle(player, battle)
    elif choice == "3":
        return switch_menu(player)
    elif choice == "4":
        return "run"
    else:
        print("Invalid choice.")
        return battle_menu(battle, player)

def run_battle_loop(battle: Battle, player: Trainer) -> str:
    opp = battle.opponent_pokemon
    print()
    print_divider("═")
    if battle.is_wild:
        shiny = " ✨ A shiny" if opp.is_shiny else " A wild"
        print(f"{shiny} {opp.species.name} appeared!  (Lv.{opp.level})")
    else:
        tc = battle.opponent.trainer_class.title_prefix
        prefix = f"{tc} " if tc else ""
        print(f"  {prefix}{battle.opponent.name} wants to battle!")
        print(f"  {battle.opponent.name} sent out {opp.nickname}!  (Lv.{opp.level})")
    print_divider("═")
    if player.pokedex:
        player.pokedex.register_seen(opp)
    while battle.result is None:
        action = battle_menu(battle, player)
        msgs   = battle.run_turn(action)
        for msg in msgs:
            if msg:
                print(f"  {msg}")
        print()
        if battle.player_pokemon.fainted and player.has_usable_pokemon():
            if battle.result is None:
                print("  Choose your next Pokémon!")
                battle.run_turn(switch_menu(player))
    print_divider()
    result = battle.result
    if result == BattleResult.WIN:
        print("  You won the battle!")
        if not battle.is_wild and battle.opponent.dialogue_win:
            say(f"  {battle.opponent.name}: {battle.opponent.dialogue_win}", player.name)
    elif result == BattleResult.LOSE:
        print("  You lost…")
    elif result == BattleResult.RUN:
        print("  You got away safely!")
    elif result == BattleResult.CATCH:
        print(f"  Caught {battle.opponent_pokemon.nickname}!")
    press_enter()
    return result


# ── Evolution ─────────────────────────────────────────────────────────────────

def handle_evolution(mon: Pokemon, player: Trainer) -> None:
    cond = check_evolution(mon, time_of_day=get_time_of_day())
    if cond is None:
        return
    old_name = mon.species.name
    print()
    print_divider("✦")
    print(f"  What? {mon.nickname} is evolving!")
    if prompt("  Press ENTER to evolve, or type 'cancel': ").lower() == "cancel":
        print(f"  {mon.nickname} stopped evolving!")
        return
    evolve(mon, cond)
    print(f"  {old_name} evolved into {mon.species.name}!")
    if player.pokedex:
        player.pokedex.register_caught(mon)
    press_enter()


# ── Wild encounter ────────────────────────────────────────────────────────────

def wild_encounter(gs: GameState, center: PokemonCenter) -> None:
    loc = LOCATIONS.get(gs.current_location)
    if not loc or not loc.wild_encounters:
        print(f"  (No wild Pokémon on {gs.current_location}.)")
        return
    entry = random.choice(loc.wild_encounters)
    species_name, min_lvl, max_lvl = entry
    if species_name not in SPECIES:
        return
    level = random.randint(min_lvl, max_lvl)
    wild  = create_pokemon(species_name, level, is_wild=True)
    if gs.player.first_usable_idx() < 0:
        print("  You have no usable Pokémon!")
        return
    wild_trainer = Trainer("Wild", party=[wild])
    battle = Battle(gs.player, wild_trainer, is_wild=True)
    result = run_battle_loop(battle, gs.player)
    if result == BattleResult.WIN:
        for mon in gs.player.party:
            if not mon.fainted:
                handle_evolution(mon, gs.player)
    if not gs.player.has_usable_pokemon():
        print("  You blacked out!  Returning to the Pokémon Center…")
        center.heal_party(gs.player)
        press_enter()


# ── NPC trainer battle ────────────────────────────────────────────────────────

def npc_battle(gs: GameState, npc_spec, center: PokemonCenter) -> bool:
    player = gs.player
    npc_party = []
    for species, lvl in npc_spec.party:
        try:
            mon = create_pokemon(species, lvl, trainer_name=npc_spec.name)
        except ValueError:
            mon = create_pokemon("Rattata", lvl, trainer_name=npc_spec.name)
        npc_party.append(mon)
    npc = Trainer(
        name=npc_spec.name,
        trainer_class=npc_spec.trainer_class,
        party=npc_party,
        money=npc_spec.money,
    )
    npc.dialogue_intro = npc_spec.dialogue_intro
    npc.dialogue_win   = npc_spec.dialogue_win
    npc.dialogue_lose  = npc_spec.dialogue_lose
    if npc.dialogue_intro:
        say(f"\n  {npc.name}: {npc.dialogue_intro}", player.name)
        press_enter()
    battle = Battle(player, npc, is_wild=False)
    result = run_battle_loop(battle, player)
    if result == BattleResult.WIN:
        prize = npc.calculate_prize()
        player.money += prize
        print(f"  You received ₽{prize}!")
        for mon in player.party:
            if not mon.fainted:
                handle_evolution(mon, player)
        if not player.has_usable_pokemon():
            center.heal_party(player)
        press_enter()
        return True
    else:
        if not player.has_usable_pokemon():
            center.heal_party(player)
            press_enter()
        return False


# ── Rival battle ──────────────────────────────────────────────────────────────

def rival_battle(gs: GameState, encounter_index: int, center: PokemonCenter) -> bool:
    player = gs.player
    starter_name = player.party[0].species.name if player.party else None
    rival = build_rival(encounter_index, starter_name)
    say(f"\n{rival.dialogue_intro}", player.name)
    press_enter()
    battle = Battle(player, rival, is_wild=False)
    result = run_battle_loop(battle, player)
    if result == BattleResult.WIN:
        prize = rival.calculate_prize()
        player.money += prize
        print(f"  You received ₽{prize}!")
        for mon in player.party:
            if not mon.fainted:
                handle_evolution(mon, player)
        press_enter()
        if not player.has_usable_pokemon():
            center.heal_party(player)
        return True
    else:
        if not player.has_usable_pokemon():
            center.heal_party(player)
            press_enter()
        return False


# ── Gym battle ────────────────────────────────────────────────────────────────

def gym_battle(gs: GameState, gym_ch: GymChallenge, center: PokemonCenter) -> None:
    player = gs.player
    if not gym_ch.can_challenge(player):
        print(f"\n  {gym_ch.challenge_refused_message()}")
        press_enter()
        return
    print(gym_ch.gym_header())
    press_enter()
    # Gym trainers
    for trainer in gym_ch.get_gym_trainers():
        if getattr(trainer, "defeated", False):
            continue
        if trainer.dialogue_intro:
            say(f"\n  {trainer.name}: {trainer.dialogue_intro}", player.name)
            press_enter()
        trainer.heal_party()
        battle = Battle(player, trainer, is_wild=False)
        result = run_battle_loop(battle, player)
        if result == BattleResult.WIN:
            trainer.defeated = True
            prize = trainer.calculate_prize()
            player.money += prize
            print(f"  You received ₽{prize}!")
            for mon in player.party:
                if not mon.fainted:
                    handle_evolution(mon, player)
        else:
            print("  You were defeated!  Heal up and try again!")
            if not player.has_usable_pokemon():
                center.heal_party(player)
            press_enter()
            gym_ch.reset_gym_trainers()
            return
    # Leader
    print_divider("═")
    say(f"\n  {gym_ch.leader.dialogue_intro}", player.name)
    press_enter()
    gym_ch.leader.heal_party()
    battle = Battle(player, gym_ch.leader, is_wild=False)
    result = run_battle_loop(battle, player)
    if result == BattleResult.WIN:
        msgs = gym_ch.award_badge(player)
        for msg in msgs:
            say(f"  {msg}", player.name)
        press_enter()
        for mon in player.party:
            if not mon.fainted:
                handle_evolution(mon, player)
    else:
        print("  Return to a Pokémon Center and try again!")
        if not player.has_usable_pokemon():
            center.heal_party(player)
        press_enter()
        gym_ch.reset_gym_trainers()


# ── Story event triggers ──────────────────────────────────────────────────────

def _trigger_story_events(gs, loc, center, mart, gym_system):
    player = gs.player
    for flag, narrative in (loc.story_events or {}).items():
        if gs.has_flag(flag):
            continue
        if flag == "OAK_LAB_INTRO":
            gs.set_flag(flag)
        elif flag == "BEAT_RIVAL_PALLET":
            say(f"\n{narrative}", player.name)
            press_enter()
            if rival_battle(gs, 0, center):
                gs.set_flag(StoryFlag.BEAT_RIVAL_PALLET)
            gs.set_flag(flag)
        elif flag == "OAK_PARCEL_DELIVERED":
            say(f"\n{narrative}", player.name)
            player.bag.add_item("Poké Ball", 5)
            press_enter()
            gs.set_flag(flag)
            gs.set_flag(StoryFlag.OAK_PARCEL_DELIVERED)
        elif flag == "MT_MOON_ROCKET_DEFEATED":
            from pykemon.story.locations import NpcTrainerSpec as NTS
            say(f"\n  Team Rocket is blocking the cave!", player.name)
            press_enter()
            for spec in [
                NTS("Rocket Grunt A", "Rocket Grunt", [("Sandshrew", 13), ("Rattata", 14)],
                    dialogue_intro="Team Rocket forbids passage!"),
                NTS("Rocket Grunt B", "Rocket Grunt", [("Zubat", 12), ("Rattata", 14), ("Zubat", 14)],
                    dialogue_intro="The fossils belong to Team Rocket!"),
            ]:
                if not npc_battle(gs, spec, center):
                    return
            say(f"\n{narrative}", player.name)
            press_enter()
            fossil_choice = choose_from_list(
                ["Dome Fossil (Kabuto)", "Helix Fossil (Omanyte)"],
                "The scientist offers you a fossil — choose one:"
            )
            if fossil_choice == 0:
                player.bag.add_item("Dome Fossil")
                print("  You took the Dome Fossil!")
            else:
                player.bag.add_item("Helix Fossil")
                print("  You took the Helix Fossil!")
            press_enter()
            gs.set_flag(StoryFlag.MT_MOON_ROCKET_DEFEATED)
            gs.set_flag(flag)
        elif flag == "BEAT_RIVAL_CERULEAN":
            say(f"\n{narrative}", player.name)
            press_enter()
            if rival_battle(gs, 1, center):
                gs.set_flag(StoryFlag.BEAT_RIVAL_CERULEAN)
            gs.set_flag(flag)
        elif flag == "SS_ANNE_VISITED":
            say(f"\n{narrative}", player.name)
            press_enter()
            if rival_battle(gs, 2, center):
                gs.set_flag(StoryFlag.BEAT_RIVAL_SS_ANNE)
                try:
                    player.bag.add_item("HM01")
                    print("  You received HM01 (Cut)!")
                except Exception:
                    pass
            gs.set_flag(flag)
        elif flag == "BEAT_RIVAL_SS_ANNE":
            gs.set_flag(flag)
        elif flag == "POKEMON_TOWER_GHOST":
            say(f"\n{narrative}", player.name)
            press_enter()
            from pykemon.story.locations import NpcTrainerSpec as NTS
            npc_battle(gs, NTS("Ghost Marowak", "Wild", [("Marowak", 30)],
                               dialogue_intro="A ghostly Marowak blocks your path!"), center)
            gs.set_flag(StoryFlag.POKEMON_TOWER_GHOST)
            gs.set_flag(flag)
        elif flag == "GAME_CORNER_CLEARED":
            from pykemon.story.locations import NpcTrainerSpec as NTS
            say(f"\n  You enter Team Rocket's hideout under the Game Corner!", player.name)
            press_enter()
            for spec in [
                NTS("Rocket Grunt C", "Rocket Grunt", [("Ekans", 22), ("Zubat", 24)],
                    dialogue_intro="Team Rocket runs this town!"),
                NTS("Rocket Grunt D", "Rocket Grunt", [("Koffing", 24), ("Drowzee", 26)],
                    dialogue_intro="No one gets past me!"),
                NTS("Giovanni", "Rocket Grunt", [("Nidorino", 30), ("Kangaskhan", 32)],
                    dialogue_intro="I am the boss of this hideout!"),
            ]:
                if not npc_battle(gs, spec, center):
                    return
            say(f"\n{narrative}", player.name)
            press_enter()
            if len(player.party) < 6:
                eevee = create_pokemon("Eevee", 25, trainer_name=player.name)
                player.add_pokemon(eevee)
                print("  You received a free Eevee!")
                press_enter()
            gs.set_flag(StoryFlag.GAME_CORNER_CLEARED)
            gs.set_flag(flag)
        elif flag == "BEAT_RIVAL_SILPH":
            say(f"\n{narrative}", player.name)
            press_enter()
            if rival_battle(gs, 3, center):
                gs.set_flag(StoryFlag.BEAT_RIVAL_SILPH)
            gs.set_flag(flag)
        elif flag == "SILPH_CO_CLEARED":
            from pykemon.story.locations import NpcTrainerSpec as NTS
            say(f"\n  Silph Co. has been taken over by Team Rocket!", player.name)
            press_enter()
            for spec in [
                NTS("Rocket Grunt F", "Rocket Grunt", [("Arbok", 34), ("Rattata", 32)],
                    dialogue_intro="Silph Co. belongs to us!"),
                NTS("Rocket Grunt G", "Rocket Grunt", [("Golbat", 36), ("Zubat", 35)],
                    dialogue_intro="Get out, kid!"),
                NTS("Giovanni", "Rocket Boss", [("Nidorino", 37), ("Kangaskhan", 35), ("Rhydon", 45)],
                    dialogue_intro="You dare challenge me here?!"),
            ]:
                if not npc_battle(gs, spec, center):
                    return
            say(f"\n{narrative}", player.name)
            press_enter()
            try:
                player.bag.add_item("Master Ball")
                print("  You received the Master Ball from the Silph Co. President!")
            except Exception:
                pass
            press_enter()
            gs.set_flag(StoryFlag.SILPH_CO_CLEARED)
            gs.set_flag(flag)
        elif flag == "SEAFOAM_VISITED":
            say(f"\n{narrative}", player.name)
            press_enter()
            articuno = create_pokemon("Articuno", 50, is_wild=True)
            wild_t = Trainer("Wild", party=[articuno])
            run_battle_loop(Battle(player, wild_t, is_wild=True), player)
            gs.set_flag(StoryFlag.SEAFOAM_VISITED)
            gs.set_flag(flag)
        elif flag == "BEAT_RIVAL_VICTORY_ROAD":
            say(f"\n{narrative}", player.name)
            press_enter()
            if rival_battle(gs, 4, center):
                gs.set_flag(StoryFlag.BEAT_RIVAL_VICTORY_ROAD)
            gs.set_flag(flag)
        elif flag == "BEAT_CHAMPION":
            gs.set_flag(flag)
        elif flag == "POWER_PLANT_VISITED":
            say(f"\n{narrative}", player.name)
            press_enter()
            zapdos = create_pokemon("Zapdos", 50, is_wild=True)
            wild_t = Trainer("Wild", party=[zapdos])
            result = run_battle_loop(Battle(player, wild_t, is_wild=True), player)
            if result == BattleResult.CATCH:
                print("  You caught the legendary ZAPDOS!")
            gs.set_flag(StoryFlag.POWER_PLANT_VISITED)
            gs.set_flag(flag)
        elif flag == "MANSION_VISITED":
            say(f"\n{narrative}", player.name)
            press_enter()
            gs.set_flag(StoryFlag.MANSION_VISITED)
            gs.set_flag(flag)
        elif flag == "CERULEAN_CAVE_VISITED":
            if gs.has_flag(StoryFlag.HALL_OF_FAME):
                say(f"\n  You enter Cerulean Cave — few trainers survive its depths.", player.name)
                press_enter()
                mewtwo = create_pokemon("Mewtwo", 70, is_wild=True)
                wild_t = Trainer("Wild", party=[mewtwo])
                result = run_battle_loop(Battle(player, wild_t, is_wild=True), player)
                if result == BattleResult.CATCH:
                    print("  You caught the legendary MEWTWO!")
                gs.set_flag(StoryFlag.CERULEAN_CAVE_VISITED)
                gs.set_flag(flag)
            else:
                print("  A guard blocks the cave.  'Only the Pokémon League Champion may enter!'")
                press_enter()
        else:
            say(f"\n{narrative}", player.name)
            press_enter()
            gs.set_flag(flag)


# ── Pokémon League ────────────────────────────────────────────────────────────

def run_pokemon_league(gs: GameState, center: PokemonCenter,
                       gym_system: GymBadgeSystem) -> None:
    player = gs.player
    league = gym_system.league
    if not league.can_challenge(player):
        print("  You need all 8 Badges to enter the Pokémon League!")
        press_enter()
        return
    print()
    print_divider("★")
    print("  Welcome to the Pokémon League!")
    print("  Defeat the Elite Four, then face the Champion.")
    print_divider("★")
    press_enter()
    league.reset()
    while not league.is_complete() and player.has_usable_pokemon():
        opponent = league.next_opponent()
        if not opponent:
            break
        intro = league.elite_four_intro(league.current_member_idx)
        say(f"\n{intro}", player.name)
        press_enter()
        opponent.heal_party()
        battle = Battle(player, opponent, is_wild=False)
        result = run_battle_loop(battle, player)
        if result == BattleResult.WIN:
            for mon in player.party:
                if not mon.fainted:
                    handle_evolution(mon, player)
            if league.advance():
                print("  Press on to the next challenger!")
                center.heal_party(player)
                press_enter()
            else:
                # Elite Four done — Gary is Champion
                print("\n  Gary is the reigning Pokémon League Champion!")
                won = rival_battle(gs, 5, center)
                if won:
                    print()
                    print_divider("★")
                    print(f"  {player.name} is the new Pokémon League Champion!")
                    print("  Your name is enshrined in the Hall of Fame forever!")
                    print_divider("★")
                    gs.set_flag(StoryFlag.BEAT_CHAMPION)
                    gs.set_flag(StoryFlag.HALL_OF_FAME)
                press_enter()
                return
        else:
            print("  You were defeated!  Train harder and return!")
            if not player.has_usable_pokemon():
                center.heal_party(player)
            press_enter()
            return


# ── Location explore menu ─────────────────────────────────────────────────────

def location_menu(gs: GameState, center: PokemonCenter, mart: PokeMart,
                  gym_system: GymBadgeSystem, fossil_lab: FossilLab,
                  ride_system: RideSystem) -> None:
    loc    = LOCATIONS.get(gs.current_location)
    player = gs.player
    while True:
        clear()
        print_divider("═")
        print(f"  ► {gs.current_location}  [{describe_time()}]")
        print(f"  {player.name}  ₽{player.money:,}  Badges: {len(player.badges)}/8")
        print_divider("═")
        if loc:
            print()
            print(loc.description)
        print()
        actions = []
        if loc and loc.wild_encounters:
            actions.append(("walk",    "Walk in tall grass (Wild Encounter)"))
        if loc and loc.trainers:
            actions.append(("trainers","Battle local trainers"))
        if loc and LocationService.POKEMON_CENTER in (loc.services or []):
            actions.append(("center",  "Pokémon Center (Heal)"))
        if loc and LocationService.POKE_MART in (loc.services or []):
            actions.append(("mart",    "Poké Mart"))
        if loc and loc.gym_number:
            gym_ch = gym_system.get_gym(loc.gym_number)
            if gym_ch and not player.has_badge(gym_ch.gym.badge_name):
                actions.append(("gym",  f"★ Challenge Gym ({gym_ch.gym.leader_name})"))
        if loc and LocationService.FOSSIL_LAB in (loc.services or []):
            actions.append(("fossils", "Fossil Revival Lab"))
        if loc and LocationService.SAFARI_ZONE in (loc.services or []):
            actions.append(("safari",  "Enter Safari Zone"))
        if loc and LocationService.SEAFOAM_CAVE in (loc.services or []):
            actions.append(("seafoam", "Explore Seafoam Islands cave"))
        actions += [
            ("party",   "View Party"),
            ("bag",     "Bag"),
            ("pokedex", "Pokédex"),
            ("ride",    "Ride Pokémon"),
            ("badges",  "Badge Case"),
            ("travel",  "Travel to next location →"),
            ("quit",    "Save & Quit"),
        ]
        idx = choose_from_list([a[1] for a in actions], "What will you do?")
        if idx < 0:
            continue
        key = actions[idx][0]
        if key == "quit":
            print("\n  Thanks for playing Pykemon!  Goodbye!")
            sys.exit(0)
        elif key == "walk":
            wild_encounter(gs, center)
        elif key == "trainers":
            if loc and loc.trainers:
                labels = [f"{t.name} ({t.trainer_class})" for t in loc.trainers]
                ti = choose_from_list(labels, "Battle which trainer?")
                if ti >= 0:
                    npc_battle(gs, loc.trainers[ti], center)
        elif key == "center":
            for msg in center.heal_party(player):
                print(f"  {msg}")
            press_enter()
        elif key == "mart":
            badge_count = len(player.badges)
            print(mart.display_stock(badge_count))
            while True:
                raw = prompt("Buy item (name) or 'done': ").strip()
                if raw.lower() == "done":
                    break
                count_raw = prompt("  How many? ").strip()
                count = int(count_raw) if count_raw.isdigit() else 1
                ok, msg = mart.buy(player, raw, count, badge_count)
                print(f"  {msg}")
        elif key == "gym":
            gym_ch = gym_system.get_gym(loc.gym_number)
            if gym_ch:
                gym_battle(gs, gym_ch, center)
        elif key == "fossils":
            print(fossil_lab.display())
            fn = prompt("  Which fossil to revive? (or 'done'): ")
            if fn.lower() != "done":
                pokemon, msgs = fossil_lab.revive(player, fn)
                for msg in msgs:
                    print(f"  {msg}")
                press_enter()
        elif key in ("safari", "seafoam"):
            wild_encounter(gs, center)
        elif key == "party":
            print(player.party_status())
            idx2 = choose_from_list([f"{m.nickname} — summary" for m in player.party], "View:")
            if idx2 >= 0:
                print(player.party[idx2].summary())
            press_enter()
        elif key == "bag":
            print(player.bag.display())
            raw = prompt("  Use an item? (name or 'done'): ")
            if raw.lower() != "done" and raw:
                item_data = ITEMS.get(raw)
                if item_data and item_data.hp_restore:
                    pcs = [f"{m.nickname} ({m.current_hp}/{m.max_hp} HP)" for m in player.party]
                    idx3 = choose_from_list(pcs, "Use on:")
                    if idx3 >= 0:
                        tgt = player.party[idx3]
                        tgt.heal(tgt.max_hp if item_data.hp_restore == -1 else item_data.hp_restore)
                        player.bag.remove_item(raw, 1)
                        print(f"  Used {raw} on {tgt.nickname}!")
            press_enter()
        elif key == "pokedex":
            if player.pokedex:
                print(player.pokedex.list_all())
                raw = prompt("  Look up a Pokémon (name or #): ")
                if raw:
                    try:
                        entry = player.pokedex.lookup(int(raw) if raw.isdigit() else raw)
                    except Exception as e:
                        entry = str(e)
                    print(entry or "No data.")
            press_enter()
        elif key == "ride":
            print(ride_system.display())
            raw = prompt("  Mount which Pokémon? (name or 'done'): ")
            if raw.lower() != "done":
                msg = ride_system.use(raw)
                print(f"  {msg}" if msg else "  That Pokémon isn't available.")
            press_enter()
        elif key == "badges":
            print(gym_system.all_badges_summary(player))
            press_enter()
        elif key == "travel":
            return


# ── Prologue ──────────────────────────────────────────────────────────────────

def prologue():
    clear()
    print("=" * 60)
    print(" " * 16 + "★  PYKEMON  ★")
    print(" " * 8 + "A Pokémon Adventure in Python")
    print("=" * 60)
    print()
    print(
        "Professor Oak: Hello there!\n"
        "Welcome to the world of POKÉMON!\n"
        "My name is Oak — people call me the Pokémon Professor.\n"
        "\nThis world is inhabited by creatures called POKÉMON!\n"
        "For some people, POKÉMON are pets.  Others use them for fights.\n"
        "Myself… I study POKÉMON as a profession.\n"
        "\nYour very own Pokémon adventure is about to unfold.\n"
        "A world of dreams and adventures with POKÉMON awaits!  Let's go!\n"
    )
    name = prompt("What is your name, Trainer? ").strip() or "Red"
    print(f"\nProfessor Oak: So your name is {name}!\n")
    press_enter()
    starters = ["Bulbasaur", "Charmander", "Squirtle"]
    print("Professor Oak: These three Pokémon are all I have left today.\n")
    for i, sname in enumerate(starters, 1):
        sp = SPECIES[sname]
        types_str = "/".join(t.value for t in sp.types)
        print(f"  {i}. {sname:<12} [{types_str}]  —  {sp.pokedex_entry[:60]}")
    print()
    while True:
        raw = prompt("Choose your starter (1/2/3): ")
        if raw.isdigit() and 1 <= int(raw) <= 3:
            chosen = starters[int(raw) - 1]
            mon = create_pokemon(chosen, 5, trainer_name=name)
            print(f"\n  {name} received {chosen}!")
            press_enter()
            return name, mon
        print("  Please enter 1, 2, or 3.")


# ── Story loop ────────────────────────────────────────────────────────────────

def story_loop(gs: GameState, center: PokemonCenter, mart: PokeMart,
               gym_system: GymBadgeSystem, fossil_lab: FossilLab,
               ride_system: RideSystem) -> None:
    player = gs.player
    loc_names = STORY_PATH.copy()
    start_idx = 0
    if gs.current_location in loc_names:
        start_idx = loc_names.index(gs.current_location)
    for loc_name in loc_names[start_idx:]:
        gs.travel_to(loc_name)
        loc = LOCATIONS.get(loc_name)
        clear()
        print_divider("═")
        print(f"  ► {loc_name}")
        print_divider("═")
        if loc:
            print()
            print(loc.description)
        print()
        press_enter()
        if loc:
            _trigger_story_events(gs, loc, center, mart, gym_system)
        if loc_name == "Indigo Plateau":
            run_pokemon_league(gs, center, gym_system)
            if gs.has_flag(StoryFlag.HALL_OF_FAME):
                _credits(player.name)
            return
        location_menu(gs, center, mart, gym_system, fossil_lab, ride_system)
    print("\n  You have completed your Kanto adventure!  Thank you for playing!")
    press_enter()


def _credits(player_name: str) -> None:
    print()
    print("═" * 60)
    print(" " * 20 + "★  HALL OF FAME  ★")
    print("═" * 60)
    print(f"\n  {player_name} — Pokémon League Champion!")
    print("\n  Thank you for playing PYKEMON!")
    print("  A complete Pokémon adventure built in Python.")
    print()
    print("═" * 60)
    press_enter()


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    name, starter = prologue()
    player = Trainer(name=name, trainer_class="Player", money=3000, is_player=True)
    player.add_pokemon(starter)
    player.bag.add_item("Poké Ball", 5)
    player.bag.add_item("Potion", 5)
    gs = GameState(player, starting_location="Pallet Town")
    gs.set_flag(StoryFlag.RECEIVED_STARTER)
    center     = PokemonCenter("Pallet Town")
    mart       = PokeMart("Viridian City")
    gym_system = GymBadgeSystem()
    fossil_lab = FossilLab("Cinnabar Island")
    ride_system = RideSystem()
    print(f"\n  Professor Oak: Here are some Pokéballs, {name}!")
    print(f"  {describe_time()}")
    press_enter()
    story_loop(gs, center, mart, gym_system, fossil_lab, ride_system)


if __name__ == "__main__":
    main()
