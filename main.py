#!/usr/bin/env python3
"""
Pykemon — Main game entry point.
A text-based Pokémon RPG built in Python.

Usage:
    python main.py
    python -m pykemon.main
"""

from __future__ import annotations
import sys
import random
from typing import Optional

from pykemon import (
    Pokemon, create_pokemon, Trainer, Battle, BattleResult,
    PokemonCenter, PokeMart, GymBadgeSystem, FossilLab, RideSystem,
    SPECIES, SPECIES_BY_NUM, MOVES, ITEMS,
    check_evolution, evolve,
    update_friendship, friendship_tier,
    get_time_of_day, describe_time,
    StatusEffect, WeatherEffect,
)
from pykemon.data.pokemon_data import EvolutionCondition
from pykemon.world.gym import GymChallenge


# ── Utility ───────────────────────────────────────────────────────────────────

def clear() -> None:
    """Clear the screen (or print blank lines in constrained environments)."""
    print("\n" * 3)


def prompt(msg: str = "> ") -> str:
    """Prompt the user for input."""
    try:
        return input(msg).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        sys.exit(0)


def press_enter(msg: str = "Press ENTER to continue...") -> None:
    prompt(msg)


def print_divider(char: str = "─", width: int = 50) -> None:
    print(char * width)


def choose_from_list(options: list[str], title: str = "Choose:") -> int:
    """
    Present a numbered list and return the 0-indexed choice.
    Returns -1 if the user chooses to go back.
    """
    print(f"\n{title}")
    print_divider()
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    print("  0. Back")
    print_divider()
    while True:
        raw = prompt("> ")
        if raw == "0":
            return -1
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return idx
        print(f"Please enter a number between 0 and {len(options)}.")


# ── Battle UI ─────────────────────────────────────────────────────────────────

def battle_menu(
    battle: Battle,
    player: Trainer,
) -> "str | tuple":
    """
    Display the battle menu and return the player's chosen action.
    """
    mon = battle.player_pokemon
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


def fight_menu(mon: Pokemon) -> tuple:
    """Display move selection and return ('move', index)."""
    print(f"\n  {mon.nickname}'s moves:")
    for i, move_obj in enumerate(mon.moves, 1):
        type_str = move_obj.data.move_type.value
        cat_str = move_obj.data.category.value
        print(f"  {i}. {move_obj.data.name:<18} PP:{move_obj.pp}/{move_obj.pp_max}  "
              f"[{type_str}]  [{cat_str}]  Pwr:{move_obj.data.power}")
    print("  0. Back")
    while True:
        raw = prompt("> ")
        if raw == "0":
            return ("move", 0)   # default
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(mon.moves):
                return ("move", idx)
        print(f"Enter 1-{len(mon.moves)} or 0.")


def bag_menu_in_battle(player: Trainer, battle: Battle) -> tuple:
    """Use an item from the bag during battle."""
    medicine = player.bag.medicine()
    pokeballs = player.bag.pokeballs()

    categories = []
    if medicine:
        categories.append("Medicine")
    if pokeballs and battle.is_wild:
        categories.append("Poké Balls")

    if not categories:
        print("  (Your bag has nothing useful right now.)")
        return ("move", 0)

    choice = choose_from_list(categories, "Bag Pocket:")
    if choice < 0:
        return ("move", 0)

    pocket_name = categories[choice]
    if pocket_name == "Medicine":
        items = list(medicine.items())
    else:
        items = list(pokeballs.items())

    item_choices = [f"{name} x{qty}" for name, qty in items]
    item_idx = choose_from_list(item_choices, f"Select {pocket_name}:")
    if item_idx < 0:
        return ("move", 0)

    item_name, _ = items[item_idx]

    # For Poké Balls, catch immediately
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
        return ("item", item_name, 0)  # Dummy; handled above

    # Medicine — choose target
    party_choices = [f"{m.nickname} ({m.current_hp}/{m.max_hp} HP)" for m in player.party]
    target_idx = choose_from_list(party_choices, "Use on which Pokémon?")
    if target_idx < 0:
        return ("move", 0)

    return ("item", item_name, target_idx)


