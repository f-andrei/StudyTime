import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timezone
from pytz import timezone
import os

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = 'database'
DB_NAME = 'studytime.sqlite3'
DB_FILE = os.path.join(ROOT_DIR, DB_DIR, DB_NAME)


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

CHANNEL_ID = 1198117804130435092

SAO_PAULO_TZ = timezone('America/Sao_Paulo')
CURRENT_TIME_UTC = datetime.utcnow()
SAO_PAULO_NOW = CURRENT_TIME_UTC.replace(tzinfo=timezone('UTC')).astimezone(SAO_PAULO_TZ)
