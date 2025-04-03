-- Shadowgate64 Connector Lua
-- Created by Mike Jackson (jjjj12212)

-- local RDRAMBase = 0x80000000;
-- local RDRAMSize = 0x800000;

local socket = require("socket")
local json = require('json')
local math = require('math')
require('common')

local SCRIPT_VERSION = 1
local SG_VERSION = "V0.1"
local PLAYER = ""
local SEED = 0

local SG_SOCK = nil

local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"
local PREV_STATE = ""
local CUR_STATE =  STATE_UNINITIALIZED
local FRAME = 0
local VERROR = false
local CLIENT_VERSION = false

local DEBUG = false
local AP_TIMEOUT_COUNTER = 0
local MESSAGE_TABLE = {}

local SGH
local TOTAL_COINS = 0
local TOTAL_BLANK_BOOK = 0
local PROGRESSIVE_END_GAME_ITEMS = 0

-------------- MAP VARS -------------
local CURRENT_MAP = nil;

--------------- DEATH LINK ----------------------
local DEATH_LINK_TRIGGERED = false;
local DEATH_LINK = false


local receive_map = { -- [ap_id] = item_id; --  Required for Async Items
    ["NA"] = "NA"
}

local ASSET_MAP_CHECK = {
    ["ALL"] = {
        ["ITEMS"] = {"1230407"}
    },
    [0x24] = { -- Sewer Entrance
        ["ITEMS"] = {"1230425", "1230386"}
    },
    [0x27] = { -- Flooded caves
        ["ITEMS"] = {"1230422", "1230484"}
    },
    [0x28] = { -- Cavern
        ["ITEMS"] = {"1230400"}
    },

    [0x30] = { -- Disiple Tower Storage
        ["ITEMS"] = {"1230410"}
    },
    [0x2F] = { -- Disiple Tower Ghost Dad
        ["ITEMS"] = {"1230397", "1230405", "1230431", "1230411"}
    },
    [0x36] = { -- Disiple Tower Lobby
        ["ITEMS"] = {"1230398", "1230416"}
    },
    [0x37] = { -- Disiple 2FL entrance
        ["ITEMS"] = {"1230472", "1230456", "1230459", "1230460"}
    },
    [0x38] = { --Disiple 2FL study
        ["ITEMS"] = {"1230476", "1230479", "1230485", "1230470"}
    },
    [0x3A] = { --Disiple 3FL right classroom
        ["ITEMS"] = {"1230396", "1230392", "1230486"}
    },
    [0x39] = { --Disiple 3FL mid classroom
        ["ITEMS"] = {"1230457", "1230395", "1230475", "1230488", "1230399"}
    },
    [0x3D] = { --Disiple 4FL Student Room 1
        ["ITEMS"] = {"1230461", "1230489", "1230469", "1230495"}
    },
    [0x3E] = { --Disiple 4FL Student Room 2
        ["ITEMS"] = {"1230458", "1230385"}
    },

    [0x0E] = { -- Cathedral Basement
        ["ITEMS"] = {"1230437", "1230384"}
    },
    [0x0D] = { -- Cathedral Basement
        ["ITEMS"] = {"1230391", "1230388", "1230426"}
    },
    [0x0C] = { -- Chathedral Coffin Room
        ["ITEMS"] = {"1230477", "1230408"}
    },
    [0x4F] = { -- Lakmir Tower 2F Kitchen
        ["ITEMS"] = {"1230382", "1230429", "1230430"}
    },
    [0x4C] = {
        ["ITEMS"] = {"1230424"}
    },
    [0x48] = { -- Lakmir Tower 1F Office Right 
        ["ITEMS"] = {"1230387", "1230480", "1230428", "1230487"}
    },
    [0x49] = { -- Lakmir Tower 1F Office Left 
        ["ITEMS"] = {"1230462", "1230427", "1230494"}
    },
    [0x57] = { -- Lakmir Tower 4F Machine Room 
        ["ITEMS"] = {"1230381", "1230394", "1230463"}
    },
    [0x58] = { -- Lakmir Tower 4F Bedroom 
        ["ITEMS"] = {"1230393", "1230448", "1230464", "1230490"}
    },
    [0x59] = { -- Lakmir Tower 4F Ring Room 
        ["ITEMS"] = {"1230403", "1230402", "1230401"}
    },
    [0x44] = { -- Lakmir Tower BF Elevator Room 
        ["ITEMS"] = {"1230424"}
    },

    [0x02] = { -- Thief Hideout 1F Left
        ["ITEMS"] = {"1230450", "1230447"}
    },
    [0x07] = { -- Thief Hideout 2F Left
        ["ITEMS"] = {"1230412", "1230455"}
    },
    [0x09] = { -- Thief Hideout 2F Storage
        ["ITEMS"] = {"1230493", "1230445", "1230446", "1230449"}
    },
    [0x05] = { -- Keepers Room
        ["ITEMS"] = {"1230421"}
    },
    [0x11] = { -- Rusty Inn
        ["ITEMS"] = {"1230390"}
    }, 
    [0x12] = { -- Rusty Inn Upstairs
        ["ITEMS"] = {"1230491", "1230492"}
    },
    [0x13] = { -- Shoppe
        ["ITEMS"] = {"1230438", "1230439", "1230440", "1230441", "1230442", "1230418", "1230419", "1230420"}
    },
    [0x14] = { -- Path to Park
        ["ITEMS"] = {"1230444", "1230433"}
    },
    [0x15] = { -- Park
        ["ITEMS"] = {"1230432"}
    },
    [0x17] = { -- Guardroom
        ["ITEMS"] = {"1230435"}
    },
    [0x1B] = { -- Excavation Area 1
        ["ITEMS"] = {"1230406"}
    },
    [0x1D] = { -- Rastolin Upstairs
        ["ITEMS"] = {"1230443", "1230474"}
    },
    [0x1F] = { -- Aagar's Room
        ["ITEMS"] = {"1230413", "1230473", "1230414", "1230404"}
    },
    [0x20] = { -- Excavation Area 2
        ["ITEMS"] = {"1230434"}
    },

    [0x5B] = { -- Trial Tower Basement Small Room
        ["ITEMS"] = {"1230465"}
    },
    [0x5C] = { -- Trial Tower Basement Study Room
        ["ITEMS"] = {"1230468", "1230467", "1230466"}
    },
    [0x5F] = { -- Trial Tower Crest Puzzle room
        ["ITEMS"] = {"1230383"}
    },
    [0x65] = { -- Trial Tower 2F Maze Starting room
        ["ITEMS"] = {"1230417"}
    },
    [0x6A] = { -- Trial Tower 4F ring room
        ["ITEMS"] = {"1230389"}
    },

    [0x6C] = { -- Dragon Tower Basement
        ["ITEMS"] = {"1230415"}
    },
    [0x6E] = { -- Dragon Tower 1F room
        ["ITEMS"] = {"1230471"}
    },
    [0x70] = { -- Dragon Tower 2F room
        ["ITEMS"] = {"1230478"}
    },
    [0x71] = { -- Dragon Tower Roof
    ["ITEMS"] = {"1230409"}
},
}