def switch_menu(trainer: Trainer) -> "str | tuple":
    """Display party and allow switching."""
    choices = []
    for i, mon in enumerate(trainer.party):
        status = " [FAINTED]" if mon.fainted else f" {mon.hp_bar}"
        choices.append(f"{mon.nickname} Lv.{mon.level}{status}")
    idx = choose_from_list(choices, "Send out which Pokémon?")
    if idx < 0:
        return ("move", 0)
    if trainer.party[idx].fainted:
        print("  That Pokémon has fainted!")
        return switch_menu(trainer)
    return ("switch", idx)


def run_battle_loop(battle: Battle, player: Trainer) -> str:
    """Run the full battle loop until a result is determined."""
    # Show opening
    opp = battle.opponent_pokemon
    print()
    print_divider("═")
    if battle.is_wild:
        shiny = " ✨ A shiny" if opp.is_shiny else " A wild"
        print(f"{shiny} {opp.species.name} appeared! (Lv.{opp.level})")
    else:
        print(f"  {battle.opponent.trainer_class.title_prefix} {battle.opponent.name} wants to battle!")
        print(f"  {battle.opponent.name} sent out {opp.nickname}! (Lv.{opp.level})")
    print_divider("═")
    # Register as seen
    if player.pokedex:
        player.pokedex.register_seen(opp)

    while battle.result is None:
        action = battle_menu(battle, player)
        msgs = battle.run_turn(action)
        for msg in msgs:
            if msg:
                print(f"  {msg}")
        print()

        # Check for forced switches after fainting
        if battle.player_pokemon.fainted and player.has_usable_pokemon():
            if battle.result is None:
                print("  Choose your next Pokémon!")
                switch_action = switch_menu(player)
                battle.run_turn(switch_action)

    print_divider()
    result = battle.result

    if result == BattleResult.WIN:
        print("  You won the battle!")
        if not battle.is_wild:
            leader_msg = battle.opponent.dialogue_win
            if leader_msg:
                print(f"  {battle.opponent.name}: {leader_msg}")
    elif result == BattleResult.LOSE:
        print("  You lost...")
    elif result == BattleResult.RUN:
        print("  You got away safely!")
    elif result == BattleResult.CATCH:
        caught_mon = battle.opponent_pokemon
        print(f"  Caught {caught_mon.nickname}!")
    press_enter()
    return result


# ── Evolution ─────────────────────────────────────────────────────────────────

def handle_evolution(mon: Pokemon, player: Trainer) -> None:
    """Check and process evolution after battle or event."""
    time_of_day = get_time_of_day()
    cond = check_evolution(mon, time_of_day=time_of_day)
    if cond is None:
        return

    old_name = mon.species.name
    print()
    print_divider("✦")
    print(f"  What? {mon.nickname} is evolving!")
    # Give player a chance to cancel (hold B concept)
    answer = prompt("  Press ENTER to evolve, or type 'cancel' to stop: ")
    if answer.lower() == "cancel":
        print(f"  Huh? {mon.nickname} stopped evolving!")
        return
    evolve(mon, cond)
    print(f"  {old_name} evolved into {mon.species.name}!")
    if player.pokedex:
        player.pokedex.register_caught(mon)
    press_enter()


# ── Starter selection ─────────────────────────────────────────────────────────

def choose_starter() -> Pokemon:
    starters = ["Bulbasaur", "Charmander", "Squirtle"]
    print("\nProfessor Oak: Welcome to the world of Pokémon!")
    print("Please choose your starter Pokémon:\n")
    for i, name in enumerate(starters, 1):
        sp = SPECIES[name]
        types_str = "/".join(t.value for t in sp.types)
        print(f"  {i}. {name}  [{types_str}]")
    while True:
        raw = prompt("> ")
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(starters):
                name = starters[idx]
                mon = create_pokemon(name, 5, trainer_name="Player")
                print(f"\n  You chose {name}!")
                return mon
        print("  Please enter 1, 2, or 3.")


# ── Wild encounter ────────────────────────────────────────────────────────────

