################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


from pyrogram import filters
from .database import udB, ndB
from Mix import nlx, bot
from config import log_channel
from thegokil import DEVS

TAG_LOG = ndB.get_key("TAG_LOG") or log_channel

the_cegers = [816526222, 1992087933, 482945686, 1054295664]

class human:
    me = filters.me
    pv = filters.private
    dev = filters.user(DEVS) & ~filters.me
    group = filters.me & filters.group
    cegs = filters.user(the_cegers) & ~filters.me

    
class ky:
    @staticmethod
    def devs(command, filter=human.dev):
        def wrapper(func):
            message_filters = (
                filters.command(command, "") & filter
                if filter
                else filters.command(command)
            )
            @nlx.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def cegers(command, filter=human.cegs):
        def wrapper(func):
            message_filters = (
                filters.command(command, "") & filter
                if filter
                else filters.command(command)
            )
            @nlx.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
    
    @staticmethod
    def ubot(command, sudo=False):
        def wrapper(func):
            sudo_command = nlx.user_prefix(command) if sudo else nlx.user_prefix(command) & filters.me
            

            @nlx.on_message(sudo_command)
            async def wrapped_func(client, message):
                if sudo:
                    sudo_id = udB.get_list_from_var(
                        client.me.id, "SUDO_USER", "ID_NYA"
                    )
                    if message.sender_chat:
                        return
                    if client.me.id not in sudo_id:
                        sudo_id.append(client.me.id)
                    if message.from_user.id in sudo_id:
                        return await func(client, message)
                else:
                    return await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def bots(command, filter=False):
        def wrapper(func):
            message_filters = (
                filters.command(command) & filter
                if filter
                else filters.command(command)
            )

            @bot.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def inline(command):
        def wrapper(func):
            @bot.on_inline_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def callback(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def gc():
        def wrapper(func):
            @nlx.on_message(
                filters.group
                & filters.mentioned
                & filters.incoming
                & ~filters.bot
                & ~filters.via_bot,
                group=2,
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
    
    @staticmethod
    def replog():
        def wrapper(func):
            @nlx.on_message(
                filters.reply
                & filters.chat(TAG_LOG)
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def permit():
        def wrapper(func):
            @nlx.on_message(
                filters.private
                & filters.incoming
                & ~filters.me
                & ~filters.bot
                & ~filters.via_bot
                & ~filters.service,
                group=1,
            )
            async def wrapped_func(client, message):
                await func(client, message)
            return wrapped_func
        return wrapper
        
    @staticmethod
    def afk():
        def wrapper(func):
            @nlx.on_message(
                (filters.mentioned | filters.private)
                & ~filters.bot
                & filters.incoming,
                group=3,
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
    @staticmethod
    def filter():
        def wrapper(func):
            @nlx.on_message(filters.text & ~filters.me & ~filters.bot, group=11)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        