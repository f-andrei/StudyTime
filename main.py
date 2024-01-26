from config import bot, TOKEN
from commands import bot as commands_bot
from events import bot as events_bot
from buttons import bot as buttons_bot


if __name__ == '__main__':
    bot.add_cog(commands_bot)
    bot.add_cog(events_bot)
    bot.add_cog(buttons_bot)
    bot.run(TOKEN)