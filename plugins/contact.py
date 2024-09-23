import asyncio, traceback
from config import OWNER_ID
from pyrogram import filters, Client as app
from pyrogram.errors.exceptions.bad_request_400 import UserIsBlocked

@app.on_message(filters.command("contact"))
async def contactAdmin(bot, message):
    try:
        user = "@" + message.from_user.username if message.from_user.username else message.from_user.mention
        if not message.reply_to_message:
            return await message.reply("<blockquote><b>Please use the method described in the image to contact admin[.](https://telegra.ph/file/9a4039a2d602486cf1c00.jpg)</b></blockquote>")
        if not message.reply_to_message.text:
            return await message.reply("<blockquote><b>Please use the method described in the image to contact admin[.](https://telegra.ph/file/9a4039a2d602486cf1c00.jpg)</b></blockquote>")
        await bot.send_message(
            chat_id=OWNER_ID, 
            text=f"""<b>
From: {user}
Id: {message.chat.id}

{message.reply_to_message.text.html}</b>"""
        )
        userMsg = await bot.send_message(
            chat_id=message.chat.id,
            text="Your message has been successfully sent to Admin.",
            reply_to_message_id=message.reply_to_message.id
        )
        await asyncio.sleep(5)
        await userMsg.delete()
    except Exception as e:
        return await message.reply(f"<blockquote><b>Traceback Info:\n{traceback.format_exc()}\nError Text:\n{e}</b></blockquote>")

@app.on_message(filters.private & filters.user(OWNER_ID))
async def replyUser(bot, message):
    try:
        if message.reply_to_message:
            chat = int(message.reply_to_message.text.split("\n")[0][-10::])
            try:
                await bot.send_message(
                    chat_id=chat,
                    text=message.text
                )
                adminMsg = await message.reply(
                    text="Successfully sent reply to User.",
                    quote=True
                )
                await asyncio.sleep(5)
                await adminMsg.delete()
            except UserIsBlocked:
                return await message.reply(
                    text="User has blocked me."
                )
    except Exception as e:
        return await message.reply(
            text=f"<blockquote><b>Traceback Info:\n{traceback.format_exc()}\nError Text:\n{e}</b></blockquote>"
        )
"""
Author: StupidBoi
Telegram: https://t.me/StupidBoi69
"""