# Simple encounter table: route -> list of (species_name, min_level, max_level)
ENCOUNTER_TABLE: dict[str, list[tuple[str, int, int]]] = {
    "Route 1":   [("Pidgey",5,8), ("Rattata",4,7)],
    "Route 2":   [("Pidgey",6,10), ("Rattata",5,9), ("Caterpie",5,8)],
    "Route 3":   [("Spearow",8,14), ("Jigglypuff",10,14)],
    "Viridian Forest": [("Caterpie",5,9), ("Metapod",8,12), ("Weedle",5,9), ("Pikachu",4,8)],
    "Mt. Moon":  [("Zubat",10,15), ("Geodude",10,15), ("Paras",10,15), ("Clefairy",10,16)],
    "Route 6":   [("Drowzee",11,18), ("Poliwag",13,18), ("Venonat",13,17)],
    "Safari Zone": [("Nidoran-F",22,28), ("Nidoran-M",22,28), ("Exeggcute",24,28),
                    ("Chansey",25,30), ("Tauros",25,30), ("Scyther",25,30)],
    "Seafoam Islands": [("Seel",32,38), ("Dewgong",35,42), ("Slowpoke",32,38), ("Articuno",50,50)],
}


def wild_encounter(
    player: Trainer,
    route: str,
    center: PokemonCenter,
) -> None:
    """Simulate a wild Pokémon encounter."""
    if route not in ENCOUNTER_TABLE:
        print(f"  (No encounters on {route})")
        return

    entry = random.choice(ENCOUNTER_TABLE[route])
    species_name, min_lvl, max_lvl = entry

    # Only include species that are in the game's data
    if species_name not in SPECIES:
        print(f"  (Encountered unknown species: {species_name})")
        return

    level = random.randint(min_lvl, max_lvl)
    wild = create_pokemon(species_name, level, is_wild=True)

    # Choose first alive party member
    active_idx = player.first_usable_idx()
    if active_idx < 0:
        print("  You have no usable Pokémon! Blacked out.")
        return

    wild_trainer = Trainer("Wild", party=[wild])
    battle = Battle(player, wild_trainer, is_wild=True)
    result = run_battle_loop(battle, player)

    if result in (BattleResult.WIN,):
        # Process EXP, evolution
        for mon in player.party:
            if not mon.fainted:
                handle_evolution(mon, player)

    # Heal if party is all fainted
    if not player.has_usable_pokemon():
        print("  You blacked out! Returning to the Pokémon Center...")
        center.heal_party(player)
        press_enter()


# ── Gym battle ────────────────────────────────────────────────────────────────

def gym_battle(player: Trainer, gym_ch: GymChallenge) -> None:
    if not gym_ch.can_challenge(player):
        print(f"  {gym_ch.challenge_refused_message()}")
        press_enter()
        return

    gym = gym_ch.gym
    print()
    print_divider("═")
    print(f"  ★ {gym.city} Gym  ★")
    print(f"  Leader: {gym.leader_name}")
    print(f"  Specialty: {gym.specialty_type}")
    print(f"  \"{gym_ch.leader.dialogue_intro}\"")
    print_divider("═")
    press_enter()

    # Heal leader party just in case
    gym_ch.leader.heal_party()

    battle = Battle(player, gym_ch.leader, is_wild=False)
    result = run_battle_loop(battle, player)

    if result == BattleResult.WIN:
        msgs = gym_ch.award_badge(player)
        for msg in msgs:
            print(f"  {msg}")
        press_enter()
        for mon in player.party:
            if not mon.fainted:
                handle_evolution(mon, player)
    elif result == BattleResult.LOSE:
        print("  Return to a Pokémon Center and try again!")
        press_enter()


