import contextlib
import datetime
import logging

from validators import *
from config import *
from database import *
from database.users import *
from helpers import *
from pyrogram import *
from pyrogram.types import *
from script import *
from bot import *

logger = logging.getLogger(__name__)

user_commands = ["set_api", "me"]
avl_web = ["runurl.in", "kingurl.in", "seturl.in", "instantearn.in"]

avl_web1 = "".join(f"- {i}\n" for i in avl_web)

@Client.on_message(filters.command('start') & filters.private & filters.incoming)
async def start(c: Client, m: Message):
    NEW_USER_REPLY_MARKUP = [
                [
                    InlineKeyboardButton('🔴 Ban', callback_data=f'ban#{m.from_user.id}'),
                    InlineKeyboardButton('📴 Close', callback_data='delete'),
                ]
            ]
    is_user = await is_user_exist(m.from_user.id)
    reply_markup = InlineKeyboardMarkup(NEW_USER_REPLY_MARKUP)

    if not is_user and LOG_CHANNEL: 
        await c.send_message(LOG_CHANNEL, f"<blockquote><b>#NewUser\n\nUser ID: {m.from_user.id}\nUser: {m.from_user.mention}</b></blockquote>", reply_markup=reply_markup)
    
    new_user = await get_user(m.from_user.id)  
    t = START_MESSAGE.format(m.from_user.mention, new_user["method"], new_user["base_site"])

    if WELCOME_IMAGE:
        return await m.reply_photo(photo=WELCOME_IMAGE, caption=t, reply_markup=START_MESSAGE_REPLY_MARKUP)
    
    await m.reply_text(t, reply_markup=START_MESSAGE_REPLY_MARKUP, disable_web_page_preview=True)


@Client.on_message(filters.command('help') & filters.private)
async def help_command(c, m: Message):
    s = HELP_MESSAGE.format(
        firstname=m.from_user.first_name,
        username=m.from_user.username or 'unknown'
    )

    if WELCOME_IMAGE:
        return await m.reply_photo(
            photo=WELCOME_IMAGE,
            caption=s,
            reply_markup=HELP_REPLY_MARKUP
        )

    await m.reply_text(
        s,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('✍️ Custom Alias', callback_data='alias_conf')],
            [InlineKeyboardButton('🏠 Home', callback_data='start_command')]
        ]),
        disable_web_page_preview=True
    )


@Client.on_message(filters.command('about'))
async def about_command(c, m: Message):
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('🏠 Home', callback_data='start_command'),
         InlineKeyboardButton('🏷️ Help', callback_data='help_command')],
        [InlineKeyboardButton('📴 Close', callback_data='delete')]
    ])

    bot = await c.get_me()
    
    if WELCOME_IMAGE:
        return await m.reply_photo(
            photo=WELCOME_IMAGE,
            caption=ABOUT_TEXT.format(bot.mention(style='md')),
            reply_markup=reply_markup
        )

    await m.reply_text(
        ABOUT_TEXT.format(bot.mention(style='md')),
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


@Client.on_message(filters.command('set_api') & filters.private)
async def shortener_api_handler(bot, m: Message):
    user_id = m.from_user.id
    user = await get_user(user_id)
    cmd = m.command
    if len(cmd) == 1:
        s = SHORTENER_API_MESSAGE.format(base_site=user["base_site"], shortener_api=user["shortener_api"])
        return await m.reply(s)
    
    elif len(cmd) == 2:
        api = cmd[1].strip()
        await update_user_info(user_id, {"shortener_api": api})
        await m.reply(f"**Shortener API updated successfully to {api}**")


@Client.on_message(filters.command('me') & filters.private)
async def me_handler(bot, m: Message):
    user_id = m.from_user.id
    user = await get_user(user_id)

    res = USER_ABOUT_MESSAGE.format(
                method=user["method"],
                base_site=user["base_site"], 
                shortener_api=user["shortener_api"])
    
    buttons = await get_me_button(user)
    reply_markup = InlineKeyboardMarkup(buttons)
    
    return await m.reply_text(res, reply_markup=reply_markup, disable_web_page_preview=True)


@Client.on_message(filters.command('ban') & filters.private & filters.user(ADMINS))
async def banned_user_handler(c: Client, m: Message):
    try:
        if len(m.command) == 1:
            x = "".join(f"- {user}\n" for user in temp.BANNED_USERS)
            txt = BANNED_USER_TXT.format(users=x or "None")
            await m.reply(txt)
        
        elif len(m.command) == 2:
            user_id = m.command[1]
            user = await get_user(int(user_id))
            if user:
                if not user["banned"]:
                    await update_user_info(user_id, {"banned": True})
                    with contextlib.suppress(Exception):
                        temp.BANNED_USERS.append(int(user_id))
                        await c.send_message(user_id, "<blockquote><b>You are now banned from the bot by Admin</b></blockquote>")
                    
                    await m.reply(f"<blockquote><b>User [{user_id}] has been banned from the bot. To Unban: /unban {user_id}</b></blockquote>")

                else:
                    await m.reply("User is already banned")
            else:
                await m.reply("User doesn't exist")
    
    except Exception as e:
        logging.exception(e, exc_info=True)


@Client.on_message(filters.command('unban') & filters.private & filters.user(ADMINS))
async def unban_user_handler(c: Client, m: Message):
    try:
        if len(m.command) == 1:
            x = "".join(f"- {user}\n" for user in temp.BANNED_USERS)
            txt = BANNED_USER_TXT.format(users=x or "None")
            await m.reply(txt)
        
        elif len(m.command) == 2:
            user_id = m.command[1]
            user = await get_user(int(user_id))
            if user:
                if user["banned"]:
                    await update_user_info(user_id, {"banned": False})
                    with contextlib.suppress(Exception):
                        temp.BANNED_USERS.remove(int(user_id))
                        await c.send_message(user_id, "<blockquote><b>You are now unbanned from the bot by Admin</b></blockquote>")
                    
                    await m.reply(f"<blockquote><b>User [{user_id}] has been unbanned from the bot. To ban again: /ban {user_id}</b></blockquote>")
                else:
                    await m.reply("User is not banned yet")
            else:
                await m.reply("User doesn't exist")
    
    except Exception as e:
        logging.exception(e, exc_info=True)

"""
Author: StupidBoi
Telegram: https://t.me/StupidBoi69
"""
