"""
Trainer class: player and NPC trainers, Gym Leaders, Elite Four, etc.
"""

from __future__ import annotations
from dataclasses import dataclass, field, field
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
    puzzle_description: str = ""  # flavour text for the gym layout/puzzle
    tip: str = ""                 # type hint shown before the battle
    tm_reward: int = 0            # TM number awarded on victory (0 = none)
    # NPC trainers inside the gym: list of (species, level) tuples per trainer
    gym_trainer_parties: list[list[tuple[str, int]]] = field(default_factory=list)


GYMS: list[GymData] = [
    GymData(
        1, "Pewter City", "Brock", "Boulder Badge", "ROCK", 0,
        description="The Rock-hard Pokémon Trainer!",
        puzzle_description=(
            "The gym floor is strewn with large boulders.  Two trainers\n"
            "block the path to Brock's podium."
        ),
        tip="Rock types are weak to Water and Grass moves!",
        tm_reward=80,   # TM80 Rock Slide
        gym_trainer_parties=[
            [("Geodude", 10)],
            [("Geodude", 11), ("Onix", 11)],
        ],
    ),
    GymData(
        2, "Cerulean City", "Misty", "Cascade Badge", "WATER", 1,
        description="The Tomboyish Mermaid!",
        puzzle_description=(
            "The gym is filled with shallow pools.  A single trainer\n"
            "patrols the bridge over the main pool."
        ),
        tip="Water types are weak to Electric and Grass moves!",
        tm_reward=18,   # TM18 Rain Dance
        gym_trainer_parties=[
            [("Goldeen", 17)],
        ],
    ),
    GymData(
        3, "Vermilion City", "Lt. Surge", "Thunder Badge", "ELECTRIC", 2,
        description="The Lightning American!",
        puzzle_description=(
            "The gym floor is lined with electric fences.\n"
            "Two Junior Trainers guard the entrance."
        ),
        tip="Electric types are weak to Ground moves!",
        tm_reward=24,   # TM24 Thunderbolt
        gym_trainer_parties=[
            [("Voltorb", 21), ("Magnemite", 20)],
            [("Pikachu", 21)],
        ],
    ),
    GymData(
        4, "Celadon City", "Erika", "Rainbow Badge", "GRASS", 3,
        description="The Nature-Loving Princess!",
        puzzle_description=(
            "The gym is a lush botanical garden.  Three junior trainers\n"
            "hide among the tall flower arrangements."
        ),
        tip="Grass types are weak to Fire, Ice, Flying, Poison, and Bug moves!",
        tm_reward=22,   # TM22 Solar Beam
        gym_trainer_parties=[
            [("Oddish", 26), ("Bellsprout", 27)],
            [("Tangela", 27)],
            [("Gloom", 28)],
        ],
    ),
    GymData(
        5, "Fuchsia City", "Koga", "Soul Badge", "POISON", 4,
        description="The Poisonous Ninja Master!",
        puzzle_description=(
            "Invisible walls create a maze through the gym.\n"
            "Two jugglers perform in the open areas."
        ),
        tip="Poison types are weak to Ground and Psychic moves!",
        tm_reward=6,    # TM06 Toxic
        gym_trainer_parties=[
            [("Koffing", 38), ("Drowzee", 36)],
            [("Arbok", 38)],
        ],
    ),
    GymData(
        6, "Saffron City", "Sabrina", "Marsh Badge", "PSYCHIC", 5,
        description="The Master of Psychic Pokémon!",
        puzzle_description=(
            "Teleportation tiles scatter trainers across\n"
            "a grid of warping platforms."
        ),
        tip="Psychic types are weak to Bug, Ghost, and Dark moves!",
        tm_reward=29,   # TM29 Psychic
        gym_trainer_parties=[
            [("Kadabra", 36), ("Hypno", 37)],
            [("Mr. Mime", 37)],
        ],
    ),
    GymData(
        7, "Cinnabar Island", "Blaine", "Volcano Badge", "FIRE", 6,
        description="The Hotheaded Quiz Master!",
        puzzle_description=(
            "A quiz machine blocks each door: answer correctly\n"
            "or face a trainer battle!  Fire surrounds the arena."
        ),
        tip="Fire types are weak to Water, Ground, and Rock moves!",
        tm_reward=38,   # TM38 Fire Blast
        gym_trainer_parties=[
            [("Growlithe", 41), ("Ponyta", 41)],
            [("Arcanine", 44)],
        ],
    ),
    GymData(
        8, "Viridian City", "Giovanni", "Earth Badge", "GROUND", 7,
        description="The Last Badge is Mine to Give or Withhold!",
        puzzle_description=(
            "A large arena with spinning tile traps.\n"
            "Three of Giovanni's elite grunts stand guard."
        ),
        tip="Ground types are weak to Water, Grass, and Ice moves!",
        tm_reward=26,   # TM26 Earthquake
        gym_trainer_parties=[
            [("Tauros", 42), ("Rhyhorn", 42)],
            [("Dugtrio", 44)],
            [("Nidoking", 44), ("Nidoqueen", 44)],
        ],
    ),
]