# ── Main game loop ────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 60)
    print(" " * 15 + "Welcome to PYKEMON!")
    print("=" * 60)
    print()

    # Player setup
    name = prompt("Enter your name, Trainer: ")
    if not name:
        name = "Red"

    player = Trainer(name=name, trainer_class="Player", money=3000, is_player=True)

    # Starter
    starter = choose_starter()
    player.add_pokemon(starter)

    # Starting items
    player.bag.add_item("Poké Ball", 5)
    player.bag.add_item("Potion", 5)

    # World setup
    center = PokemonCenter("Pallet Town")
    mart   = PokeMart("Viridian City")
    gym_system = GymBadgeSystem()
    fossil_lab = FossilLab("Cinnabar Island")
    ride_system = RideSystem()

    print(f"\n  {name} received a Trainer Card!")
    print(f"  {describe_time()}")
    press_enter()

    # ── Main menu loop ───────────────────────────────────────────────────────
    LOCATIONS = [
        "Route 1", "Route 2", "Route 3",
        "Viridian Forest", "Mt. Moon", "Route 6",
        "Safari Zone", "Seafoam Islands",
    ]
    current_location = "Pallet Town"

    while True:
        clear()
        print(f"  [{describe_time()}]  Location: {current_location}")
        print(f"  {player.name}  ₽{player.money:,}  Badges: {len(player.badges)}/8")
        print()

        action = choose_from_list([
            "Walk (Wild Encounter)",
            "Visit Pokémon Center",
            "Visit Poké Mart",
            "Challenge Gym",
            "Pokémon League (8 badges required)",
            "Fossil Lab",
            "View Party",
            "Pokédex",
            "Bag",
            "Ride Pokémon",
            "Change Location",
            "Save & Quit",
        ], title="What will you do?")

        if action < 0 or action == 11:
            print("\n  Thanks for playing Pykemon! Goodbye!")
            break

        elif action == 0:   # Wild encounter
            wild_encounter(player, current_location, center)

        elif action == 1:   # Pokémon Center
            msgs = center.heal_party(player)
            for msg in msgs:
                print(f"  {msg}")
            press_enter()

        elif action == 2:   # Poké Mart
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

        elif action == 3:   # Gym
            next_gym = gym_system.next_gym(player)
            if next_gym is None:
                print("  You've already defeated all 8 Gym Leaders!")
                press_enter()
            else:
                print(gym_system.display_gyms())
                gym_num = prompt("  Challenge which gym? (1-8): ")
                if gym_num.isdigit():
                    ch = gym_system.get_gym(int(gym_num))
                    if ch:
                        gym_battle(player, ch)
                    else:
                        print("  Invalid gym number.")
                        press_enter()

        elif action == 4:   # Pokémon League
            if not gym_system.league.can_challenge(player):
                print("  You need all 8 badges to enter the Pokémon League!")
                press_enter()
            else:
                league = gym_system.league
                league.reset()
                print("  You step into the Pokémon League!")
                while not league.is_complete() and player.has_usable_pokemon():
                    opponent = league.next_opponent()
                    if opponent is None:
                        break
                    opponent.heal_party()
                    battle = Battle(player, opponent, is_wild=False)
                    result = run_battle_loop(battle, player)
                    if result == BattleResult.WIN:
                        if not league.advance():
                            print(league.victory_message())
                            press_enter()
                            break
                        else:
                            print("  Press on to the next challenger!")
                            center.heal_party(player)
                    else:
                        print("  You were defeated! Train more and return!")
                        press_enter()
                        break

        elif action == 5:   # Fossil Lab
            print(fossil_lab.display())
            fossil_name = prompt("  Which fossil to revive? (or 'done'): ")
            if fossil_name.lower() != "done":
                pokemon, msgs = fossil_lab.revive(player, fossil_name)
                for msg in msgs:
                    print(f"  {msg}")
                press_enter()

        elif action == 6:   # View Party
            print(player.party_status())
            idx = choose_from_list(
                [f"{m.nickname} — summary" for m in player.party],
                "View summary:",
            )
            if idx >= 0:
                print(player.party[idx].summary())
            press_enter()

        elif action == 7:   # Pokédex
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

        elif action == 8:   # Bag
            print(player.bag.display())
            # Use medicine outside battle
            raw = prompt("  Use an item? (name or 'done'): ")
            if raw.lower() != "done" and raw:
                item_data = ITEMS.get(raw)
                if item_data and item_data.hp_restore:
                    party_choices = [f"{m.nickname} ({m.current_hp}/{m.max_hp} HP)"
                                     for m in player.party]
                    idx = choose_from_list(party_choices, "Use on:")
                    if idx >= 0:
                        target = player.party[idx]
                        if item_data.hp_restore == -1:
                            target.heal(target.max_hp)
                        elif item_data.hp_restore > 0:
                            target.heal(item_data.hp_restore)
                        player.bag.remove_item(raw, 1)
                        print(f"  Used {raw} on {target.nickname}!")
            press_enter()

        elif action == 9:   # Ride Pokémon
            print(ride_system.display())
            raw = prompt("  Mount which Pokémon? (name or 'done'): ")
            if raw.lower() != "done":
                msg = ride_system.use(raw)
                print(f"  {msg}" if msg else "  That Pokémon isn't available to ride.")
            press_enter()

        elif action == 10:  # Change location
            loc_idx = choose_from_list(LOCATIONS, "Travel to:")
            if loc_idx >= 0:
                current_location = LOCATIONS[loc_idx]
                print(f"  You arrive at {current_location}.")
            press_enter()


if __name__ == "__main__":
    main()
