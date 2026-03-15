"""
pykemon/story/events.py

Story flags and a GameState that tracks the player's progress through the
Kanto adventure.  All flags are plain strings so they can easily be serialised.
"""

from __future__ import annotations
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
    POKEMON_TOWER_GHOST      = "POKEMON_TOWER_GHOST"    # ghost Marowak defeated
    GAME_CORNER_CLEARED      = "GAME_CORNER_CLEARED"    # Rocket at Game Corner gone
    SILPH_CO_CLEARED         = "SILPH_CO_CLEARED"       # Rocket HQ cleared
    SEAFOAM_VISITED          = "SEAFOAM_VISITED"        # Articuno optional fight
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
