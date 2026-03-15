"""
Trainer class: player and NPC trainers, Gym Leaders, Elite Four, etc.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from .bag import Bag
from .pokedex import Pokedex

if TYPE_CHECKING:
    from .pokemon import Pokemon


@dataclass
class TrainerClass:
    name: str           # e.g. "Gym Leader", "Elite Four", "Champion", "Bug Catcher"
    title_prefix: str   # e.g. "Leader"
    reward_multiplier: float = 1.0


TRAINER_CLASSES = {
    "Player":        TrainerClass("Player", "", 0.0),
    "Youngster":     TrainerClass("Youngster", "Youngster", 1.0),
    "Lass":          TrainerClass("Lass", "Lass", 1.0),
    "Bug Catcher":   TrainerClass("Bug Catcher", "Bug Catcher", 1.0),
    "Camper":        TrainerClass("Camper", "Camper", 1.0),
    "Picnicker":     TrainerClass("Picnicker", "Picnicker", 1.0),
    "Hiker":         TrainerClass("Hiker", "Hiker", 1.2),
    "Jr. Trainer":   TrainerClass("Jr. Trainer", "Jr. Trainer", 1.2),
    "Scientist":     TrainerClass("Scientist", "Scientist", 1.5),
    "Rocket Grunt":  TrainerClass("Team Rocket Grunt", "Grunt", 1.5),
    "Gym Leader":    TrainerClass("Gym Leader", "Leader", 3.0),
    "Elite Four":    TrainerClass("Elite Four", "Elite Four", 4.0),
    "Champion":      TrainerClass("Champion", "Champion", 5.0),
    "Rival":         TrainerClass("Rival", "", 2.0),
}


class Trainer:
    """
    Represents a Pokémon trainer (player or NPC).
    """

    def __init__(
        self,
        name: str,
        trainer_class: str = "Player",
        party: Optional[list["Pokemon"]] = None,
        money: int = 0,
        badges: Optional[list[str]] = None,
        is_player: bool = False,
    ):
        self.name = name
        self.trainer_class_name = trainer_class
        self.trainer_class = TRAINER_CLASSES.get(trainer_class, TRAINER_CLASSES["Youngster"])
        self.party: list["Pokemon"] = party or []
        self.money = money
        self.badges: list[str] = badges or []
        self.is_player = is_player
        self.bag = Bag()
        self.pokedex = Pokedex() if is_player else None
        self.defeated = False  # has this trainer been defeated?
        self.dialogue_intro = ""
        self.dialogue_win = ""
        self.dialogue_lose = ""

    # ── Party management ──────────────────────────────────────────────────────

    def add_pokemon(self, pokemon: "Pokemon") -> bool:
        """Add a Pokémon to the party (max 6). Returns True if added."""
        if len(self.party) >= 6:
            return False
        pokemon.trainer_name = self.name
        self.party.append(pokemon)
        if self.is_player and self.pokedex:
            self.pokedex.register_caught(pokemon)
        return True

    def remove_pokemon(self, idx: int) -> Optional["Pokemon"]:
        if 0 <= idx < len(self.party):
            return self.party.pop(idx)
        return None

    def has_usable_pokemon(self) -> bool:
        return any(not m.fainted for m in self.party)

    def first_usable_idx(self) -> int:
        for i, m in enumerate(self.party):
            if not m.fainted:
                return i
        return -1

    def heal_party(self) -> None:
        """Fully restore all party Pokémon."""
        for mon in self.party:
            mon.full_heal()
            for move in mon.moves:
                move.restore_pp()

    # ── Rewards ───────────────────────────────────────────────────────────────

    def calculate_prize(self) -> int:
        """Prize money the player wins from defeating this trainer."""
        if not self.party:
            return 0
        highest_level = max(m.level for m in self.party)
        mult = self.trainer_class.reward_multiplier
        return int(highest_level * 100 * mult)

    # ── Gym badge ─────────────────────────────────────────────────────────────

    def award_badge(self, badge_name: str) -> None:
        if badge_name not in self.badges:
            self.badges.append(badge_name)

    def has_badge(self, badge_name: str) -> bool:
        return badge_name in self.badges

    # ── Display ───────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        tc = self.trainer_class.title_prefix
        prefix = f"{tc} " if tc else ""
        return f"{prefix}{self.name}"

    def party_status(self) -> str:
        lines = [f"=== {self!r}'s Party ==="]
        for i, mon in enumerate(self.party):
            faint_marker = "✗" if mon.fainted else "♥"
            lines.append(f"  [{faint_marker}] {i+1}. {mon}")
        return "\n".join(lines)


# ── Gym Leaders ───────────────────────────────────────────────────────────────

@dataclass
class GymData:
    number: int
    city: str
    leader_name: str
    badge_name: str
    specialty_type: str
    required_badges: int    # badges needed to challenge
    description: str = ""


GYMS: list[GymData] = [
    GymData(1, "Pewter City",      "Brock",    "Boulder Badge", "ROCK",     0,
            "The Rock-hard Pokémon Trainer!"),
    GymData(2, "Cerulean City",    "Misty",    "Cascade Badge", "WATER",    1,
            "The Tomboyish Mermaid!"),
    GymData(3, "Vermilion City",   "Lt. Surge","Thunder Badge", "ELECTRIC", 2,
            "The Lightning American!"),
    GymData(4, "Celadon City",     "Erika",    "Rainbow Badge", "GRASS",    3,
            "The Nature-Loving Princess!"),
    GymData(5, "Fuchsia City",     "Koga",     "Soul Badge",    "POISON",   4,
            "The Poisonous Ninja Master!"),
    GymData(6, "Saffron City",     "Sabrina",  "Marsh Badge",   "PSYCHIC",  5,
            "The Master of Psychic Pokémon!"),
    GymData(7, "Cinnabar Island",  "Blaine",   "Volcano Badge", "FIRE",     6,
            "The Hotheaded Quiz Master!"),
    GymData(8, "Viridian City",    "Giovanni", "Earth Badge",   "GROUND",   7,
            "The Last Badge is Mine to Give or Withhold!"),
]


def build_gym_leader(gym: GymData) -> Trainer:
    """Build a Gym Leader trainer with a pre-defined party."""
    from ..core.pokemon import create_pokemon

    party_data: dict[str, list[tuple[str, int]]] = {
        "Brock": [
            ("Geodude", 12), ("Onix", 14),
        ],
        "Misty": [
            ("Staryu", 18), ("Starmie", 21),
        ],
        "Lt. Surge": [
            ("Voltorb", 21), ("Pikachu", 18), ("Raichu", 24),
        ],
        "Erika": [
            ("Victreebel", 29), ("Tangela", 24), ("Vileplume", 29),
        ],
        "Koga": [
            ("Koffing", 37), ("Muk", 39), ("Koffing", 37), ("Weezing", 43),
        ],
        "Sabrina": [
            ("Kadabra", 38), ("Mr. Mime", 37), ("Venomoth", 38), ("Alakazam", 43),
        ],
        "Blaine": [
            ("Growlithe", 42), ("Ponyta", 40), ("Rapidash", 42), ("Arcanine", 47),
        ],
        "Giovanni": [
            ("Rhyhorn", 45), ("Dugtrio", 42), ("Nidoqueen", 44), ("Nidoking", 45), ("Rhydon", 50),
        ],
    }

    leader_data = party_data.get(gym.leader_name, [])
    party = [create_pokemon(name, lvl, trainer_name=gym.leader_name)
             for name, lvl in leader_data]
    trainer = Trainer(
        name=gym.leader_name,
        trainer_class="Gym Leader",
        party=party,
        money=gym.number * 1500,
    )
    trainer.dialogue_intro = gym.description
    trainer.dialogue_win = f"... I can't believe it. You beat me. Fine — take the {gym.badge_name}."
    trainer.dialogue_lose = "Hmph. You lost! Train more!"
    return trainer


# ── Elite Four ────────────────────────────────────────────────────────────────

ELITE_FOUR = [
    {"name": "Lorelei",  "specialty": "ICE",      "class": "Elite Four"},
    {"name": "Bruno",    "specialty": "FIGHTING",  "class": "Elite Four"},
    {"name": "Agatha",   "specialty": "GHOST",     "class": "Elite Four"},
    {"name": "Lance",    "specialty": "DRAGON",    "class": "Elite Four"},
    {"name": "Blue",     "specialty": "MIXED",     "class": "Champion"},
]


def build_elite_four_member(member: dict) -> Trainer:
    """Build an Elite Four / Champion trainer."""
    from ..core.pokemon import create_pokemon

    party_data = {
        "Lorelei": [
            ("Dewgong", 54), ("Cloyster", 55), ("Slowbro", 56),
            ("Jynx", 56), ("Lapras", 60),
        ],
        "Bruno": [
            ("Onix", 53), ("Hitmonchan", 55), ("Hitmonlee", 55),
            ("Onix", 56), ("Machamp", 62),
        ],
        "Agatha": [
            ("Gengar", 56), ("Haunter", 55), ("Gengar", 59),
            ("Arbok", 58), ("Gengar", 65),
        ],
        "Lance": [
            ("Gyarados", 58), ("Dragonair", 56), ("Dragonair", 56),
            ("Aerodactyl", 60), ("Dragonite", 68),
        ],
        "Blue": [
            ("Pidgeot", 63), ("Alakazam", 65), ("Rhydon", 65),
            ("Arcanine", 65), ("Exeggutor", 65), ("Blastoise", 68),
        ],
    }
    name = member["name"]
    party = [create_pokemon(sname, lvl, trainer_name=name)
             for sname, lvl in party_data.get(name, [])]
    return Trainer(
        name=name,
        trainer_class=member["class"],
        party=party,
        money=10000,
    )
