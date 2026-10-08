"""Read-only N64 RAM state pollers.

Author: Umed (UmedMuzl).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from .flag_data import ITEMS

if TYPE_CHECKING:
    from ..Sg64Client import BTEmuLoaderClient


ANCHOR_CHECK_LOCATIONS = 0x7


class SGHReader:
    """Pointer-chase + flag-check helpers for the BTHACK injected struct."""

    def __init__(self, loader: BTEmuLoaderClient):
        self.loader = loader

    def anchor(self) -> Optional[int]:
        return self.loader.get_anchor()

    def bit_at(self, ptr: Optional[int], addr: int, bit: int) -> bool:
        if ptr is None:
            return False
        byte = self.loader.read_u8(ptr + addr)
        return ((byte >> bit) & 1) == 1

# Comprehensive polling
def poll_all_locations(sgh: SGHReader) -> Dict[int, bool]:

    out: Dict[int, bool] = {}
    anchor = sgh.anchor()
    location_addr = anchor + ANCHOR_CHECK_LOCATIONS
    for loc_id, spec in ITEMS.items():
        val = sgh.loader.read_u8(location_addr + spec[1])
        if val == 1:
            out[loc_id] = True
        else:
            out[loc_id] = False
    return out