local ITEM_TABLE = {}; -- reverses ROM_ITEM so the key is the Item
local ROM_ITEM_TABLE = {
    "AP_ITEM_CREST_KEY",
    "AP_ITEM_BOTTLE_OF_OIL",
    "AP_ITEM_FRAGMENTS_OF_CREST",
    "AP_ITEM_DRAGON_TEARS",
    "AP_ITEM_PIXIE_FLUTE",
    "AP_ITEM_TREASURE",
    "AP_ITEM_RUSTY_KEY",
    "AP_ITEM_ORNATE_KEY",
    "AP_ITEM_RING_OF_THE_KINGDOM",
    "AP_ITEM_ORB",
    "AP_ITEM_GOLDEN_KEY",
    "AP_ITEM_LIQUID_SUNSET",
    "AP_ITEM_NIGHT_ELIXIR",
    "AP_ITEM_FOREST_NECTAR",
    "AP_ITEM_PRIMITIVE_MAN_STATUE",
    "AP_ITEM_APEMAN_SCULPTURE",
    "AP_ITEM_FAIRY_SCULPTURE",
    "AP_ITEM_ELF_STATUE",
    "AP_ITEM_ANCIENT_COIN",
    "AP_ITEM_PICK_AXE",
    "AP_ITEM_RING_OF_THE_DEAD",
    "AP_ITEM_BLUE_RING",
    "AP_ITEM_GREEN_RING",
    "AP_ITEM_LEVER",
    "AP_ITEM_SLIPPER",
    "AP_ITEM_DIRTY_SLIPPER",
    "AP_ITEM_PAIR_OF_SLIPPERS",
    "AP_ITEM_JEZIBEL_PENDANT",
    "AP_ITEM_STAFF_OF_AGES",
    "AP_ITEM_ROPE",
    "AP_ITEM_CEMETERY_KEY",
    "AP_ITEM_FLOWER",
    "AP_ITEM_FLINT",
    "AP_ITEM_FANG",
    "AP_ITEM_DRAGON_EYE",
    "AP_ITEM_DRAGON_FLUTE",
    "AP_ITEM_BURNING_CANDLE",
    "AP_ITEM_CHIPPED_VIOLIN",
    "AP_ITEM_STRINGLESS_VIOLIN",
    "AP_ITEM_BROKEN_VIOLIN",
    "AP_ITEM_DUNGEON_KEY",
    "AP_ITEM_MAP",
    "AP_ITEM_BONE",
    "AP_ITEM_STARCREST",
    "AP_ITEM_IRON_BAR",
    "AP_ITEM_CROWBAR",
    "AP_ITEM_HAIR_OF_GIANT",
    "AP_ITEM_MUG",
    "AP_ITEM_WATER",
    "AP_ITEM_WATER_DRAGON_TEARS",
    "AP_ITEM_STONE_OF_THIRST",
    "AP_ITEM_COIN1",
    "AP_ITEM_COIN2",
    "AP_ITEM_COIN3",
    "AP_ITEM_COIN4",
    "AP_ITEM_COIN5",
    "AP_ITEM_NAIL",
    "AP_ITEM_BROOCH",
    "AP_ITEM_JEWELRY_BOX",
    "AP_ITEM_FRUIT",
    "AP_ITEM_GAUNTLET",
    "AP_ITEM_CUP",
    "AP_ITEM_ARTWORK",
    "AP_ITEM_POISONOUS_HERB",
    "AP_ITEM_BRACELET",
    "AP_ITEM_PRECIOUS_STONE",
    "AP_ITEM_BROKEN_SWORD",
    "AP_ITEM_QUILL",
    "AP_ITEM_PLATE",
    "AP_ITEM_BROKEN_LANCE",
    "AP_ITEM_MAX",
    "AP_ITEM_UNKOWN72",
    "AP_ITEM_UNKOWN73",
    "AP_ITEM_UNKOWN74",
    "AP_ITEM_DNARTH_CHRONICLES",
    "AP_ITEM_FINAL_BATTLE",
    "AP_ITEM_SPEECHES_JAIR",
    "AP_ITEM_BLANK_BOOK",
    "AP_ITEM_BLANK_BOOK2",
    "AP_ITEM_BLANK_BOOK3",
    "AP_ITEM_STUDENT_DIARY",
    "AP_ITEM_ACOLYTE_DIARY",
    "AP_ITEM_PERSONAL_JOURNAL",
    "AP_ITEM_MEMOIRS",
    "AP_ITEM_NOVICE_JOURNAL",
    "AP_ITEM_TRIALS_KINGDOM",
    "AP_ITEM_BROTHERHOOD_REPORT",
    "AP_ITEM_WRITINGS_KONNOR",
    "AP_ITEM_HOUSE_DRESLIN",
    "AP_ITEM_MEMORANDUM",
    "AP_ITEM_LAST_DRAGON",
    "AP_ITEM_RIDING_DRAGONS",
    "AP_ITEM_RESEARCH_LOG",
    "AP_ITEM_MUSINGS_LUNATIC",
    "AP_ITEM_ORDERS",
    "AP_ITEM_LAWS_MAGIC",
    "AP_ITEM_FAMILY_DIARY",
    "AP_ITEM_WORDS_DNARTH",
    "AP_ITEM_ARTIFACTS_POWER",
    "AP_ITEM_MAGICAL_ELIXIRS",
    "AP_ITEM_BOOK_MAX",
    "AP_ITEM_BOOK_UNKOWN27",
    "AP_ITEM_BOOK_UNKOWN28",
    "AP_ITEM_JOURNAL",
    "AP_ITEM_WATCHMAN_MEMO",
    "AP_ITEM_REPORT",
    "AP_ITEM_OFFICIAL_ARTICLE",
    "AP_ITEM_LECTURE_NOTES",
    "AP_ITEM_PERSONAL_LETTER",
    "AP_ITEM_INNER_CHAMBER",
    "AP_ITEM_TRAVELOGUE",
    "AP_ITEM_TRAVEL_GUIDE",
    "AP_ITEM_PETITION",
    "AP_ITEM_RECEIPT",
    "AP_ITEM_PERSONAL_NOTE",
    "AP_ITEM_BOOK_42",
    "AP_ITEM_BOOK_43",
    "AP_ITEM_BOOK_44",
    "AP_ITEM_NOTE_MAX"
};


