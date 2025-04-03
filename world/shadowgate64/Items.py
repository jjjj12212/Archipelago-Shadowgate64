from BaseClasses import Item
import typing
from .Names import itemName
from .Names import locationName


class Shadowgate64Item(Item):
    #start at 1230380
    game: str = "Shadowgate64"
class ItemData(typing.NamedTuple):
    id: int = 0
    type: str = ""
    default_location: str = "",
    qty: int = 1

items_table = {
    itemName.CREST_KEY:             ItemData(1230381, "progress", locationName.LOC_CREST_KEY, 1),
    itemName.BOTTLE_OF_OIL:         ItemData(1230382, "progress", locationName.LOC_BOTTLE_OF_OIL, 1),
    itemName.FRAGMENTS_OF_CREST:    ItemData(1230383, "progress", locationName.LOC_FRAGMENTS_OF_CREST, 1),
    itemName.DRAGON_TEARS:          ItemData(1230384, "progress", locationName.LOC_DRAGON_TEARS, 1),
    itemName.PIXIE_FLUTE:           ItemData(1230385, "progress", locationName.LOC_PIXIE_FLUTE, 1),
    itemName.TREASURE:              ItemData(1230386, "progress", locationName.LOC_TREASURE, 1),
    itemName.RUSTY_KEY:             ItemData(1230387, "progress", locationName.LOC_RUSTY_KEY, 1),
    itemName.ORNATE_KEY:            ItemData(1230388, "progress", locationName.LOC_ORNATE_KEY, 1),
    itemName.RING_OF_THE_KINGDOM:   ItemData(1230389, "progress", locationName.LOC_RING_OF_THE_KINGDOM, 1),
    itemName.ORB:                   ItemData(1230390, "progress", locationName.LOC_ORB, 1),
    itemName.GOLDEN_KEY:            ItemData(1230391, "progress", locationName.LOC_GOLDEN_KEY, 1),
    itemName.LIQUID_SUNSET:         ItemData(1230392, "progress", locationName.LOC_LIQUID_SUNSET, 1),
    itemName.NIGHT_ELIXIR:          ItemData(1230393, "progress", locationName.LOC_NIGHT_ELIXIR, 1),
    itemName.FOREST_NECTAR:         ItemData(1230394, "filler", locationName.LOC_FOREST_NECTAR, 1),
    itemName.PRIMITIVE_MAN_STATUE:  ItemData(1230395, "filler", locationName.LOC_PRIMITIVE_MAN_STATUE, 1),
    itemName.APEMAN_SCULPTURE:      ItemData(1230396, "filler", locationName.LOC_APEMAN_SCULPTURE, 1),
    itemName.FAIRY_SCULPTURE:       ItemData(1230397, "progress", locationName.LOC_FAIRY_SCULPTURE, 1),
    itemName.ELF_STATUE:            ItemData(1230398, "progress", locationName.LOC_ELF_STATUE, 1),
    itemName.ANCIENT_COIN:          ItemData(1230399, "progress", locationName.LOC_ANCIENT_COIN, 1),
    itemName.PICK_AXE:              ItemData(1230400, "progress", locationName.LOC_PICK_AXE, 1),
    itemName.RING_OF_THE_DEAD:      ItemData(1230401, "progress", locationName.LOC_RING_OF_THE_DEAD, 1),
    itemName.BLUE_RING:             ItemData(1230402, "useful", locationName.LOC_BLUE_RING, 1),
    itemName.GREEN_RING:            ItemData(1230403, "filler", locationName.LOC_GREEN_RING, 1),
    itemName.LEVER:                 ItemData(1230404, "progress", locationName.LOC_LEVER, 1),
    itemName.SLIPPER:               ItemData(1230405, "progress", locationName.LOC_SLIPPER, 1),
    itemName.DIRTY_SLIPPER:         ItemData(1230406, "progress", locationName.LOC_DIRTY_SLIPPER, 1),
    itemName.PAIR_OF_SLIPPERS:      ItemData(1230407, "progress", locationName.LOC_PAIR_OF_SLIPPERS, 1),
    #itemName.JEZIBEL_PENDANT:       ItemData(1230408, "progress", locationName.LOC_JEZIBEL_PENDANT, 1),
    #itemName.STAFF_OF_AGES:         ItemData(1230409, "progress", locationName.LOC_STAFF_OF_AGES, 1),
    itemName.ROPE:                  ItemData(1230410, "progress", locationName.LOC_ROPE, 1),
    itemName.CEMETERY_KEY:          ItemData(1230411, "progress", locationName.LOC_CEMETERY_KEY, 1),
    itemName.FLOWER:                ItemData(1230412, "progress", locationName.LOC_FLOWER, 1),
    #itemName.FLINT:                 ItemData(1230413, "progress", locationName.LOC_FLINT, 1),
    itemName.FANG:                  ItemData(1230414, "progress", locationName.LOC_FANG, 1),
    itemName.DRAGON_EYE:            ItemData(1230415, "progress", locationName.LOC_DRAGON_EYE, 1),
    itemName.DRAGON_FLUTE:          ItemData(1230416, "progress", locationName.LOC_DRAGON_FLUTE, 1),
    itemName.BURNING_CANDLE:        ItemData(1230417, "progress", locationName.LOC_BURNING_CANDLE, 1),
    itemName.CHIPPED_VIOLIN:        ItemData(1230418, "progress", locationName.LOC_CHIPPED_VIOLIN, 1),
    itemName.STRINGLESS_VIOLIN:     ItemData(1230419, "filler", locationName.LOC_STRINGLESS_VIOLIN, 1),
    itemName.BROKEN_VIOLIN:         ItemData(1230420, "filler", locationName.LOC_BROKEN_VIOLIN, 1),
    itemName.DUNGEON_KEY:           ItemData(1230421, "progress", locationName.LOC_DUNGEON_KEY, 1),
    itemName.MAP:                   ItemData(1230422, "useful", locationName.LOC_MAP, 1),
    itemName.BONE:                  ItemData(1230423, "progress", locationName.LOC_BONE, 1),
    itemName.STARCREST:             ItemData(1230424, "progress", locationName.LOC_STARCREST, 1),
    itemName.IRON_BAR:              ItemData(1230425, "progress", locationName.LOC_IRON_BAR, 1),
    itemName.CROWBAR:               ItemData(1230426, "progress", locationName.LOC_CROWBAR, 1),
    itemName.HAIR_OF_GIANT:         ItemData(1230427, "useful", locationName.LOC_HAIR_OF_GIANT, 1),
    itemName.MUG:                   ItemData(1230428, "progress", locationName.LOC_MUG, 1),
    itemName.WATER:                 ItemData(1230429, "filler", locationName.LOC_WATER, 1),
    itemName.WATER_DRAGON_TEARS:    ItemData(1230430, "progress", locationName.LOC_WATER_DRAGON_TEARS, 1),
    itemName.STONE_OF_THIRST:       ItemData(1230431, "progress", locationName.LOC_STONE_OF_THIRST, 1),
    itemName.COIN:                  ItemData(1230432, "progress", None, 4),
    itemName.NAIL:                  ItemData(1230437, "progress", locationName.LOC_NAIL, 1),
    itemName.BROOCH:                ItemData(1230438, "filler", locationName.LOC_BROOCH, 1),
    itemName.JEWELRY_BOX:           ItemData(1230439, "filler", locationName.LOC_JEWELRY_BOX, 1),
    itemName.FRUIT:                 ItemData(1230440, "filler", locationName.LOC_FRUIT, 1),
    itemName.GAUNTLET:              ItemData(1230441, "filler", locationName.LOC_GAUNTLET, 1),
    itemName.CUP:                   ItemData(1230442, "filler", locationName.LOC_CUP, 1),
    itemName.ARTWORK:               ItemData(1230443, "filler", locationName.LOC_ARTWORK, 1),
    itemName.POISONOUS_HERB:        ItemData(1230444, "filler", locationName.LOC_POISONOUS_HERB, 1),
    itemName.BRACELET:              ItemData(1230445, "filler", locationName.LOC_BRACELET, 1),
    itemName.PRECIOUS_STONE:        ItemData(1230446, "filler", locationName.LOC_PRECIOUS_STONE, 1),
    itemName.BROKEN_SWORD:          ItemData(1230447, "filler", locationName.LOC_BROKEN_SWORD, 1),
    itemName.QUILL:                 ItemData(1230448, "filler", locationName.LOC_QUILL, 1),
    itemName.PLATE:                 ItemData(1230449, "filler", locationName.LOC_PLATE, 1),
    itemName.BROKEN_LANCE:          ItemData(1230450, "filler", locationName.LOC_BROKEN_LANCE, 1),
    itemName.END_GAME_PROGRESSION:  ItemData(1230451, "progress", None, 2) #1 is autofilled. Contains Pendant, Flint, Staff
}

