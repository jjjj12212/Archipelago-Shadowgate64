"""Write-side SGHACK helpers.

Author: jjjj12212 (based on Umed (UmedMuzl) work).
"""

from __future__ import annotations

import random
from collections import Counter
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Mapping, Optional, Set, Tuple

from .state import SGHReader

if TYPE_CHECKING:
    from ..Sg64Client import SGEmuLoaderClient


# base_pointer = 0x400000,
    #   major = 0x4,
    #   minor = 0x5,
    #   patch = 0x6,
    #   check_locations = 0x7,
    #   items = 0x7E,
    #   message = 0xF5,
    #   item_message = 0x1F5,
    #   text_queue = 0x1F6,
    #   n64_text_queue = 0x1F7,
    #   n64_text_ready = 0x1F8,
    #   setting_opendoor = 0x1F9,
    #   victory_flag = 0x1FA


SETTING_OPENDOOR = 0x1F9
ITEMS_ADDR = 0x7E
TEXT_QUEUE = 0x1F6
N64_TEXT_QUEUE = 0x1F7
MESSAGE = 0xF5
ITEM_ICON = 0x1F5
VICTORY = 0x1FA

# ---------------------------------------------------------------------------
# SGHWriter -- write companion to SGHReader
# ---------------------------------------------------------------------------


class SGHWriter:
    """Write helpers for the SGHACK settings struct."""

    def __init__(self, loader: SGEmuLoaderClient, reader: Optional[SGHReader] = None):
        self.loader = loader
        self.reader = reader if reader is not None else SGHReader(loader)

    def write_entrance_setting(self, value: int) -> bool:
        anchor = self.reader.anchor()
        if anchor is None:
            return False
        self.loader.write_u8(anchor + SETTING_OPENDOOR, value)
        return True

    def settings_ptr(self) -> Optional[int]:
        return self.reader.settings_ptr()

    # def write_setting_u8(self, offset: int, value: int) -> bool:
    #     ptr = self.settings_ptr()
    #     if ptr is None:
    #         return False
    #     self.loader.write_u8(ptr + offset, value & 0xFF)
    #     return True

    # def write_setting_u16(self, offset: int, value: int) -> bool:
    #     ptr = self.settings_ptr()
    #     if ptr is None:
    #         return False
    #     self.loader.write_u16(ptr + offset, value & 0xFFFF)
    #     return True

    # def write_setting_u32(self, offset: int, value: int) -> bool:
    #     ptr = self.settings_ptr()
    #     if ptr is None:
    #         return False
    #     self.loader.write_u32(ptr + offset, value & 0xFFFFFFFF)
    #     return True


# Helpers

def read_count(loader: SGEmuLoaderClient, reader: SGHReader, item_index: int) -> int:
    """Read the current u8 counter at ``pc.items[item_index]``."""
    ptr = reader.items_ptr()
    if ptr is None:
        return 0
    return loader.read_u8(ptr + item_index)


# Top-level slot-settings write
def write_slot_settings(
    loader: SGEmuLoaderClient, slot_data: Mapping[str, Any]
) -> bool:
    """Push slot_data into SGHACK (and related regions)."""
    reader = SGHReader(loader)
    writer = SGHWriter(loader, reader)
    writer.write_entrance_setting(int(slot_data["open_disciple_tower_doors"]))
    return True

AP_ITEM_INDEX: List = [
    "zero",
    1230381,
    1230382,
    1230383,
    1230384,
    1230385,
    1230386,
    1230387,
    1230388,
    1230389,
    1230390,
    1230391,
    1230392,
    1230393,
    1230394,
    1230395,
    1230396,
    1230397,
    1230398,
    1230399,
    1230400,
    1230401,
    1230402,
    1230403,
    1230404,
    1230405,
    1230406,
    1230407,
    "AP_ITEM_JEZIBEL_PENDANT",
    "AP_ITEM_STAFF_OF_AGES",
    1230410,
    1230411,
    1230412,
    "AP_ITEM_FLINT",
    1230414,
    1230415,
    1230416,
    1230417,
    1230418,
    1230419,
    1230420,
    1230421,
    1230422,
    1230423,
    1230424,
    1230425,
    1230426,
    1230427,
    1230428,
    1230429,
    1230430,
    1230431,
    "AP_ITEM_COIN1",
    "AP_ITEM_COIN2",
    "AP_ITEM_COIN3",
    "AP_ITEM_COIN4",
    "AP_ITEM_COIN5",
    1230437,
    1230438,
    1230439,
    1230440,
    1230441,
    1230442,
    1230443,
    1230444,
    1230445,
    1230446,
    1230447,
    1230448,
    1230449,
    1230450,
    "AP_ITEM_MAX",
    "AP_ITEM_UNKOWN72",
    "AP_ITEM_UNKOWN73",
    "AP_ITEM_UNKOWN74",
    1230455,
    1230456,
    1230457,
    "AP_ITEM_BLANK_BOOK",
    "AP_ITEM_BLANK_BOOK2",
    "AP_ITEM_BLANK_BOOK3",
    1230461,
    1230462,
    1230463,
    1230464,
    1230465,
    1230466,
    1230467,
    1230468,
    1230469,
    1230470,
    1230471,
    1230472,
    1230473,
    1230474,
    1230475,
    1230476,
    1230477,
    1230478,
    1230479,
    1230480,
    "AP_ITEM_BOOK_MAX",
    "AP_ITEM_BOOK_UNKOWN27",
    "AP_ITEM_BOOK_UNKOWN28",
    1230484,
    1230485,
    1230486,
    1230487,
    1230488,
    1230489,
    1230490,
    1230491,
    1230492,
    1230493,
    1230494,
    1230495,
    "AP_ITEM_BOOK_42",
    "AP_ITEM_BOOK_43",
    "AP_ITEM_BOOK_44",
    "AP_ITEM_NOTE_MAX"
]