-- Address Map for Shadowgate64
local ADDRESS_MAP = {
    ["ITEMS"] = {
        ["1230381"] = { ["addr"] = 0x01, ["name"] = "Crest Key"}, -- DONE
        ["1230382"] = { ["addr"] = 0x02, ["name"] = "Bottle of Oil"}, -- DONE
        ["1230383"] = { ["addr"] = 0x03, ["name"] = "Fragments of Crest"}, -- DONE
        ["1230384"] = { ["addr"] = 0x04, ["name"] = "Dragon Tears"}, -- DONE
        ["1230385"] = { ["addr"] = 0x05, ["name"] = "Pixie Flute"}, -- DONE
        ["1230386"] = { ["addr"] = 0x06, ["name"] = "Treasure"}, --DONE
        ["1230387"] = { ["addr"] = 0x07, ["name"] = "Rusty Key"}, -- DONE
        ["1230388"] = { ["addr"] = 0x08, ["name"] = "Ornate Key"}, -- DONE
        ["1230389"] = { ["addr"] = 0x09, ["name"] = "Ring of the Kingdom"}, -- DONE
        ["1230390"] = { ["addr"] = 0x0A, ["name"] = "Magical Orb"}, -- DONE
        ["1230391"] = { ["addr"] = 0x0B, ["name"] = "Golden Key"}, -- DONE
        ["1230392"] = { ["addr"] = 0x0C, ["name"] = "Liquid Sunset"}, -- DONE
        ["1230393"] = { ["addr"] = 0x0D, ["name"] = "Night Elixir"}, -- DONE
        ["1230394"] = { ["addr"] = 0x0E, ["name"] = "Forest Nectar"}, -- DONE
        ["1230395"] = { ["addr"] = 0x0F, ["name"] = "Primitive Man Statue"}, -- DONE
        ["1230396"] = { ["addr"] = 0x10, ["name"] = "Apeman Sculpture"}, -- DONE
        ["1230397"] = { ["addr"] = 0x11, ["name"] = "Fairy Sculpture"}, -- DONE
        ["1230398"] = { ["addr"] = 0x12, ["name"] = "Elf Statue"}, -- DONE
        ["1230399"] = { ["addr"] = 0x13, ["name"] = "Ancient Coin"}, -- DONE
        ["1230400"] = { ["addr"] = 0x14, ["name"] = "Pickaxe"}, -- DONE
        ["1230401"] = { ["addr"] = 0x15, ["name"] = "Ring of the Dead"}, -- DONE
        ["1230402"] = { ["addr"] = 0x16, ["name"] = "Blue Ring"}, -- DONE
        ["1230403"] = { ["addr"] = 0x17, ["name"] = "Green Ring"}, -- DONE
        ["1230404"] = { ["addr"] = 0x18, ["name"] = "Lever"}, -- DONE
        ["1230405"] = { ["addr"] = 0x19, ["name"] = "Slipper"}, -- DONE
        ["1230406"] = { ["addr"] = 0x1A, ["name"] = "Dirty Slipper"}, -- DONE
        ["1230407"] = { ["addr"] = 0x1B, ["name"] = "Pair of Slippers"}, -- DONE
        ["1230408"] = { ["addr"] = 0x1C, ["name"] = "Jezibel Pendant"}, -- DONE
        ["1230409"] = { ["addr"] = 0x1D, ["name"] = "Staff of Ages"}, -- DONE
        ["1230410"] = { ["addr"] = 0x1E, ["name"] = "Rope"}, -- DONE
        ["1230411"] = { ["addr"] = 0x1F, ["name"] = "Cemetery Key"}, -- DONE
        ["1230412"] = { ["addr"] = 0x20, ["name"] = "Flower"}, -- DONE
        ["1230413"] = { ["addr"] = 0x21, ["name"] = "Flint"}, -- DONE
        ["1230414"] = { ["addr"] = 0x22, ["name"] = "Fang" }, -- DONE
        ["1230415"] = { ["addr"] = 0x23, ["name"] = "Dragon Eye"}, -- DONE
        ["1230416"] = { ["addr"] = 0x24, ["name"] = "Dragon Flute"}, -- DONE
        ["1230417"] = { ["addr"] = 0x25, ["name"] = "Burning Candle"}, -- DONE
        ["1230418"] = { ["addr"] = 0x26, ["name"] = "Chipped Violin"}, -- DONE
        ["1230419"] = { ["addr"] = 0x27, ["name"] = "Stringless Violin"}, -- DONE
        ["1230420"] = { ["addr"] = 0x28, ["name"] = "Broken Violin"}, -- DONE
        ["1230421"] = { ["addr"] = 0x29, ["name"] = "Dungeon Key"}, -- DONE
        ["1230422"] = { ["addr"] = 0x2A, ["name"] = "Map"}, --DONE
        ["1230424"] = { ["addr"] = 0x2C, ["name"] = "Starcrest"}, -- DONE
        ["1230425"] = { ["addr"] = 0x2D, ["name"] = "Iron Bar"}, --DONE
        ["1230426"] = { ["addr"] = 0x2E, ["name"] = "Crowbar"}, -- DONE
        ["1230427"] = { ["addr"] = 0x2F, ["name"] = "Hair of Giant"}, -- DONE
        ["1230428"] = { ["addr"] = 0x30, ["name"] = "Mug"}, -- DONE
        ["1230429"] = { ["addr"] = 0x31, ["name"] = "Water"}, -- DONE
        ["1230430"] = { ["addr"] = 0x32, ["name"] = "Water with Dragon Tears"}, -- DONE
        ["1230431"] = { ["addr"] = 0x33, ["name"] = "Stone of Thirst"}, -- DONE
        ["1230432"] = { ["addr"] = 0x34, ["name"] = "Coin1"}, -- DONE Park
        ["1230433"] = { ["addr"] = 0x35, ["name"] = "Coin2"}, -- DONE Path to Park
        ["1230434"] = { ["addr"] = 0x36, ["name"] = "Coin3"}, -- DONE Exacav 2
        ["1230435"] = { ["addr"] = 0x37, ["name"] = "Coin4"}, -- DONE Guardroom
        ["1230437"] = { ["addr"] = 0x39, ["name"] = "Nail"}, -- DONE
        ["1230438"] = { ["addr"] = 0x3A, ["name"] = "Brooch"}, -- DONE
        ["1230439"] = { ["addr"] = 0x3B, ["name"] = "Jewelry Box"}, -- DONE
        ["1230440"] = { ["addr"] = 0x3C, ["name"] = "Fruit"}, -- DONE
        ["1230441"] = { ["addr"] = 0x3D, ["name"] = "Gauntlet"}, -- DONE
        ["1230442"] = { ["addr"] = 0x3E, ["name"] = "Cup"}, -- DONE
        ["1230443"] = { ["addr"] = 0x3F, ["name"] = "Artwork"}, -- DONE
        ["1230444"] = { ["addr"] = 0x40, ["name"] = "Poisonous Herb"}, -- DONE
        ["1230445"] = { ["addr"] = 0x41, ["name"] = "Bracelet"}, -- DONE
        ["1230446"] = { ["addr"] = 0x42, ["name"] = "Precious Stone"}, -- DONE
        ["1230447"] = { ["addr"] = 0x43, ["name"] = "Broken Sword"}, -- DONE
        ["1230448"] = { ["addr"] = 0x44, ["name"] = "Quill"}, -- DONE
        ["1230449"] = { ["addr"] = 0x45, ["name"] = "Plate"}, -- DONE
        ["1230450"] = { ["addr"] = 0x46, ["name"] = "Broken Lance"}, -- DONE

        ["1230455"] = { ["addr"] = 0x4B, ["name"] = "D'Narth Family Chronicles"}, -- DONE
        ["1230456"] = { ["addr"] = 0x4C, ["name"] = "The Final Battle"}, -- DONE
        ["1230457"] = { ["addr"] = 0x4D, ["name"] = "The Speeches of Jair"}, -- DONE
        ["1230458"] = { ["addr"] = 0x4E, ["name"] = "Blank Book 1"}, -- DONE RED in STUDENT ROOM
        ["1230459"] = { ["addr"] = 0x4F, ["name"] = "Blank Book 2"}, -- DONE GREEN
        ["1230460"] = { ["addr"] = 0x50, ["name"] = "Blank Book 3"}, -- DONE BLUE
        ["1230461"] = { ["addr"] = 0x51, ["name"] = "Student's Diary"}, -- DONE
        ["1230462"] = { ["addr"] = 0x52, ["name"] = "Acolyte's Diary"}, -- DONE
        ["1230463"] = { ["addr"] = 0x53, ["name"] = "Personal Journal"}, -- DONE
        ["1230464"] = { ["addr"] = 0x54, ["name"] = "Memoirs"}, -- DONE
        ["1230465"] = { ["addr"] = 0x55, ["name"] = "Novice Journal"}, -- DONE
        ["1230466"] = { ["addr"] = 0x56, ["name"] = "The Trials of the Kingdom"}, -- DONE
        ["1230467"] = { ["addr"] = 0x57, ["name"] = "The Brotherhood Report"}, -- DONE
        ["1230468"] = { ["addr"] = 0x58, ["name"] = "The Writings of Konnor"}, -- DONE
        ["1230469"] = { ["addr"] = 0x59, ["name"] = "The House of Dreslin"}, -- DONE
        ["1230470"] = { ["addr"] = 0x5A, ["name"] = "Memorandum"}, -- DONE
        ["1230471"] = { ["addr"] = 0x5B, ["name"] = "The Last Dragon"}, -- DONE
        ["1230472"] = { ["addr"] = 0x5C, ["name"] = "Of Riding Dragons"}, -- DONE
        ["1230473"] = { ["addr"] = 0x5D, ["name"] = "Research Log"}, -- DONE
        ["1230474"] = { ["addr"] = 0x5E, ["name"] = "Musings of a Lunatic"}, -- DONE
        ["1230475"] = { ["addr"] = 0x5F, ["name"] = "The Book of Orders"}, -- DONE
        ["1230476"] = { ["addr"] = 0x60, ["name"] = "Laws of Magic"}, -- DONE
        ["1230477"] = { ["addr"] = 0x61, ["name"] = "Family Diary"}, -- DONE
        ["1230478"] = { ["addr"] = 0x62, ["name"] = "Words of D'narth"}, -- DONE
        ["1230479"] = { ["addr"] = 0x63, ["name"] = "Artifacts of Power"}, -- DONE
        ["1230480"] = { ["addr"] = 0x64, ["name"] = "Magical Elixirs"}, -- DONE

        ["1230484"] = { ["addr"] = 0x68, ["name"] = "Journal"}, --DONE
        ["1230485"] = { ["addr"] = 0x69, ["name"] = "Watchman's Memo"}, --DONE
        ["1230486"] = { ["addr"] = 0x6A, ["name"] = "Report"}, --DONE
        ["1230487"] = { ["addr"] = 0x6B, ["name"] = "Official's Article"}, -- DONE
        ["1230488"] = { ["addr"] = 0x6C, ["name"] = "Lecture Notes"}, -- DONE
        ["1230489"] = { ["addr"] = 0x6D, ["name"] = "Personal Letter"}, -- DONE
        ["1230490"] = { ["addr"] = 0x6E, ["name"] = "The Inner Chamber"}, -- DONE
        ["1230491"] = { ["addr"] = 0x6F, ["name"] = "Travelogue"}, -- DONE
        ["1230492"] = { ["addr"] = 0x70, ["name"] = "Travel Guide"}, -- DONE
        ["1230493"] = { ["addr"] = 0x71, ["name"] = "Petition"}, -- DONE
        ["1230494"] = { ["addr"] = 0x72, ["name"] = "Receipt"}, -- DONE
        ["1230495"] = { ["addr"] = 0x73, ["name"] = "Personal Note"}, -- DONE
    }
}

