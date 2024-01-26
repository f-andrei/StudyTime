# main.py
from config import TOKEN, bot
import discord
# from discord.ext import commands
from commands import bot as bot_commands
from events import Events
import asyncio

# startup_extensions = ["events"]

@bot.event
async def on_ready():
    events_cog = Events(bot)
    await events_cog.on_ready()


bot.add_cog(Events(bot))
bot.add_cog(bot_commands)
bot.run(TOKEN)
