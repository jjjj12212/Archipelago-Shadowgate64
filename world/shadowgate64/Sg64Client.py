import asyncio
import hashlib
import io
import json
import os
import multiprocessing
import copy
import pathlib
import random
import subprocess
import sys
import time
from typing import Union
import zipfile
from asyncio import StreamReader, StreamWriter
import bsdiff4

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
import Utils
import settings
from Utils import async_start
from worlds import network_data_package
from . import Shadowgate64World
from .client import state as emu_state, game as emu_game


# For when its a global package
try:
    from emu_loader import EmuLoaderClient, ProcessMemory
# For when its in the apworld itself
except ImportError:
    from .emu_loader import EmuLoaderClient, ProcessMemory

# BTHACK signature validation
RDRAM_BASE = 0x80000000  # KSEG0 start; RDRAM mirror
RDRAM_SIZE = 0x800000  # 8 MB with expansion pak (required by SG)
SGHACK_ANCHOR_OFFSET = 0x400000  # physical RDRAM offset of AP_MEMORY_PTR
SGHACK_STRUCT_SIZE = 502


def is_rdram_pointer(value: int) -> bool:
    return RDRAM_BASE <= value < RDRAM_BASE + RDRAM_SIZE

class SGEmuLoaderClient(EmuLoaderClient):
    """EmuLoaderClient with SGHACK pointer-chase helpers."""

    def __init__(self) -> None:
        super().__init__(validation_func= validate_bt_signature)

    def deref(self, address: int) -> int | None:
        ptr = self.read_u32(address)
        return ptr & 0x7FFFFFFF if is_rdram_pointer(ptr) else None

    def get_anchor(self) -> int | None:
        return self.deref(RDRAM_BASE + SGHACK_ANCHOR_OFFSET)

    def get_rom_version(self) -> tuple[int, int, int] | None:
        anchor = self.get_anchor()
        if anchor is None:
            return None
        major = self.read_u8(RDRAM_BASE + anchor + 0x4)
        minor = self.read_u8(RDRAM_BASE + anchor + 0x5)
        patch = self.read_u8(RDRAM_BASE + anchor + 0x6)
        return (major, minor, patch)


def validate_bt_signature(pm: ProcessMemory, rdram_base: int) -> bool:
    """Return True if ``rdram_base`` looks like AP-Banjo-Tooie RDRAM.

    - u32 at ``rdram_base + 0x400000`` must be a valid 0x80xxxxxx pointer
      (BTHACK's ``AP_MEMORY_PTR``).
    - At the dereferenced ``ap_memory_ptr_t`` struct, all 12 sub-pointers
      at offsets 0x04..0x30 must themselves be valid RDRAM pointers. The
      patch's ``inject_hooks()`` populates every one of them at game boot.
    """
    try:
        anchor = int.from_bytes(
            pm.read_bytes(rdram_base + SGHACK_ANCHOR_OFFSET, 4), "little"
        )
    except Exception:
        return False
    if not is_rdram_pointer(anchor):
        return False
    physical = anchor & 0x7FFFFFFF
    if physical + SGHACK_STRUCT_SIZE > RDRAM_SIZE:
        return False
    try:
        #struct_bytes = pm.read_bytes(rdram_base + physical, 3)
        val = pm.read_bytes(rdram_base + physical, 4)
        if val == b'\x00\x00\x00\x00\x00\x00\x00\x00' or val == b'\x00\x00\x00\x00':
            return False
        if val == b'"!!\x12':
            return True
        else:
            return False
    except Exception:
        return False
    # for offset in BTHACK_SUB_POINTER_OFFSETS:
    #     sub_ptr = int.from_bytes(struct_bytes[offset : offset + 4], "little")
    #     if not is_rdram_pointer(sub_ptr):
    #         return False
    return True

SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart connector_shadowgate64.lua"
CONNECTION_REFUSED_STATUS = "Connection refused. Please start your emulator and make sure connector_shadowgate64.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart connector_shadowgate64.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