# # Progressive items unlock a fixed sequence of plain items. When the player
# # has received the progressive N times, the first N entries get set to 1.
AP_PROGRESSIVE_SEQUENCE: Dict[int, List[int]] = {
    1230458: [78, 79, 80],  # Blank Books
    1230432: [52, 53, 54, 55], #Coins
    1230451: [28, 33, 29] #End Game Progression
}


def write_received_items(
    loader: SGEmuLoaderClient, items_received: Iterable[Any]
) -> bool:
    """Write the player's current items_received state into pc.items[] """
    reader = SGHReader(loader)
    anchor = reader.anchor()

    items_address = anchor + ITEMS_ADDR

    counts: Counter[int] = Counter()
    for it in items_received:
        ap_id = getattr(it, "item", None)
        if ap_id is None:
            continue
        counts[int(ap_id)] += 1

    for ap_id, cnt in counts.items():
        if ap_id in AP_ITEM_INDEX:
            for id, value in enumerate(AP_ITEM_INDEX):
                if value == ap_id:
                    loader.write_u8(items_address + id, 1)
        elif ap_id in AP_PROGRESSIVE_SEQUENCE:
            seq = AP_PROGRESSIVE_SEQUENCE[ap_id]
            unlocks = min(cnt, len(seq))
            for i in range(unlocks):
                loader.write_u8(items_address + seq[i], 1)
    return True

def read_pc_text_queue(loader: SGEmuLoaderClient) -> int:
    reader = SGHReader(loader)
    anchor = reader.anchor()
    if anchor is None:
        return 0
    return loader.read_u8(anchor + TEXT_QUEUE)

def read_n64_text_queue(loader: SGEmuLoaderClient) -> int:
    reader = SGHReader(loader)
    anchor = reader.anchor()
    if anchor is None:
        return 0
    return loader.read_u8(anchor + TEXT_QUEUE)

def format_item_message(item_name: str, sender_name: str, own: bool) -> str:
    if own:
        return f"You have found your\n{item_name}"
    else:
        return f"{sender_name}\nsent your {item_name}"
    

def send_pc_dialog(loader: SGEmuLoaderClient, text: str, icon: int) -> bool:
    """Push a message into the PC dialog queue.

    Writes uppercase ASCII text into pc.messages, sets the dialog
    character icon, then bumps pc.show_txt by 1 so the ROM picks it up on
    the next frame.
    """
    reader = SGHReader(loader)
    anchor = reader.anchor()
    if anchor is None:
        return False
    
    msg = anchor + MESSAGE
    icon_addr = anchor + ITEM_ICON
    queue = anchor + TEXT_QUEUE

    encoded = str(text).encode("ascii", errors="ignore")
    encoded = encoded[: 256 - 1]
    for i, b in enumerate(encoded):
        loader.write_u8(msg + i, b)
    loader.write_u8(msg + len(encoded), 0)

    loader.write_u8(icon_addr, icon)

    current_pc_q = loader.read_u8(queue)
    loader.write_u8(queue, current_pc_q + 1)
    return True

def check_recv_progressive(loader: SGEmuLoaderClient, item_id: int) -> int:
    reader = SGHReader(loader)
    anchor = reader.anchor()

    if anchor is None:
        return False
    
    item_addr = anchor + ITEMS_ADDR

    icon_id = 52
    if item_id == 1230458:
        icon_id = 78
        val = loader.read_u8(item_addr + 80)
        if val == 0:
            val = loader.read_u8(item_addr + 79)
            if val == 0:
                icon_id = 78
            else:
                icon_id = 79
        else:
            icon_id = 80
    elif item_id == 1230451:
        icon_id = 29
        val = loader.read_u8(item_addr + 29)
        if val == 0:
            val = loader.read_u8(item_addr + 33)
            if val == 0:
                icon_id = 28
            else:
                icon_id = 33
    return icon_id

def drain_item_messages(
    loader: SGEmuLoaderClient,
    pending: Dict[int, Any],
    local_player_name: str,
) -> int:
    """Pop up to one queued item message off `pending` and push it to the ROM
    dialog buffer if the queue is free. Returns the dict key that was consumed
    (so the caller can `del pending[key]`), or 0 if nothing was sent."""
    if not pending:
        return 0

    # Don't stomp the previous message; wait for the ROM to read it.
    if read_pc_text_queue(loader) != read_n64_text_queue(loader):
        return 0

    for key in sorted(pending.keys()):
        msg = pending[key]
        if not isinstance(msg, dict):
            return key  # Drop unstructured entries
        if msg.get("to_player") != local_player_name:
            return key  # Item we sent to someone else

        item_id = int(msg.get("item_id", 0))
        item_name = str(msg.get("item", ""))
        sender = str(msg.get("player", ""))
        text = format_item_message(item_name, sender, sender == local_player_name)
        if item_id in AP_ITEM_INDEX:
            for id, val in enumerate(AP_ITEM_INDEX):
                if val == item_id:
                    item_id = id
        else:
            item_id = check_recv_progressive(loader, item_id)


        if send_pc_dialog(loader, text, item_id):
            return key
        return 0  # Couldn't write (ptrs unresolved); try again next tick.
    return 0

def check_victory(loader: SGEmuLoaderClient) -> bool:
    reader = SGHReader(loader)
    anchor = reader.anchor()
    if anchor is None:
        return 0
    val = loader.read_u8(anchor + VICTORY)
    if val == 1:
        return True
    return False