SGHACK = {
    RDRAMBase = 0x80000000,
    RDRAMSize = 0x800000,
    base_index = 0x400000,
        version = 0x0,
    check_locations = 0x4020E8, -- ap_memory_ptrs
        n64_text_queue = 0x77,
        n64_text_ready = 0x78,
    starting_address = 0x402168, --ap_memory
        items = 0x0,
        message = 0x77,
        item_message = 0x177,
        text_queue = 0x178,
        setting_opendoor = 0x179,
    txt_queue = 0
}

function SGHACK:new(t)
    t = t or {}
    setmetatable(t, self)
    self.__index = self
   return self
end

function SGHACK:setItem(index)
    mainmemory.writebyte(index + (self.starting_address + self.items), 1);
end

function SGHACK:setTextQueue()
    -- self.txt_queue = self.txt_queue + 1
    mainmemory.writebyte(self.text_queue + self.starting_address, self.txt_queue);
end

function SGHACK:setSettingDoor()
    mainmemory.writebyte(self.setting_opendoor + self.starting_address, 1);
end

function SGHACK:getCurrentMap()
    return mainmemory.read_u16_be(0x0E7A72);
end

function SGHACK:getPCQueue()
    return self.txt_queue
end

function SGHACK:setPCQueue()
    local n64_queue = mainmemory.readbyte(self.n64_text_queue + self.starting_address);
    self.txt_queue = n64_queue
    mainmemory.writebyte(self.text_queue + self.starting_address, self.txt_queue);
end

function SGHACK:getCurrentQueue()
    return mainmemory.readbyte(self.n64_text_queue + self.check_locations);
end

function SGHACK:getCheckLocation(item)
    local addr = mainmemory.readbyte(self.check_locations + item);
    if addr == 1
    then
        return true
    else
        return false
    end
end

function SGHACK:setDialog(message, item)
    self.txt_queue = self.txt_queue + 1;
    local overflow = false
    local last_char = 0
    for idx = 0, string.len(message)-1 do
        if idx == 256
        then
            overflow = true
            mainmemory.writebyte((self.starting_address + self.message ) + idx, 0x0B);
            break;
        end
        last_char = last_char + 1;
        mainmemory.writebyte((self.starting_address + self.message ) + idx, message:byte(idx + 1));
    end
    if overflow == false
    then
        mainmemory.writebyte((self.starting_address + self.message ) + last_char, 0x0B);
        mainmemory.writebyte((self.starting_address + self.message ) + last_char + 1, 0x00);
    end
    mainmemory.writebyte((self.starting_address + self.item_message), item);
    -- mainmemory.writebyte((self.starting_address + self.text_queue), txt_queue);
    self:setTextQueue()
end

