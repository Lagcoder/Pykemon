"""
pykemon/story/locations.py

Kanto world data: every location has a description, a list of story events
that fire once on arrival, NPC trainers to battle, available services, and a
wild Pokémon encounter table.

``LOCATIONS`` is an ordered dict that mirrors the canonical story path.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class LocationService(Enum):
    POKEMON_CENTER = "Pokémon Center"
    POKE_MART      = "Poké Mart"
    FOSSIL_LAB     = "Fossil Lab"
    BIKE_SHOP      = "Bike Shop"
    SS_ANNE        = "S.S. Anne"
    SAFARI_ZONE    = "Safari Zone"
    GAME_CORNER    = "Game Corner"
    SILPH_CO       = "Silph Co."
    POKEMON_TOWER  = "Pokémon Tower"
    SEAFOAM_CAVE   = "Seafoam Islands Cave"
    VICTORY_ROAD_CAVE = "Victory Road"


@dataclass
class NpcTrainerSpec:
    """Lightweight spec — built into a Trainer lazily to save memory."""
    name: str
    trainer_class: str
    party: list[tuple[str, int]]   # (species, level)
    dialogue_intro: str = ""
    dialogue_win: str   = ""
    dialogue_lose: str  = ""
    money: int = 0


@dataclass
class Location:
    name: str
    description: str
    # Story events: mapping {flag_name: narrative_text}
    # Text is shown the first time the player arrives (flag not yet set).
    story_events: dict[str, str] = field(default_factory=dict)
    # NPC trainers
    trainers: list[NpcTrainerSpec] = field(default_factory=list)
    # Wild encounter table: list of (species, min_level, max_level)
    wild_encounters: list[tuple[str, int, int]] = field(default_factory=list)
    # Available services
    services: list[LocationService] = field(default_factory=list)
    # Gym number (1-8) if this location has a gym
    gym_number: Optional[int] = None
    # The next location the player unlocks after completing all story events
    unlocks: Optional[str] = None


# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────

def _npc(name, cls, party, intro="", win="", lose="", money=0) -> NpcTrainerSpec:
    return NpcTrainerSpec(
        name=name, trainer_class=cls, party=party,
        dialogue_intro=intro, dialogue_win=win, dialogue_lose=lose,
        money=money or max(p[1] for p in party) * 60,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Location data
# ─────────────────────────────────────────────────────────────────────────────

LOCATIONS: dict[str, Location] = {}


def _loc(loc: Location) -> Location:
    LOCATIONS[loc.name] = loc
    return loc


# ── Pallet Town ──────────────────────────────────────────────────────────────

_loc(Location(
    name="Pallet Town",
    description=(
        "A quiet, unassuming town where your adventure begins.\n"
        "The smell of fresh grass fills the air.  Oak's Laboratory\n"
        "stands at the edge of town, humming with energy."
    ),
    story_events={
        "OAK_LAB_INTRO": (
            "Professor Oak: Ah, {player}!  Just in time.\n"
            "The world of Pokémon awaits you.  Every Pokémon Trainer\n"
            "begins their journey by choosing a partner.\n"
            "Step up to the table and make your choice!"
        ),
        "BEAT_RIVAL_PALLET": (
            "Gary: {player}!  So you got a Pokémon too?  Let's see\n"
            "how good yours really is.  I challenge you!"
        ),
    },
    services=[LocationService.POKEMON_CENTER],
    unlocks="Route 1",
))

# ── Route 1 ──────────────────────────────────────────────────────────────────

_loc(Location(
    name="Route 1",
    description=(
        "A simple dirt path connecting Pallet Town to Viridian City.\n"
        "Pidgey and Rattata scurry through the tall grass.\n"
        "An old man is teaching his grandson how to catch Pokémon."
    ),
    trainers=[
        _npc("Joey",  "Youngster", [("Rattata", 5)],
             intro="Hey! I've got the strongest Rattata!",
             win="My Rattata is in the top percentage!",
             lose="Huh? My Rattata lost?"),
    ],
    wild_encounters=[
        ("Pidgey",  4,  8),
        ("Rattata", 3,  7),
    ],
    unlocks="Viridian City",
))

# ── Viridian City ─────────────────────────────────────────────────────────────

_loc(Location(
    name="Viridian City",
    description=(
        "A city that blends naturally with the surrounding forest.\n"
        "The Pokémon Gym here is strangely locked — rumour has it\n"
        "the Leader is never around.  The Poké Mart stocks the basics."
    ),
    story_events={
        "OAK_PARCEL_DELIVERED": (
            "Old Man: Oh! You have Oak's Parcel?  Hand it over!\n"
            "Professor Oak: Thank you, {player}.  Here — take these\n"
            "Pokéballs and the Pokédex.  Register every Pokémon!"
        ),
    },
    services=[LocationService.POKEMON_CENTER, LocationService.POKE_MART],
    unlocks="Route 2",
))

# ── Route 2 ──────────────────────────────────────────────────────────────────

_loc(Location(
    name="Route 2",
    description=(
        "A short winding road leading north from Viridian City.\n"
        "Trees grow thicker as you approach Viridian Forest.\n"
        "Bug Catchers and young trainers patrol the path."
    ),
    trainers=[
        _npc("Mikey", "Bug Catcher", [("Caterpie", 6), ("Weedle", 6)],
             intro="I love Bug-type Pokémon!"),
        _npc("Tim",   "Bug Catcher", [("Weedle", 7), ("Kakuna", 7)],
             intro="I'll bug you until you battle me!"),
    ],
    wild_encounters=[
        ("Pidgey",   5,  9),
        ("Rattata",  5,  8),
        ("Caterpie", 4,  7),
        ("Weedle",   4,  7),
    ],
    unlocks="Viridian Forest",
))

# ── Viridian Forest ───────────────────────────────────────────────────────────

_loc(Location(
    name="Viridian Forest",
    description=(
        "A sprawling ancient forest buzzing with insect cries.\n"
        "Sunlight barely filters through the canopy.\n"
        "Many trainers come here to catch Pikachu — be ready!"
    ),
    trainers=[
        _npc("Sammy",  "Bug Catcher", [("Caterpie", 7), ("Metapod", 7), ("Caterpie", 7)],
             intro="I've been training in this forest all week!"),
        _npc("Lara",   "Lass",        [("Pidgey", 9), ("Rattata", 9)],
             intro="Catch me if you can!"),
        _npc("Francis","Bug Catcher", [("Metapod", 9), ("Metapod", 9)],
             intro="My Metapod can Harden forever!",
             win="I'll harden up and battle you again!"),
    ],
    wild_encounters=[
        ("Caterpie", 5,  9),
        ("Metapod",  7, 12),
        ("Weedle",   5,  9),
        ("Kakuna",   7, 12),
        ("Pikachu",  4,  8),
    ],
    unlocks="Pewter City",
))

# ── Pewter City ───────────────────────────────────────────────────────────────

_loc(Location(
    name="Pewter City",
    description=(
        "A stone-grey city nestled in the mountains.\n"
        "The Pewter Museum of Science displays rare fossils.\n"
        "Gym Leader Brock, master of Rock types, awaits challengers."
    ),
    story_events={
        "BEAT_BROCK": (
            "Brock: I like to think I'm a pretty good Trainer, but\n"
            "you've proven me wrong.  Take the Boulder Badge!"
        ),
    },
    services=[LocationService.POKEMON_CENTER, LocationService.POKE_MART],
    gym_number=1,
    unlocks="Route 3",
))

# ── Route 3 ───────────────────────────────────────────────────────────────────

_loc(Location(
    name="Route 3",
    description=(
        "The route east of Pewter winds through open grassland.\n"
        "Junior Trainers flock here to train against each other.\n"
        "The distant peak of Mt. Moon looms on the horizon."
    ),
    trainers=[
        _npc("Martin",  "Youngster", [("Spearow", 11), ("NidoranM", 11)],
             intro="Don't underestimate my birds!"),
        _npc("Rachel",  "Lass",      [("Rattata", 11), ("Rattata", 12)],
             intro="I bet my Rattata is faster than yours!"),
        _npc("Kyle",    "Jr. Trainer", [("Spearow", 13), ("Mankey", 12)],
             intro="I've been training all the way from Pallet!"),
        _npc("Roberta", "Lass",      [("Jigglypuff", 14), ("Clefairy", 13)],
             intro="Singing Pokémon are the best!"),
    ],
    wild_encounters=[
        ("Spearow",   8, 14),
        ("NidoranM",  8, 13),
        ("NidoranF",  8, 13),
        ("Jigglypuff",10, 14),
    ],
    unlocks="Mt. Moon",
))

# ── Mt. Moon ──────────────────────────────────────────────────────────────────

_loc(Location(
    name="Mt. Moon",
    description=(
        "A vast, winding cave system said to contain rare Clefairy\n"
        "who dance under the moonstone's glow.\n"
        "Team Rocket has been excavating fossils in the lower caverns!"
    ),
    story_events={
        "MT_MOON_ROCKET_DEFEATED": (
            "Team Rocket Grunt: Boss won't be happy…  We were so close\n"
            "to stealing those fossils!  Curse you, {player}!\n\n"
            "Mysterious Scientist: Th-thank you!  Here — take one\n"
            "of these fossils as thanks.  They hold ancient Pokémon!"
        ),
    },
    trainers=[
        _npc("Elena",    "Jr. Trainer",  [("Clefairy", 12)],
             intro="Clefairy only comes out under the moon!"),
        _npc("Rex",      "Hiker",        [("Geodude", 12), ("Onix", 13)],
             intro="These rocks are my friends!"),
        _npc("Grunt A",  "Rocket Grunt", [("Sandshrew", 13), ("Rattata", 14)],
             intro="Halt! Team Rocket forbids passage!",
             win="Team Rocket will not be stopped so easily.",
             lose="Ugh… tell no one of this…"),
        _npc("Grunt B",  "Rocket Grunt", [("Zubat", 12), ("Rattata", 14), ("Zubat", 14)],
             intro="Give us your fossils — they belong to Team Rocket!",
             win="The Boss will hear about this defeat.",
             lose="How did we lose to a kid?!"),
    ],
    wild_encounters=[
        ("Zubat",    10, 15),
        ("Geodude",  10, 15),
        ("Paras",    10, 15),
        ("Clefairy", 10, 16),
    ],
    unlocks="Cerulean City",
))

# ── Cerulean City ─────────────────────────────────────────────────────────────

_loc(Location(
    name="Cerulean City",
    description=(
        "A seaside city with a calm, flowing river running through it.\n"
        "The Cerulean City Gym is known for its Water-type specialists.\n"
        "Gary is waiting on the Nugget Bridge — he wants a rematch!"
    ),
    story_events={
        "BEAT_RIVAL_CERULEAN": (
            "Gary: Hey, {player}!  I've got two badges already.\n"
            "What do you say — care to lose again?"
        ),
        "BEAT_MISTY": (
            "Misty: You're much stronger than I expected!\n"
            "Alright — you've earned the Cascade Badge!"
        ),
    },
    trainers=[
        _npc("Bob",     "Jr. Trainer",  [("Rattata", 15), ("Pidgey", 14)],
             intro="Catch me on the Nugget Bridge!"),
        _npc("Cindy",   "Jr. Trainer",  [("Bellsprout", 15), ("Oddish", 15)],
             intro="Flowers beat water any day!"),
        _npc("Nick",    "Jr. Trainer",  [("Mankey", 16), ("Machop", 16)],
             intro="Fighting types dominate!"),
    ],
    services=[LocationService.POKEMON_CENTER, LocationService.POKE_MART],
    gym_number=2,
    unlocks="Route 6",
))

# ── Route 6 ──────────────────────────────────────────────────────────────────

_loc(Location(
    name="Route 6",
    description=(
        "A wide open route leading south to Vermilion City.\n"
        "The route passes through verdant fields and small ponds.\n"
        "Psychic trainers meditate beside the water."
    ),
    trainers=[
        _npc("Paula",  "Picnicker", [("Poliwag", 16), ("Bellsprout", 16)],
             intro="I'm on a picnic AND a training journey!"),
        _npc("Ethan",  "Camper",    [("Drowzee", 17), ("Oddish", 15)],
             intro="Psychic powers will overcome you!"),
        _npc("Jenny",  "Lass",      [("Meowth", 17), ("Meowth", 18)],
             intro="Meowth pay day! Show me what you've got!"),
    ],
    wild_encounters=[
        ("Drowzee",  11, 18),
        ("Poliwag",  13, 18),
        ("Venonat",  13, 17),
    ],
    unlocks="Vermilion City",
))

# ── Vermilion City ────────────────────────────────────────────────────────────

_loc(Location(
    name="Vermilion City",
    description=(
        "A port city with the briny smell of the sea.\n"
        "The luxury cruise liner S.S. Anne is docked at the harbour.\n"
        "Lt. Surge, the Lightning American, runs the Electric gym."
    ),
    story_events={
        "SS_ANNE_VISITED": (
            "Gary: {player}!  I see you've come to the S.S. Anne too.\n"
            "I already beat all the trainers onboard.  Come battle me!\n\n"
            "After defeating Gary, the Captain gives you HM01 (Cut)!\n"
            "Now you can cut down small trees blocking your path."
        ),
        "BEAT_RIVAL_SS_ANNE": (
            "Gary: Dang it!  You're pretty good, {player}.\n"
            "I'll have to step up my training."
        ),
        "BEAT_SURGE": (
            "Lt. Surge: You're tough!  Even my Pokémon couldn't \n"
            "stop you.  Here's the Thunder Badge!  It's yours!"
        ),
    },
    services=[LocationService.POKEMON_CENTER, LocationService.POKE_MART, LocationService.SS_ANNE],
    gym_number=3,
    unlocks="Lavender Town",
))

# ── Lavender Town ─────────────────────────────────────────────────────────────

_loc(Location(
    name="Lavender Town",
    description=(
        "A small, eerie town known as the resting place of Pokémon.\n"
        "Pokémon Tower looms here, filled with the spirits of the departed.\n"
        "A ghostly presence haunts the upper floors…"
    ),
    story_events={
        "POKEMON_TOWER_GHOST": (
            "A faceless ghost blocks the staircase!\n"
            "With the Silph Scope, you reveal it as a MAROWAK —\n"
            "the spirit of a mother slain by Team Rocket.\n"
            "After a solemn battle, the ghost is finally at peace."
        ),
    },
    trainers=[
        _npc("Mr. Fuji", "Scientist", [("Cubone", 20), ("Marowak", 24)],
             intro="Please… find peace for the spirits here.",
             win="Thank you.  This tower can rest now.",
             lose="Even I could not protect them…"),
        _npc("Channeler A", "Scientist", [("Gastly", 22)],
             intro="The spirit speaks through me!"),
        _npc("Channeler B", "Scientist", [("Haunter", 24), ("Haunter", 24)],
             intro="Stay away from the tower!"),
    ],
    wild_encounters=[
        ("Gastly",  22, 28),
        ("Haunter", 24, 28),
        ("Cubone",  20, 26),
    ],
    services=[LocationService.POKEMON_CENTER],
    unlocks="Celadon City",
))

# ── Celadon City ──────────────────────────────────────────────────────────────

_loc(Location(
    name="Celadon City",
    description=(
        "The largest city in Kanto, famous for its department store.\n"
        "The Celadon Game Corner hides a Team Rocket hideout in the back!\n"
        "Gym Leader Erika specialises in beautiful Grass-type Pokémon."
    ),
    story_events={
        "GAME_CORNER_CLEARED": (
            "Team Rocket Boss Giovanni: Impressive, {player}.\n"
            "But Team Rocket will return — count on it!\n"
            "Giovanni flees!  The Game Corner is safe again.\n"
            "A grateful patron gives you a free Eevee!"
        ),
        "BEAT_ERIKA": (
            "Erika: What a delightful battle!  You've bested me,\n"
            "{player}.  Accept the Rainbow Badge as proof!"
        ),
    },
    trainers=[
        _npc("Grunt C", "Rocket Grunt", [("Ekans", 22), ("Zubat", 24)],
             intro="Team Rocket runs this town!",
             lose="Retreat! Retreat!"),
        _npc("Grunt D", "Rocket Grunt", [("Koffing", 24), ("Drowzee", 26)],
             intro="No one gets past me!",
             lose="The boss will be furious…"),
        _npc("Grunt E", "Rocket Grunt", [("Rattata", 25), ("Sandshrew", 27), ("Clefairy", 23)],
             intro="You'll regret messing with Team Rocket!"),
    ],
    services=[LocationService.POKEMON_CENTER, LocationService.POKE_MART, LocationService.GAME_CORNER],
    gym_number=4,
    unlocks="Fuchsia City",
))

# ── Fuchsia City ──────────────────────────────────────────────────────────────

_loc(Location(
    name="Fuchsia City",
    description=(
        "A city at the southern edge of Kanto, known for its Safari Zone.\n"
        "The Safari Zone is home to rare Pokémon not found elsewhere.\n"
        "Gym Leader Koga, the ninja master, specialises in Poison types."
    ),
    story_events={
        "BEAT_KOGA": (
            "Koga: A true Pokémon Master must master the mind as well\n"
            "as the body.  You have done both.  Take the Soul Badge."
        ),
    },
    services=[LocationService.POKEMON_CENTER, LocationService.POKE_MART, LocationService.SAFARI_ZONE],
    gym_number=5,
    unlocks="Saffron City",
))

# ── Saffron City ──────────────────────────────────────────────────────────────

_loc(Location(
    name="Saffron City",
    description=(
        "The largest metropolis in Kanto, home to the Silph Company.\n"
        "Team Rocket has seized the Silph Co. building — they want\n"
        "the Master Ball prototype!  Gary is somewhere inside too."
    ),
    story_events={
        "SILPH_CO_CLEARED": (
            "Giovanni: You again, {player}?!  You've ruined everything!\n"
            "Team Rocket, retreat!  This battle is over for now.\n"
            "Silph Co. President: Thank you!  Please accept the Master Ball —\n"
            "the ultimate Pokémon catching device!"
        ),
        "BEAT_RIVAL_SILPH": (
            "Gary: {player}!  I was just warming up for you here.\n"
            "Don't think this means anything — let's battle!"
        ),
        "BEAT_SABRINA": (
            "Sabrina: I foresaw your victory, and yet I still lost.\n"
            "You've earned the Marsh Badge, {player}."
        ),
    },
    trainers=[
        _npc("Grunt F", "Rocket Grunt", [("Arbok", 34), ("Rattata", 32), ("Sandshrew", 35)],
             intro="Silph Co. belongs to Team Rocket now!",
             lose="The Boss… won't be pleased."),
        _npc("Grunt G", "Rocket Grunt", [("Zubat", 35), ("Golbat", 36)],
             intro="Go away, kid!",
             lose="You're too strong for us!"),
        _npc("Grunt H", "Rocket Grunt", [("Machop", 35), ("Drowzee", 37), ("Kadabra", 38)],
             intro="Protect the Master Ball!  Stop that trainer!",
             lose="I can't believe it…"),
    ],
    services=[LocationService.POKEMON_CENTER, LocationService.POKE_MART, LocationService.SILPH_CO],
    gym_number=6,
    unlocks="Cinnabar Island",
))

# ── Cinnabar Island ───────────────────────────────────────────────────────────

_loc(Location(
    name="Cinnabar Island",
    description=(
        "A volcanic island south of Pallet Town.\n"
        "The Pokémon Fossil Lab can restore ancient Pokémon from fossils.\n"
        "Blaine, the Hotheaded Quiz Master, runs the Fire-type Gym."
    ),
    story_events={
        "BEAT_BLAINE": (
            "Blaine: Magnificent!  Your Pokémon turned my blazing\n"
            "strategy to ash.  Take the Volcano Badge, you've earned it!"
        ),
    },
    services=[
        LocationService.POKEMON_CENTER,
        LocationService.POKE_MART,
        LocationService.FOSSIL_LAB,
    ],
    gym_number=7,
    unlocks="Viridian City (Return)",
))

# ── Viridian City (Return) ────────────────────────────────────────────────────

_loc(Location(
    name="Viridian City (Return)",
    description=(
        "The Viridian Gym is finally open!\n"
        "Rumour has it the Gym Leader is connected to Team Rocket.\n"
        "Seven badges in hand — this is the final Gym."
    ),
    story_events={
        "BEAT_GIOVANNI": (
            "Giovanni: Hmm…  So you bested me.  I am the Leader of\n"
            "Team Rocket as well as this Gym.  You've foiled us at\n"
            "every turn, {player}.  Perhaps I should reconsider\n"
            "my path.  Take the Earth Badge — you've more than earned it."
        ),
    },
    services=[LocationService.POKEMON_CENTER, LocationService.POKE_MART],
    gym_number=8,
    unlocks="Victory Road",
))

# ── Victory Road ──────────────────────────────────────────────────────────────

_loc(Location(
    name="Victory Road",
    description=(
        "A treacherous cave path carved by ancient trainers seeking glory.\n"
        "Powerful wild Pokémon lurk in the darkness.\n"
        "Gary is waiting at the far end for one final battle."
    ),
    story_events={
        "BEAT_RIVAL_VICTORY_ROAD": (
            "Gary: {player}!  This is it — our final battle before\n"
            "the Pokémon League.  Give it everything you've got!"
        ),
    },
    trainers=[
        _npc("Alan",   "Hiker",       [("Graveler", 46), ("Onix", 48), ("Graveler", 46)],
             intro="Only the strong survive Victory Road!"),
        _npc("Cara",   "Jr. Trainer", [("Clefable", 49), ("Jigglypuff", 47)],
             intro="My Clefable will stop you here!"),
        _npc("Simon",  "Cooltrainer", [("Electrode", 47), ("Slowbro", 48), ("Dewgong", 50)],
             intro="You'll go no further, rookie!"),
        _npc("Archer", "Cooltrainer", [("Clefable", 50), ("Chansey", 50), ("Tauros", 52)],
             intro="To reach the League you must beat me!"),
    ],
    wild_encounters=[
        ("Graveler", 40, 48),
        ("Venomoth", 38, 45),
        ("Machoke",  40, 46),
        ("Onix",     38, 44),
        ("Ditto",    35, 42),
    ],
    unlocks="Indigo Plateau",
))

# ── Indigo Plateau ────────────────────────────────────────────────────────────

_loc(Location(
    name="Indigo Plateau",
    description=(
        "The home of the Pokémon League — the pinnacle of Trainer achievement.\n"
        "Beyond these doors wait the Elite Four, and beyond them, the Champion.\n"
        "Only Trainers with all 8 Badges may enter.  Your destiny awaits."
    ),
    story_events={
        "BEAT_CHAMPION": (
            "Congratulations, {player}!\n"
            "You have defeated the Pokémon League Champion and proven\n"
            "yourself the greatest Trainer in all of Kanto!\n"
            "Professor Oak: {player}!  I always knew you had it in you.\n"
            "Your name will live on in the Hall of Fame forever."
        ),
    },
    services=[LocationService.POKEMON_CENTER],
))

# ── Optional: Safari Zone ─────────────────────────────────────────────────────

_loc(Location(
    name="Safari Zone",
    description=(
        "A protected nature reserve in Fuchsia City.\n"
        "Rare Pokémon like Chansey, Tauros, Scyther, and Kangaskhan\n"
        "can be found here — but you can only use Safari Balls!"
    ),
    wild_encounters=[
        ("NidoranF", 22, 28),
        ("NidoranM", 22, 28),
        ("Exeggcute",24, 28),
        ("Chansey",  25, 30),
        ("Tauros",   25, 30),
        ("Scyther",  25, 30),
        ("Kangaskhan",25,30),
        ("Pinsir",   25, 30),
    ],
))

# ── Optional: Seafoam Islands ─────────────────────────────────────────────────

_loc(Location(
    name="Seafoam Islands",
    description=(
        "A pair of icy caverns on the route between Cinnabar and Fuchsia.\n"
        "Powerful Water and Ice Pokémon dwell in the freezing pools.\n"
        "Deep inside slumbers Articuno, the legendary Ice bird."
    ),
    story_events={
        "SEAFOAM_VISITED": (
            "You navigate the complex cave puzzles and reach the\n"
            "innermost chamber.  In the heart of the ice… ARTICUNO!"
        ),
    },
    wild_encounters=[
        ("Seel",      32, 38),
        ("Dewgong",   35, 42),
        ("Slowpoke",  32, 38),
        ("Shellder",  32, 38),
        ("Articuno",  50, 50),
    ],
    services=[LocationService.SEAFOAM_CAVE],
))


# ── Story-path order ──────────────────────────────────────────────────────────

STORY_PATH: list[str] = [
    "Pallet Town",
    "Route 1",
    "Viridian City",
    "Route 2",
    "Viridian Forest",
    "Pewter City",
    "Route 3",
    "Mt. Moon",
    "Cerulean City",
    "Route 6",
    "Vermilion City",
    "Lavender Town",
    "Celadon City",
    "Fuchsia City",
    "Saffron City",
    "Cinnabar Island",
    "Viridian City (Return)",
    "Victory Road",
    "Indigo Plateau",
]
