################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


from hydrogram import __version__ as pyrover
from importlib import import_module
import importlib
from sys import version as pyver
from math import ceil
from pytgcalls import __version__ as pytgver
from hydrogram.types import InlineKeyboardButton
from hydrogram.errors import *
from Mix import nlx, bot
from modular import USER_MOD
from os import execvp
from sys import executable

from .class_handler import TAG_LOG
from .class_log import LOGGER
from .database import ndB

CMD_HELP = {}

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(page_n, module_dict, prefix, chat=None):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__modles__,
                    callback_data="{}_module({})".format(
                        prefix, x.__modles__.replace(" ", "_").lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__modles__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__modles__.replace(" ", "_").lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    line = 3
    pairs = list(zip(modules[::2], modules[1::2]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )
        
 

    max_num_pages = ceil(len(pairs) / line)
    modulo_page = page_n % max_num_pages

    if len(pairs) > line:
        pairs = pairs[modulo_page * line : line * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "⪻",
                    callback_data="{}_prev({})".format(prefix, modulo_page),
                ),
                EqInlineKeyboardButton(
                    "ⓧ",
                    callback_data="close",
                ),
                EqInlineKeyboardButton(
                    "⪼",
                    callback_data="{}_next({})".format(prefix, modulo_page),
                ),
            )
        ]

    return pairs
    
    
    
async def refresh_modules():
    LOGGER.info(f"Importing All Modules...")
    for modul in USER_MOD:
        imported_module = importlib.import_module(f"modular.{modul}")
        if hasattr(imported_module, "__modles__") and imported_module.__modles__:
            imported_module.__modles__ = imported_module.__modles__
            if hasattr(imported_module, "__help__") and imported_module.__help__:
                CMD_HELP[
                    imported_module.__modles__.replace(" ", "_").lower()
                ] = imported_module
        
        
 


async def getFinish():
    emut = await nlx.get_prefix(nlx.me.id)
    xx = " ".join(emut)
    try:
        await bot.send_message(
            TAG_LOG,
            f"""
<b>Userbot Successfully Deploy !!</b>

<b>Modules : {len(CMD_HELP)}</b>
<b>Python : {pyver.split()[0]}</b>
<b>Pyrogram : {pyrover}</b>
<b>Pytgcalls : {pytgver}</b>
<b>Prefixes : {xx}</b>
""")
    except (ChannelInvalid, PeerIdInvalid):
        ndB.del_key("TAG_LOG")
        execvp(executable, [executable, "-m", "Mix"])