sg_loc_name_to_id = network_data_package["games"]["Shadowgate 64"]["location_name_to_id"]
sg_itm_name_to_id = network_data_package["games"]["Shadowgate 64"]["item_name_to_id"]
script_version: int = 1
version: str = Shadowgate64World.world_version.as_simple_string()
game_append_version: str = "V01_0_1"
patch_md5: str = "9778e82f207425f9d9ae8cc4c4673e64"

def get_item_value(ap_id):
    return ap_id

async def run_game(romfile):
        # auto_start = settings.get_settings()["shadowgate64_options"].get("rom_start", True)
        # if auto_start is True:
        #     import webbrowser
        #     webbrowser.open(romfile)
        # elif os.path.isfile(auto_start):
        #     subprocess.Popen([auto_start, romfile],
        #                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return

async def apply_patch():
    fpath = pathlib.Path(__file__)
    archipelago_root = None
    for i in range(0, 5,+1) :
        if fpath.parents[i].stem == "Archipelago":
            archipelago_root = pathlib.Path(__file__).parents[i]
            break
    patch_path = None
    if archipelago_root:
        patch_path = os.path.join(archipelago_root, "Randogate64"+game_append_version+".n64")
    if not patch_path or check_rom(patch_path) != patch_md5:
        logger.info("Please open Shadowgate 64 and load connector_shadowgate64.lua")
        await asyncio.sleep(0.01)
        rom = Utils.open_filename("Open your Shadowgate 64 ROM", (("Rom Files", (".z64", ".n64")), ("All Files", "*"),))
        if not rom:
            logger.info("No ROM selected. Please restart Shadowgate 64 Client to try again.")
            return
        if not patch_path:
            patch_path = os.path.split(rom) + "/Randogate64"+game_append_version+".n64"
        patch_rom(rom, patch_path, "Randogate64.patch")
    if patch_path:
        logger.info("Patched Shadowgate 64 is located in " + patch_path)


class Shadowgate64CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_n64(self):
        """Check N64 Connection State"""
        if isinstance(self.ctx, Shadowgate64Context):
            logger.info(f"N64 Status: {self.ctx.n64_status}")

    def _cmd_writesettings(self):
            """Manually push slot settings into BTHACK memory via emu_loader (the ROM refuses to boot until settings are populated)."""
            if not isinstance(self.ctx, Shadowgate64Context):
                return
            ctx = self.ctx
            if ctx.emu_loader is None or not ctx.emu_loader.is_connected():
                return
            if not ctx.slot_data:
                return
            if emu_game.write_slot_settings(ctx.emu_loader, ctx.slot_data):
                ctx.emu_settings_written = True