function obtain_AP_Item(item_id)
    if DEBUG == true
    then
        print("Item Obtained")
    end
    if item_id == 1230381
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_CREST_KEY"])
    elseif item_id == 1230382
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_BOTTLE_OF_OIL"])
    elseif item_id == 1230383
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_FRAGMENTS_OF_CREST"])
    elseif item_id == 1230384
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_DRAGON_TEARS"])
    elseif item_id == 1230385
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_PIXIE_FLUTE"])
    elseif item_id == 1230386
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_TREASURE"])
    elseif item_id == 1230387
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_RUSTY_KEY"])
    elseif item_id == 1230388
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_ORNATE_KEY"])
    elseif item_id == 1230389
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_RING_OF_THE_KINGDOM"])
    elseif item_id == 1230390
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_ORB"])
    elseif item_id == 1230391
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_GOLDEN_KEY"])
    elseif item_id == 1230392
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_LIQUID_SUNSET"])
    elseif item_id == 1230393
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_NIGHT_ELIXIR"])
    elseif item_id == 1230394
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_FOREST_NECTAR"])
    elseif item_id == 1230395
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_PRIMITIVE_MAN_STATUE"])
    elseif item_id == 1230396
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_APEMAN_SCULPTURE"])
    elseif item_id == 1230397
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_FAIRY_SCULPTURE"])
    elseif item_id == 1230398
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_ELF_STATUE"])
    elseif item_id == 1230399
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_ANCIENT_COIN"])
    elseif item_id == 1230400
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_PICK_AXE"])
    elseif item_id == 1230401
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_RING_OF_THE_DEAD"])
    elseif item_id == 1230402
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_BLUE_RING"])
    elseif item_id == 1230403
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_GREEN_RING"])
    elseif item_id == 1230404
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_LEVER"])
    elseif item_id == 1230405
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_SLIPPER"])
    elseif item_id == 1230406
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_DIRTY_SLIPPER"])
    elseif item_id == 1230407
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_PAIR_OF_SLIPPERS"])
    elseif item_id == 1230408
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_JEZIBEL_PENDANT"])
    elseif item_id == 1230409
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_STAFF_OF_AGES"])
    elseif item_id == 1230410
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_ROPE"])
    elseif item_id == 1230411
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_CEMETERY_KEY"])
    elseif item_id == 1230412
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_FLOWER"])
    elseif item_id == 1230413
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_FLINT"])
    elseif item_id == 1230414
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_FANG"])
    elseif item_id == 1230415
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_DRAGON_EYE"])
    elseif item_id == 1230416
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_DRAGON_FLUTE"])
    elseif item_id == 1230417
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_BURNING_CANDLE"])
    elseif item_id == 1230418
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_CHIPPED_VIOLIN"])
    elseif item_id == 1230419
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_STRINGLESS_VIOLIN"])
    elseif item_id == 1230420
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_BROKEN_VIOLIN"])
    elseif item_id == 1230421
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_DUNGEON_KEY"])
    elseif item_id == 1230422
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_MAP"])
    elseif item_id == 1230423
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_BONE"])
    elseif item_id == 1230424
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_STARCREST"])
    elseif item_id == 1230425
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_IRON_BAR"])
    elseif item_id == 1230426
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_CROWBAR"])
    elseif item_id == 1230427
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_HAIR_OF_GIANT"])
    elseif item_id == 1230428
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_MUG"])
    elseif item_id == 1230429
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_WATER"])
    elseif item_id == 1230430
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_WATER_DRAGON_TEARS"])
    elseif item_id == 1230431
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_STONE_OF_THIRST"])
    elseif item_id == 1230432
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_COIN1"] + TOTAL_COINS)
        TOTAL_COINS = TOTAL_COINS + 1
    elseif item_id == 1230437
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_NAIL"])
    elseif item_id == 1230438
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_BROOCH"])
    elseif item_id == 1230439
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_JEWELRY_BOX"])
    elseif item_id == 1230440
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_FRUIT"])
    elseif item_id == 1230441
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_GAUNTLET"])
    elseif item_id == 1230442
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_CUP"])
    elseif item_id == 1230443
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_ARTWORK"])
    elseif item_id == 1230444
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_POISONOUS_HERB"])
    elseif item_id == 1230445
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_BRACELET"])
    elseif item_id == 1230446
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_PRECIOUS_STONE"])
    elseif item_id == 1230447
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_BROKEN_SWORD"])
    elseif item_id == 1230448
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_QUILL"])
    elseif item_id == 1230449
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_PLATE"])
    elseif item_id == 1230450
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_BROKEN_LANCE"])
    elseif item_id == 1230451
    then
        if PROGRESSIVE_END_GAME_ITEMS == 0
        then
            SGHACK:setItem(ITEM_TABLE["AP_ITEM_JEZIBEL_PENDANT"])
        elseif PROGRESSIVE_END_GAME_ITEMS == 1
        then
            SGHACK:setItem(ITEM_TABLE["AP_ITEM_FLINT"])
        elseif PROGRESSIVE_END_GAME_ITEMS == 2
        then
            SGHACK:setItem(ITEM_TABLE["AP_ITEM_STAFF_OF_AGES"])
        end
        PROGRESSIVE_END_GAME_ITEMS = PROGRESSIVE_END_GAME_ITEMS + 1
    elseif item_id == 1230455
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_DNARTH_CHRONICLES"])
    elseif item_id == 1230456
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_FINAL_BATTLE"])
    elseif item_id == 1230457
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_SPEECHES_JAIR"])
    elseif item_id == 1230458
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_BLANK_BOOK"] + TOTAL_BLANK_BOOK)
        TOTAL_BLANK_BOOK = TOTAL_BLANK_BOOK + 1
    elseif item_id == 1230461
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_STUDENT_DIARY"])
    elseif item_id == 1230462
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_ACOLYTE_DIARY"])
    elseif item_id == 1230463
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_PERSONAL_JOURNAL"])
    elseif item_id == 1230464
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_MEMOIRS"])
    elseif item_id == 1230465
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_NOVICE_JOURNAL"])
    elseif item_id == 1230466
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_TRIALS_KINGDOM"])
    elseif item_id == 1230467
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_BROTHERHOOD_REPORT"])
    elseif item_id == 1230468
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_WRITINGS_KONNOR"])
    elseif item_id == 1230469
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_HOUSE_DRESLIN"])
    elseif item_id == 1230470
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_MEMORANDUM"])
    elseif item_id == 1230471
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_LAST_DRAGON"])
    elseif item_id == 1230472
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_RIDING_DRAGONS"])
    elseif item_id == 1230473
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_RESEARCH_LOG"])
    elseif item_id == 1230474
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_MUSINGS_LUNATIC"])
    elseif item_id == 1230475
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_ORDERS"])
    elseif item_id == 1230476
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_LAWS_MAGIC"])
    elseif item_id == 1230477
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_FAMILY_DIARY"])
    elseif item_id == 1230478
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_WORDS_DNARTH"])
    elseif item_id == 1230479
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_ARTIFACTS_POWER"])
    elseif item_id == 1230480
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_MAGICAL_ELIXIRS"])
    elseif item_id == 1230484
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_JOURNAL"])
    elseif item_id == 1230485
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_WATCHMAN_MEMO"])
    elseif item_id == 1230486
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_REPORT"])
    elseif item_id == 1230487
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_OFFICIAL_ARTICLE"])
    elseif item_id == 1230488
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_LECTURE_NOTES"])
    elseif item_id == 1230489
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_PERSONAL_LETTER"])
    elseif item_id == 1230490
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_INNER_CHAMBER"])
    elseif item_id == 1230491
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_TRAVELOGUE"])
    elseif item_id == 1230492
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_TRAVEL_GUIDE"])
    elseif item_id == 1230493
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_PETITION"])
    elseif item_id == 1230494
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_RECEIPT"])
    elseif item_id == 1230495
    then
        SGHACK:setItem(ITEM_TABLE["AP_ITEM_PERSONAL_NOTE"])
    end

end

