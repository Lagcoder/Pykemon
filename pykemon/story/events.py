"""
pykemon/story/events.py

Story flags and a GameState that tracks the player's progress through the
Kanto adventure.  All flags are plain strings so they can easily be serialised.
"""

from __future__ import annotations
import json
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.trainer import Trainer
    from ..core.pokemon import Pokemon


# ── Story flags ───────────────────────────────────────────────────────────────

class StoryFlag:
    """String constants for every named story checkpoint."""
    # Opening
    RECEIVED_STARTER         = "RECEIVED_STARTER"
    BEAT_RIVAL_PALLET        = "BEAT_RIVAL_PALLET"    # Gary, Pallet Town
    OAK_PARCEL_DELIVERED     = "OAK_PARCEL_DELIVERED"

    # Gym badges (mirrored from badge names for convenience)
    BEAT_BROCK               = "BEAT_BROCK"
    BEAT_MISTY               = "BEAT_MISTY"
    BEAT_SURGE               = "BEAT_SURGE"
    BEAT_ERIKA               = "BEAT_ERIKA"
    BEAT_KOGA                = "BEAT_KOGA"
    BEAT_SABRINA             = "BEAT_SABRINA"
    BEAT_BLAINE              = "BEAT_BLAINE"
    BEAT_GIOVANNI            = "BEAT_GIOVANNI"

    # Rival battles
    BEAT_RIVAL_CERULEAN      = "BEAT_RIVAL_CERULEAN"    # Gary, Cerulean bridge
    BEAT_RIVAL_SS_ANNE       = "BEAT_RIVAL_SS_ANNE"     # Gary, S.S. Anne
    BEAT_RIVAL_SILPH         = "BEAT_RIVAL_SILPH"       # Gary, Silph Co.
    BEAT_RIVAL_VICTORY_ROAD  = "BEAT_RIVAL_VICTORY_ROAD"
    BEAT_CHAMPION            = "BEAT_CHAMPION"

    # Key story beats
    MT_MOON_ROCKET_DEFEATED  = "MT_MOON_ROCKET_DEFEATED"
    FOSSIL_CHOSEN            = "FOSSIL_CHOSEN"          # chosen fossil in Mt. Moon
    SS_ANNE_VISITED          = "SS_ANNE_VISITED"        # got HM01 Cut
    BILL_RESCUED             = "BILL_RESCUED"           # Bill on Route 25, got S.S. Ticket
    POKEMON_TOWER_GHOST      = "POKEMON_TOWER_GHOST"    # ghost Marowak defeated
    GAME_CORNER_CLEARED      = "GAME_CORNER_CLEARED"    # Rocket at Game Corner gone
    SILPH_CO_CLEARED         = "SILPH_CO_CLEARED"       # Rocket HQ cleared
    SEAFOAM_VISITED          = "SEAFOAM_VISITED"        # Articuno optional fight
    MOLTRES_ENCOUNTERED      = "MOLTRES_ENCOUNTERED"    # Moltres at Victory Road
    HALL_OF_FAME             = "HALL_OF_FAME"           # game complete

    # Optional areas
    POWER_PLANT_VISITED      = "POWER_PLANT_VISITED"    # Zapdos encounter
    MANSION_VISITED          = "MANSION_VISITED"        # Pokémon Mansion lore
    CERULEAN_CAVE_VISITED    = "CERULEAN_CAVE_VISITED"  # post-game Mewtwo


BADGE_TO_FLAG: dict[str, str] = {
    "Boulder Badge": StoryFlag.BEAT_BROCK,
    "Cascade Badge": StoryFlag.BEAT_MISTY,
    "Thunder Badge": StoryFlag.BEAT_SURGE,
    "Rainbow Badge": StoryFlag.BEAT_ERIKA,
    "Soul Badge":    StoryFlag.BEAT_KOGA,
    "Marsh Badge":   StoryFlag.BEAT_SABRINA,
    "Volcano Badge": StoryFlag.BEAT_BLAINE,
    "Earth Badge":   StoryFlag.BEAT_GIOVANNI,
}


# ── GameState ─────────────────────────────────────────────────────────────────

