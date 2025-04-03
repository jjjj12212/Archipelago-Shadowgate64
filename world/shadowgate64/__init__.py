from math import ceil, floor
import random
from multiprocessing import Process
import settings
import typing
from typing import Dict, Any
from .Items import ItemData, Shadowgate64Item, all_item_table, all_group_table
from .Locations import LocationData, all_location_table
from .Regions import create_regions, connect_regions
from .Options import Shadowgate64Options
from .Rules import Shadowgate64Rules
from .Names import itemName, locationName, regionName

from BaseClasses import ItemClassification, Tutorial, Item, Region, MultiWorld
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def run_client():
    from worlds.shadowgate64.Sg64Client import main  # lazy import
    launch_subprocess(main)

components.append(Component("Shadowgate 64 Client", func=run_client, component_type=Type.CLIENT))

class Shadowgate64Web(WebWorld):
    setup = Tutorial("Setup Shadowgate 64",
        """A guide to setting up Archipelago Shadowgate64 on your computer.""",
        "English",
        "setup_en.md",
        "setup/en",
        ["jjjj12212"])
    
    tutorials = [setup]
    

class Shadowgate64World(World):
    """
    Shadowgate 64: Trials of the Four Towers, also known simply as Shadowgate 64 is a sequel to the original Shadowgate.
    Its a first person puzzle solving adventure game.
    """
    
    game: str = "Shadowgate 64"
    web = Shadowgate64Web()
    topology_present = True
    item_name_to_id = {}

    for name, data in all_item_table.items():
        if data.id is None:  # Skip Victory Item
            continue
        item_name_to_id[name] = data.id

    location_name_to_id = {name: data.id for name, data in all_location_table.items()}
    location_name_to_group = {name: data.group for name, data in all_location_table.items()}

    item_name_groups = {
        "Items": all_group_table["items"],
        "Books": all_group_table["books"],
        "Notes": all_group_table["notes"]
    }
        
    options_dataclass =  Shadowgate64Options
    options: Shadowgate64Options

    def __init__(self, world, player):
        self.version = "V0.1"
        super(Shadowgate64World, self).__init__(world, player)
        
    def item_code(self, itemname: str) -> int:
        return all_item_table[itemname].id

    def create_item(self, itemname: str) -> Item:
        item = all_item_table.get(itemname)
        if item.type == 'progress':
            if not self.options.shop_items and itemname == itemName.COIN:
                item_classification = ItemClassification.filler    
            else:
                item_classification = ItemClassification.progression    
        elif item.type == 'useful':
                item_classification = ItemClassification.useful
        elif item.type == 'filler':
            item_classification = ItemClassification.filler 
        elif item.type == 'trap':
            item_classification = ItemClassification.trap
        elif item.type == "victory":
            victory_item = Shadowgate64Item(itemName.VICTORY, ItemClassification.filler, None, self.player)
            return victory_item
        created_item = Shadowgate64Item(self.item_id_to_name[item.id], item_classification, item.id, self.player)
        return created_item

    def create_event_item(self, name: str) -> Item:
        item_classification = ItemClassification.progression
        created_item = Shadowgate64Item(name, item_classification, None, self.player)
        return created_item
    
    def create_items(self) -> None:
        itempool = []
        for name, itemData in all_item_table.items():
            item = self.create_item(name)
            if self.item_filter(name):
                for i in range(itemData.qty):
                    itempool += [self.create_item(name)]
        self.multiworld.itempool.extend(itempool)
        # for item in itempool:
        #     self.multiworld.itempool.append(item)


    def item_filter(self, item_name: str) -> bool:
        if item_name == itemName.BONE or item_name == itemName.WATER or item_name == itemName.WATER_DRAGON_TEARS \
            or item_name == itemName.PAIR_OF_SLIPPERS or item_name == itemName.STRINGLESS_VIOLIN \
            or item_name == itemName.BROKEN_VIOLIN or item_name == itemName.CUP or item_name == itemName.STAFF_OF_AGES \
            or item_name == itemName.DUNGEON_KEY:
            return False
        
        if not self.options.books and item_name in (self.item_name_groups["Books"]):
            return False
        elif not self.options.notes and item_name in (self.item_name_groups["Notes"]):
            return False
        
        if not self.options.shop_items and (item_name == itemName.BROOCH or item_name == itemName.JEWELRY_BOX \
            or item_name == itemName.FRUIT or item_name == itemName.GAUNTLET):
            return False
        return True

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)
        self.pre_fill_me()


    def generate_early(self) -> None:
        bone = self.create_item(itemName.BONE)
        self.multiworld.push_precollected(bone)

    def set_rules(self) -> None:
        rules = Rules.Shadowgate64Rules(self)
        return rules.set_rules()
    
    def pre_fill_me(self) -> None:
        if not self.options.books:
            self.shadowgate_pre_fills("Books")
        if not self.options.notes:
            self.shadowgate_pre_fills("Notes")
        item = self.create_item(itemName.WATER)
        self.get_location(locationName.LOC_WATER).place_locked_item(item)   
        item = self.create_item(itemName.WATER_DRAGON_TEARS)
        self.get_location(locationName.LOC_WATER_DRAGON_TEARS).place_locked_item(item)
        item = self.create_item(itemName.PAIR_OF_SLIPPERS)
        self.get_location(locationName.LOC_PAIR_OF_SLIPPERS).place_locked_item(item)
        item = self.create_item(itemName.BROKEN_VIOLIN)
        self.get_location(locationName.LOC_BROKEN_VIOLIN).place_locked_item(item)
        item = self.create_item(itemName.STRINGLESS_VIOLIN)
        self.get_location(locationName.LOC_STRINGLESS_VIOLIN).place_locked_item(item) 
        if not self.options.shop_items:
            item = self.create_item(itemName.BROOCH)
            self.get_location(locationName.LOC_BROOCH).place_locked_item(item) 
            item = self.create_item(itemName.JEWELRY_BOX)
            self.get_location(locationName.LOC_JEWELRY_BOX).place_locked_item(item)
            item = self.create_item(itemName.FRUIT)
            self.get_location(locationName.LOC_FRUIT).place_locked_item(item)
            item = self.create_item(itemName.GAUNTLET)
            self.get_location(locationName.LOC_GAUNTLET).place_locked_item(item)
        item = self.create_item(itemName.CUP)
        self.get_location(locationName.LOC_CUP).place_locked_item(item)
        #item = self.create_item(itemName.STAFF_OF_AGES)
        item = self.create_item(itemName.END_GAME_PROGRESSION)
        self.get_location(locationName.LOC_STAFF_OF_AGES).place_locked_item(item)
        item = self.create_item(itemName.DUNGEON_KEY) 
        self.get_location(locationName.LOC_DUNGEON_KEY).place_locked_item(item)
        

    def get_filler_item_name(self) -> str:
        return itemName.BLANK_BOOK

    def shadowgate_pre_fills(self, item_type: str) -> None:
        if item_type == "Books" or item_type == "Notes":
            for item_name in self.item_name_groups[item_type]:
                item = self.create_item(item_name)
                item_data = all_item_table[item_name]
                if item_data.qty == 1:
                    location_name:str = self.location_id_to_name[item.code]
                    self.get_location(location_name).place_locked_item(item)
                else:
                    location_id = item_data.id
                    for i in range(item_data.qty):
                        location_name:str = self.location_id_to_name[location_id + i]
                        self.get_location(location_name).place_locked_item(item)


    

    def fill_slot_data(self) -> Dict[str, Any]:
        options = self.options.as_dict("open_disciple_tower_doors")
        options["player_name"] = self.multiworld.player_name[self.player]
        options["seed"] = self.random.randint(12212, 9090763)
        options["version"] = self.version
        return options