class Shadowgate64Context(CommonContext):
    command_processor = Shadowgate64CommandProcessor
    items_handling = 0b111 #full

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = 'Shadowgate 64'
        self.startup = False
        self.n64_streams: (StreamReader, StreamWriter) = None # type: ignore
        self.n64_sync_task = None
        self.n64_status = CONNECTION_INITIAL_STATUS
        self.emu_loader: SGEmuLoaderClient | None = None
        self.emu_monitor_task: asyncio.Task | None = None
        self.version_warning = False
        self.emu_settings_written: bool = False
        self.emu_last_items_count: int = -1
        self.emu_sent_world_entrances: set[int] = set()
        self.emu_goal_printed: bool = False
        self.emu_waiting_logged: bool = False
        self.emu_attached_logged: bool = False
        self.emu_status: str = "Not attached"
        self.awaiting_rom = False
        self.messages = {}
        self.slot_data = {}
        self.sendSlot = False
        self.item_check_table = {}
        self.book_check_table = {}
        self.note_check_table = {}
        self.check_location_table = []
        self.settings_processed = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(Shadowgate64Context, self).server_auth(password_requested)
        if not self.auth:
            await self.get_username()
            await self.send_connect()
            self.awaiting_rom = True
            return
        return

    def _set_message(self, msg: dict, msg_id: Union[int, None]):
        if msg_id == None:
            self.messages.update({len(self.messages)+1: msg })
        else:
            self.messages.update({msg_id:msg})

    def run_gui(self):
        from kvui import GameManager

        class Shadowgate64Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Shadowgate 64 Client"

        self.ui = Shadowgate64Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
        asyncio.create_task(apply_patch())

    def on_package(self, cmd, args):
        if cmd == 'Connected':
            self.slot_data = args.get('slot_data', None)
            if version != self.slot_data["version"]:
                logger.error("Your Shadowgate 64 AP does not match with the generated world.")
                logger.error("Your version: "+version+" | Generated version: "+self.slot_data["version"])
                # self.event_invalid_game()
                raise Exception("Your Shadowgate 64 AP does not match with the generated world.\n" +
                                "Your version: "+version+" | Generated version: "+self.slot_data["version"])
            fpath = pathlib.Path(__file__)
            archipelago_root = None
            for i in range(0, 5,+1) :
                if fpath.parents[i].stem == "Archipelago":
                    archipelago_root = pathlib.Path(__file__).parents[i]
                    break
            async_start(run_game(os.path.join(archipelago_root, "Shadowgate64"+game_append_version+".n64")))
        elif cmd == "ReceivedItems":
            if self.startup == False:
                for item in args["items"]:
                    player = ""
                    item_name = ""
                    for (i, name) in self.player_names.items():
                        if i == item.player:
                            player = name
                            break
                    for (name, i) in sg_itm_name_to_id.items():
                        if item.item == i:
                            item_name = name
                            break
                    logger.info(player + " sent " + item_name)
                logger.info("The above items will be sent when Shadowgate64 is loaded.")
                self.startup = True

    def on_print_json(self, args: dict):
        if self.ui:
            self.ui.print_json(copy.deepcopy(args["data"]))
            relevant = args.get("type", None) in {"ItemSend"}
            if relevant:
                relevant = False
                item = args["item"]
                if self.slot_concerns_self(args["receiving"]):
                    relevant = True
                elif self.slot_concerns_self(item.player):
                    relevant = True

                if relevant == True:
                    msg = self.raw_text_parser(copy.deepcopy(args["data"]))
                    player = self.player_names[int(args["data"][0]["text"])]
                    to_player = self.player_names[int(args["data"][0]["text"])]
                    for id, data in enumerate(args["data"]):
                        if id == 0:
                            continue
                        if "type" in data and data['type'] == "player_id":
                            to_player = self.player_names[int(data["text"])]
                            break
                    item_name = self.item_names.lookup_in_slot(int(args["data"][2]["text"]))
                    self._set_message({"player":player, "item":item_name, "item_id":int(args["data"][2]["text"]), "to_player":to_player }, None)
        else:
            text = self.jsontotextparser(copy.deepcopy(args["data"]))
            logger.info(text)
            relevant = args.get("type", None) in {"ItemSend"}
            if relevant:
                msg = self.raw_text_parser(copy.deepcopy(args["data"]))
                player = self.player_names[int(args["data"][0]["text"])]
                to_player = self.player_names[int(args["data"][0]["text"])]
                for id, data in enumerate(args["data"]):
                        if id == 0:
                            continue
                        if "type" in data and data['type'] == "player_id":
                            to_player = self.player_names[int(data["text"])]
                            break
                item_name = self.item_names.lookup_in_slot(int(args["data"][2]["text"]))
                self._set_message({"player":player, "item":item_name, "item_id":int(args["data"][2]["text"]), "to_player":to_player}, None)

def get_payload(ctx: Shadowgate64Context):
    payload = json.dumps({
            "items": [get_item_value(item.item) for item in ctx.items_received],
            "playerNames": [name for (i, name) in ctx.player_names.items() if i != 0],
            "triggerDeath": False,
            "messages": [message for (i, message) in ctx.messages.items() if i != 0],
        })
    if len(ctx.messages) > 0:
        ctx.messages = {}
    return payload

