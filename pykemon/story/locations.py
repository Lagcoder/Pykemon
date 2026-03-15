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
    POWER_PLANT    = "Power Plant"
    POKEMON_MANSION = "Pokémon Mansion"
    CERULEAN_CAVE  = "Cerulean Cave"


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
    # Fishing encounter table per rod: {"Old Rod": [...], "Good Rod": [...], "Super Rod": [...]}
    fish_encounters: dict[str, list[tuple[str, int, int]]] = field(default_factory=dict)
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
    fish_encounters={
        "Old Rod":   [("Magikarp", 5, 10)],
        "Good Rod":  [("Magikarp", 10, 20), ("Poliwag", 12, 18)],
        "Super Rod": [("Poliwag", 20, 30), ("Poliwhirl", 25, 35), ("Gyarados", 15, 25)],
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
        _npc("Martin",  "Youngster", [("Spearow", 11), ("Nidoran♂", 11)],
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
        ("Nidoran♂",  8, 13),
        ("Nidoran♀",  8, 13),
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
    fish_encounters={
        "Old Rod":   [("Magikarp", 10, 15)],
        "Good Rod":  [("Poliwag", 15, 22), ("Magikarp", 15, 20)],
        "Super Rod": [("Poliwhirl", 25, 35), ("Goldeen", 22, 30), ("Seaking", 30, 38)],
    },
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
    fish_encounters={
        "Old Rod":   [("Magikarp", 10, 15)],
        "Good Rod":  [("Poliwag", 14, 20), ("Magikarp", 14, 18)],
        "Super Rod": [("Poliwhirl", 22, 32), ("Slowpoke", 20, 28)],
    },
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
    fish_encounters={
        "Old Rod":   [("Magikarp", 10, 15)],
        "Good Rod":  [("Tentacool", 15, 22), ("Horsea", 15, 22)],
        "Super Rod": [("Shellder", 25, 35), ("Tentacruel", 30, 40), ("Gyarados", 20, 30)],
    },
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
    fish_encounters={
        "Old Rod":   [("Magikarp", 15, 20)],
        "Good Rod":  [("Goldeen", 18, 26), ("Magikarp", 16, 22)],
        "Super Rod": [("Seaking", 28, 38), ("Dratini", 10, 20), ("Gyarados", 20, 30)],
    },
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
        "MOLTRES_ENCOUNTERED": (
            "Deep in the cave, a warm, orange glow flickers ahead…\n"
            "MOLTRES — the legendary Fire bird — blocks your path!\n"
            "Its scorching wings could melt the cave walls.  Be ready!"
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
        ("Moltres",  50, 50),
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
        ("Nidoran♀", 22, 28),
        ("Nidoran♂", 22, 28),
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


# ── Route 4 ──────────────────────────────────────────────────────────────────

_loc(Location(
    name="Route 4",
    description=(
        "The short route east of Mt. Moon leading into Cerulean City.\n"
        "Trainers gather here after conquering the cave.\n"
        "The occasional wild Magikarp leaps from the pond."
    ),
    trainers=[
        _npc("Evan",   "Jr. Trainer", [("Spearow", 14), ("Rattata", 14)],
             intro="Fresh out of Mt. Moon — and ready to win!",
             win="Go challenge Misty!  She's tough!",
             lose="Beaten before I even reached Cerulean…"),
        _npc("Sandra", "Jr. Trainer", [("Clefairy", 15), ("Jigglypuff", 15)],
             intro="Normal-type Pokémon are stronger than people think!",
             win="Cerulean Gym is right ahead — and Misty is fierce!",
             lose="My Clefairy used Sing but it didn't work in time!"),
        _npc("Pete",   "Hiker",       [("Geodude", 13), ("Geodude", 14), ("Machop", 13)],
             intro="I've been hiking since before you were born, kid!",
             win="Ha!  Your training has just begun!",
             lose="Solid effort!  Keep it up on the road ahead."),
    ],
    wild_encounters=[
        ("Spearow",  10, 16),
        ("Rattata",  10, 15),
        ("Ekans",    12, 16),
        ("Magikarp", 12, 15),
    ],
))

# ── Rock Tunnel ───────────────────────────────────────────────────────────────

_loc(Location(
    name="Rock Tunnel",
    description=(
        "A pitch-black cave connecting Route 9 to Lavender Town.\n"
        "Without Flash, trainers stumble blindly through the dark.\n"
        "Hikers and rock-type enthusiasts call this cave their training ground."
    ),
    trainers=[
        _npc("Lorenzo",  "Hiker",       [("Machop", 22), ("Onix", 24)],
             intro="You need Flash to navigate here — I know every inch!",
             win="Stumble on, then!  Lavender Town awaits.",
             lose="You found your way in the dark better than I did!"),
        _npc("Grace",    "Jr. Trainer", [("Geodude", 23), ("Geodude", 23), ("Graveler", 24)],
             intro="Rock-types are as solid as this mountain!",
             win="You can't chip through my defences!",
             lose="Cracked… like a geode."),
        _npc("Ronald",   "Hiker",       [("Onix", 25), ("Onix", 25)],
             intro="Two Onix!  Try and stop us!",
             win="Hah!  Two heads are better than one!",
             lose="Both my Onix fainted…  Unbelievable."),
        _npc("Melissa",  "Jr. Trainer", [("Paras", 23), ("Parasect", 25)],
             intro="My Parasect knows all about cave life!",
             win="Parasect's spores will put you to sleep!",
             lose="My spores failed to take hold…"),
    ],
    wild_encounters=[
        ("Zubat",    15, 22),
        ("Geodude",  15, 22),
        ("Machop",   16, 22),
        ("Onix",     17, 24),
    ],
))

# ── Power Plant ───────────────────────────────────────────────────────────────

_loc(Location(
    name="Power Plant",
    description=(
        "An abandoned electricity-generating plant north of Cerulean City.\n"
        "Electric Pokémon have taken over every room.\n"
        "Somewhere in the deepest chamber, legend says a lightning bird lurks."
    ),
    story_events={
        "POWER_PLANT_VISITED": (
            "Sparks crackle.  Every circuit buzzes.\n"
            "Deep inside the generator room, a bolt of light ROARS at you!\n"
            "It's ZAPDOS — the legendary Electric bird!"
        ),
    },
    trainers=[
        _npc("Winston", "Scientist",  [("Magnemite", 30), ("Magneton", 33)],
             intro="This plant's power now belongs to the Pokémon!",
             win="The voltage here is off the charts!",
             lose="Short-circuited by a challenger…"),
        _npc("Frank",   "Scientist",  [("Voltorb", 31), ("Electrode", 35)],
             intro="One wrong step and BOOM — Electrode!",
             win="Ha!  You'll set one off eventually!",
             lose="My Electrode… detonated too early."),
    ],
    wild_encounters=[
        ("Magnemite", 22, 32),
        ("Magneton",  25, 35),
        ("Voltorb",   22, 32),
        ("Electrode", 25, 36),
        ("Electabuzz",28, 36),
        ("Zapdos",    50, 50),
    ],
))

# ── Pokémon Mansion ───────────────────────────────────────────────────────────

_loc(Location(
    name="Pokémon Mansion",
    description=(
        "A scorched, crumbling mansion on Cinnabar Island.\n"
        "Once the research home of the scientist who created Mewtwo.\n"
        "Journals describe a terrible experiment gone horribly wrong."
    ),
    story_events={
        "MANSION_VISITED": (
            "You find charred journals describing the creation of MEW TWO.\n"
            "The entry reads: 'We have created the world's most powerful Pokémon.\n"
            "But we cannot control it…  It has escaped to CERULEAN CAVE.'"
        ),
    },
    trainers=[
        _npc("Dr. Fuji",  "Scientist", [("Magmar", 38), ("Ditto", 35)],
             intro="These ruins hold the secret to the most powerful Pokémon!",
             win="Mewtwo's power dwarfs anything you have seen!",
             lose="Even here… a trainer defeats me."),
        _npc("Marcus",    "Scientist", [("Ponyta", 36), ("Growlithe", 38)],
             intro="The mansion's fire Pokémon protect these secrets!",
             win="Stay away from the journals!",
             lose="The secrets burn through my defences!"),
        _npc("Team R. Scientist", "Rocket Grunt",
             [("Koffing", 38), ("Grimer", 37), ("Muk", 40)],
             intro="Team Rocket still searches for Mewtwo's data!",
             win="We will find Mewtwo and control it!",
             lose="The data…  We must report this to the Boss."),
    ],
    wild_encounters=[
        ("Growlithe", 30, 38),
        ("Ponyta",    30, 38),
        ("Grimer",    30, 38),
        ("Koffing",   30, 38),
        ("Magmar",    34, 40),
        ("Ditto",     28, 36),
    ],
))

# ── Cerulean Cave ─────────────────────────────────────────────────────────────

_loc(Location(
    name="Cerulean Cave",
    description=(
        "A forbidden cave north of Cerulean City — entry is restricted\n"
        "until you become Pokémon League Champion.\n"
        "The bio-engineered Pokémon MEWTWO dwells deep within."
    ),
    wild_encounters=[
        ("Rhydon",    55, 65),
        ("Golduck",   52, 60),
        ("Parasect",  50, 58),
        ("Ditto",     48, 55),
        ("Mewtwo",    70, 70),
    ],
))

# ── Route 9 / Route 10 ────────────────────────────────────────────────────────

_loc(Location(
    name="Route 9",
    description=(
        "A winding path east of Cerulean City leading to Rock Tunnel.\n"
        "Tough trainers patrol the cliffside edges.\n"
        "The distant sound of the Power Plant's hum fills the air."
    ),
    trainers=[
        _npc("Bruce",  "Jr. Trainer", [("Ekans", 20), ("Spearow", 22)],
             intro="Nobody gets past my checkpoint!",
             win="Keep heading east for the Rock Tunnel!",
             lose="I let the tunnel's trainer down!"),
        _npc("April",  "Lass",        [("Meowth", 21), ("Persian", 22)],
             intro="My Persian will claw you to ribbons!",
             win="Persian is too cool to lose!",
             lose="Oh no — my favourite Pokémon lost!"),
        _npc("Victor", "Camper",      [("Nidorino", 22), ("Nidorina", 22)],
             intro="Nido-twins — double the trouble for you!",
             win="Double defeat — for you!",
             lose="Both my Nidos down?  Unbelievable!"),
    ],
    wild_encounters=[
        ("Ekans",    18, 25),
        ("Spearow",  18, 24),
        ("Nidoran♂", 18, 24),
        ("Nidoran♀", 18, 24),
    ],
))

# ── Route 11 / Route 12 ───────────────────────────────────────────────────────

_loc(Location(
    name="Route 11",
    description=(
        "A long flat road stretching east of Vermilion City.\n"
        "Trainers on the lookout for trading partners roam here.\n"
        "Drowzee are oddly common — keep your wits sharp."
    ),
    trainers=[
        _npc("Ollie",  "Youngster",  [("Drowzee", 21), ("Hypno", 22)],
             intro="Drowzee put me to sleep — but not in battle!",
             win="Hypno will hypnotise you!",
             lose="I've been put to sleep by my own team!"),
        _npc("Brenda", "Lass",       [("Pidgey", 20), ("Pidgeotto", 22)],
             intro="My birds will fly circles around your team!",
             win="Pidgeot incoming — next time!",
             lose="Grounded by a rookie!"),
        _npc("Ivan",   "Jr. Trainer",[("Ekans", 22), ("Arbok", 24)],
             intro="The poison of Arbok will paralyse your spirit!",
             win="Run while you can!",
             lose="My Arbok's Wrap couldn't hold you!"),
    ],
    wild_encounters=[
        ("Spearow",  15, 22),
        ("Ekans",    15, 22),
        ("Drowzee",  17, 24),
        ("Rattata",  15, 21),
    ],
))

# ── Route 13 / Route 14 / Route 15 ───────────────────────────────────────────

_loc(Location(
    name="Route 13",
    description=(
        "A narrow path woven between tall hedges south of Lavender Town.\n"
        "Bird-keeper trainers line every hedge gap.\n"
        "Scyther can sometimes be spotted cutting through the brush."
    ),
    trainers=[
        _npc("Frank",  "Bird Keeper", [("Pidgeotto", 26), ("Fearow", 27)],
             intro="My birds own the sky above this route!",
             win="You're grounded, rookie!",
             lose="Brought down to earth…"),
        _npc("Ally",   "Lass",        [("Venonat", 27), ("Venomoth", 28)],
             intro="Night or day, Venomoth's powder will blind you!",
             win="You can't see what you can't dodge!",
             lose="My powder scattered in the wind!"),
        _npc("Dale",   "Jr. Trainer", [("Scyther", 28)],
             intro="Scyther slices through any obstacle!",
             win="Scyther's blades are too fast to dodge!",
             lose="Cut down by a stronger trainer!"),
    ],
    wild_encounters=[
        ("Pidgey",   22, 28),
        ("Venonat",  22, 28),
        ("Scyther",  25, 30),
        ("Ditto",    24, 28),
    ],
))

# ── Route 16 / Route 17 (Cycling Road) ───────────────────────────────────────

_loc(Location(
    name="Cycling Road",
    description=(
        "The famous downhill route between Celadon City and Fuchsia City.\n"
        "Bikers race down the long slope at breakneck speed.\n"
        "You need a Bicycle to ride here — or a fast Pokémon!"
    ),
    trainers=[
        _npc("Rex",    "Biker",  [("Weezing", 30), ("Koffing", 29)],
             intro="Bikers rule this road!  Out of my way!",
             win="VROOOOM!  See ya!",
             lose="My engine stalled!"),
        _npc("Marco",  "Biker",  [("Ponyta", 31), ("Rapidash", 33)],
             intro="My Rapidash is faster than any bicycle!",
             win="No one outraces me!",
             lose="Got lapped on my own road!"),
        _npc("Yolanda","Biker",  [("Grimer", 30), ("Muk", 32)],
             intro="My Muk will slow you down to a crawl!",
             win="Sludge!  Sludge everywhere!",
             lose="Even my Muk got wiped clean!"),
    ],
    wild_encounters=[
        ("Spearow",  25, 30),
        ("Rattata",  24, 29),
        ("Doduo",    25, 31),
    ],
))

# ── Route 18 / Route 19 (Sea Routes) ─────────────────────────────────────────

_loc(Location(
    name="Sea Route 19",
    description=(
        "Open ocean waters stretching south of Fuchsia City.\n"
        "Swimmers and divers patrol the waves on their Pokémon.\n"
        "Tentacool swarm the surface — bring Repels!"
    ),
    trainers=[
        _npc("Carol",  "Swimmer", [("Tentacool", 30), ("Staryu", 31)],
             intro="The sea belongs to Water-type trainers!",
             win="Sink or swim, rookie!",
             lose="Wiped out by the current!"),
        _npc("Derek",  "Swimmer", [("Goldeen", 31), ("Seaking", 33)],
             intro="My Seaking will gore you!",
             win="Horn Drill — coming for you!",
             lose="My Seaking floundered!"),
    ],
    wild_encounters=[
        ("Tentacool",  25, 35),
        ("Tentacruel", 30, 38),
        ("Horsea",     25, 32),
        ("Seadra",     30, 38),
    ],
    fish_encounters={
        "Old Rod":   [("Magikarp", 20, 28)],
        "Good Rod":  [("Horsea", 22, 32), ("Tentacool", 22, 30)],
        "Super Rod": [("Seadra", 30, 40), ("Staryu", 28, 38), ("Gyarados", 25, 35)],
    },
))

# ── Route 5 (Cerulean → Saffron Underground) ─────────────────────────────────

_loc(Location(
    name="Route 5",
    description=(
        "A broad road connecting Cerulean City southward to Saffron City.\n"
        "The underground path beneath the road is a shortcut used by Trainers.\n"
        "Psychic and Normal-type trainers frequent the grassy stretch."
    ),
    trainers=[
        _npc("James",   "Jr. Trainer", [("Pidgeotto", 18), ("Rattata", 17)],
             intro="I've been training here every day!",
             win="You barely beat me — Saffron won't be easy!",
             lose="Beaten on my own route!"),
        _npc("Susan",   "Lass",        [("Clefairy", 18), ("Jigglypuff", 18)],
             intro="My Clefairy is precious — and powerful!",
             win="No one beats my Clefairy!",
             lose="My Clefairy's Metronome… misfire."),
        _npc("Huey",    "Camper",      [("Meowth", 19), ("Abra", 20)],
             intro="I've got a Psychic-type AND a Normal-type!  Try me!",
             win="Abra will teleport your victory away!",
             lose="Abra used Teleport… on me."),
    ],
    wild_encounters=[
        ("Pidgey",   13, 20),
        ("Meowth",   14, 20),
        ("Rattata",  13, 19),
        ("Abra",     14, 20),
    ],
    fish_encounters={
        "Old Rod":   [("Magikarp", 10, 18)],
        "Good Rod":  [("Poliwag", 16, 22)],
        "Super Rod": [("Poliwhirl", 22, 30), ("Slowpoke", 20, 28)],
    },
))

# ── Route 7 (Celadon ↔ Saffron) ──────────────────────────────────────────────

_loc(Location(
    name="Route 7",
    description=(
        "A short stretch between Celadon City and Saffron City.\n"
        "The western end opens into Celadon's lush gardens.\n"
        "Psychics often set up camp here, testing their powers."
    ),
    trainers=[
        _npc("Hannah",  "Psychic",     [("Drowzee", 25), ("Hypno", 28)],
             intro="My Hypno will make you forget you ever challenged me!",
             win="You cannot resist the power of hypnosis!",
             lose="My trance… broken!"),
        _npc("Logan",   "Jr. Trainer", [("Raichu", 26), ("Electabuzz", 28)],
             intro="Electric power surges through both my Pokémon!",
             win="The voltage was too much for you!",
             lose="Short-circuited by a stranger!"),
    ],
    wild_encounters=[
        ("Pidgey",   22, 28),
        ("Vulpix",   22, 28),
        ("Growlithe",22, 28),
        ("Drowzee",  22, 28),
    ],
))

# ── Route 8 (Lavender ↔ Celadon Underground) ─────────────────────────────────

_loc(Location(
    name="Route 8",
    description=(
        "The road linking Lavender Town west toward Celadon City.\n"
        "The underground path cuts through to Celadon's south gate.\n"
        "Trainers here tend to be superstitious — blame the proximity to the Tower."
    ),
    trainers=[
        _npc("Gina",    "Lass",        [("Ninetales", 27), ("Wigglytuff", 28)],
             intro="My Ninetales has nine tails and nine tricks!",
             win="You'll curse the day you challenged me!",
             lose="My nine lives used up at once!"),
        _npc("Cooper",  "Jr. Trainer", [("Kadabra", 28), ("Mr. Mime", 27)],
             intro="Psychic-types see through all your strategies!",
             win="Kadabra predicted your every move!",
             lose="I did NOT see that coming!"),
        _npc("Tina",    "Picnicker",   [("Clefable", 28), ("Chansey", 27)],
             intro="My Normal-types are tougher than they look!",
             win="Chansey's Softboiled is unstoppable!",
             lose="Egg shell cracked…"),
    ],
    wild_encounters=[
        ("Ekans",    22, 28),
        ("Ninetales",25, 30),
        ("Growlithe",22, 28),
        ("Drowzee",  22, 28),
    ],
))

# ── Route 22 (Pallet → Viridian south gate) ───────────────────────────────────

_loc(Location(
    name="Route 22",
    description=(
        "A grassy route west of Viridian City leading toward Victory Road.\n"
        "Trainers with all 8 badges come here to warm up before the League.\n"
        "The western gate is sealed until all 8 Gym badges are earned."
    ),
    trainers=[
        _npc("Billy",   "Youngster",   [("Spearow", 4), ("Rattata", 4)],
             intro="I'm training to be the best — starting here!",
             win="Beat me?  Just a warm-up!",
             lose="I'll train harder tonight!"),
    ],
    wild_encounters=[
        ("Spearow", 2, 5),
        ("Rattata",  2, 5),
        ("Nidoran♂", 3, 5),
        ("Nidoran♀", 3, 5),
    ],
))

# ── Route 24 / Nugget Bridge (Cerulean north) ────────────────────────────────

_loc(Location(
    name="Route 24",
    description=(
        "The famous Nugget Bridge stretches north of Cerulean City.\n"
        "Five trainers guard the bridge — defeat them all and earn a Nugget!\n"
        "Team Rocket waits at the end with an offer you'll want to refuse."
    ),
    trainers=[
        _npc("Josh",    "Bug Catcher", [("Caterpie", 14), ("Weedle", 14)],
             intro="Beat all five of us and get a prize!",
             win="Bug-types have you in their grip!",
             lose="Squished!"),
        _npc("Mikey",   "Youngster",   [("Spearow", 14), ("Mankey", 15)],
             intro="I've been waiting on this bridge all week!",
             win="Flying AND Fighting — you never had a chance!",
             lose="Knocked off the bridge by a rookie!"),
        _npc("Jenna",   "Lass",        [("Oddish", 15), ("Bellsprout", 15)],
             intro="Grass-types thrive near water — just like on this bridge!",
             win="Grass beats Water — you're done!",
             lose="My petals scattered in the breeze!"),
        _npc("Chad",    "Jr. Trainer", [("Pidgeotto", 16), ("Rattata", 15)],
             intro="Only the strong make it past the Nugget Bridge!",
             win="Return to Cerulean and try again!",
             lose="You got the better of me — the prize awaits!"),
        _npc("Rocket Grunt", "Rocket Grunt",
             [("Ekans", 16), ("Sandshrew", 16)],
             intro="Excellent work, Trainer!  Now join Team Rocket — or face us!",
             win="Heh.  Joining was the smart choice — too bad you refused.",
             lose="You dare defy Team Rocket?!  I'll report this to the Boss!"),
    ],
    wild_encounters=[
        ("Caterpie", 12, 17),
        ("Weedle",   12, 17),
        ("Metapod",  14, 18),
        ("Kakuna",   14, 18),
        ("Oddish",   13, 18),
    ],
    fish_encounters={
        "Old Rod":   [("Magikarp", 10, 15)],
        "Good Rod":  [("Poliwag", 14, 20), ("Goldeen", 15, 20)],
        "Super Rod": [("Poliwhirl", 25, 32), ("Seaking", 28, 36)],
    },
))

# ── Route 25 (Cape / Bill's House) ────────────────────────────────────────────

_loc(Location(
    name="Route 25",
    description=(
        "A winding coastal path leading to Bill's cottage on Sea Cottage Cape.\n"
        "Bill, the Pokémon Storage creator, accidentally fused with a Pokémon!\n"
        "Help him — and earn the ticket to the S.S. Anne."
    ),
    story_events={
        "BILL_RESCUED": (
            "Bill: Ahh!  A Trainer!  I need your help.\n"
            "I've merged with a Pokémon in a teleportation experiment.\n"
            "Please — operate the machine and separate us!\n\n"
            "Bill: Phew — I'm myself again!  As thanks, take this S.S. Ticket!\n"
            "Board the S.S. Anne in Vermilion City for a Trainer-rich voyage!"
        ),
    },
    trainers=[
        _npc("Tammy",   "Jr. Trainer", [("Goldeen", 17), ("Poliwag", 16)],
             intro="The view from this cape is beautiful — fight me or miss it!",
             win="The cape belongs to those who can battle!",
             lose="Swept away like the tide!"),
        _npc("Lance",   "Jr. Trainer", [("Slowpoke", 18), ("Psyduck", 17)],
             intro="Water and Psychic both live on this route!",
             win="Calm as the ocean — and twice as deep!",
             lose="My head hurts from this loss!"),
    ],
    wild_encounters=[
        ("Caterpie",  12, 17),
        ("Weedle",    12, 17),
        ("Bellsprout",13, 18),
        ("Oddish",    13, 18),
    ],
    fish_encounters={
        "Old Rod":   [("Magikarp", 10, 15)],
        "Good Rod":  [("Horsea", 15, 20), ("Tentacool", 14, 20)],
        "Super Rod": [("Seadra", 28, 35), ("Staryu", 25, 32)],
    },
))

# ── Story-path order ──────────────────────────────────────────────────────────

STORY_PATH: list[str] = [
    "Pallet Town",
    "Route 22",
    "Route 1",
    "Viridian City",
    "Route 2",
    "Viridian Forest",
    "Pewter City",
    "Route 3",
    "Mt. Moon",
    "Route 4",
    "Route 24",
    "Route 25",
    "Cerulean City",
    "Route 5",
    "Route 9",
    "Rock Tunnel",
    "Route 8",
    "Lavender Town",
    "Route 6",
    "Vermilion City",
    "Route 11",
    "Route 7",
    "Celadon City",
    "Route 13",
    "Cycling Road",
    "Fuchsia City",
    "Saffron City",
    "Sea Route 19",
    "Cinnabar Island",
    "Pokémon Mansion",
    "Viridian City (Return)",
    "Victory Road",
    "Indigo Plateau",
]
