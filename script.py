from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
Author: StupidBoi
Telegram: https://t.me/StupidBoi69
"""

START_MESSAGE = f'''<blockquote><b>Hello, {}!
I'm Adlinkfly-Shortener-Bot, designed to convert links directly from your {Config.BASE_SITE} account.

**Getting Started:**
1. Get DEVELOPER API from:
https://{Config.BASE_SITE}/member/tools/api

2. Copy your API Key.
3. Use the command /set_api followed by a space and your API Key (example below).

Example: /set_api 20eb8456008878c0349fc79d40fb4d1634cccf12
'''

CREDIT_TEXT = """<blockquote><b>
Bot Information:
- 🤖 Name: {}
- 📝 Language: [Python 3](https://www.python.org/)
- 🧰 Framework: [Pyrogram](https://github.com/pyrogram/pyrogram)
- 👨‍💻 Developer: [StupidBoi69](https://t.me/StupidBoi69)
</b></blockquote>"""

CUSTOM_ALIAS_MESSAGE = """<b>To set a custom alias, use the format [link] | [custom_alias].

Note: Custom alias is only available in private mode.

Example: https://t.me/example | Example</b>
"""

ADMINS_MESSAGE = """
**Admins with Access:
{admin_list}**
"""

ALIAS_REPLY_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton('🏠 Home', callback_data='start_command')],
    [InlineKeyboardButton('🏷️ Credit', callback_data='credit_command')]
])

CREDIT_REPLY_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton('⏺️ Custom Alias', callback_data='alias_conf')],
    [InlineKeyboardButton('📴 Close', callback_data='delete')]
])

START_MESSAGE_REPLY_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton('🏷️ Credit', callback_data='credit_command')],
    [InlineKeyboardButton('📴 Close', callback_data='delete')]
])

BACK_REPLY_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton('◀️ Back', callback_data='help_command')]
])

USER_ABOUT_MESSAGE = f"""<b>
Account Information

- Base site: {Config.BASE_SITE}
- API Key: {shortener_api}
</b>"""

SHORTENER_API_MESSAGE = f"""<b>To set or update your API key, use the command:

/set_api [api]
Example: /set_api 20eb8456008878c0349fc79d40fb4d1634cccf12

Get your DEVELOPER API from:
https://{Config.BASE_SITE}/member/tools/api

Current API Key: {shortener_api}
</b>"""

BANNED_USER_TXT = """<b>
Ban or Unban Users:
- /ban [User ID]
- /unban [User ID]

Currently Banned Users:
{users}</b>
"""
