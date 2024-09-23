import asyncio
import contextlib
import logging
import os
import re
import sys

from config import *
from database import *
from database.users import *
from helpers import *
from pyrogram import *
from pyrogram.errors import *
from pyrogram.types import *
from script import *
from bot import *

logger = logging.getLogger(__name__)

@Client.on_callback_query(filters.regex(r"^ban"))
async def ban_cb_handler(c: Client, m: CallbackQuery):
    try:
        user_id = m.data.split("#")[1]
        user = await get_user(int(user_id))

        if user:
            if not user["banned"]:
                temp.BANNED_USERS.append(int(user_id))
                await update_user_info(user_id, {"banned": True})
                try:
                    owner = await c.get_users(int(OWNER_ID))
                    await c.send_message(user_id, f"**🔴 You have been banned by Admin. Contact {owner.mention(style='md')} for details.**")
                except Exception as e:
                    logger.error(e)

                # Directly place the ban/unban reply markup here
                await m.edit_message_reply_markup(InlineKeyboardMarkup([
                    [InlineKeyboardButton('🟢 Unban', callback_data=f'unban#{user_id}'),
                     InlineKeyboardButton('📴 Close', callback_data='delete')]
                ]))
                await m.answer(f"**User [{user_id}] has been banned.**", show_alert=True)
            else:
                await m.answer("**User is already banned.**", show_alert=True)
        else:
            await m.answer("**User not found.**", show_alert=True)
    except Exception as e:
        logger.exception(e, exc_info=True)

@Client.on_callback_query(filters.regex("^unban"))
async def unban_cb_handler(c: Client, m: CallbackQuery):
    try:
        user_id = m.data.split("#")[1]
        user = await get_user(int(user_id))

        if user:
            if user["banned"]:
                temp.BANNED_USERS.remove(int(user_id))
                await update_user_info(user_id, {"banned": False})
                with contextlib.suppress(Exception):
                    await c.send_message(user_id, "**🟢 You have been unbanned and can use the bot again.**")

                # Directly place the unban/ban reply markup here
                await m.edit_message_reply_markup(InlineKeyboardMarkup([
                    [InlineKeyboardButton('🔴 Ban', callback_data=f'ban#{user_id}'),
                     InlineKeyboardButton('📴 Close', callback_data='delete')]
                ]))
                await m.answer("**User has been unbanned.**", show_alert=True)
            else:
                await m.answer("**User is not banned.**", show_alert=True)
        else:
            await m.answer("**User not found.**", show_alert=True)
    except Exception as e:
        logger.exception(e, exc_info=True)

@Client.on_callback_query(filters.regex("^setgs"))
async def user_setting_cb(c: Client, query: CallbackQuery):
    try:
        _, setting, toggle, user_id = query.data.split('#')
        myvalues = {setting: toggle == "True"}
        await update_user_info(user_id, myvalues)

        user = await get_user(user_id)
        buttons = await get_me_button(user)

        # Directly use reply markup generated from user settings
        await query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))

        setting_name = re.sub("is|_", " ", setting).title()
        toggle_status = "Enabled" if toggle == "True" else "Disabled"
        await query.answer(f"{setting_name} {toggle_status} updated successfully", show_alert=True)
    except Exception as e:
        logger.error("Error occurred while updating user settings", exc_info=True)

@Client.on_callback_query()
async def on_callback_query(bot: Client, query: CallbackQuery):
    user_id = query.from_user.id
    h = Helpers()
    user = await get_user(user_id)

    if query.data == 'delete':
        await query.message.delete()

    elif query.data == 'help_command':
        await query.message.edit(
            HELP_MESSAGE.format(firstname=temp.FIRST_NAME, username=temp.BOT_USERNAME),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('✍️ Custom Alias', callback_data='alias_conf')],
                [InlineKeyboardButton('🏠 Home', callback_data='start_command')]
            ]),
            disable_web_page_preview=True
        )

    elif query.data == 'about_command':
        bot_info = await bot.get_me()
        await query.message.edit(
            ABOUT_TEXT.format(bot_info.mention(style='md')),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('🏠 Home', callback_data='start_command'),
                 InlineKeyboardButton('🏷️ Help', callback_data='help_command')],
                [InlineKeyboardButton('📴 Close', callback_data='delete')]
            ]),
            disable_web_page_preview=True
        )

    elif query.data == 'start_command':
        new_user = await get_user(query.from_user.id)
        welcome_message = START_MESSAGE.format(query.from_user.mention, new_user["method"])

        # Directly use the start command reply markup
        await query.message.edit(welcome_message, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('🏷️ Help', callback_data='help_command'),
             InlineKeyboardButton('📝 About', callback_data='about_command')],
            [InlineKeyboardButton('📴 Close', callback_data='delete')]
        ]), disable_web_page_preview=True)

    elif query.data == 'alias_conf':
        await query.message.edit(CUSTOM_ALIAS_MESSAGE, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('◀️ Back', callback_data='help_command')]
        ]), disable_web_page_preview=True)

    elif query.data == 'admins_list':
        if user_id not in ADMINS:
            return await query.message.edit("This feature is only available to admins.", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('◀️ Back', callback_data='help_command')]
            ]))

        admin_list = await h.get_admins()
        await query.message.edit(ADMINS_MESSAGE.format(admin_list=admin_list), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('◀️ Back', callback_data='help_command')]
        ]))

    elif query.data == 'restart':
        await query.message.edit('**Restarting...**')
        await asyncio.sleep(5)
        os.execl(sys.executable, sys.executable, *sys.argv)

    await query.answer()