function convertItemtoHex(item_id)
    if item_id == 1230381
    then
        return ITEM_TABLE["AP_ITEM_CREST_KEY"]
    elseif item_id == 1230382
    then
        return ITEM_TABLE["AP_ITEM_BOTTLE_OF_OIL"]
    elseif item_id == 1230383
    then
        return ITEM_TABLE["AP_ITEM_FRAGMENTS_OF_CREST"]
    elseif item_id == 1230384
    then
        return ITEM_TABLE["AP_ITEM_DRAGON_TEARS"]
    elseif item_id == 1230385
    then
        return ITEM_TABLE["AP_ITEM_PIXIE_FLUTE"]
    elseif item_id == 1230386
    then
        return ITEM_TABLE["AP_ITEM_TREASURE"]
    elseif item_id == 1230387
    then
        return ITEM_TABLE["AP_ITEM_RUSTY_KEY"]
    elseif item_id == 1230388
    then
        return ITEM_TABLE["AP_ITEM_ORNATE_KEY"]
    elseif item_id == 1230389
    then
        return ITEM_TABLE["AP_ITEM_RING_OF_THE_KINGDOM"]
    elseif item_id == 1230390
    then
        return ITEM_TABLE["AP_ITEM_ORB"]
    elseif item_id == 1230391
    then
        return ITEM_TABLE["AP_ITEM_GOLDEN_KEY"]
    elseif item_id == 1230392
    then
        return ITEM_TABLE["AP_ITEM_LIQUID_SUNSET"]
    elseif item_id == 1230393
    then
        return ITEM_TABLE["AP_ITEM_NIGHT_ELIXIR"]
    elseif item_id == 1230394
    then
        return ITEM_TABLE["AP_ITEM_FOREST_NECTAR"]
    elseif item_id == 1230395
    then
        return ITEM_TABLE["AP_ITEM_PRIMITIVE_MAN_STATUE"]
    elseif item_id == 1230396
    then
        return ITEM_TABLE["AP_ITEM_APEMAN_SCULPTURE"]
    elseif item_id == 1230397
    then
        return ITEM_TABLE["AP_ITEM_FAIRY_SCULPTURE"]
    elseif item_id == 1230398
    then
        return ITEM_TABLE["AP_ITEM_ELF_STATUE"]
    elseif item_id == 1230399
    then
        return ITEM_TABLE["AP_ITEM_ANCIENT_COIN"]
    elseif item_id == 1230400
    then
        return ITEM_TABLE["AP_ITEM_PICK_AXE"]
    elseif item_id == 1230401
    then
        return ITEM_TABLE["AP_ITEM_RING_OF_THE_DEAD"]
    elseif item_id == 1230402
    then
        return ITEM_TABLE["AP_ITEM_BLUE_RING"]
    elseif item_id == 1230403
    then
        return ITEM_TABLE["AP_ITEM_GREEN_RING"]
    elseif item_id == 1230404
    then
        return ITEM_TABLE["AP_ITEM_LEVER"]
    elseif item_id == 1230405
    then
        return ITEM_TABLE["AP_ITEM_SLIPPER"]
    elseif item_id == 1230406
    then
        return ITEM_TABLE["AP_ITEM_DIRTY_SLIPPER"]
    elseif item_id == 1230407
    then
        return ITEM_TABLE["AP_ITEM_PAIR_OF_SLIPPERS"]
    elseif item_id == 1230408
    then
        return ITEM_TABLE["AP_ITEM_JEZIBEL_PENDANT"]
    elseif item_id == 1230409
    then
        return ITEM_TABLE["AP_ITEM_STAFF_OF_AGES"]
    elseif item_id == 1230410
    then
        return ITEM_TABLE["AP_ITEM_ROPE"]
    elseif item_id == 1230411
    then
        return ITEM_TABLE["AP_ITEM_CEMETERY_KEY"]
    elseif item_id == 1230412
    then
        return ITEM_TABLE["AP_ITEM_FLOWER"]
    elseif item_id == 1230413
    then
        return ITEM_TABLE["AP_ITEM_FLINT"]
    elseif item_id == 1230414
    then
        return ITEM_TABLE["AP_ITEM_FANG"]
    elseif item_id == 1230415
    then
        return ITEM_TABLE["AP_ITEM_DRAGON_EYE"]
    elseif item_id == 1230416
    then
        return ITEM_TABLE["AP_ITEM_DRAGON_FLUTE"]
    elseif item_id == 1230417
    then
        return ITEM_TABLE["AP_ITEM_BURNING_CANDLE"]
    elseif item_id == 1230418
    then
        return ITEM_TABLE["AP_ITEM_CHIPPED_VIOLIN"]
    elseif item_id == 1230419
    then
        return ITEM_TABLE["AP_ITEM_STRINGLESS_VIOLIN"]
    elseif item_id == 1230420
    then
        return ITEM_TABLE["AP_ITEM_BROKEN_VIOLIN"]
    elseif item_id == 1230421
    then
        return ITEM_TABLE["AP_ITEM_DUNGEON_KEY"]
    elseif item_id == 1230422
    then
        return ITEM_TABLE["AP_ITEM_MAP"]
    elseif item_id == 1230423
    then
        return ITEM_TABLE["AP_ITEM_BONE"]
    elseif item_id == 1230424
    then
        return ITEM_TABLE["AP_ITEM_STARCREST"]
    elseif item_id == 1230425
    then
        return ITEM_TABLE["AP_ITEM_IRON_BAR"]
    elseif item_id == 1230426
    then
        return ITEM_TABLE["AP_ITEM_CROWBAR"]
    elseif item_id == 1230427
    then
        return ITEM_TABLE["AP_ITEM_HAIR_OF_GIANT"]
    elseif item_id == 1230428
    then
        return ITEM_TABLE["AP_ITEM_MUG"]
    elseif item_id == 1230429
    then
        return ITEM_TABLE["AP_ITEM_WATER"]
    elseif item_id == 1230430
    then
        return ITEM_TABLE["AP_ITEM_WATER_DRAGON_TEARS"]
    elseif item_id == 1230431
    then
        return ITEM_TABLE["AP_ITEM_STONE_OF_THIRST"]
    elseif item_id == 1230432
    then
        return ITEM_TABLE["AP_ITEM_COIN1"] + TOTAL_COINS
    elseif item_id == 1230437
    then
        return ITEM_TABLE["AP_ITEM_NAIL"]
    elseif item_id == 1230438
    then
        return ITEM_TABLE["AP_ITEM_BROOCH"]
    elseif item_id == 1230439
    then
        return ITEM_TABLE["AP_ITEM_JEWELRY_BOX"]
    elseif item_id == 1230440
    then
        return ITEM_TABLE["AP_ITEM_FRUIT"]
    elseif item_id == 1230441
    then
        return ITEM_TABLE["AP_ITEM_GAUNTLET"]
    elseif item_id == 1230442
    then
        return ITEM_TABLE["AP_ITEM_CUP"]
    elseif item_id == 1230443
    then
        return ITEM_TABLE["AP_ITEM_ARTWORK"]
    elseif item_id == 1230444
    then
        return ITEM_TABLE["AP_ITEM_POISONOUS_HERB"]
    elseif item_id == 1230445
    then
        return ITEM_TABLE["AP_ITEM_BRACELET"]
    elseif item_id == 1230446
    then
        return ITEM_TABLE["AP_ITEM_PRECIOUS_STONE"]
    elseif item_id == 1230447
    then
        return ITEM_TABLE["AP_ITEM_BROKEN_SWORD"]
    elseif item_id == 1230448
    then
        return ITEM_TABLE["AP_ITEM_QUILL"]
    elseif item_id == 1230449
    then
        return ITEM_TABLE["AP_ITEM_PLATE"]
    elseif item_id == 1230450
    then
        return ITEM_TABLE["AP_ITEM_BROKEN_LANCE"]
    elseif item_id == 1230451
    then
        if PROGRESSIVE_END_GAME_ITEMS == 0
        then
            return ITEM_TABLE["AP_ITEM_JEZIBEL_PENDANT"]
        elseif PROGRESSIVE_END_GAME_ITEMS == 1
        then
            return ITEM_TABLE["AP_ITEM_FLINT"]
        elseif PROGRESSIVE_END_GAME_ITEMS == 2
        then
            return ITEM_TABLE["AP_ITEM_STAFF_OF_AGES"]
        end
    elseif item_id == 1230455
    then
        return ITEM_TABLE["AP_ITEM_DNARTH_CHRONICLES"]
    elseif item_id == 1230456
    then
        return ITEM_TABLE["AP_ITEM_FINAL_BATTLE"]
    elseif item_id == 1230457
    then
        return ITEM_TABLE["AP_ITEM_SPEECHES_JAIR"]
    elseif item_id == 1230458
    then
        return ITEM_TABLE["AP_ITEM_BLANK_BOOK"] + TOTAL_BLANK_BOOK
    elseif item_id == 1230461
    then
        return ITEM_TABLE["AP_ITEM_STUDENT_DIARY"]
    elseif item_id == 1230462
    then
        return ITEM_TABLE["AP_ITEM_ACOLYTE_DIARY"]
    elseif item_id == 1230463
    then
        return ITEM_TABLE["AP_ITEM_PERSONAL_JOURNAL"]
    elseif item_id == 1230464
    then
        return ITEM_TABLE["AP_ITEM_MEMOIRS"]
    elseif item_id == 1230465
    then
        return ITEM_TABLE["AP_ITEM_NOVICE_JOURNAL"]
    elseif item_id == 1230466
    then
        return ITEM_TABLE["AP_ITEM_TRIALS_KINGDOM"]
    elseif item_id == 1230467
    then
        return ITEM_TABLE["AP_ITEM_BROTHERHOOD_REPORT"]
    elseif item_id == 1230468
    then
        return ITEM_TABLE["AP_ITEM_WRITINGS_KONNOR"]
    elseif item_id == 1230469
    then
        return ITEM_TABLE["AP_ITEM_HOUSE_DRESLIN"]
    elseif item_id == 1230470
    then
        return ITEM_TABLE["AP_ITEM_MEMORANDUM"]
    elseif item_id == 1230471
    then
        return ITEM_TABLE["AP_ITEM_LAST_DRAGON"]
    elseif item_id == 1230472
    then
        return ITEM_TABLE["AP_ITEM_RIDING_DRAGONS"]
    elseif item_id == 1230473
    then
        return ITEM_TABLE["AP_ITEM_RESEARCH_LOG"]
    elseif item_id == 1230474
    then
        return ITEM_TABLE["AP_ITEM_MUSINGS_LUNATIC"]
    elseif item_id == 1230475
    then
        return ITEM_TABLE["AP_ITEM_ORDERS"]
    elseif item_id == 1230476
    then
        return ITEM_TABLE["AP_ITEM_LAWS_MAGIC"]
    elseif item_id == 1230477
    then
        return ITEM_TABLE["AP_ITEM_FAMILY_DIARY"]
    elseif item_id == 1230478
    then
        return ITEM_TABLE["AP_ITEM_WORDS_DNARTH"]
    elseif item_id == 1230479
    then
        return ITEM_TABLE["AP_ITEM_ARTIFACTS_POWER"]
    elseif item_id == 1230480
    then
        return ITEM_TABLE["AP_ITEM_MAGICAL_ELIXIRS"]
    elseif item_id == 1230484
    then
        return ITEM_TABLE["AP_ITEM_JOURNAL"]
    elseif item_id == 1230485
    then
        return ITEM_TABLE["AP_ITEM_WATCHMAN_MEMO"]
    elseif item_id == 1230486
    then
        return ITEM_TABLE["AP_ITEM_REPORT"]
    elseif item_id == 1230487
    then
        return ITEM_TABLE["AP_ITEM_OFFICIAL_ARTICLE"]
    elseif item_id == 1230488
    then
        return ITEM_TABLE["AP_ITEM_LECTURE_NOTES"]
    elseif item_id == 1230489
    then
        return ITEM_TABLE["AP_ITEM_PERSONAL_LETTER"]
    elseif item_id == 1230490
    then
        return ITEM_TABLE["AP_ITEM_INNER_CHAMBER"]
    elseif item_id == 1230491
    then
        return ITEM_TABLE["AP_ITEM_TRAVELOGUE"]
    elseif item_id == 1230492
    then
        return ITEM_TABLE["AP_ITEM_TRAVEL_GUIDE"]
    elseif item_id == 1230493
    then
        return ITEM_TABLE["AP_ITEM_PETITION"]
    elseif item_id == 1230494
    then
        return ITEM_TABLE["AP_ITEM_RECEIPT"]
    elseif item_id == 1230495
    then
        return ITEM_TABLE["AP_ITEM_PERSONAL_NOTE"]
    end