def get_slot_payload(ctx: Shadowgate64Context):
    payload = json.dumps({
            "slot_player": ctx.slot_data["player_name"],
            "slot_seed": ctx.slot_data["seed"],
            "slot_deathlink": False,
            "slot_opendiscdoor": ctx.slot_data["open_disciple_tower_doors"],
            "slot_version": version,
        })
    ctx.sendSlot = False
    return payload


async def parse_payload(payload: dict, ctx: Shadowgate64Context, force: bool):

    # Refuse to do anything if ROM is detected as changed
    if ctx.auth and payload['playerName'] != ctx.auth:
        logger.warning("ROM change detected. Disconnecting and reconnecting...")
        ctx.finished_game = False
        ctx.auth = payload['playerName']
        await ctx.send_connect()
        return

    # Locations handling
    #locations = payload['locations']
    check_locations = payload['check_locations']
    victory = payload['victory']

    # The Lua JSON library serializes an empty table into a list instead of a dict. Verify types for safety:
    # if isinstance(locations, list):
    #     locations = {}
    if isinstance(check_locations, list):
        check_locations = {}

    locs1 = []
    if ctx.check_location_table != check_locations:
        ctx.check_location_table = check_locations
        for locationId, value in check_locations.items():
            if value == True:
                locs1.append(int(locationId))

    if len(locs1) > 0:
        await ctx.send_msgs([{
            "cmd": "LocationChecks",
            "locations": locs1
        }])

    if victory == "true" and not ctx.finished_game:
        await ctx.send_msgs([{
            "cmd": "StatusUpdate",
            "status": 30
        }])
        ctx.finished_game = True
        ctx._set_message("You have completed your goal", None)


async def emu_loader_monitor_task(ctx: Shadowgate64Context):
    """Direct-emulator-memory bridge."""
    poll_interval = 0.2

    # wait_for_emulator() has its own internal retry loop
    # lets instead do this just one time so we dont get spammed
    logger.info(
        "Waiting for a supported emulator to attach... "
    )
    ctx.emu_waiting_logged = True

    while not ctx.exit_event.is_set():
      ctx.emu_status = "Waiting for emulator"
      ctx.emu_loader = SGEmuLoaderClient()
      ctx.emu_settings_written = False
      ctx.emu_last_items_count = -1
      ctx.emu_sent_world_entrances.clear()
      ctx.emu_goal_printed = False
      setattr(emu_loader_monitor_task, "_prev", None)
      await ctx.emu_loader.wait_for_emulator()

      if ctx.exit_event.is_set():
          return

      emu_name = ctx.emu_loader.emulator_info.id
      logger.info(f"Connected to {emu_name}.")
      ctx.emu_status = f"Connected to {emu_name}"
      ctx.emu_attached_logged = True

      while not ctx.exit_event.is_set():
        try:
            if ctx.version_warning:
                logger.error(f"ERROR: Your Patched ROM is version {ctx.rom_version}, expected {version}. " +
                    "Please update to the latest version.")
                return

            sgh = emu_state.SGHReader(ctx.emu_loader)

            rom_version_tuple = ctx.emu_loader.get_rom_version()
            if rom_version_tuple is not None and rom_version_tuple[0] > 0 and ctx.version_warning is False:
                ctx.rom_version = str(rom_version_tuple[0]) +"."+ str(rom_version_tuple[1]) + "." + str(rom_version_tuple[2])
                if version != ctx.rom_version:
                    ctx.version_warning = True
                    continue
            if ctx.slot_data and not ctx.settings_processed:
                emu_game.write_slot_settings(ctx.emu_loader, ctx.slot_data)
                ctx.settings_processed = True
            

            current_items_count = len(ctx.items_received) if ctx.items_received else 0
            if (ctx.settings_processed and current_items_count != ctx.emu_last_items_count):
                emu_game.write_received_items(ctx.emu_loader, ctx.items_received)
                ctx.emu_last_items_count = current_items_count

            if ctx.messages and ctx.auth:
                consumed = emu_game.drain_item_messages(
                    ctx.emu_loader, ctx.messages, ctx.auth)
                if consumed:
                    ctx.messages.pop(consumed, None)

            if not ctx.finished_game and ctx.server is not None:
                if emu_game.check_victory(ctx.emu_loader):
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": 30}])
                    ctx.finished_game = True


            collected = emu_state.poll_all_locations(sgh)
            new_sgid = []
            for loc_id, value in collected.items():
                if value and loc_id not in ctx.check_location_table:
                    new_sgid.append(loc_id) 
                    ctx.check_location_table.append(loc_id)


            if new_sgid and ctx.server is not None:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": new_sgid,
                }])

            # setattr(emu_loader_monitor_task, "_prev", collected)
        except Exception:
            logger.exception("Shadowgate64 emulator monitor lost its connection; reconnecting")
            ctx.emu_status = "Lost emulator connection; reconnecting..."
            try:
                if ctx.emu_loader is not None:
                    ctx.emu_loader.disconnect()
            except Exception:
                pass
            ctx.emu_loader = None
            break

        try:
            await asyncio.wait_for(ctx.exit_event.wait(), timeout=poll_interval)
            return
        except asyncio.TimeoutError:
            pass


