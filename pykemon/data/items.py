"""
Item definitions for Pykemon: Poké Balls, Bag Items, TMs, HMs, Held Items, Fossils.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ItemCategory(Enum):
    POKEBALL = "Poké Ball"
    MEDICINE = "Medicine"
    BATTLE_ITEM = "Battle Item"
    TM = "TM"
    HM = "HM"
    HELD = "Held Item"
    FOSSIL = "Fossil"
    KEY = "Key Item"
    BERRY = "Berry"
    OTHER = "Other"


@dataclass
class ItemData:
    name: str
    category: ItemCategory
    price: int                       # 0 = not for sale
    description: str = ""
    # Ball-specific
    catch_rate_modifier: float = 1.0
    # Medicine-specific
    hp_restore: int = 0              # HP restored; -1 = full heal
    cures_status: list[str] = field(default_factory=list)  # list of StatusEffect names
    revives: bool = False
    # Held item effects (passive)
    held_boost_type: Optional[str] = None
    held_boost_factor: float = 1.0
    held_burn_on_hit: bool = False
    held_paralysis_on_hit: bool = False
    held_poison_on_hit: bool = False
    held_hp_restore_fraction: float = 0.0   # fraction of max HP restored each turn
    held_speed_boost: bool = False
    held_choice_locked: Optional[str] = None  # "atk", "spa", "spe"
    held_leftovers: bool = False
    held_scope_lens: bool = False    # Boosts crit ratio
    held_choice_band: bool = False
    held_choice_specs: bool = False
    held_choice_scarf: bool = False
    # Fossil revival
    revives_to: Optional[str] = None   # Pokémon name this fossil revives to


ITEMS: dict[str, ItemData] = {}


def _item(item: ItemData) -> ItemData:
    ITEMS[item.name] = item
    return item


# ── Poké Balls ───────────────────────────────────────────────────────────────
_item(ItemData("Poké Ball", ItemCategory.POKEBALL, 200,
               catch_rate_modifier=1.0,
               description="A device for catching wild Pokémon. It is thrown like a ball."))
_item(ItemData("Great Ball", ItemCategory.POKEBALL, 600,
               catch_rate_modifier=1.5,
               description="A good, high-performance Poké Ball that provides a higher catch rate than a standard Poké Ball."))
_item(ItemData("Ultra Ball", ItemCategory.POKEBALL, 1200,
               catch_rate_modifier=2.0,
               description="An ultra-high-performance Poké Ball that provides a higher success rate for catching Pokémon than the Great Ball."))
_item(ItemData("Master Ball", ItemCategory.POKEBALL, 0,
               catch_rate_modifier=255.0,
               description="The best Poké Ball with the ultimate level of performance. It will catch any wild Pokémon without fail."))
_item(ItemData("Safari Ball", ItemCategory.POKEBALL, 0,
               catch_rate_modifier=1.5,
               description="A special Poké Ball that is used only in the Safari Zone. It is decorated in a camouflage pattern."))
_item(ItemData("Net Ball", ItemCategory.POKEBALL, 1000,
               catch_rate_modifier=3.5,
               description="A somewhat different Poké Ball that is more effective when attempting to catch Water- and Bug-type Pokémon."))
_item(ItemData("Dive Ball", ItemCategory.POKEBALL, 1000,
               catch_rate_modifier=3.5,
               description="A somewhat different Poké Ball that works especially well on Pokémon that live underwater."))
_item(ItemData("Dusk Ball", ItemCategory.POKEBALL, 1000,
               catch_rate_modifier=3.5,
               description="A somewhat different Poké Ball that makes it easier to catch wild Pokémon at night or in dark places."))
_item(ItemData("Heal Ball", ItemCategory.POKEBALL, 300,
               catch_rate_modifier=1.0,
               description="A remedial Poké Ball that restores the caught Pokémon's HP and eliminates any status conditions."))
_item(ItemData("Quick Ball", ItemCategory.POKEBALL, 1000,
               catch_rate_modifier=5.0,
               description="A somewhat different Poké Ball that has a more successful catch rate if used at the start of a wild encounter."))
_item(ItemData("Timer Ball", ItemCategory.POKEBALL, 1000,
               catch_rate_modifier=1.0,
               description="A Poké Ball that becomes progressively better the more turns that are taken in battle."))
_item(ItemData("Repeat Ball", ItemCategory.POKEBALL, 1000,
               catch_rate_modifier=3.0,
               description="A Poké Ball that works especially well on Pokémon species that were previously caught."))
_item(ItemData("Luxury Ball", ItemCategory.POKEBALL, 1000,
               catch_rate_modifier=1.0,
               description="A comfortable Poké Ball that makes a caught wild Pokémon quickly grow friendlier."))

# ── Medicine ─────────────────────────────────────────────────────────────────
_item(ItemData("Potion", ItemCategory.MEDICINE, 300, hp_restore=20,
               description="A spray-type medicine for treating wounds. It restores the HP of one Pokémon by 20 points."))
_item(ItemData("Super Potion", ItemCategory.MEDICINE, 700, hp_restore=60,
               description="A spray-type medicine for treating wounds. It restores the HP of one Pokémon by 60 points."))
_item(ItemData("Hyper Potion", ItemCategory.MEDICINE, 1200, hp_restore=120,
               description="A spray-type medicine for treating wounds. It restores the HP of one Pokémon by 120 points."))
_item(ItemData("Max Potion", ItemCategory.MEDICINE, 2500, hp_restore=-1,
               description="A spray-type medicine for treating wounds. It fully restores the HP of a single Pokémon."))
_item(ItemData("Full Restore", ItemCategory.MEDICINE, 3000, hp_restore=-1,
               cures_status=["BURN", "FREEZE", "PARALYSIS", "POISON", "BADLY_POISONED", "SLEEP", "CONFUSION"],
               description="A medicine that can be used to fully restore the HP of a single Pokémon and heal any status conditions."))
_item(ItemData("Revive", ItemCategory.MEDICINE, 1500, hp_restore=-2, revives=True,
               description="Revives a fainted Pokémon, restoring it to half of its max HP."))
_item(ItemData("Max Revive", ItemCategory.MEDICINE, 0, hp_restore=-1, revives=True,
               description="Revives a fainted Pokémon, fully restoring its HP."))
_item(ItemData("Antidote", ItemCategory.MEDICINE, 100, cures_status=["POISON", "BADLY_POISONED"],
               description="A spray-type medicine. It lifts the effect of poison from one Pokémon."))
_item(ItemData("Burn Heal", ItemCategory.MEDICINE, 250, cures_status=["BURN"],
               description="A spray-type medicine. It heals a single Pokémon that is suffering from a burn."))
_item(ItemData("Ice Heal", ItemCategory.MEDICINE, 250, cures_status=["FREEZE"],
               description="A spray-type medicine for use on a single Pokémon. It thaws a Pokémon that has been frozen solid."))
_item(ItemData("Awakening", ItemCategory.MEDICINE, 250, cures_status=["SLEEP"],
               description="A spray-type medicine. It awakens a Pokémon from the clutches of sleep."))
_item(ItemData("Paralyze Heal", ItemCategory.MEDICINE, 200, cures_status=["PARALYSIS"],
               description="A spray-type medicine. It eliminates paralysis from a single Pokémon."))
_item(ItemData("Full Heal", ItemCategory.MEDICINE, 600,
               cures_status=["BURN", "FREEZE", "PARALYSIS", "POISON", "BADLY_POISONED", "SLEEP", "CONFUSION"],
               description="A spray-type medicine that is very versatile. It can be used to heal all the status conditions of a single Pokémon."))
_item(ItemData("Ether", ItemCategory.MEDICINE, 0, hp_restore=0,
               description="It restores the PP of a Pokémon's move by 10 points."))
_item(ItemData("Max Ether", ItemCategory.MEDICINE, 0, hp_restore=0,
               description="It fully restores the PP of a single selected move that has been used by the target Pokémon."))
_item(ItemData("Elixir", ItemCategory.MEDICINE, 0, hp_restore=0,
               description="It restores the PP of all the moves learned by the target Pokémon by 10 points each."))
_item(ItemData("Max Elixir", ItemCategory.MEDICINE, 0, hp_restore=0,
               description="It fully restores the PP of all the moves of a Pokémon."))

# ── Battle Items ─────────────────────────────────────────────────────────────
_item(ItemData("X Attack", ItemCategory.BATTLE_ITEM, 500,
               description="An item that raises the Attack stat of a Pokémon during battle."))
_item(ItemData("X Defense", ItemCategory.BATTLE_ITEM, 550,
               description="An item that raises the Defense stat of a Pokémon during battle."))
_item(ItemData("X Sp. Atk", ItemCategory.BATTLE_ITEM, 350,
               description="An item that raises the Sp. Atk stat of a Pokémon during battle."))
_item(ItemData("X Sp. Def", ItemCategory.BATTLE_ITEM, 350,
               description="An item that raises the Sp. Def stat of a Pokémon during battle."))
_item(ItemData("X Speed", ItemCategory.BATTLE_ITEM, 350,
               description="An item that raises the Speed stat of a Pokémon during battle."))
_item(ItemData("X Accuracy", ItemCategory.BATTLE_ITEM, 950,
               description="An item that raises the accuracy of a Pokémon during battle."))
_item(ItemData("Dire Hit", ItemCategory.BATTLE_ITEM, 650,
               description="It raises the likelihood of a critical hit."))
_item(ItemData("Guard Spec.", ItemCategory.BATTLE_ITEM, 700,
               description="An item that prevents stat reduction among the Trainer's party Pokémon for five turns after its use in battle."))

# ── Held Items ───────────────────────────────────────────────────────────────
_item(ItemData("Leftovers", ItemCategory.HELD, 0,
               held_leftovers=True, held_hp_restore_fraction=0.0625,
               description="An item to be held by a Pokémon. The holder's HP is slowly but steadily restored throughout every battle."))
_item(ItemData("Choice Band", ItemCategory.HELD, 0,
               held_choice_band=True, held_choice_locked="atk",
               description="An item to be held by a Pokémon. This curious band boosts the holder's Attack stat but only allows one move to be used."))
_item(ItemData("Choice Specs", ItemCategory.HELD, 0,
               held_choice_specs=True, held_choice_locked="spa",
               description="An item to be held by a Pokémon. These curious specs boost Sp. Atk but only allow the use of one move."))
_item(ItemData("Choice Scarf", ItemCategory.HELD, 0,
               held_choice_scarf=True, held_choice_locked="spe",
               description="An item to be held by a Pokémon. This scarf boosts Speed but only allows the use of one move."))
_item(ItemData("Scope Lens", ItemCategory.HELD, 0,
               held_scope_lens=True,
               description="An item to be held by a Pokémon. It is a lens that boosts the holder's critical-hit ratio."))
_item(ItemData("Shell Bell", ItemCategory.HELD, 0,
               held_hp_restore_fraction=0.125,
               description="An item to be held by a Pokémon. The holder regains a little HP every time it inflicts damage on others."))
_item(ItemData("Charcoal", ItemCategory.HELD, 9800,
               held_boost_type="FIRE", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. It is a piece of charcoal that boosts the power of Fire-type moves."))
_item(ItemData("Mystic Water", ItemCategory.HELD, 9800,
               held_boost_type="WATER", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. It is a teardrop-shaped gem that boosts the power of Water-type moves."))
_item(ItemData("Miracle Seed", ItemCategory.HELD, 9800,
               held_boost_type="GRASS", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. It is a seed imbued with the power of nature that boosts Grass-type moves."))
_item(ItemData("Magnet", ItemCategory.HELD, 9800,
               held_boost_type="ELECTRIC", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. It is a powerful magnet that boosts the power of Electric-type moves."))
_item(ItemData("Never-Melt Ice", ItemCategory.HELD, 9800,
               held_boost_type="ICE", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. It is a piece of ice that does not melt that boosts Ice-type moves."))
_item(ItemData("Black Belt", ItemCategory.HELD, 9800,
               held_boost_type="FIGHTING", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. This belt helps the wearer to focus and boosts the power of Fighting-type moves."))
_item(ItemData("Poison Barb", ItemCategory.HELD, 9800,
               held_boost_type="POISON", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. It is a sharp barb that boosts the power of Poison-type moves."))
_item(ItemData("Soft Sand", ItemCategory.HELD, 9800,
               held_boost_type="GROUND", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. It is a loose, silky sand that boosts the power of Ground-type moves."))
_item(ItemData("Sharp Beak", ItemCategory.HELD, 9800,
               held_boost_type="FLYING", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. It is a long, sharp beak that boosts the power of Flying-type moves."))
_item(ItemData("Twisted Spoon", ItemCategory.HELD, 9800,
               held_boost_type="PSYCHIC", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. A spoon imbued with telekinetic power that boosts Psychic-type moves."))
_item(ItemData("Silver Powder", ItemCategory.HELD, 9800,
               held_boost_type="BUG", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. A shiny silver powder that boosts the power of Bug-type moves."))
_item(ItemData("Hard Stone", ItemCategory.HELD, 9800,
               held_boost_type="ROCK", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. A plain stone of some sort that boosts Rock-type moves."))
_item(ItemData("Spell Tag", ItemCategory.HELD, 9800,
               held_boost_type="GHOST", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. A sinister tag that boosts the power of Ghost-type moves."))
_item(ItemData("Dragon Fang", ItemCategory.HELD, 9800,
               held_boost_type="DRAGON", held_boost_factor=1.2,
               description="An item to be held by a Pokémon. A hard and sharp fang that boosts the power of Dragon-type moves."))
_item(ItemData("Flame Orb", ItemCategory.HELD, 0,
               description="An item to be held by a Pokémon. When held, it inflicts a burn on the holder during battle."))
_item(ItemData("Toxic Orb", ItemCategory.HELD, 0,
               description="An item to be held by a Pokémon. When held, it badly poisons the holder during battle."))
_item(ItemData("Life Orb", ItemCategory.HELD, 0,
               description="An item to be held by a Pokémon. It boosts the power of moves, but at the cost of some HP."))
_item(ItemData("Rocky Helmet", ItemCategory.HELD, 0,
               description="An item to be held by a Pokémon. If the holder is hit, the attacker will take damage."))
_item(ItemData("Eviolite", ItemCategory.HELD, 0,
               description="A mysterious evolutionary lump. When held by a Pokémon that can still evolve, it raises Defense and Sp. Def."))
_item(ItemData("Assault Vest", ItemCategory.HELD, 0,
               description="An item to be held by a Pokémon. This offensive vest raises Sp. Def but only allows the use of attack moves."))
_item(ItemData("Weakness Policy", ItemCategory.HELD, 0,
               description="An item to be held by a Pokémon. Attack and Sp. Atk sharply increase if the holder is hit with a move it's weak to."))
_item(ItemData("Sitrus Berry", ItemCategory.HELD, 0,
               held_hp_restore_fraction=0.25,
               description="A Berry to be held by a Pokémon. If the holder's HP drops to half or less, it restores the holder's HP by a quarter of its max HP."))
_item(ItemData("Oran Berry", ItemCategory.HELD, 100,
               held_hp_restore_fraction=0.0,
               description="A Berry to be held by a Pokémon. If the holder's HP drops to half or less, this Berry is consumed and restores 10 HP."))

# ── Evolution Stones & Special Items ─────────────────────────────────────────
for stone_name, stone_desc in [
    ("Fire Stone", "A peculiar stone that can make certain species of Pokémon evolve. It has a fiery orange heart."),
    ("Water Stone", "A peculiar stone that can make certain species of Pokémon evolve. It is a clear, light blue."),
    ("Thunder Stone", "A peculiar stone that can make certain species of Pokémon evolve. It has a sharp, spiky shape."),
    ("Leaf Stone", "A peculiar stone that can make certain species of Pokémon evolve. It has an appealing fresh scent."),
    ("Moon Stone", "A peculiar stone that can make certain species of Pokémon evolve. It is as black as the night sky."),
    ("Sun Stone", "A peculiar stone that can make certain species of Pokémon evolve. It has a brilliant, shining pattern."),
    ("Shiny Stone", "A peculiar stone that can make certain species of Pokémon evolve. It shines with a dazzling light."),
    ("Dusk Stone", "A peculiar stone that can make certain species of Pokémon evolve. It holds shadows as dark as can be."),
    ("Dawn Stone", "A peculiar stone that can make certain species of Pokémon evolve. It sparkles like a glittering eye."),
    ("Ice Stone", "A peculiar stone that can make certain species of Pokémon evolve. It has an unmistakably cold feel."),
]:
    _item(ItemData(stone_name, ItemCategory.OTHER, 2100, description=stone_desc))

for link_item, link_desc in [
    ("King's Rock", "An item to be held by a Pokémon. It may make the target flinch when the holder inflicts damage."),
    ("Metal Coat", "An item to be held by a Pokémon. It is a special metallic film that boosts the power of Steel-type moves."),
    ("Dragon Scale", "A very tough and inflexible scale. It evolves a certain Pokémon when held during a trade."),
    ("Upgrade", "A transparent device somehow filled with all sorts of data. It upgrades a certain Pokémon when traded."),
    ("Dubious Disc", "A transparent device overflowing with dubious data. It evolves a certain Pokémon when held during a trade."),
    ("Magmarizer", "Boosts the power of the holder's Fire-type moves or is used to evolve Magmar."),
    ("Electirizer", "An item to be held by Electabuzz. Boosts the power of the holder's Electric-type moves."),
    ("Prism Scale", "A mysterious scale that evolves a certain Pokémon when held during a trade."),
    ("Oval Stone", "A stone with an unusual shape that evolves a certain Pokémon when it levels up."),
    ("Protector", "A protective item of some sort. It evolves a certain Pokémon when held during a trade."),
    ("Razor Fang", "An item to be held by a Pokémon. The sharp fang may make the target flinch, and evolves Gligar."),
    ("Razor Claw", "An item to be held by a Pokémon. The sharp claw may cause the foe to flinch and evolves Sneasel."),
    ("Deep Sea Tooth", "A rare tooth that evolves Clamperl when held during a trade."),
    ("Deep Sea Scale", "A rare scale that evolves Clamperl when held during a trade."),
    ("Reaper Cloth", "A cloth imbued with horrific energy that evolves Dusclops when held during a trade."),
]:
    _item(ItemData(link_item, ItemCategory.HELD, 0, description=link_desc))

# ── Fossils ───────────────────────────────────────────────────────────────────
_item(ItemData("Dome Fossil", ItemCategory.FOSSIL, 0, revives_to="Kabuto",
               description="A fossil from an ancient and long-since-gone era. It appears to be a piece of a primeval shellfish."))
_item(ItemData("Helix Fossil", ItemCategory.FOSSIL, 0, revives_to="Omanyte",
               description="A fossil from an ancient and long-since-gone era. It appears to be part of a primeval shellfish."))
_item(ItemData("Old Amber", ItemCategory.FOSSIL, 0, revives_to="Aerodactyl",
               description="A piece of amber that contains the genetic material of an ancient Pokémon."))
_item(ItemData("Root Fossil", ItemCategory.FOSSIL, 0, revives_to="Lileep",
               description="A fossil from an ancient and long-since-gone era. It appears to be part of the roots of an ancient Pokémon."))
_item(ItemData("Claw Fossil", ItemCategory.FOSSIL, 0, revives_to="Anorith",
               description="A fossil from an ancient and long-since-gone era. It appears to be a part of a primeval claw."))
_item(ItemData("Skull Fossil", ItemCategory.FOSSIL, 0, revives_to="Cranidos",
               description="A fossil from an ancient and long-since-gone era. It appears to be part of the skull of a primeval Pokémon."))
_item(ItemData("Armor Fossil", ItemCategory.FOSSIL, 0, revives_to="Shieldon",
               description="A fossil from an ancient and long-since-gone era. It appears to be part of the shell of a primeval Pokémon."))

# ── Key Items ─────────────────────────────────────────────────────────────────
for ki_name, ki_desc in [
    ("Bicycle", "A folding bicycle that allows you to get around much faster than when walking."),
    ("Old Rod", "An old and somewhat beat-up fishing rod. Use it by any body of water to fish for wild aquatic Pokémon."),
    ("Good Rod", "A new, good-quality fishing rod. Use it by any body of water to fish for wild aquatic Pokémon."),
    ("Super Rod", "An amazing, high-tech fishing rod. Use it by any body of water to fish for wild aquatic Pokémon."),
    ("Pokédex", "A high-tech device that automatically records data on all Pokémon you've seen and caught."),
    ("Town Map", "A very convenient map that can be viewed anytime. It even shows your current location in the region."),
    ("SS Ticket", "A ticket for the cruise ship known as the S.S. Anne."),
    ("Secret Key", "The key to the Cinnabar Island Gym."),
    ("Card Key", "A card key that opens the automatic doors in Silph Co."),
    ("Lift Key", "The key to the elevator in the Rocket Hideout."),
    ("Silph Scope", "A device that can identify mysterious, invisible Pokémon."),
    ("Coin Case", "A case for storing coins obtained at the Game Corner."),
    ("Itemfinder", "A device that can detect nearby items that are buried or otherwise hidden."),
]:
    _item(ItemData(ki_name, ItemCategory.KEY, 0, description=ki_desc))

# ── TM/HM items ───────────────────────────────────────────────────────────────
# These are generated dynamically from move data; the items are stored here for bag purposes
# See moves.py for TM_MOVES and HM_MOVES
