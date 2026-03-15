"""
Move definitions and move data for Pykemon.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from .types import PokemonType


class MoveCategory(Enum):
    PHYSICAL = "Physical"
    SPECIAL = "Special"
    STATUS = "Status"


class StatusEffect(Enum):
    BURN = "BRN"
    FREEZE = "FRZ"
    PARALYSIS = "PAR"
    POISON = "PSN"
    BADLY_POISONED = "TOX"
    SLEEP = "SLP"
    CONFUSION = "CNF"
    FLINCH = "FLN"


class WeatherEffect(Enum):
    NONE = "None"
    SUNNY = "Sunny"
    RAIN = "Rain"
    SANDSTORM = "Sandstorm"
    HAIL = "Hail"
    FOG = "Fog"


@dataclass
class MoveEffect:
    status: Optional[StatusEffect] = None
    status_chance: float = 0.0         # 0.0 - 1.0
    stat_changes: dict[str, int] = field(default_factory=dict)  # e.g. {"atk": -1}
    stat_change_chance: float = 1.0
    target_self: bool = False           # Does the stat change apply to user?
    sets_weather: Optional[WeatherEffect] = None
    heals_user: float = 0.0            # Fraction of damage dealt healed to user
    recoil: float = 0.0               # Fraction of damage dealt as recoil to user
    drains_hp: float = 0.0            # Fraction of target max HP drained per turn
    flinch_chance: float = 0.0
    priority: int = 0                  # Move priority (+1, +2 etc.)
    hits_multiple: bool = False        # Does the move hit both opponents in doubles?
    hits_twice: bool = False           # Hits 2-5 times
    crits_always: bool = False
    charges_turn: bool = False         # Takes a turn to charge before hitting
    can_thaw: bool = False            # Thaws the user if frozen
    bypass_accuracy: bool = False


@dataclass
class MoveData:
    name: str
    move_type: PokemonType
    category: MoveCategory
    power: int            # 0 for status moves
    accuracy: int         # 0-100; 101 = always hits
    pp: int
    effect: MoveEffect = field(default_factory=MoveEffect)
    description: str = ""
    is_hm: bool = False
    tm_number: Optional[int] = None   # TM number if applicable
    hm_number: Optional[int] = None   # HM number if applicable
    hits_multiple: bool = False        # Hits all opponents (e.g. Surf, Earthquake)


# ---------------------------------------------------------------------------
# Move registry
# ---------------------------------------------------------------------------
MOVES: dict[str, MoveData] = {}


def _add(move: MoveData) -> MoveData:
    MOVES[move.name] = move
    return move


# ── Physical Moves ──────────────────────────────────────────────────────────
_add(MoveData("Tackle", PokemonType.NORMAL, MoveCategory.PHYSICAL, 40, 100, 35,
              description="A physical attack in which the user charges and slams into the target."))
_add(MoveData("Scratch", PokemonType.NORMAL, MoveCategory.PHYSICAL, 40, 100, 35,
              description="Hard, pointed, sharp claws rake the target to inflict damage."))
_add(MoveData("Pound", PokemonType.NORMAL, MoveCategory.PHYSICAL, 40, 100, 35,
              description="The target is physically pounded with a long tail, a foreleg, or the like."))
_add(MoveData("Quick Attack", PokemonType.NORMAL, MoveCategory.PHYSICAL, 40, 100, 30,
              effect=MoveEffect(priority=1),
              description="The user lunges at the target at a speed that makes it almost invisible."))
_add(MoveData("Body Slam", PokemonType.NORMAL, MoveCategory.PHYSICAL, 85, 100, 15,
              effect=MoveEffect(status=StatusEffect.PARALYSIS, status_chance=0.3),
              description="The user drops onto the target with its full body weight."))
_add(MoveData("Double-Edge", PokemonType.NORMAL, MoveCategory.PHYSICAL, 120, 100, 15,
              effect=MoveEffect(recoil=0.33),
              description="A reckless, life-risking tackle that also hurts the user."))
_add(MoveData("Hyper Fang", PokemonType.NORMAL, MoveCategory.PHYSICAL, 80, 90, 15,
              effect=MoveEffect(flinch_chance=0.1),
              description="The user bites hard on the target with its sharp front fangs."))
_add(MoveData("Slash", PokemonType.NORMAL, MoveCategory.PHYSICAL, 70, 100, 20,
              effect=MoveEffect(crits_always=True),
              description="The target is attacked with a slash of claws or blades."))
_add(MoveData("Headbutt", PokemonType.NORMAL, MoveCategory.PHYSICAL, 70, 100, 15,
              effect=MoveEffect(flinch_chance=0.3),
              description="The user sticks out its head and attacks."))
_add(MoveData("Strength", PokemonType.NORMAL, MoveCategory.PHYSICAL, 80, 100, 15,
              hm_number=4,
              description="The target is slugged with a punch thrown at maximum power."))

_add(MoveData("Ember", PokemonType.FIRE, MoveCategory.SPECIAL, 40, 100, 25,
              effect=MoveEffect(status=StatusEffect.BURN, status_chance=0.1),
              description="The target is attacked with small flames."))
_add(MoveData("Flamethrower", PokemonType.FIRE, MoveCategory.SPECIAL, 90, 100, 15,
              effect=MoveEffect(status=StatusEffect.BURN, status_chance=0.1),
              tm_number=35,
              description="The target is scorched with an intense blast of fire."))
_add(MoveData("Fire Blast", PokemonType.FIRE, MoveCategory.SPECIAL, 110, 85, 5,
              effect=MoveEffect(status=StatusEffect.BURN, status_chance=0.1),
              tm_number=38,
              description="The target is attacked with an intense blast of all-consuming fire."))
_add(MoveData("Fire Spin", PokemonType.FIRE, MoveCategory.SPECIAL, 35, 85, 15,
              description="The target becomes trapped within a fierce vortex of fire."))

_add(MoveData("Water Gun", PokemonType.WATER, MoveCategory.SPECIAL, 40, 100, 25,
              description="The target is blasted with a forceful shot of water."))
_add(MoveData("Surf", PokemonType.WATER, MoveCategory.SPECIAL, 90, 100, 15,
              hm_number=3, hits_multiple=True,
              description="The user attacks everything around it by swamping its surroundings with a giant wave."))
_add(MoveData("Hydro Pump", PokemonType.WATER, MoveCategory.SPECIAL, 110, 80, 5,
              description="The target is blasted by a huge volume of water launched under great pressure."))
_add(MoveData("Waterfall", PokemonType.WATER, MoveCategory.PHYSICAL, 80, 100, 15,
              hm_number=7, effect=MoveEffect(flinch_chance=0.2),
              description="The user charges the target at full speed."))
_add(MoveData("Bubble", PokemonType.WATER, MoveCategory.SPECIAL, 40, 100, 30,
              effect=MoveEffect(stat_changes={"spe": -1}, stat_change_chance=0.1),
              description="A spray of bubbles is forcefully ejected at the target."))
_add(MoveData("Bubble Beam", PokemonType.WATER, MoveCategory.SPECIAL, 65, 100, 20,
              effect=MoveEffect(stat_changes={"spe": -1}, stat_change_chance=0.33),
              description="A spray of bubbles is forcefully ejected at the target."))

_add(MoveData("Vine Whip", PokemonType.GRASS, MoveCategory.PHYSICAL, 45, 100, 25,
              description="The target is struck with slender, whiplike vines."))
_add(MoveData("Razor Leaf", PokemonType.GRASS, MoveCategory.PHYSICAL, 55, 95, 25,
              effect=MoveEffect(crits_always=True),
              description="Sharp-edged leaves are launched to slash at the opposing Pokémon."))
_add(MoveData("Solar Beam", PokemonType.GRASS, MoveCategory.SPECIAL, 120, 100, 10,
              effect=MoveEffect(charges_turn=True),
              tm_number=22,
              description="The user gathers light, then blasts a bundled beam on the next turn."))
_add(MoveData("Petal Dance", PokemonType.GRASS, MoveCategory.SPECIAL, 120, 100, 10,
              description="The user attacks the target by scattering petals for two to three turns."))

_add(MoveData("Thundershock", PokemonType.ELECTRIC, MoveCategory.SPECIAL, 40, 100, 30,
              effect=MoveEffect(status=StatusEffect.PARALYSIS, status_chance=0.1),
              description="A jolt of electricity crashes down on the target."))
_add(MoveData("Thunderbolt", PokemonType.ELECTRIC, MoveCategory.SPECIAL, 90, 100, 15,
              effect=MoveEffect(status=StatusEffect.PARALYSIS, status_chance=0.1),
              tm_number=24,
              description="A strong electric blast crashes down on the target."))
_add(MoveData("Thunder", PokemonType.ELECTRIC, MoveCategory.SPECIAL, 110, 70, 10,
              effect=MoveEffect(status=StatusEffect.PARALYSIS, status_chance=0.3),
              tm_number=25,
              description="A wicked thunderbolt is dropped on the target."))
_add(MoveData("Thunder Wave", PokemonType.ELECTRIC, MoveCategory.STATUS, 0, 90, 20,
              effect=MoveEffect(status=StatusEffect.PARALYSIS, status_chance=1.0),
              tm_number=45,
              description="The user launches a weak jolt of electricity that paralyzes the target."))

_add(MoveData("Ice Beam", PokemonType.ICE, MoveCategory.SPECIAL, 90, 100, 10,
              effect=MoveEffect(status=StatusEffect.FREEZE, status_chance=0.1),
              tm_number=13,
              description="The target is struck with an icy-cold beam of energy."))
_add(MoveData("Blizzard", PokemonType.ICE, MoveCategory.SPECIAL, 110, 70, 5,
              effect=MoveEffect(status=StatusEffect.FREEZE, status_chance=0.1),
              tm_number=14,
              description="A howling blizzard is summoned to strike opposing Pokémon."))
_add(MoveData("Ice Punch", PokemonType.ICE, MoveCategory.PHYSICAL, 75, 100, 15,
              effect=MoveEffect(status=StatusEffect.FREEZE, status_chance=0.1),
              description="The target is punched with an icy fist."))

_add(MoveData("Karate Chop", PokemonType.FIGHTING, MoveCategory.PHYSICAL, 50, 100, 25,
              effect=MoveEffect(crits_always=True),
              description="The target is attacked with a sharp chop."))
_add(MoveData("Low Kick", PokemonType.FIGHTING, MoveCategory.PHYSICAL, 65, 100, 20,
              effect=MoveEffect(flinch_chance=0.3),
              description="A powerful low kick that makes the target stumble."))
_add(MoveData("High Jump Kick", PokemonType.FIGHTING, MoveCategory.PHYSICAL, 130, 90, 10,
              description="The target is attacked with a knee kick from a jump."))
_add(MoveData("Submission", PokemonType.FIGHTING, MoveCategory.PHYSICAL, 80, 80, 20,
              effect=MoveEffect(recoil=0.25),
              description="The user grabs the target and recklessly dives for the ground."))

_add(MoveData("Poison Sting", PokemonType.POISON, MoveCategory.PHYSICAL, 15, 100, 35,
              effect=MoveEffect(status=StatusEffect.POISON, status_chance=0.3),
              description="The user stabs the target with a poisonous stinger."))
_add(MoveData("Sludge Bomb", PokemonType.POISON, MoveCategory.SPECIAL, 90, 100, 10,
              effect=MoveEffect(status=StatusEffect.POISON, status_chance=0.3),
              tm_number=36,
              description="Unsanitary sludge is hurled at the target."))
_add(MoveData("Toxic", PokemonType.POISON, MoveCategory.STATUS, 0, 90, 10,
              effect=MoveEffect(status=StatusEffect.BADLY_POISONED, status_chance=1.0),
              tm_number=6,
              description="A move that leaves the target badly poisoned. Its poison damage worsens every turn."))

_add(MoveData("Earthquake", PokemonType.GROUND, MoveCategory.PHYSICAL, 100, 100, 10,
              tm_number=26, hits_multiple=True,
              description="The user sets off an earthquake that strikes every Pokémon around it."))
_add(MoveData("Dig", PokemonType.GROUND, MoveCategory.PHYSICAL, 80, 100, 10,
              hm_number=6, effect=MoveEffect(charges_turn=True),
              description="The user burrows, then attacks on the next turn."))
_add(MoveData("Sand Attack", PokemonType.GROUND, MoveCategory.STATUS, 0, 100, 15,
              effect=MoveEffect(stat_changes={"acc": -1}, stat_change_chance=1.0),
              description="Sand is hurled in the target's face, reducing its accuracy."))

_add(MoveData("Wing Attack", PokemonType.FLYING, MoveCategory.PHYSICAL, 60, 100, 35,
              description="The target is struck with large, imposing wings spread wide."))
_add(MoveData("Fly", PokemonType.FLYING, MoveCategory.PHYSICAL, 90, 95, 15,
              hm_number=2, effect=MoveEffect(charges_turn=True),
              description="The user soars, then strikes the target on the next turn."))
_add(MoveData("Gust", PokemonType.FLYING, MoveCategory.SPECIAL, 40, 100, 35,
              description="A gust of wind is whipped up by wings and launched at the target."))
_add(MoveData("Drill Peck", PokemonType.FLYING, MoveCategory.PHYSICAL, 80, 100, 20,
              description="A corkscrewing attack with the sharp beak acting as a drill."))

_add(MoveData("Confusion", PokemonType.PSYCHIC, MoveCategory.SPECIAL, 50, 100, 25,
              effect=MoveEffect(status=StatusEffect.CONFUSION, status_chance=0.1),
              description="The target is hit by a weak telekinetic force."))
_add(MoveData("Psychic", PokemonType.PSYCHIC, MoveCategory.SPECIAL, 90, 100, 10,
              effect=MoveEffect(stat_changes={"spd": -1}, stat_change_chance=0.1),
              tm_number=29,
              description="The target is hit by a strong telekinetic force."))
_add(MoveData("Psybeam", PokemonType.PSYCHIC, MoveCategory.SPECIAL, 65, 100, 20,
              effect=MoveEffect(status=StatusEffect.CONFUSION, status_chance=0.1),
              description="The target is attacked with a peculiar ray."))
_add(MoveData("Future Sight", PokemonType.PSYCHIC, MoveCategory.SPECIAL, 120, 100, 10,
              description="Two turns after this move is used, a hunk of psychic energy attacks the target."))

_add(MoveData("Leech Life", PokemonType.BUG, MoveCategory.PHYSICAL, 80, 100, 10,
              effect=MoveEffect(heals_user=0.5),
              description="The user drains the target's blood. The user's HP is restored by half the damage taken by the target."))
_add(MoveData("String Shot", PokemonType.BUG, MoveCategory.STATUS, 0, 95, 40,
              effect=MoveEffect(stat_changes={"spe": -2}, stat_change_chance=1.0),
              description="Opposing Pokémon are bound with silk blown from the user's mouth."))
_add(MoveData("Twineedle", PokemonType.BUG, MoveCategory.PHYSICAL, 25, 100, 20,
              effect=MoveEffect(status=StatusEffect.POISON, status_chance=0.2, hits_twice=True),
              description="The user stabs the target with two spikes."))

_add(MoveData("Rock Throw", PokemonType.ROCK, MoveCategory.PHYSICAL, 50, 90, 15,
              description="The user picks up and throws a small rock at the target."))
_add(MoveData("Rock Slide", PokemonType.ROCK, MoveCategory.PHYSICAL, 75, 90, 10,
              effect=MoveEffect(flinch_chance=0.3), hits_multiple=True,
              tm_number=80,
              description="Large boulders are hurled at the opposing Pokémon to inflict damage."))
_add(MoveData("Rock Blast", PokemonType.ROCK, MoveCategory.PHYSICAL, 25, 90, 10,
              effect=MoveEffect(hits_twice=True),
              description="The user hurls hard rocks at the target."))

_add(MoveData("Lick", PokemonType.GHOST, MoveCategory.PHYSICAL, 30, 100, 30,
              effect=MoveEffect(status=StatusEffect.PARALYSIS, status_chance=0.3),
              description="The target is licked with a long tongue, causing damage."))
_add(MoveData("Night Shade", PokemonType.GHOST, MoveCategory.SPECIAL, 1, 100, 15,
              description="The user makes the target see a frightening mirage. It inflicts damage equal to the user's level."))
_add(MoveData("Shadow Ball", PokemonType.GHOST, MoveCategory.SPECIAL, 80, 100, 15,
              effect=MoveEffect(stat_changes={"spd": -1}, stat_change_chance=0.2),
              tm_number=30,
              description="The user hurls a shadowy blob at the target."))

_add(MoveData("Dragon Rage", PokemonType.DRAGON, MoveCategory.SPECIAL, 1, 100, 10,
              description="This attack hits the target with a shock wave of pure rage. This attack always inflicts 40 HP damage."))
_add(MoveData("Dragon Claw", PokemonType.DRAGON, MoveCategory.PHYSICAL, 80, 100, 15,
              tm_number=2,
              description="The user slashes the target with huge, sharp claws."))
_add(MoveData("Dragon Breath", PokemonType.DRAGON, MoveCategory.SPECIAL, 60, 100, 20,
              effect=MoveEffect(status=StatusEffect.PARALYSIS, status_chance=0.3),
              description="The user lets loose a blast of heavy breath."))

# ── Status / Utility Moves ───────────────────────────────────────────────────
_add(MoveData("Growl", PokemonType.NORMAL, MoveCategory.STATUS, 0, 100, 40,
              effect=MoveEffect(stat_changes={"atk": -1}, stat_change_chance=1.0),
              description="The user growls in an endearing way, making opposing Pokémon less wary."))
_add(MoveData("Leer", PokemonType.NORMAL, MoveCategory.STATUS, 0, 100, 30,
              effect=MoveEffect(stat_changes={"def": -1}, stat_change_chance=1.0),
              description="The user gives opposing Pokémon an intimidating leer that lowers the Defense stat."))
_add(MoveData("Tail Whip", PokemonType.NORMAL, MoveCategory.STATUS, 0, 100, 30,
              effect=MoveEffect(stat_changes={"def": -1}, stat_change_chance=1.0),
              description="The user wags its tail cutely, making opposing Pokémon less wary."))
_add(MoveData("Sing", PokemonType.NORMAL, MoveCategory.STATUS, 0, 55, 15,
              effect=MoveEffect(status=StatusEffect.SLEEP, status_chance=1.0),
              description="A soothing lullaby is sung in a calming voice that puts the target into a deep slumber."))
_add(MoveData("Sleep Powder", PokemonType.GRASS, MoveCategory.STATUS, 0, 75, 15,
              effect=MoveEffect(status=StatusEffect.SLEEP, status_chance=1.0),
              description="The user scatters a big cloud of sleep-inducing dust around the target."))
_add(MoveData("Stun Spore", PokemonType.GRASS, MoveCategory.STATUS, 0, 75, 30,
              effect=MoveEffect(status=StatusEffect.PARALYSIS, status_chance=1.0),
              description="The user scatters a cloud of numbing powder that paralyzes the target."))
_add(MoveData("Poison Powder", PokemonType.POISON, MoveCategory.STATUS, 0, 75, 35,
              effect=MoveEffect(status=StatusEffect.POISON, status_chance=1.0),
              description="The user scatters a cloud of poisonous dust on the target."))
_add(MoveData("Hypnosis", PokemonType.PSYCHIC, MoveCategory.STATUS, 0, 60, 20,
              effect=MoveEffect(status=StatusEffect.SLEEP, status_chance=1.0),
              description="The user employs hypnotic suggestion to make the target fall into a deep sleep."))
_add(MoveData("Spore", PokemonType.GRASS, MoveCategory.STATUS, 0, 100, 15,
              effect=MoveEffect(status=StatusEffect.SLEEP, status_chance=1.0),
              description="The user scatters bursts of spores that induce sleep."))

_add(MoveData("Swords Dance", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 20,
              effect=MoveEffect(stat_changes={"atk": 2}, stat_change_chance=1.0, target_self=True),
              tm_number=75,
              description="A frenetic dance to uplift the fighting spirit. It sharply raises the user's Attack stat."))
_add(MoveData("Harden", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 30,
              effect=MoveEffect(stat_changes={"def": 1}, stat_change_chance=1.0, target_self=True),
              description="The user stiffens all the muscles in its body to raise its Defense stat."))
_add(MoveData("Withdraw", PokemonType.WATER, MoveCategory.STATUS, 0, 101, 40,
              effect=MoveEffect(stat_changes={"def": 1}, stat_change_chance=1.0, target_self=True),
              description="The user withdraws its body into its hard shell, raising its Defense stat."))
_add(MoveData("Defense Curl", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 40,
              effect=MoveEffect(stat_changes={"def": 1}, stat_change_chance=1.0, target_self=True),
              description="The user curls up to conceal weak spots and raise its Defense stat."))
_add(MoveData("Agility", PokemonType.PSYCHIC, MoveCategory.STATUS, 0, 101, 30,
              effect=MoveEffect(stat_changes={"spe": 2}, stat_change_chance=1.0, target_self=True),
              tm_number=33,
              description="The user relaxes and lightens its body to move faster."))
_add(MoveData("Amnesia", PokemonType.PSYCHIC, MoveCategory.STATUS, 0, 101, 20,
              effect=MoveEffect(stat_changes={"spa": 2}, stat_change_chance=1.0, target_self=True),
              description="The user temporarily empties its mind to forget its concerns."))

_add(MoveData("Recover", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 10,
              effect=MoveEffect(heals_user=-0.5),  # negative = heal self
              description="Restoring its own cells, the user restores its own HP by half of its max HP."))
_add(MoveData("Softboiled", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 10,
              effect=MoveEffect(heals_user=-0.5),
              description="The user restores its own HP by up to half of its max HP."))
_add(MoveData("Rest", PokemonType.PSYCHIC, MoveCategory.STATUS, 0, 101, 10,
              effect=MoveEffect(heals_user=-1.0, status=StatusEffect.SLEEP, status_chance=1.0, target_self=True),
              tm_number=44,
              description="The user goes to sleep for two turns. It fully restores the user's HP and heals any status conditions."))

_add(MoveData("Metronome", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 10,
              description="The user waggles a finger and stimulates its brain into randomly using nearly any move."))
_add(MoveData("Mimic", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 10,
              description="The user copies the target's last move."))
_add(MoveData("Mirror Move", PokemonType.FLYING, MoveCategory.STATUS, 0, 101, 20,
              description="The user counters the target by mimicking the target's last move."))

_add(MoveData("Whirlwind", PokemonType.NORMAL, MoveCategory.STATUS, 0, 85, 20,
              description="The target is blown away, and a different Pokémon is dragged out."))
_add(MoveData("Roar", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 20,
              effect=MoveEffect(priority=-6),
              description="The target is scared off, and a different Pokémon is dragged out."))

_add(MoveData("Substitute", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 10,
              tm_number=50,
              description="The user makes a copy of itself using some of its HP."))
_add(MoveData("Disable", PokemonType.NORMAL, MoveCategory.STATUS, 0, 100, 20,
              description="For four turns, this move prevents the target from using the move it last used."))

_add(MoveData("Minimize", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 10,
              effect=MoveEffect(stat_changes={"eva": 2}, stat_change_chance=1.0, target_self=True),
              description="The user compresses its body to make itself look smaller, which sharply raises its evasiveness."))
_add(MoveData("Double Team", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 15,
              effect=MoveEffect(stat_changes={"eva": 1}, stat_change_chance=1.0, target_self=True),
              tm_number=32,
              description="By moving rapidly, the user makes illusory copies of itself to raise its evasiveness."))

_add(MoveData("Protect", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 10,
              effect=MoveEffect(priority=4),
              tm_number=17,
              description="Enables the user to evade all attacks."))
_add(MoveData("Detect", PokemonType.FIGHTING, MoveCategory.STATUS, 0, 101, 5,
              effect=MoveEffect(priority=4),
              description="Enables the user to evade all attacks."))

_add(MoveData("Sunny Day", PokemonType.FIRE, MoveCategory.STATUS, 0, 101, 5,
              effect=MoveEffect(sets_weather=WeatherEffect.SUNNY),
              tm_number=11,
              description="The user intensifies the sun for five turns."))
_add(MoveData("Rain Dance", PokemonType.WATER, MoveCategory.STATUS, 0, 101, 5,
              effect=MoveEffect(sets_weather=WeatherEffect.RAIN),
              tm_number=18,
              description="The user summons a heavy rain that falls for five turns."))
_add(MoveData("Sandstorm", PokemonType.ROCK, MoveCategory.STATUS, 0, 101, 5,
              effect=MoveEffect(sets_weather=WeatherEffect.SANDSTORM),
              tm_number=37,
              description="A five-turn sandstorm is summoned to pelt the opposing Pokémon."))
_add(MoveData("Hail", PokemonType.ICE, MoveCategory.STATUS, 0, 101, 10,
              effect=MoveEffect(sets_weather=WeatherEffect.HAIL),
              tm_number=7,
              description="The user summons a hailstorm lasting five turns."))

# ── More Attack Moves ────────────────────────────────────────────────────────
_add(MoveData("Skull Bash", PokemonType.NORMAL, MoveCategory.PHYSICAL, 130, 100, 10,
              effect=MoveEffect(charges_turn=True, stat_changes={"def": 1}, stat_change_chance=1.0, target_self=True),
              description="The user tucks in its head to raise its Defense stat on the first turn, then rams the target on the next turn."))
_add(MoveData("Take Down", PokemonType.NORMAL, MoveCategory.PHYSICAL, 90, 85, 20,
              effect=MoveEffect(recoil=0.25),
              description="A reckless full-body charge attack for slamming into the target."))
_add(MoveData("Mega Punch", PokemonType.NORMAL, MoveCategory.PHYSICAL, 80, 85, 20,
              description="The target is slugged by a punch thrown with muscle-packed power."))
_add(MoveData("Mega Kick", PokemonType.NORMAL, MoveCategory.PHYSICAL, 120, 75, 5,
              description="The target is attacked by a kick launched with muscle-packed power."))
_add(MoveData("Cut", PokemonType.NORMAL, MoveCategory.PHYSICAL, 50, 95, 30,
              hm_number=1,
              description="The target is cut with a scythe or a claw."))
_add(MoveData("Flash", PokemonType.NORMAL, MoveCategory.STATUS, 0, 70, 20,
              effect=MoveEffect(stat_changes={"acc": -1}, stat_change_chance=1.0),
              hm_number=5,
              description="The user flashes a bright light that cuts the target's accuracy."))
_add(MoveData("Surf", PokemonType.WATER, MoveCategory.SPECIAL, 90, 100, 15,  # duplicate check
              hm_number=3, hits_multiple=True,
              description="The user attacks everything around it by swamping its surroundings."))
_add(MoveData("Whirlpool", PokemonType.WATER, MoveCategory.SPECIAL, 35, 85, 15,
              hm_number=6,
              description="The user traps the target in a violent swirling whirlpool."))

_add(MoveData("Thunderpunch", PokemonType.ELECTRIC, MoveCategory.PHYSICAL, 75, 100, 15,
              effect=MoveEffect(status=StatusEffect.PARALYSIS, status_chance=0.1),
              description="The target is punched with an electrified fist."))
_add(MoveData("Fire Punch", PokemonType.FIRE, MoveCategory.PHYSICAL, 75, 100, 15,
              effect=MoveEffect(status=StatusEffect.BURN, status_chance=0.1),
              description="The target is punched with a fiery fist."))

_add(MoveData("Aurora Beam", PokemonType.ICE, MoveCategory.SPECIAL, 65, 100, 20,
              effect=MoveEffect(stat_changes={"atk": -1}, stat_change_chance=0.1),
              description="The target is hit with a rainbow-colored beam."))
_add(MoveData("Mist", PokemonType.ICE, MoveCategory.STATUS, 0, 101, 30,
              description="The user cloaks itself and its allies in a white mist that prevents any of their stats from being lowered for five turns."))

_add(MoveData("Stomp", PokemonType.NORMAL, MoveCategory.PHYSICAL, 65, 100, 20,
              effect=MoveEffect(flinch_chance=0.3),
              description="The target is stomped with a big foot."))
_add(MoveData("Horn Attack", PokemonType.NORMAL, MoveCategory.PHYSICAL, 65, 100, 25,
              description="The target is jabbed with a sharply pointed horn."))
_add(MoveData("Fury Attack", PokemonType.NORMAL, MoveCategory.PHYSICAL, 15, 85, 20,
              effect=MoveEffect(hits_twice=True),
              description="The target is jabbed repeatedly with a horn or beak two to five times in a row."))
_add(MoveData("Horn Drill", PokemonType.NORMAL, MoveCategory.PHYSICAL, 1, 30, 5,
              description="The user stabs the target with a horn that rotates like a drill. If it hits, the target faints instantly."))
_add(MoveData("Fissure", PokemonType.GROUND, MoveCategory.PHYSICAL, 1, 30, 5,
              description="The user opens up a fissure in the ground and drops the target in. The target faints instantly if this hits."))

_add(MoveData("Smog", PokemonType.POISON, MoveCategory.SPECIAL, 30, 70, 20,
              effect=MoveEffect(status=StatusEffect.POISON, status_chance=0.4),
              description="The target is attacked with a discharge of filthy gases."))
_add(MoveData("Acid", PokemonType.POISON, MoveCategory.SPECIAL, 40, 100, 30,
              effect=MoveEffect(stat_changes={"spd": -1}, stat_change_chance=0.1),
              description="The opposing Pokémon are attacked with a spray of harsh acid."))

_add(MoveData("Bone Club", PokemonType.GROUND, MoveCategory.PHYSICAL, 65, 85, 20,
              effect=MoveEffect(flinch_chance=0.1),
              description="The user clubs the target with a bone."))
_add(MoveData("Bonemerang", PokemonType.GROUND, MoveCategory.PHYSICAL, 50, 90, 10,
              effect=MoveEffect(hits_twice=True),
              description="The user throws the bone it holds. The bone loops around to hit the target twice."))
_add(MoveData("Mud Slap", PokemonType.GROUND, MoveCategory.SPECIAL, 20, 100, 10,
              effect=MoveEffect(stat_changes={"acc": -1}, stat_change_chance=1.0),
              tm_number=28,
              description="The user hurls mud in the target's face to inflict damage and lower its accuracy."))

_add(MoveData("Jump Kick", PokemonType.FIGHTING, MoveCategory.PHYSICAL, 100, 95, 10,
              description="The user jumps up high, then strikes with a kick."))
_add(MoveData("Double Kick", PokemonType.FIGHTING, MoveCategory.PHYSICAL, 30, 100, 30,
              effect=MoveEffect(hits_twice=True),
              description="The target is quickly kicked twice in succession using both feet."))
_add(MoveData("Mega Drain", PokemonType.GRASS, MoveCategory.SPECIAL, 40, 100, 15,
              effect=MoveEffect(heals_user=0.5),
              description="A nutrient-draining attack. The user's HP is restored by half the damage taken by the target."))
_add(MoveData("Absorb", PokemonType.GRASS, MoveCategory.SPECIAL, 20, 100, 25,
              effect=MoveEffect(heals_user=0.5),
              description="A nutrient-draining attack. The user's HP is restored by half the damage taken by the target."))

_add(MoveData("Psy Wave", PokemonType.PSYCHIC, MoveCategory.SPECIAL, 1, 80, 15,
              description="The user fires off a wave of psychic energy."))
_add(MoveData("Teleport", PokemonType.PSYCHIC, MoveCategory.STATUS, 0, 101, 20,
              description="Use it to flee from any wild Pokémon. Can also be used to warp to the last visited Pokémon Center."))

_add(MoveData("Screech", PokemonType.NORMAL, MoveCategory.STATUS, 0, 85, 40,
              effect=MoveEffect(stat_changes={"def": -2}, stat_change_chance=1.0),
              description="An earsplitting screech harshly lowers the target's Defense stat."))
_add(MoveData("Supersonic", PokemonType.NORMAL, MoveCategory.STATUS, 0, 55, 20,
              effect=MoveEffect(status=StatusEffect.CONFUSION, status_chance=1.0),
              description="The user generates odd sound waves from its body that confuse the target."))
_add(MoveData("Confuse Ray", PokemonType.GHOST, MoveCategory.STATUS, 0, 100, 10,
              effect=MoveEffect(status=StatusEffect.CONFUSION, status_chance=1.0),
              description="The target is exposed to a sinister ray that triggers confusion."))

_add(MoveData("Flail", PokemonType.NORMAL, MoveCategory.PHYSICAL, 1, 100, 15,
              description="The user flails about aimlessly to attack. The lower the user's HP, the greater the move's power."))
_add(MoveData("Wrap", PokemonType.NORMAL, MoveCategory.PHYSICAL, 15, 90, 20,
              description="A long body, vines, or the like are used to wrap and squeeze the target for four to five turns."))
_add(MoveData("Bind", PokemonType.NORMAL, MoveCategory.PHYSICAL, 15, 85, 20,
              description="Things such as long bodies or tentacles are used to bind and squeeze the target for four to five turns."))
_add(MoveData("Constrict", PokemonType.NORMAL, MoveCategory.PHYSICAL, 10, 100, 35,
              effect=MoveEffect(stat_changes={"spe": -1}, stat_change_chance=0.1),
              description="The target is attacked with long, creeping tentacles or vines."))

_add(MoveData("Hyper Beam", PokemonType.NORMAL, MoveCategory.SPECIAL, 150, 90, 5,
              tm_number=15,
              description="The target is attacked with a powerful beam. The user can't move on the next turn."))

_add(MoveData("Bite", PokemonType.NORMAL, MoveCategory.PHYSICAL, 60, 100, 25,
              effect=MoveEffect(flinch_chance=0.3),
              description="The target is bitten with viciously sharp fangs."))
_add(MoveData("Pay Day", PokemonType.NORMAL, MoveCategory.PHYSICAL, 40, 100, 20,
              tm_number=16,
              description="Numerous coins are hurled at the target to inflict damage."))
_add(MoveData("Rage", PokemonType.NORMAL, MoveCategory.PHYSICAL, 20, 100, 20,
              description="As long as this move is in use, the power of rage raises the Attack stat each time the user is hit in battle."))
_add(MoveData("Seismic Toss", PokemonType.FIGHTING, MoveCategory.PHYSICAL, 1, 100, 20,
              description="The target is thrown using the power of gravity. It inflicts damage equal to the user's level."))
_add(MoveData("Counter", PokemonType.FIGHTING, MoveCategory.PHYSICAL, 1, 100, 20,
              effect=MoveEffect(priority=-5),
              description="A retaliation move that counters any physical attack, inflicting double the damage taken."))
_add(MoveData("Clamp", PokemonType.WATER, MoveCategory.PHYSICAL, 35, 85, 15,
              description="The target is clamped and squeezed by the user's very hard claws for four to five turns."))
_add(MoveData("Crabhammer", PokemonType.WATER, MoveCategory.PHYSICAL, 100, 90, 10,
              effect=MoveEffect(crits_always=True),
              description="The target is hammered with a large pincer."))
_add(MoveData("Explosion", PokemonType.NORMAL, MoveCategory.PHYSICAL, 250, 100, 5,
              hits_multiple=True,
              description="The user explodes to inflict damage on all Pokémon in battle. The user faints upon using this move."))
_add(MoveData("Selfdestruct", PokemonType.NORMAL, MoveCategory.PHYSICAL, 200, 100, 5,
              hits_multiple=True,
              description="The user attacks all Pokémon and faints."))
_add(MoveData("Barrage", PokemonType.NORMAL, MoveCategory.PHYSICAL, 15, 85, 20,
              effect=MoveEffect(hits_twice=True),
              description="Round objects are hurled at the target to strike two to five times in a row."))
_add(MoveData("Egg Bomb", PokemonType.NORMAL, MoveCategory.PHYSICAL, 100, 75, 10,
              description="A large egg is hurled at the target."))
_add(MoveData("Kinesis", PokemonType.PSYCHIC, MoveCategory.STATUS, 0, 80, 15,
              effect=MoveEffect(stat_changes={"acc": -1}, stat_change_chance=1.0),
              description="The user distracts the target by bending a spoon. This lowers the target's accuracy."))
_add(MoveData("Sharpen", PokemonType.NORMAL, MoveCategory.STATUS, 0, 101, 30,
              effect=MoveEffect(stat_changes={"atk": 1}, stat_change_chance=1.0, target_self=True),
              description="The user makes its edges more jagged, which raises its Attack stat."))

_add(MoveData("Spiky Shield", PokemonType.GRASS, MoveCategory.STATUS, 0, 101, 10,
              effect=MoveEffect(priority=4),
              description="The user blocks incoming attacks with a shield of sharp spikes."))
_add(MoveData("Spikes", PokemonType.GROUND, MoveCategory.STATUS, 0, 101, 20,
              description="The user lays a trap of spikes at the opposing team's feet."))

_add(MoveData("Smokescreen", PokemonType.NORMAL, MoveCategory.STATUS, 0, 100, 20,
              effect=MoveEffect(stat_changes={"acc": -1}, stat_change_chance=1.0),
              description="The user releases an obscuring cloud of smoke or ink."))

# Build a lookup for TMs and HMs
TM_MOVES: dict[int, MoveData] = {m.tm_number: m for m in MOVES.values() if m.tm_number}
HM_MOVES: dict[int, MoveData] = {m.hm_number: m for m in MOVES.values() if m.hm_number}


def _register_tm_hm_items() -> None:
    """
    Register TM and HM items into the global ITEMS registry.
    Called after both moves.py and items.py are fully loaded.
    """
    from .items import ITEMS, ItemData, ItemCategory

    for num, move in TM_MOVES.items():
        name = f"TM{num:02d}"
        if name not in ITEMS:
            ITEMS[name] = ItemData(
                name=name,
                category=ItemCategory.TM,
                price=3000,
                description=f"TM{num:02d}: Teaches {move.name} to a compatible Pokémon.",
            )

    for num, move in HM_MOVES.items():
        name = f"HM{num:02d}"
        if name not in ITEMS:
            ITEMS[name] = ItemData(
                name=name,
                category=ItemCategory.HM,
                price=0,
                description=f"HM{num:02d}: Teaches {move.name}. Cannot be removed from the Pokémon.",
            )


_register_tm_hm_items()