def read_file(path):
    with open(path, 'rb') as fi:
        data = fi.read()
    return data

def write_file(path, data):
    with open(path, 'wb') as fi:
        fi.write(data)

def swap(data):
    swapped_data = bytearray(b'\0'*len(data))
    for i in range(0, len(data), 2):
        swapped_data[i] = data[i+1]
        swapped_data[i+1] = data[i]
    return bytes(swapped_data)

def check_rom(patchedRom):
    if os.path.isfile(patchedRom):
        rom = read_file(patchedRom)
        md5 = hashlib.md5(rom).hexdigest()
        return md5
    else:
        return "00000"

def patch_rom(romPath, dstPath, patchPath):
    rom = read_file(romPath)
    md5 = hashlib.md5(rom).hexdigest()
    # if (md5 == "ca0df738ae6a16bfb4b46d3860c159d9"): # byte swapped
    #     rom = swap(rom)
    # elif (md5 != "407a1a18bd7dbe0485329296c3f84eb8"):
    if (md5 != "407a1a18bd7dbe0485329296c3f84eb8"):
        logger.error("Unknown ROM!")
        return
    patch = openFile(patchPath).read()
    write_file(dstPath, bsdiff4.patch(rom, patch))

def openFile(resource: str, mode: str = "rb", encoding: str = None):
    filename = sys.modules[__name__].__file__
    apworldExt = ".apworld"
    game = "shadowgate64/"
    if apworldExt in filename:
        zip_path = pathlib.Path(filename[:filename.index(apworldExt) + len(apworldExt)])
        with zipfile.ZipFile(zip_path) as zf:
            zipFilePath = game + resource
            if mode == 'rb':
                return zf.open(zipFilePath, 'r')
            else:
                return io.TextIOWrapper(zf.open(zipFilePath, 'r'), encoding)
    else:
        return open(os.path.join(pathlib.Path(__file__).parent, resource), mode, encoding=encoding)

def main():
    Utils.init_logging("Shadowgate64 Client")
    parser = get_base_parser()
    args = sys.argv[1:]  # the default for parse_args()
    if "Shadowgate64 Client" in args:
        args.remove("Shadowgate64 Client")
    args = parser.parse_args(args)

    async def _main():
        multiprocessing.freeze_support()

        ctx = Shadowgate64Context(args.connect, args.password)
        #ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        ctx.emu_monitor_task = asyncio.create_task(emu_loader_monitor_task(ctx), name="EmuLoader Monitor")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.n64_sync_task:
            await ctx.n64_sync_task

        if ctx.emu_monitor_task:
            try:
                await asyncio.wait_for(ctx.emu_monitor_task, timeout=3.0)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                pass
            if ctx.emu_loader is not None:
                try:
                    ctx.emu_loader.disconnect()
                except Exception:
                    pass

    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == '__main__':
    main()