end

function check_locations()
    local checks = {}
        if ASSET_MAP_CHECK[CURRENT_MAP] ~= nil
        then
            if ASSET_MAP_CHECK[CURRENT_MAP]["ITEMS"] ~= nil
            then
                for _,locationId in pairs(ASSET_MAP_CHECK[CURRENT_MAP]["ITEMS"])
                do
                    checks[locationId] = SGHACK:getCheckLocation(ADDRESS_MAP["ITEMS"][locationId]['addr'])
                    if DEBUG == true
                    then
                        print(ADDRESS_MAP["ITEMS"][locationId]['name']..":"..tostring(checks[locationId]))
                    end
                end
            end
        end
        for _,locationId in pairs(ASSET_MAP_CHECK["ALL"]["ITEMS"])
        do
            checks[locationId] = SGHACK:getCheckLocation(ADDRESS_MAP["ITEMS"][locationId]['addr'])
            if DEBUG == true
            then
                print(ADDRESS_MAP["ITEMS"][locationId]['name']..":"..tostring(checks[locationId]))
            end
        end
    return checks
end

function check_victory()
    local scene = mainmemory.read_u16_be(0x0E7A22);
    if scene == 0x026C
    then
        return "true"
    end
    return "false"
end

---------------------- ARCHIPELAGO FUNCTIONS -------------

function processAGIItem(item_list)
    for ap_id, memlocation in pairs(item_list) -- Items unrelated to AGI_MAP like Consumables
    do
        if receive_map[tostring(ap_id)] == nil
        then
            if(1230381 <= memlocation and memlocation <= 1230495)
            then
                obtain_AP_Item(memlocation)
            end
            receive_map[tostring(ap_id)] = tostring(memlocation)
        end
    end
end

