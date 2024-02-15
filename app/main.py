from config import TOKEN, bot
from commands import bot as bot_commands
from events import Events


@bot.event
async def on_ready():
    events_cog = Events(bot)
    await events_cog.on_ready()


bot.add_cog(Events(bot))
bot.add_cog(bot_commands)
bot.run(TOKEN)
