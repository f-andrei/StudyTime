from langchain_openai import ChatOpenAI
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
DISCORD_ID = discord.Object(id=os.getenv('DISCORD_ID'))
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DATABASE_API_URL = os.getenv("DATABASE_API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_TOKEN")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = 'database'
DB_NAME = 'studytime.sqlite3'
DB_FILE = os.path.join(ROOT_DIR, DB_DIR, DB_NAME)

TIMEZONE = 'America/Sao_Paulo'

DELETE_AFTER = 60

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

model = ChatOpenAI(model="gpt-4-turbo-preview", api_key=OPENAI_API_KEY)
