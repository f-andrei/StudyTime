from langchain_openai import ChatOpenAI
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

# DISCORD TOKEN
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Database's API URL (assuming you've deployed it to heroku using this API: 
# https://github.com/f-andrei/fast-api-tasks-notes-crud)

DATABASE_API_URL = os.getenv("DATABASE_API_URL")

# To run locally use your localhost
#DATABASE_API_URL = "http://127.0.0.1:8000" 

# Openai's API key
OPENAI_API_KEY = os.getenv("OPENAI_TOKEN")


TIMEZONE = 'America/Sao_Paulo'

# Time for Bot messages to get deleted
DELETE_AFTER = 180
# Delay for listing tasks/notes
MESSAGE_DELAY = 0.5
# Discord's task loop interval for checking new tasks
REMIND_LOOP_INTERVAL = 15
# Interval to update Bot's status ("watching you study...", "watching .help")
STATUS_LOOP_INTERVAL = 10
# Task scheduler interval 
SLEEP_DURATION = 20

# Discord's button colors
BLURPLE_STYLE = discord.ButtonStyle.blurple
RED_STYLE = discord.ButtonStyle.red
SUCCESS_STYLE = discord.ButtonStyle.success
SUCCESS_STYLE = discord.ButtonStyle.success
GRAY_STYLE = discord.ButtonStyle.gray


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

model = ChatOpenAI(model="gpt-4-turbo-preview", api_key=OPENAI_API_KEY)
