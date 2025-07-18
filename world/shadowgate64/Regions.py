import copy
import typing
from BaseClasses import Region

from .Names import regionName, locationName, itemName
from .Locations import Shadowgate64Location
from .Rules import Shadowgate64Rules

# This dict contains all the regions, as well as all the locations that are always tracked by Archipelago.
Shadowgate64Maps: typing.Dict[str, typing.List[str]] = {
    "Menu":              [],
    regionName.INTRO_PRISON_CELL: [],
    regionName.SEWER_PRISON: [
        locationName.LOC_IRON_BAR,
        locationName.LOC_PAIR_OF_SLIPPERS,
        locationName.LOC_TREASURE,
        locationName.LOC_MAP,
    ],
    regionName.SEWER_ACROSS: [
        locationName.LOC_PICK_AXE,
        locationName.LOC_JOURNAL,
    ],
    regionName.TOWER1_ENTRANCE: [
        locationName.LOC_ROPE,
        locationName.LOC_FAIRY_SCULPTURE,
        locationName.LOC_ELF_STATUE,
        locationName.LOC_CEMETERY_KEY,
        locationName.LOC_SLIPPER,
        locationName.LOC_STONE_OF_THIRST,
        locationName.LOC_DRAGON_FLUTE,
    ],
    regionName.TOWER1_UPSTAIRS: [
        locationName.LOC_BLANK_BOOK3,
        locationName.LOC_RIDING_DRAGONS,
        locationName.LOC_FINAL_BATTLE,
        locationName.LOC_BLANK_BOOK2,
        locationName.LOC_LAWS_MAGIC,
        locationName.LOC_MEMORANDUM,
        locationName.LOC_ARTIFACTS_POWER,
        locationName.LOC_APEMAN_SCULPTURE,
        locationName.LOC_LIQUID_SUNSET,
        locationName.LOC_ANCIENT_COIN,
        locationName.LOC_LECTURE_NOTES,
        locationName.LOC_ORDERS,
        locationName.LOC_PRIMITIVE_MAN_STATUE,
        locationName.LOC_SPEECHES_JAIR,
        locationName.LOC_WATCHMAN_MEMO,
        locationName.LOC_REPORT
    ],
    regionName.TOWER1_PAST_STATUES: [
        locationName.LOC_BLANK_BOOK1,
        locationName.LOC_PIXIE_FLUTE,
        locationName.LOC_STUDENT_DIARY,
        locationName.LOC_HOUSE_DRESLIN,
        locationName.LOC_PERSONAL_NOTE,
        locationName.LOC_PERSONAL_LETTER,

    ],
    regionName.CEMETERY_AND_SANTUARY: [
        locationName.LOC_DRAGON_TEARS,
        locationName.LOC_GOLDEN_KEY,
        locationName.LOC_ORNATE_KEY,
        locationName.LOC_CROWBAR,
        locationName.LOC_NAIL,
        locationName.LOC_JEZIBEL_PENDANT,
        locationName.LOC_FAMILY_DIARY,
    ],
    regionName.SANTUARY_ROOF: [],
    regionName.LAKMIR_TOWER_TOP_FLOOR: [
        locationName.LOC_BOTTLE_OF_OIL,
        locationName.LOC_WATER,
        locationName.LOC_WATER_DRAGON_TEARS,
    ],
    regionName.LAKMIR_TOWER_MAIN_ENTRANCE: [
        locationName.LOC_ACOLYTE_DIARY,
        locationName.LOC_RECEIPT,
        locationName.LOC_HAIR_OF_GIANT,
        locationName.LOC_MAGICAL_ELIXIRS,
        locationName.LOC_RUSTY_KEY,
        locationName.LOC_MUG,
        locationName.LOC_OFFICIAL_ARTICLE,
    ],
    regionName.LAKMIR_TOWER_BASEMENT: [
        locationName.LOC_STARCREST,
    ],
    regionName.LAKMIR_TOWER_BASEMENT_MAZE: [],
    regionName.LAKMIR_INNER_TOWER: [
        locationName.LOC_PERSONAL_JOURNAL,
        locationName.LOC_FOREST_NECTAR,
        locationName.LOC_CREST_KEY,
        locationName.LOC_MEMOIRS,
        locationName.LOC_QUILL,
        locationName.LOC_NIGHT_ELIXIR,
        locationName.LOC_INNER_CHAMBER,
    ],
    regionName.LAKMIR_RING_ROOM: [
        locationName.LOC_RING_OF_THE_DEAD,
        locationName.LOC_BLUE_RING,
        locationName.LOC_GREEN_RING,
    ],
    regionName.OUTSIDE: [
        locationName.LOC_COIN1,
        locationName.LOC_POISONOUS_HERB,
        locationName.LOC_COIN2,
        locationName.LOC_DIRTY_SLIPPER,
        locationName.LOC_ARTWORK,
        locationName.LOC_MUSINGS_LUNATIC,
        locationName.LOC_COIN3,
        locationName.LOC_BROKEN_SWORD,
        locationName.LOC_BROKEN_LANCE,
        locationName.LOC_PETITION,
        locationName.LOC_PRECIOUS_STONE,
        locationName.LOC_PLATE,
        locationName.LOC_BRACELET,
        locationName.LOC_DNARTH_CHRONICLES,
        locationName.LOC_FLOWER,
        locationName.LOC_DUNGEON_KEY,
        locationName.LOC_CHIPPED_VIOLIN,
        locationName.LOC_STRINGLESS_VIOLIN,
        locationName.LOC_BROKEN_VIOLIN,
        locationName.LOC_COIN4,
        locationName.LOC_BROOCH,
        locationName.LOC_JEWELRY_BOX,
        locationName.LOC_FRUIT,
        locationName.LOC_GAUNTLET,
        locationName.LOC_CUP,
    ],
    regionName.INN: [
        locationName.LOC_TRAVEL_GUIDE,
        locationName.LOC_TRAVELOGUE,
        locationName.LOC_ORB,
    ],
    regionName.PRISONER_HOUSE: [
        locationName.LOC_FLINT,
        locationName.LOC_FANG,
        locationName.LOC_LEVER,
        locationName.LOC_RESEARCH_LOG,

    ],
    regionName.RESERVOIR: [],
    regionName.TRIALS_TOWER: [
        locationName.LOC_FRAGMENTS_OF_CREST,
        locationName.LOC_NOVICE_JOURNAL,
        locationName.LOC_WRITINGS_KONNOR,
        locationName.LOC_BROTHERHOOD_REPORT,
        locationName.LOC_TRIALS_KINGDOM,

    ],
    regionName.TRIALS_TOWER_PAST_CREST: [
        locationName.LOC_BURNING_CANDLE,
    ],
    regionName.TRIALS_TOWER_PAST_MAZE: [
        locationName.LOC_RING_OF_THE_KINGDOM,
    ],
    regionName.DRAGON_TOWER: [
        locationName.LOC_LAST_DRAGON,
        locationName.LOC_DRAGON_EYE,
    ],
    regionName.DRAGON_TOWER_SECOND: [
        locationName.LOC_WORDS_DNARTH,

    ],
    regionName.DRAGON_TOWER_TOP: [
        locationName.LOC_STAFF_OF_AGES,
    ],
    regionName.ALERTED_TOWN: [],
    regionName.THE_END: [
        locationName.LOC_VICTORY
    ]
}
    
