################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

from .class_log import LOGGER
from .database import ndB
from .class_handler import TAG_LOG
from Mix import nlx, bot
import wget
import asyncio
from hydrogram.types import ChatPrivileges
from os import execvp
from sys import executable

async def check_logger():
    LOGGER.info(f"Check Grup Log User...")
    if TAG_LOG is not None:
        return
    LOGGER.info(f"Creating Grup Log...")
    nama = f"Mix-Userbot Logs"
    des = "Jangan Keluar Dari Grup Log Ini\n\nPowered by: @KynanSupport"
    log_pic = "https://telegra.ph//file/ee7fc86ab183a0ff90392.jpg"
    gc = await nlx.create_supergroup(nama, des)
    bhan = wget.download(f"{log_pic}")
    gmbr = {"video": bhan} if bhan.endswith(".mp4") else {"photo": bhan}
    kntl = gc.id
    await asyncio.sleep(1)
    await nlx.set_chat_photo(kntl, **gmbr)
    await asyncio.sleep(1)
    await nlx.promote_chat_member(
        kntl, 
        bot.me.nlxname,
        privileges=ChatPrivileges(
            can_change_info=True,
            can_invite_nlxs=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=True,
            can_manage_chat=True,
            can_manage_video_chats=True))
    await asyncio.sleep(1)
    ndB.set_key("TAG_LOG", kntl)
    await nlx.send_message(
        kntl,
        f"<b>Group Log Berhasil Dibuat.</b>")
    LOGGER.info(f"Group Logger Enable...")
    execvp(executable, [executable, "-m", "Mix"])
   