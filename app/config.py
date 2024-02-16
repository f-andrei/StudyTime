from langchain_openai import ChatOpenAI
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_KEY")
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = 'database'
DB_NAME = 'studytime.sqlite3'
DB_FILE = os.path.join(ROOT_DIR, DB_DIR, DB_NAME)
DISCORD_ID = discord.Object(id=os.getenv('DISCORD_ID'))

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

model = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