def create_regions(self):
    multiworld = self.multiworld
    player = self.player
    active_locations = self.location_name_to_id
    region_map = copy.deepcopy(Shadowgate64Maps)

    multiworld.regions += [create_region(multiworld, player, active_locations, region, locations) for region, locations in
                           region_map.items()] 
    multiworld.get_location(locationName.LOC_VICTORY, player).place_locked_item(
      multiworld.worlds[player].create_event_item(itemName.VICTORY))

def create_region(multiworld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        loc_to_id = {loc: active_locations.get(loc, 0) for loc in locations if active_locations.get(loc, None)}
        if locationName.LOC_VICTORY in locations:
            ret.add_locations({locationName.LOC_VICTORY: None})
        else:
            ret.add_locations(loc_to_id, Shadowgate64Location)
    return ret

def connect_regions(self):
    multiworld = self.multiworld
    player = self.player
    rules = Shadowgate64Rules(self)

    region_menu = multiworld.get_region("Menu", player)
    region_menu.add_exits({regionName.INTRO_PRISON_CELL})

    next_working_region = multiworld.get_region(regionName.INTRO_PRISON_CELL, player)
    next_working_region.add_exits({regionName.SEWER_PRISON},{
                                  regionName.SEWER_PRISON: lambda state: rules.has_bone(state)
                                  })
    
    next_working_region = multiworld.get_region(regionName.SEWER_PRISON, player)
    next_working_region.add_exits({regionName.SEWER_ACROSS, regionName.TOWER1_ENTRANCE},{
                                  regionName.SEWER_ACROSS: lambda state: rules.has_bar(state),
                                  regionName.TOWER1_ENTRANCE: lambda state: rules.has_pickaxe(state)
                                  })
    next_working_region = multiworld.get_region(regionName.SEWER_ACROSS, player)
    next_working_region.add_exits({regionName.SEWER_PRISON, regionName.CEMETERY_AND_SANTUARY, regionName.TOWER1_ENTRANCE},{
                                  regionName.SEWER_PRISON: lambda state: rules.has_bar(state) and state.can_reach_region(regionName.SEWER_PRISON, self.player),
                                  regionName.CEMETERY_AND_SANTUARY: lambda state: rules.has_rusty_key(state),
                                  regionName.TOWER1_ENTRANCE: lambda state: rules.has_rusty_key(state)
                                  })
    
    next_working_region = multiworld.get_region(regionName.TOWER1_ENTRANCE, player)
    next_working_region.add_exits({regionName.SEWER_PRISON, regionName.SEWER_ACROSS, regionName.TOWER1_UPSTAIRS,
                                   regionName.CEMETERY_AND_SANTUARY, regionName.OUTSIDE, regionName.ALERTED_TOWN},{
                                  regionName.SEWER_ACROSS: lambda state: rules.has_rusty_key(state),
                                  regionName.SEWER_PRISON: lambda state: rules.has_pickaxe(state),
                                  regionName.CEMETERY_AND_SANTUARY: lambda state: rules.tower_to_cementery(state),
                                  regionName.OUTSIDE: lambda state: rules.from_disciple_tower_to_shadowgate(state),
                                  regionName.ALERTED_TOWN: lambda state: rules.can_pursade_guards(state) and rules.from_disciple_tower_to_shadowgate(state)
                                  })
    
    next_working_region = multiworld.get_region(regionName.TOWER1_UPSTAIRS, player)
    next_working_region.add_exits({regionName.TOWER1_ENTRANCE, regionName.TOWER1_PAST_STATUES},{
                                  regionName.TOWER1_PAST_STATUES: lambda state: rules.can_solve_statue_puzzle(state)
                                  })
    next_working_region = multiworld.get_region(regionName.TOWER1_PAST_STATUES, player)
    next_working_region.add_exits({regionName.TOWER1_UPSTAIRS})
    
    next_working_region = multiworld.get_region(regionName.CEMETERY_AND_SANTUARY, player)
    next_working_region.add_exits({regionName.SANTUARY_ROOF, regionName.SEWER_ACROSS, regionName.OUTSIDE, regionName.ALERTED_TOWN},{
                                  regionName.SANTUARY_ROOF: lambda state: rules.has_crowbar(state),
                                  regionName.SEWER_ACROSS: lambda state: rules.has_rusty_key(state),
                                  regionName.OUTSIDE: lambda state: rules.has_cementery_key(state),
                                  regionName.ALERTED_TOWN: lambda state: rules.can_pursade_guards(state)
                                  })
    
    next_working_region = multiworld.get_region(regionName.SANTUARY_ROOF, player)
    next_working_region.add_exits({regionName.CEMETERY_AND_SANTUARY, regionName.LAKMIR_TOWER_TOP_FLOOR})
    
    next_working_region = multiworld.get_region(regionName.LAKMIR_TOWER_TOP_FLOOR, player)
    next_working_region.add_exits({regionName.CEMETERY_AND_SANTUARY, regionName.LAKMIR_TOWER_MAIN_ENTRANCE})

    next_working_region = multiworld.get_region(regionName.LAKMIR_TOWER_MAIN_ENTRANCE, player)
    next_working_region.add_exits({regionName.LAKMIR_TOWER_TOP_FLOOR, regionName.LAKMIR_TOWER_BASEMENT},{
                                  regionName.LAKMIR_TOWER_BASEMENT: lambda state: rules.has_oil(state)
                                  })
    
    next_working_region = multiworld.get_region(regionName.LAKMIR_TOWER_BASEMENT, player)
    next_working_region.add_exits({regionName.LAKMIR_TOWER_MAIN_ENTRANCE, regionName.LAKMIR_TOWER_BASEMENT_MAZE}, {
                                   regionName.LAKMIR_TOWER_BASEMENT_MAZE: lambda state: rules.open_basement_maze(state)
                                  })
    
    next_working_region = multiworld.get_region(regionName.LAKMIR_TOWER_BASEMENT_MAZE, player)
    next_working_region.add_exits({regionName.LAKMIR_TOWER_BASEMENT, regionName.LAKMIR_INNER_TOWER})

    next_working_region = multiworld.get_region(regionName.LAKMIR_INNER_TOWER, player)
    next_working_region.add_exits({regionName.LAKMIR_TOWER_BASEMENT_MAZE, regionName.LAKMIR_RING_ROOM}, {
                                  regionName.LAKMIR_RING_ROOM: lambda state: rules.open_ring_room(state)
                                  })
    
    next_working_region = multiworld.get_region(regionName.LAKMIR_RING_ROOM, player)
    next_working_region.add_exits({regionName.LAKMIR_INNER_TOWER})

    next_working_region = multiworld.get_region(regionName.OUTSIDE, player)
    next_working_region.add_exits({regionName.TOWER1_ENTRANCE, regionName.CEMETERY_AND_SANTUARY,
                                   regionName.INN, regionName.PRISONER_HOUSE, regionName.RESERVOIR,
                                   regionName.TRIALS_TOWER, regionName.DRAGON_TOWER, regionName.ALERTED_TOWN},
                                  {
                                  regionName.CEMETERY_AND_SANTUARY: lambda state: rules.has_cementery_key(state),
                                  regionName.INN: lambda state: rules.has_pendent(state),
                                  regionName.PRISONER_HOUSE: lambda state: rules.free_prisoner(state),
                                  regionName.RESERVOIR: lambda state: rules.can_reach_reservoir(state),
                                  regionName.TRIALS_TOWER: lambda state: rules.can_reach_trials_tower(state),
                                  regionName.DRAGON_TOWER: lambda state: rules.has_dragon_flute(state),
                                  regionName.ALERTED_TOWN: lambda state: rules.can_pursade_guards(state)
                                  })
    
    next_working_region = multiworld.get_region(regionName.INN, player)
    next_working_region.add_exits({regionName.OUTSIDE, regionName.ALERTED_TOWN}, {
        regionName.ALERTED_TOWN: lambda state: rules.can_pursade_guards(state)
    })

    next_working_region = multiworld.get_region(regionName.PRISONER_HOUSE, player)
    next_working_region.add_exits({regionName.OUTSIDE, regionName.ALERTED_TOWN}, {
        regionName.ALERTED_TOWN: lambda state: rules.can_pursade_guards(state)
    })

    next_working_region = multiworld.get_region(regionName.RESERVOIR, player)
    next_working_region.add_exits({regionName.OUTSIDE, regionName.ALERTED_TOWN}, {
        regionName.ALERTED_TOWN: lambda state: rules.can_pursade_guards(state)
    })

    next_working_region = multiworld.get_region(regionName.TRIALS_TOWER, player)
    next_working_region.add_exits({regionName.OUTSIDE, regionName.TRIALS_TOWER_PAST_CREST, regionName.ALERTED_TOWN},{
                                  regionName.TRIALS_TOWER_PAST_CREST: lambda state: rules.has_crest_fragments(state),
                                  regionName.ALERTED_TOWN: lambda state: rules.can_pursade_guards(state)
                                 })
    
    next_working_region = multiworld.get_region(regionName.TRIALS_TOWER_PAST_CREST, player)
    next_working_region.add_exits({regionName.TRIALS_TOWER, regionName.TRIALS_TOWER_PAST_MAZE},{
                                  regionName.TRIALS_TOWER_PAST_MAZE: lambda state: rules.has_candle(state)
                                 })
    
    next_working_region = multiworld.get_region(regionName.TRIALS_TOWER_PAST_MAZE, player)
    next_working_region.add_exits({regionName.TRIALS_TOWER})
    
    next_working_region = multiworld.get_region(regionName.DRAGON_TOWER, player)
    next_working_region.add_exits({regionName.OUTSIDE, regionName.DRAGON_TOWER_SECOND},{
                                 regionName.DRAGON_TOWER_SECOND: lambda state: rules.has_fang(state),
                                 regionName.ALERTED_TOWN: lambda state: rules.can_pursade_guards(state)
                                 })
    
    next_working_region = multiworld.get_region(regionName.DRAGON_TOWER_SECOND, player)
    next_working_region.add_exits({regionName.DRAGON_TOWER, regionName.DRAGON_TOWER_TOP, })
        
    next_working_region = multiworld.get_region(regionName.DRAGON_TOWER_TOP, player)
    next_working_region.add_exits({regionName.DRAGON_TOWER_SECOND, regionName.OUTSIDE, regionName.ALERTED_TOWN}, {
        regionName.ALERTED_TOWN: lambda state: rules.can_pursade_guards(state)
    })
    #------------------------------------ Normal Castle Town State ---------------------------------------------

    next_working_region = multiworld.get_region(regionName.ALERTED_TOWN, player)
    next_working_region.add_exits({regionName.THE_END})