book_table = {
    itemName.DNARTH_CHRONICLES:      ItemData(1230455, "filler", locationName.LOC_DNARTH_CHRONICLES, 1),
    itemName.FINAL_BATTLE:           ItemData(1230456, "filler", locationName.LOC_FINAL_BATTLE, 1),
    itemName.SPEECHES_JAIR:          ItemData(1230457, "filler", locationName.LOC_SPEECHES_JAIR, 1),
    itemName.BLANK_BOOK:             ItemData(1230458, "filler", None, 3),
    itemName.STUDENT_DIARY:          ItemData(1230461, "filler", locationName.LOC_STUDENT_DIARY, 1),
    itemName.ACOLYTE_DIARY:          ItemData(1230462, "filler", locationName.LOC_ACOLYTE_DIARY, 1),
    itemName.PERSONAL_JOURNAL:       ItemData(1230463, "filler", locationName.LOC_PERSONAL_JOURNAL, 1),
    itemName.MEMOIRS:                ItemData(1230464, "filler", locationName.LOC_MEMOIRS, 1),
    itemName.NOVICE_JOURNAL:         ItemData(1230465, "filler", locationName.LOC_NOVICE_JOURNAL, 1),
    itemName.TRIALS_KINGDOM:         ItemData(1230466, "filler", locationName.LOC_TRIALS_KINGDOM, 1),
    itemName.BROTHERHOOD_REPORT:     ItemData(1230467, "filler", locationName.LOC_BROTHERHOOD_REPORT, 1),
    itemName.WRITINGS_KONNOR:        ItemData(1230468, "filler", locationName.LOC_WRITINGS_KONNOR, 1),
    itemName.HOUSE_DRESLIN:          ItemData(1230469, "filler", locationName.LOC_HOUSE_DRESLIN, 1),
    itemName.MEMORANDUM:             ItemData(1230470, "filler", locationName.LOC_MEMORANDUM, 1),
    itemName.LAST_DRAGON:            ItemData(1230471, "filler", locationName.LOC_LAST_DRAGON, 1),
    itemName.RIDING_DRAGONS:         ItemData(1230472, "filler", locationName.LOC_RIDING_DRAGONS, 1),
    itemName.RESEARCH_LOG:           ItemData(1230473, "filler", locationName.LOC_RESEARCH_LOG, 1),
    itemName.MUSINGS_LUNATIC:        ItemData(1230474, "filler", locationName.LOC_MUSINGS_LUNATIC, 1),
    itemName.ORDERS:                 ItemData(1230475, "filler", locationName.LOC_ORDERS, 1),
    itemName.LAWS_MAGIC:             ItemData(1230476, "filler", locationName.LOC_LAWS_MAGIC, 1),
    itemName.FAMILY_DIARY:           ItemData(1230477, "filler", locationName.LOC_FAMILY_DIARY, 1),
    itemName.WORDS_DNARTH:           ItemData(1230478, "filler", locationName.LOC_WORDS_DNARTH, 1),
    itemName.ARTIFACTS_POWER:        ItemData(1230479, "filler", locationName.LOC_ARTIFACTS_POWER, 1),
    itemName.MAGICAL_ELIXIRS:        ItemData(1230480, "filler", locationName.LOC_MAGICAL_ELIXIRS, 1)
}

