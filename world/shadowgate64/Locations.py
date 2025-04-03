from BaseClasses import Location
import typing
from .Names import locationName

class Shadowgate64Location(Location):
    game: str = "Shadowgate64"
    
class LocationData(typing.NamedTuple):
    id: int = 0
    group: str  = '' # some items are part of a group that needs to be processed seperately

loc_item_table = {
    locationName.LOC_CREST_KEY:             LocationData(1230381, None),
    locationName.LOC_BOTTLE_OF_OIL:         LocationData(1230382, None),
    locationName.LOC_FRAGMENTS_OF_CREST:    LocationData(1230383, None),
    locationName.LOC_DRAGON_TEARS:          LocationData(1230384, None),
    locationName.LOC_PIXIE_FLUTE:           LocationData(1230385, None),
    locationName.LOC_TREASURE:              LocationData(1230386, None),
    locationName.LOC_RUSTY_KEY:             LocationData(1230387, None),
    locationName.LOC_ORNATE_KEY:            LocationData(1230388, None),
    locationName.LOC_RING_OF_THE_KINGDOM:   LocationData(1230389, None),
    locationName.LOC_ORB:                   LocationData(1230390, None),
    locationName.LOC_GOLDEN_KEY:            LocationData(1230391, None),
    locationName.LOC_LIQUID_SUNSET:         LocationData(1230392, None),
    locationName.LOC_NIGHT_ELIXIR:          LocationData(1230393, None),
    locationName.LOC_FOREST_NECTAR:         LocationData(1230394, None),
    locationName.LOC_PRIMITIVE_MAN_STATUE:  LocationData(1230395, None),
    locationName.LOC_APEMAN_SCULPTURE:      LocationData(1230396, None),
    locationName.LOC_FAIRY_SCULPTURE:       LocationData(1230397, None),
    locationName.LOC_ELF_STATUE:            LocationData(1230398, None),
    locationName.LOC_ANCIENT_COIN:          LocationData(1230399, None),
    locationName.LOC_PICK_AXE:               LocationData(1230400, None),
    locationName.LOC_RING_OF_THE_DEAD:      LocationData(1230401, None),
    locationName.LOC_BLUE_RING:             LocationData(1230402, None),
    locationName.LOC_GREEN_RING:            LocationData(1230403, None),
    locationName.LOC_LEVER:                 LocationData(1230404, None),
    locationName.LOC_SLIPPER:               LocationData(1230405, None),
    locationName.LOC_DIRTY_SLIPPER:         LocationData(1230406, None),
    locationName.LOC_PAIR_OF_SLIPPERS:      LocationData(1230407, None),
    locationName.LOC_JEZIBEL_PENDANT:       LocationData(1230408, None),
    locationName.LOC_STAFF_OF_AGES:         LocationData(1230409, None),
    locationName.LOC_ROPE:                  LocationData(1230410, None),
    locationName.LOC_CEMETERY_KEY:          LocationData(1230411, None),
    locationName.LOC_FLOWER:                LocationData(1230412, None),
    locationName.LOC_FLINT:                 LocationData(1230413, None),
    locationName.LOC_FANG:                  LocationData(1230414, None),
    locationName.LOC_DRAGON_EYE:            LocationData(1230415, None),
    locationName.LOC_DRAGON_FLUTE:          LocationData(1230416, None),
    locationName.LOC_BURNING_CANDLE:        LocationData(1230417, None),
    locationName.LOC_CHIPPED_VIOLIN:        LocationData(1230418, None),
    locationName.LOC_STRINGLESS_VIOLIN:     LocationData(1230419, None),
    locationName.LOC_BROKEN_VIOLIN:         LocationData(1230420, None),
    locationName.LOC_DUNGEON_KEY:           LocationData(1230421, None),
    locationName.LOC_MAP:                   LocationData(1230422, None),
    #locationName.LOC_BONE:                  LocationData(1230423, None),
    locationName.LOC_STARCREST:             LocationData(1230424, None),
    locationName.LOC_IRON_BAR:              LocationData(1230425, None),
    locationName.LOC_CROWBAR:               LocationData(1230426, None),
    locationName.LOC_HAIR_OF_GIANT:         LocationData(1230427, None),
    locationName.LOC_MUG:                   LocationData(1230428, None),
    locationName.LOC_WATER:                 LocationData(1230429, None),
    locationName.LOC_WATER_DRAGON_TEARS:    LocationData(1230430, None),
    locationName.LOC_STONE_OF_THIRST:       LocationData(1230431, None),
    locationName.LOC_COIN1:                 LocationData(1230432, "Coin"),
    locationName.LOC_COIN2:                 LocationData(1230433, "Coin"),
    locationName.LOC_COIN3:                 LocationData(1230434, "Coin"),
    locationName.LOC_COIN4:                 LocationData(1230435, "Coin"),
    # locationName.LOC_COIN5:                 LocationData(1230436, "Coin"), 
    locationName.LOC_NAIL:                  LocationData(1230437, None),
    locationName.LOC_BROOCH:                LocationData(1230438, None),
    locationName.LOC_JEWELRY_BOX:           LocationData(1230439, None),
    locationName.LOC_FRUIT:                 LocationData(1230440, None),
    locationName.LOC_GAUNTLET:              LocationData(1230441, None),
    locationName.LOC_CUP:                   LocationData(1230442, None),
    locationName.LOC_ARTWORK:               LocationData(1230443, None),
    locationName.LOC_POISONOUS_HERB:        LocationData(1230444, None),
    locationName.LOC_BRACELET:              LocationData(1230445, None),
    locationName.LOC_PRECIOUS_STONE:        LocationData(1230446, None),
    locationName.LOC_BROKEN_SWORD:          LocationData(1230447, None),
    locationName.LOC_QUILL:                 LocationData(1230448, None),
    locationName.LOC_PLATE:                 LocationData(1230449, None),
    locationName.LOC_BROKEN_LANCE:          LocationData(1230450, None),
}