function process_block(block)
    -- Sometimes the block is nothing, if this is the case then quietly stop processing
    if block == nil then
        return
    end
    if block['slot_player'] ~= nil
    then
        return
    end
    if next(block['messages']) ~= nil
    then
        local msg = ""
        for k, msg_table in pairs(block['messages'])
        do
            Messages(msg_table)
        end
    end
    if next(block['items']) ~= nil
    then
        processAGIItem(block['items'])
    end
    if block['triggerDeath'] == true and DEATH_LINK == true
    then
        print("not implemented")
    end
end

function Messages(msg_table)
    local msg = ""
    if msg_table["player"] == PLAYER and msg_table["to_player"] == PLAYER
    then
        msg = "You have found your\n" .. msg_table["item"]
    elseif msg_table["to_player"] == PLAYER
    then
        msg = msg_table["player"] .. "\nsent your " .. msg_table["item"]
    else
        return
    end
    local item = convertItemtoHex(msg_table["item_id"])
    table.insert(MESSAGE_TABLE, {msg, item})
end

function SendToClient()
    local retTable = {}
    retTable["scriptVersion"] = SCRIPT_VERSION;
    retTable["playerName"] = PLAYER;
    retTable["deathlinkActive"] = DEATH_LINK;
    retTable["check_locations"] = check_locations()
    retTable["sync_ready"] = "true"
    retTable["victory"] = check_victory()

    local msg = json.encode(retTable).."\n"
    local ret, error = SG_SOCK:send(msg)
    if ret == nil then
        print(error)
    elseif CUR_STATE == STATE_INITIAL_CONNECTION_MADE then
        CUR_STATE = STATE_TENTATIVELY_CONNECTED
    elseif CUR_STATE == STATE_TENTATIVELY_CONNECTED then
        print("Connected!")
        CUR_STATE = STATE_OK
    end
end

function receive()
    if PLAYER == "" and SEED == 0
    then
        getSlotData()
    else
        -- Send the message
        SendToClient()

        l, e = SG_SOCK:receive()
        -- Handle incoming message
        if e == 'closed' then
            if CUR_STATE == STATE_OK then
                print("Connection closed")
            end
            CUR_STATE = STATE_UNINITIALIZED
            return
        elseif e == 'timeout' then
            AP_TIMEOUT_COUNTER = AP_TIMEOUT_COUNTER + 1
            if AP_TIMEOUT_COUNTER == 5
            then
                print("Archipelago Timeout")
                AP_TIMEOUT_COUNTER = 0
            end
            return
        elseif e ~= nil then
            print(e)
            CUR_STATE = STATE_UNINITIALIZED
            return
        end
        AP_TIMEOUT_COUNTER = 0
        process_block(json.decode(l))
    end
end

function getSlotData()
    local retTable = {}
    retTable["getSlot"] = true;
    local msg = json.encode(retTable).."\n"
    local ret, error = SG_SOCK:send(msg)
    l, e = SG_SOCK:receive()
    -- Handle incoming message
    if e == 'closed' then
        if CUR_STATE == STATE_OK then
            print("Connection closed")
        end
        CUR_STATE = STATE_UNINITIALIZED
        return
    elseif e == 'timeout' then
        AP_TIMEOUT_COUNTER = AP_TIMEOUT_COUNTER + 1
        if AP_TIMEOUT_COUNTER == 10
        then
            print("Archipelago Timeout")
            AP_TIMEOUT_COUNTER = 0
        end
        print("timeout")
        return
    elseif e ~= nil then
        print(e)
        CUR_STATE = STATE_UNINITIALIZED
        return
    end
    AP_TIMEOUT_COUNTER = 0
    process_slot(json.decode(l))
end

function process_slot(block)
    for index, item in pairs(ROM_ITEM_TABLE)
    do
        ITEM_TABLE[item] = index
    end
    if block['slot_player'] ~= nil and block['slot_player'] ~= ""
    then
        PLAYER = block['slot_player']
    end
    if block['slot_seed'] ~= nil and block['slot_seed'] ~= ""
    then
        SEED = block['slot_seed']
    end
    if block['slot_deathlink'] ~= nil and block['slot_deathlink'] ~= "false"
    then
        DEATH_LINK = false
    end
    if block['slot_version'] ~= nil and block['slot_version'] ~= ""
    then
        CLIENT_VERSION = block['slot_version']
        if CLIENT_VERSION ~= SG_VERSION
        then
            VERROR = true
            return false
        end
    end
    if block['slot_opendiscdoor'] ~= nil and block['slot_opendiscdoor'] ~= 0
    then
        SGH:setSettingDoor()
    end
    return true
end


function messageQueue()
    local processed = -1;
    if SGH:getCurrentQueue() == SGH:getPCQueue()
    then
        for id, message in pairs(MESSAGE_TABLE)
        do
            SGH:setDialog(message[1], message[2])
            processed = id
            break
        end
        if processed ~= -1
        then
            table.remove(MESSAGE_TABLE, processed)
        end
    end
end

---------------------- MAIN LUA LOOP -------------------------

function main()
    if not checkBizHawkVersion() then
        return
    end
    print("Shadowgate64 Archipelago Version " .. SG_VERSION)
    SGH = SGHACK:new(nil)
    SGH:setPCQueue()
    -- while SGHACK:getSettingPointer() == nil
    -- do
    --     emu.frameadvance()
    -- end
    server, error = socket.bind('localhost', 21222)
    local changed_map = 0x0
    local SNEAK = false
    while true do
        FRAME = FRAME + 1
        if not (CUR_STATE == PREV_STATE) then
            PREV_STATE = CUR_STATE
        end
        if (CUR_STATE == STATE_OK) or (CUR_STATE == STATE_INITIAL_CONNECTION_MADE) or (CUR_STATE == STATE_TENTATIVELY_CONNECTED) then
            if (FRAME % 30 == 1) then
                CURRENT_MAP = SGH:getCurrentMap()
                receive();
                messageQueue();
                if VERROR == true
                then
                    print("ERROR: Shadowgate64_connector Mismatch. Please obtain the correct version")
                    print("Connector Version: " .. SG_VERSION)
                    print("Client Version: " .. CLIENT_VERSION)
                    return
                end
                -- local check_controls = joypad.get()
                -- -- SNEAK
                -- if check_controls ~= nil and check_controls['P1 DPad U'] == true and SNEAK == false
                -- then
                --     table.insert(MESSAGE_TABLE, {"jjjj12212 is the best!", 0x2B})
                --     SNEAK = true
                -- elseif check_controls ~= nil and check_controls['P1 DPad U'] == false and SNEAK == true
                -- then
                --     SNEAK = false
                -- end
            end
        elseif (CUR_STATE == STATE_UNINITIALIZED) then
            if  (FRAME % 60 == 1) then
                server:settimeout(2)
                local client, timeout = server:accept()
                if timeout == nil then
                    print('Initial Connection Made')
                    CUR_STATE = STATE_INITIAL_CONNECTION_MADE
                    SG_SOCK = client
                    SG_SOCK:settimeout(0)
                else
                    print('Connection failed, ensure Shadowgate64 Client is running, connected, reboot Core and rerun shadowgate64_connector.lua')
                    return
                end
            end
        end
        emu.frameadvance()
    end
end

main()