note_table = {
    itemName.JOURNAL:                ItemData(1230484, "filler", locationName.LOC_JOURNAL, 1),
    itemName.WATCHMAN_MEMO:          ItemData(1230485, "filler", locationName.LOC_WATCHMAN_MEMO, 1),
    itemName.REPORT:                 ItemData(1230486, "filler", locationName.LOC_REPORT, 1),
    itemName.OFFICIAL_ARTICLE:       ItemData(1230487, "filler", locationName.LOC_OFFICIAL_ARTICLE, 1),
    itemName.LECTURE_NOTES:          ItemData(1230488, "filler", locationName.LOC_LECTURE_NOTES, 1),
    itemName.PERSONAL_LETTER:        ItemData(1230489, "filler", locationName.LOC_PERSONAL_LETTER, 1),
    itemName.INNER_CHAMBER:          ItemData(1230490, "filler", locationName.LOC_INNER_CHAMBER, 1),
    itemName.TRAVELOGUE:             ItemData(1230491, "filler", locationName.LOC_TRAVELOGUE, 1),
    itemName.TRAVEL_GUIDE:           ItemData(1230492, "filler", locationName.LOC_TRAVEL_GUIDE, 1),
    itemName.PETITION:               ItemData(1230493, "filler", locationName.LOC_PETITION, 1),
    itemName.RECEIPT:                ItemData(1230494, "filler", locationName.LOC_RECEIPT, 1),
    itemName.PERSONAL_NOTE:          ItemData(1230495, "filler", locationName.LOC_PERSONAL_NOTE, 1)
}


all_item_table = {
    **items_table,
    **book_table,
    **note_table
}

all_group_table = {
    "items": items_table,
    "books": book_table,
    "notes": note_table
}
