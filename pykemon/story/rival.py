"""
pykemon/story/rival.py

The player's rival, Gary Oak.  His team grows at every encounter and is
chosen to be slightly ahead of or equal to the player's progression.
He always picks the starter that is weak against the player's starter
(giving the player a type advantage from the very first battle).
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.trainer import Trainer

RIVAL_NAME = "Gary"


# Maps player starter → rival's starter (type is weak AGAINST the player's starter).
# e.g. player picks Bulbasaur (Grass) → rival gets Squirtle (Water, weak to Grass).
_COUNTER_STARTER: dict[str, str] = {
    "Bulbasaur":  "Squirtle",    # Water is weak to Grass
    "Charmander": "Bulbasaur",   # Grass is weak to Fire
    "Squirtle":   "Charmander",  # Fire is weak to Water
}

# Teams at each encounter.  The last entry of each list is always the rival's
# starter (substituted at runtime once we know what the player chose).
# Format: list of (species_name, level).
# STARTER placeholder is replaced when building the team.
_RIVAL_PARTIES: list[dict] = [
    # 0 — Pallet Town (Route 22): just received a starter
    {
        "intro": (
            "Gary: Smell ya later, {player}!\n"
            "I've already got a better Pokémon than you!"
        ),
        "win":  "Gary: Heh, I just got this thing. I'll train harder. Smell ya later!",
        "lose": "Gary: Too easy!  Study my technique, {player}!",
        "team": [("STARTER", 5)],
    },

    # 1 — Cerulean City (Nugget Bridge): after Cascade Badge
    {
        "intro": (
            "Gary: {player}!  What took you so long?\n"
            "I've had two badges longer than you've had one!"
        ),
        "win":  "Gary: Wh-what?!  You beat me again?!  I'll remember this!",
        "lose": "Gary: Haha, still too slow!  Better keep training!",
        "team": [("Pidgeotto", 18), ("Abra", 16), ("STARTER", 20)],
    },

    # 2 — S.S. Anne (Vermilion City): before Thunder Badge
    {
        "intro": (
            "Gary: Oh, {player}.  I'm cruising in style on this ship.\n"
            "If you want to battle so badly, let's go!"
        ),
        "win":  "Gary: Ugh!  You cheated somehow.  I know it.",
        "lose": "Gary: HAHAHA!  The difference in our skills is obvious!",
        "team": [
            ("Pidgeotto", 22), ("Rattata", 19), ("Clefairy", 20),
            ("Growlithe", 22), ("STARTER", 25),
        ],
    },

    # 3 — Silph Co. (Saffron City): Team Rocket showdown
    {
        "intro": (
            "Gary: {player}!  Don't think I'm doing this to save you.\n"
            "I just wanted a strong Pokémon battle!"
        ),
        "win":  "Gary: ...Okay, fine.  You're decent.  Don't get cocky.",
        "lose": "Gary: Your Pokémon and techniques are amateurish!",
        "team": [
            ("Pidgeot", 40), ("Jolteon", 38), ("Alakazam", 38),
            ("Rhydon", 38), ("STARTER", 43),
        ],
    },

    # 4 — Victory Road (before the Pokémon League)
    {
        "intro": (
            "Gary: {player}!  I knew I'd find you here.\n"
            "I've been waiting for this final showdown before the League!"
        ),
        "win":  "Gary: No way…  I'm stronger — I should have won!",
        "lose": "Gary: Heh.  The Pokémon League will show you the gap between us.",
        "team": [
            ("Pidgeot", 53), ("Alakazam", 55), ("Rhydon", 53),
            ("Arcanine", 54), ("Exeggutor", 53), ("STARTER", 58),
        ],
    },

    # 5 — Indigo Plateau (as Pokémon League Champion)
    {
        "intro": (
            "Gary: So you made it.  I've been waiting, {player}.\n"
            "I became Champion while you were still fumbling around!\n"
            "Your Pokémon better be ready — this is the real thing!"
        ),
        "win": (
            "Gary: …I lost.  To you.\n"
            "You're better than I thought.  No — you're… good.\n"
            "Congratulations, {player}.  You're the new Champion."
        ),
        "lose": "Gary: As expected.  I am the Champion, after all.",
        "team": [
            ("Pidgeot", 63), ("Alakazam", 65), ("Rhydon", 65),
            ("Arcanine", 65), ("Exeggutor", 65), ("STARTER", 68),
        ],
    },
]


def build_rival(encounter_index: int, player_starter_name: str | None = None) -> "Trainer":
    """
    Build the rival trainer for the given encounter index (0-5).
    ``player_starter_name`` is used to pick the counter-starter for the rival.
    """
    from ..core.pokemon import create_pokemon
    from ..core.trainer import Trainer

    if encounter_index < 0 or encounter_index >= len(_RIVAL_PARTIES):
        raise IndexError(f"No rival encounter #{encounter_index}")

    enc = _RIVAL_PARTIES[encounter_index]

    # Resolve rival's starter
    if player_starter_name and player_starter_name in _COUNTER_STARTER:
        rival_starter = _COUNTER_STARTER[player_starter_name]
    else:
        rival_starter = "Charmander"

    party = []
    for species, lvl in enc["team"]:
        if species == "STARTER":
            species = rival_starter
        try:
            mon = create_pokemon(species, lvl, trainer_name=RIVAL_NAME)
        except ValueError:
            mon = create_pokemon("Eevee", lvl, trainer_name=RIVAL_NAME)
        party.append(mon)

    rival = Trainer(
        name=RIVAL_NAME,
        trainer_class="Champion" if encounter_index == 5 else "Rival",
        party=party,
        money=max(2000, 1500 * (encounter_index + 1)),
    )
    rival.dialogue_intro = enc["intro"]
    rival.dialogue_win  = enc["win"]
    rival.dialogue_lose = enc["lose"]
    return rival
