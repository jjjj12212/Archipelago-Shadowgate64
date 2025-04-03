from dataclasses import dataclass
from Options import Toggle, DeathLink, PerGameCommonOptions, Choice, DefaultOnToggle, Range, StartInventoryPool, FreeText

class RandomizeBooks(DefaultOnToggle):
    """Randomize Books (Filler Item)."""
    display_name = "Randomize Books"

class RandomizeNotes(DefaultOnToggle):
    """Randomize Notes (Filler Item)."""
    display_name = "Randomize Notes"

class RandomizeShopItems(DefaultOnToggle):
    """Randomize Shop Items. If set to True, the logic expects the item order is the amount of coins to obtain.
        eg. first item requires 1 coin, second item requires 2 coins, etc.
        If set to false, the shop will not be randomized and coins are filler."""
    display_name = "Randomize Shop Items"

class DiscipleTowerDoor(Toggle):
    """Opens the Door from Disciple Tower to the rest of Shadowgate"""
    display_name = "Open Disciple Tower Door without Ring of Undead"

@dataclass
class Shadowgate64Options(PerGameCommonOptions):
    books: RandomizeBooks
    notes: RandomizeNotes
    shop_items: RandomizeShopItems
    open_disciple_tower_doors: DiscipleTowerDoor
    start_inventory_from_pool: StartInventoryPool