loc_book_table = {
    locationName.LOC_DNARTH_CHRONICLES:     LocationData(1230455, None),
    locationName.LOC_FINAL_BATTLE:          LocationData(1230456, None),
    locationName.LOC_SPEECHES_JAIR:         LocationData(1230457, None),
    locationName.LOC_BLANK_BOOK1:           LocationData(1230458, "Blank Book"),
    locationName.LOC_BLANK_BOOK2:           LocationData(1230459, "Blank Book"),
    locationName.LOC_BLANK_BOOK3:           LocationData(1230460, "Blank Book"),
    locationName.LOC_STUDENT_DIARY:         LocationData(1230461, None),
    locationName.LOC_ACOLYTE_DIARY:         LocationData(1230462, None),
    locationName.LOC_PERSONAL_JOURNAL:      LocationData(1230463, None),
    locationName.LOC_MEMOIRS:               LocationData(1230464, None),
    locationName.LOC_NOVICE_JOURNAL:        LocationData(1230465, None),
    locationName.LOC_TRIALS_KINGDOM:        LocationData(1230466, None),
    locationName.LOC_BROTHERHOOD_REPORT:    LocationData(1230467, None),
    locationName.LOC_WRITINGS_KONNOR:       LocationData(1230468, None),
    locationName.LOC_HOUSE_DRESLIN:         LocationData(1230469, None),
    locationName.LOC_MEMORANDUM:            LocationData(1230470, None),
    locationName.LOC_LAST_DRAGON:           LocationData(1230471, None),
    locationName.LOC_RIDING_DRAGONS:        LocationData(1230472, None),
    locationName.LOC_RESEARCH_LOG:          LocationData(1230473, None),
    locationName.LOC_MUSINGS_LUNATIC:       LocationData(1230474, None),
    locationName.LOC_ORDERS:                LocationData(1230475, None),
    locationName.LOC_LAWS_MAGIC:            LocationData(1230476, None),
    locationName.LOC_FAMILY_DIARY:          LocationData(1230477, None),
    locationName.LOC_WORDS_DNARTH:          LocationData(1230478, None),
    locationName.LOC_ARTIFACTS_POWER:       LocationData(1230479, None),
    locationName.LOC_MAGICAL_ELIXIRS:       LocationData(1230480, None),
}

loc_note_table = {
    locationName.LOC_JOURNAL:               LocationData(1230484, None),
    locationName.LOC_WATCHMAN_MEMO:         LocationData(1230485, None),
    locationName.LOC_REPORT:                LocationData(1230486, None),
    locationName.LOC_OFFICIAL_ARTICLE:      LocationData(1230487, None),
    locationName.LOC_LECTURE_NOTES:         LocationData(1230488, None),
    locationName.LOC_PERSONAL_LETTER:       LocationData(1230489, None),
    locationName.LOC_INNER_CHAMBER:         LocationData(1230490, None),
    locationName.LOC_TRAVELOGUE:            LocationData(1230491, None),
    locationName.LOC_TRAVEL_GUIDE:          LocationData(1230492, None),
    locationName.LOC_PETITION:              LocationData(1230493, None),
    locationName.LOC_RECEIPT:               LocationData(1230494, None),
    locationName.LOC_PERSONAL_NOTE:         LocationData(1230495, None),
}



all_location_table = {
    **loc_item_table,
    **loc_book_table,
    **loc_note_table
}