_LEADER_DIALOGUES: dict[str, dict[str, str]] = {
    "Brock": {
        "intro": (
            "Brock: I can see why you made it here.\n"
            "My rock-hard Pokémon have never lost in this gym!\n"
            "As a Rock-type Gym Leader, I don't yield easily!"
        ),
        "win":  "I can't believe I lost!  Here — take the Boulder Badge!",
        "lose": "Hmmph.  Just as I expected.  Come back when you've trained more.",
    },
    "Misty": {
        "intro": (
            "Misty: Hmph!  You don't look like much to me.\n"
            "Do you know what I love most?  Strong Pokémon!\n"
            "My Water-types are as tough as a crashing wave!"
        ),
        "win":  "You were a splashing success!  Accept the Cascade Badge!",
        "lose": "Too bad!  My Water Pokémon won't show any mercy!",
    },
    "Lt. Surge": {
        "intro": (
            "Lt. Surge: Hey kid!  Electric Pokémon saved my life once.\n"
            "I won't allow anyone to show disrespect to Electric types!\n"
            "I'll zap you into paralysis!"
        ),
        "win":  "Whoa!  Your Pokémon are shockingly strong!  Here's the Thunder Badge!",
        "lose": "HAHAHAHA!  You can't handle the voltage, kid!",
    },
    "Erika": {
        "intro": (
            "Erika: Oh my…  I was napping.  Who are you?\n"
            "Hmm, a challenger?  Very well.\n"
            "My Grass-type Pokémon have been infused with\n"
            "the power of the earth.  This won't be easy for you."
        ),
        "win":  "Oh my!  You are quite skilled.  Please accept the Rainbow Badge.",
        "lose": "You did not have the constitution for this battle…",
    },
    "Koga": {
        "intro": (
            "Koga: Fwa ha ha!  Welcome to your doom!\n"
            "I am Koga, master of poisons and ninja arts.\n"
            "I'll have you know — before you lose — that\n"
            "Pokémon battles are a test of the mind, not the body!"
        ),
        "win":  "You are a superior Trainer!  I present the Soul Badge.",
        "lose": "Hm, your spirit is weak.  Begone!",
    },
    "Sabrina": {
        "intro": (
            "Sabrina: I foresaw your arrival.\n"
            "And… I foresaw your defeat.\n"
            "My Psychic-type Pokémon will crush your will."
        ),
        "win":  "I… lost.  I foresaw it, yet I couldn't prevent it.  The Marsh Badge is yours.",
        "lose": "As I predicted.  Your mind was an open book.",
    },
    "Blaine": {
        "intro": (
            "Blaine: Welcome, challenger, to my burning quiz!\n"
            "If you can answer this: what type is weak to Fire?\n"
            "Ha!  Trick question — you'll find out firsthand!\n"
            "My Pokémon are hotter than a volcano's core!"
        ),
        "win":  "Your Pokémon blazed straight through my team!  The Volcano Badge is yours!",
        "lose": "My flames of passion still burn, and yours have been extinguished!",
    },
    "Giovanni": {
        "intro": (
            "Giovanni: Hmph.  You have some skill to have come this far.\n"
            "I am Giovanni — Gym Leader of Viridian City, and the\n"
            "Boss of Team Rocket.  Your meddling ends here!\n"
            "My Ground-type Pokémon have crushed everyone who stood before me!"
        ),
        "win": (
            "Giovanni: …I see.  You've bested me — and Team Rocket.\n"
            "This outcome was… unexpected.  Take the Earth Badge.\n"
            "I need time to reflect on my actions."
        ),
        "lose": "As I expected.  No one defeats Team Rocket's Boss!",
    },
}


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
    dialogues = _LEADER_DIALOGUES.get(gym.leader_name, {})

    party = [create_pokemon(name, lvl, trainer_name=gym.leader_name)
             for name, lvl in leader_data]
    trainer = Trainer(
        name=gym.leader_name,
        trainer_class="Gym Leader",
        party=party,
        money=gym.number * 1500,
    )
    trainer.dialogue_intro = dialogues.get("intro", gym.description)
    trainer.dialogue_win   = dialogues.get("win",  f"... I can't believe it. You beat me. Fine — take the {gym.badge_name}.")
    trainer.dialogue_lose  = dialogues.get("lose", "Hmph. You lost! Train more!")
    return trainer


def build_gym_trainers(gym: GymData) -> list[Trainer]:
    """Build the NPC trainers inside the gym (fought before the leader)."""
    from ..core.pokemon import create_pokemon

    trainers = []
    for i, party_spec in enumerate(gym.gym_trainer_parties):
        party = [create_pokemon(name, lvl, trainer_name=f"Gym Trainer")
                 for name, lvl in party_spec]
        t = Trainer(
            name=f"{gym.leader_name}'s Trainer {i + 1}",
            trainer_class="Jr. Trainer",
            party=party,
            money=max(lvl for _, lvl in party_spec) * 80,
        )
        t.dialogue_intro = f"You shall not pass to {gym.leader_name}!"
        t.dialogue_win   = "I lost?! No way!"
        t.dialogue_lose  = "Hah! That was nothing!"
        trainers.append(t)
    return trainers


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