class GameState:
    """
    Central store for all mutable game-wide state: player, story flags,
    current location, and a reference to the rival trainer.
    """

    def __init__(self, player: "Trainer", starting_location: str = "Pallet Town"):
        self.player = player
        self.current_location: str = starting_location
        self.flags: set[str] = set()
        self.rival: "Trainer | None" = None          # rebuilt at each encounter
        self.seen_locations: list[str] = []          # ordered visit history
        # Name of the starter the player chose (e.g. "Bulbasaur").
        # Used to give the rival the starter that is weak against the player's.
        self.player_starter: str = ""

    # ── Flag helpers ─────────────────────────────────────────────────────────

    def set_flag(self, flag: str) -> None:
        self.flags.add(flag)

    def has_flag(self, flag: str) -> bool:
        return flag in self.flags

    def badge_count(self) -> int:
        return len(self.player.badges)

    def has_badge(self, badge_name: str) -> bool:
        return self.player.has_badge(badge_name)

    # ── Travel ───────────────────────────────────────────────────────────────

    def travel_to(self, location_name: str) -> None:
        if self.current_location != location_name:
            self.seen_locations.append(self.current_location)
        self.current_location = location_name

    # ── Persistence summary (human-readable) ─────────────────────────────────

    def status_line(self) -> str:
        name = self.player.name
        money = self.player.money
        badges = self.badge_count()
        return f"  {name}  ₽{money:,}  Badges: {badges}/8  | {self.current_location}"

    # ── Save / Load ───────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Serialise game state to a JSON-compatible dict."""
        from ..core.pokemon import Pokemon
        player = self.player

        def _move_dict(m) -> dict:
            return {"name": m.data.name, "pp": m.pp}

        def _mon_dict(mon: "Pokemon") -> dict:
            return {
                "species":      mon.species.name,
                "nickname":     mon.nickname,
                "level":        mon.level,
                "experience":   mon.experience,
                "is_shiny":     mon.is_shiny,
                "gender":       mon.gender,
                "friendship":   mon.friendship,
                "current_hp":   mon.current_hp,
                "moves":        [_move_dict(m) for m in mon.moves],
                "held_item":    mon.held_item,
                "trainer_name": mon.original_trainer,
                "ivs":          mon.ivs,
                "evs":          mon.evs,
            }

        return {
            "version": 1,
            "player_name":      player.name,
            "money":            player.money,
            "badges":           player.badges,
            "bag":              player.bag.all_items(),
            "party":            [_mon_dict(m) for m in player.party],
            "pc_box":           [[_mon_dict(m) for m in box]
                                 for box in (player.bag._pc_boxes
                                             if hasattr(player.bag, "_pc_boxes") else [])],
            "current_location": self.current_location,
            "flags":            sorted(self.flags),
            "seen_locations":   self.seen_locations,
            "player_starter":   self.player_starter,
            "pokedex_seen":     sorted(player.pokedex._seen)   if player.pokedex else [],
            "pokedex_caught":   sorted(player.pokedex._caught) if player.pokedex else [],
        }

    def save(self, filepath: str = "pykemon_save.json") -> None:
        """Save game state to a JSON file."""
        data = self.to_dict()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, filepath: str = "pykemon_save.json") -> "GameState":
        """Load a previously saved game state from a JSON file."""
        from ..core.trainer import Trainer
        from ..core.pokemon import create_pokemon
        from ..data.moves import MOVES

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Save file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        player = Trainer(
            name=data["player_name"],
            money=data["money"],
            badges=data.get("badges", []),
            is_player=True,
        )
        # Restore bag
        for item_name, qty in data.get("bag", {}).items():
            player.bag.add_item(item_name, qty)
        # Restore party
        for md in data.get("party", []):
            mon = create_pokemon(md["species"], md["level"], trainer_name=md["trainer_name"])
            mon.nickname   = md.get("nickname", mon.nickname)
            mon.experience = md.get("experience", mon.experience)
            mon.is_shiny   = md.get("is_shiny", False)
            mon.gender     = md.get("gender", mon.gender)
            mon.friendship = md.get("friendship", mon.friendship)
            mon.current_hp = md.get("current_hp", mon.max_hp)
            mon.ivs        = md.get("ivs", mon.ivs)
            mon.evs        = md.get("evs", mon.evs)
            if md.get("held_item"):
                mon.held_item = md["held_item"]
            # Restore moves with saved PP
            saved_moves = {m["name"]: m["pp"] for m in md.get("moves", [])}
            for mv in mon.moves:
                if mv.data.name in saved_moves:
                    mv.pp = saved_moves[mv.data.name]
            player.party.append(mon)
        # Restore Pokédex (stores Pokémon numbers as ints)
        if player.pokedex:
            player.pokedex._seen   = set(data.get("pokedex_seen",   []))
            player.pokedex._caught = set(data.get("pokedex_caught", []))

        gs = cls(player, starting_location=data.get("current_location", "Pallet Town"))
        gs.flags          = set(data.get("flags", []))
        gs.seen_locations = data.get("seen_locations", [])
        gs.player_starter = data.get("player_starter", "")
        return gs
