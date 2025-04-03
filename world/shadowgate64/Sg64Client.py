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
version: str = "V0.1"
game_append_version: str = "V01"
patch_md5: str = "9d369956a0d42a8700c8263651a06a81"

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
        self.awaiting_rom = False
        self.messages = {}
        self.slot_data = {}
        self.sendSlot = False
        self.item_check_table = {}
        self.book_check_table = {}
        self.note_check_table = {}
        self.check_location_table = {}

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
            self.n64_sync_task = asyncio.create_task(n64_sync_task(self), name="N64 Sync")
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


async def n64_sync_task(ctx: Shadowgate64Context):
    logger.info("Starting n64 connector. Use /n64 for status information.")
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.n64_streams:
            (reader, writer) = ctx.n64_streams
            if ctx.sendSlot == True:
                msg = get_slot_payload(ctx).encode()
            else:
                msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    data = await asyncio.wait_for(reader.readline(), timeout=10)
                    data_decoded = json.loads(data.decode())
                    reported_version = data_decoded.get('scriptVersion', 0)
                    getSlotData = data_decoded.get('getSlot', 0)
                    if getSlotData == True:
                        ctx.sendSlot = True
                    elif reported_version >= script_version:
                        if ctx.game is not None and 'sync_ready' in data_decoded:
                            # Not just a keep alive ping, parse
                            async_start(parse_payload(data_decoded, ctx, False))
                        if not ctx.auth:
                            ctx.auth = data_decoded['playerName']
                            if ctx.awaiting_rom:
                                await ctx.server_auth(False)
                    else:
                        if not ctx.version_warning:
                            logger.warning(f"Your Lua script is version {reported_version}, expected {script_version}. "
                                "Please update to the latest version. "
                                "Your connection to the Archipelago server will not be accepted.")
                            ctx.version_warning = True
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.n64_streams = None
                except ConnectionResetError as e:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.n64_streams = None
            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.n64_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.n64_streams = None
            if ctx.n64_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to N64")
                    ctx.n64_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.n64_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.n64_status = error_status
                logger.info("Lost connection to N64 and attempting to reconnect. Use /n64 for status updates")
        else:
            try:
                logger.debug("Attempting to connect to N64")
                ctx.n64_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 21222), timeout=10)
                ctx.n64_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.n64_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.n64_status = CONNECTION_REFUSED_STATUS
                continue

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
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.n64_sync_task:
            await ctx.n64_sync_task

    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == '__main__':
    main()
