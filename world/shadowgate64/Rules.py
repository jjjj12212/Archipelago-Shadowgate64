from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from .Names import regionName, itemName, locationName
from .Items import Shadowgate64Item
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import Shadowgate64World
else:
    Shadowgate64World = object

# Shamelessly Stolen from KH2 :D
    
class Shadowgate64Rules:
    player: int
    world: Shadowgate64World

    def __init__(self, world: Shadowgate64World) -> None:
        self.player = world.player
        self.world = world

        self.item_rules = {
            locationName.LOC_NAIL:  lambda state: self.has_crowbar(state),
            locationName.LOC_WATER: lambda state: self.has_mug(state),
            locationName.LOC_WATER_DRAGON_TEARS: lambda state: self.has_mug_and_tears(state),
            locationName.LOC_CREST_KEY: lambda state: self.has_something_metal(state),
            locationName.LOC_CEMETERY_KEY: lambda state: self.has_ring_of_dead(state),
            locationName.LOC_SLIPPER: lambda state: self.has_ring_of_dead(state),
            locationName.LOC_DIRTY_SLIPPER: lambda state: self.has_ancient_coin(state),
            locationName.LOC_PAIR_OF_SLIPPERS: lambda state: self.both_slippers(state),
            locationName.LOC_TREASURE: lambda state: self.reliquish_treasure(state),
            locationName.LOC_CHIPPED_VIOLIN: lambda state: self.can_trade_violin(state),
            locationName.LOC_BROKEN_VIOLIN: lambda state: self.can_trade_violin(state),
            locationName.LOC_STRINGLESS_VIOLIN: lambda state: self.can_trade_violin(state),
            locationName.LOC_JEZIBEL_PENDANT: lambda state: self.speak_to_ded_mom(state),
            locationName.LOC_FAMILY_DIARY: lambda state: self.speak_to_ded_mom(state),
            locationName.LOC_DUNGEON_KEY: lambda state: self.distract_guard(state),
            locationName.LOC_STONE_OF_THIRST: lambda state: self.obtain_stone_of_thirst(state),
            locationName.LOC_BURNING_CANDLE: lambda state: self.has_flint(state),
            locationName.LOC_DRAGON_FLUTE: lambda state: self.has_ring_of_kingdom(state),
            locationName.LOC_STAFF_OF_AGES: lambda state: self.has_ring_of_kingdom(state),
            locationName.LOC_VICTORY: lambda state: self.can_beat_game(state)
        }

        self.shop_item_rules = {
            locationName.LOC_BROOCH: lambda state: self.has_coins(state, 1),
            locationName.LOC_JEWELRY_BOX: lambda state: self.has_coins(state, 2),
            locationName.LOC_FRUIT: lambda state: self.has_coins(state, 3),
            locationName.LOC_GAUNTLET: lambda state: self.has_coins(state, 4),
            locationName.LOC_CUP: lambda state: self.has_coins(state, 4)
        }

    def has_bone(self, state: CollectionState) -> bool:
        return state.has(itemName.BONE, self.player)
    
    def has_bar(self, state: CollectionState) -> bool:
        return state.has(itemName.IRON_BAR, self.player)
    
    def has_pickaxe(self, state: CollectionState) -> bool:
        return state.has(itemName.PICK_AXE, self.player)
    
    def has_crowbar(self, state: CollectionState) -> bool:
        return state.has(itemName.CROWBAR, self.player)
    
    def has_oil(self, state: CollectionState) -> bool:
        return state.has(itemName.BOTTLE_OF_OIL, self.player)
    
    def has_mug(self, state: CollectionState) -> bool:
        return state.has(itemName.MUG, self.player)
    
    def has_rusty_key(self, state: CollectionState) -> bool:
        return state.has(itemName.RUSTY_KEY, self.player)
    
    def has_ring_of_dead(self, state: CollectionState) -> bool:
        return state.has(itemName.RING_OF_THE_DEAD, self.player)
    
    def has_cementery_key(self, state: CollectionState) -> bool:
        return state.has(itemName.CEMETERY_KEY, self.player)

    def has_ancient_coin(self, state: CollectionState) -> bool:
        return state.has(itemName.ANCIENT_COIN, self.player)
    
    def has_pendent(self, state: CollectionState) -> bool:
        #return state.has(itemName.JEZIBEL_PENDANT, self.player)
        return state.has(itemName.END_GAME_PROGRESSION, self.player, 1)

    
    def has_coins(self, state: CollectionState, amt: int) -> bool:
        return state.has(itemName.COIN, self.player, amt)
    
    def has_flint(self, state: CollectionState) -> bool:
        #return state.has(itemName.FLINT, self.player)
        return state.has(itemName.END_GAME_PROGRESSION, self.player, 2)
    
    def has_ring_of_kingdom(self, state: CollectionState) -> bool:
        return state.has(itemName.RING_OF_THE_KINGDOM, self.player)
    
    def has_dragon_flute(self, state: CollectionState) -> bool:
        return state.has(itemName.DRAGON_FLUTE, self.player)
    
    def has_dragon_eye(self, state: CollectionState) -> bool:
        return state.has(itemName.DRAGON_EYE, self.player)
    
    def has_fang(self, state: CollectionState) -> bool:
        return state.has(itemName.FANG, self.player)
    
    # def has_hair(self, state: CollectionState) -> bool:
    #     return state.has(itemName.HAIR_OF_GIANT, self.player)

    def has_candle(self, state: CollectionState) -> bool:
        return state.has(itemName.BURNING_CANDLE, self.player)
    
    def speak_to_ded_mom(self, state: CollectionState) -> bool:
        return state.has(itemName.RING_OF_THE_DEAD, self.player) and state.has(itemName.GOLDEN_KEY, self.player)
    
    def distract_guard(self, state: CollectionState) -> bool:
        return state.has(itemName.ORB, self.player) and state.has(itemName.CHIPPED_VIOLIN, self.player)
    
    def free_prisoner(self, state: CollectionState) -> bool:
        return self.distract_guard(state) and state.has(itemName.DUNGEON_KEY, self.player)
    
    def has_something_metal(self, state: CollectionState) -> bool:
        return state.has(itemName.NAIL, self.player) or state.has(itemName.CROWBAR, self.player)
    
    def has_mug_and_tears(self, state: CollectionState) -> bool:
        return state.has(itemName.MUG, self.player) and state.has(itemName.DRAGON_TEARS, self.player)
    
    def can_solve_statue_puzzle(self, state: CollectionState) -> bool:
        return state.has(itemName.ELF_STATUE, self.player) and state.has(itemName.FAIRY_SCULPTURE, self.player)
    
    def tower_to_cementery(self, state: CollectionState) -> bool:
        return state.has(itemName.ROPE, self.player) and state.has(itemName.PIXIE_FLUTE, self.player)
    
    def open_basement_maze(self, state: CollectionState) -> bool:
        return state.has(itemName.STARCREST, self.player) and state.has(itemName.WATER_DRAGON_TEARS, self.player)
    
    def open_ring_room(self, state: CollectionState) -> bool:
        return state.has(itemName.CREST_KEY, self.player) and state.has(itemName.LIQUID_SUNSET, self.player) \
        and state.has(itemName.NIGHT_ELIXIR, self.player)
    
    def access_to_the_end(self, state: CollectionState) -> bool:
        #return state.has(itemName.STAFF_OF_AGES, self.player)
        return state.has(itemName.END_GAME_PROGRESSION, self.player, 3)
    
    def from_disciple_tower_to_shadowgate(self, state: CollectionState) -> bool:
        if self.world.options.open_disciple_tower_doors:
            return True
        else:
            return self.has_ring_of_dead(state)

    
    def can_pursade_guards(self, state: CollectionState) -> bool:
        return self.has_flint(state) and self.has_pendent(state) and self.access_to_the_end(state)
    
    def can_beat_game(self, state: CollectionState) -> bool:
        return self.has_flint(state) and self.has_pendent(state) and self.has_dragon_eye(state) \
        and self.access_to_the_end(state) and self.has_ring_of_kingdom(state)
    
    def both_slippers(self, state: CollectionState) -> bool:
        return state.has(itemName.DIRTY_SLIPPER, self.player) and state.has(itemName.SLIPPER, self.player)
    
    def obtain_stone_of_thirst(self, state: CollectionState) -> bool:
        return self.both_slippers(state) and self.has_ring_of_dead(state) and state.can_reach_region(regionName.OUTSIDE, self.player)
    
    def reliquish_treasure(self, state: CollectionState) -> bool:
        return state.has(itemName.FLOWER, self.player) and state.has(itemName.RING_OF_THE_DEAD, self.player) \
        and state.can_reach_region(regionName.CEMETERY_AND_SANTUARY, self.player)
    
    def can_reach_reservoir(self, state: CollectionState) -> bool:
        return state.has(itemName.STONE_OF_THIRST, self.player) and self.has_ring_of_dead(state) \
        and state.has(itemName.DRAGON_TEARS, self.player) and state.can_reach_region(regionName.CEMETERY_AND_SANTUARY, self.player)
    
    def has_lever(self, state: CollectionState) -> bool:
        return state.has(itemName.LEVER, self.player)
    
    def can_reach_trials_tower(self, state: CollectionState) -> bool:
        return self.can_reach_reservoir(state) and self.has_lever(state)
    
    def has_crest_fragments(self, state: CollectionState) -> bool:
        return state.has(itemName.FRAGMENTS_OF_CREST, self.player)
    
    def can_trade_violin(self, state:CollectionState) -> bool:
        return state.has(itemName.TREASURE, self.player) or \
        state.has(itemName.CHIPPED_VIOLIN, self.player)

    def set_rules(self) -> None:
        for location, rules in self.item_rules.items():
            key_item = self.world.multiworld.get_location(location, self.player)
            set_rule(key_item, rules)
        if self.world.options.shop_items:
            for location, rules in self.shop_item_rules.items():
                key_item = self.world.multiworld.get_location(location, self.player)
                set_rule(key_item, rules)

        self.world.multiworld.completion_condition[self.player] = lambda state: state.has(itemName.VICTORY, self.player)
