from datetime import datetime
from utils.dt_manager import DateTimeManager
import discord
from config import CHANNEL_ID, bot, DELETE_AFTER
from database.task_operations import get_due_tasks_days

dt_manager = DateTimeManager('America/Sao_Paulo')
dt_now = datetime.now()


async def display_embed(data, id=None, title=None, type=None, del_after=None, color=discord.Color.brand_green()):
    channel = bot.get_channel(CHANNEL_ID)
    name = ""
    description = ""
    links = ""
    start_date = ""
    duration = ""
    is_repeatable = ""
    repeat_days = []
    repeat_days_list = []
    if type == 'task':
        match len(data):
            case 9:
                id, name, description, links, start_date, time, duration, user_id, repeat_days = data
            case 8:
                id, name, description, links, start_date, time, duration, user_id = data
            case 6:
                name, description, links, start_date, time, duration = data
            case 5:
                name, description, links, start_date, duration = data

    if type == 'note':
        match len(data):
            case 6:
                id, name, description, links, created_at, user_id = data
            case 5:
                id, name, description, links, created_at = data
            case 4:
                name, description, links, created_at = data
            case 3:
                name, description, links = data


    number_to_day = {
        6: "Sunday",
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday"
    }

    repeat_days = get_due_tasks_days(id)
    if repeat_days:
        try:
            for _, _, day in repeat_days:
                repeat_days_list.append(number_to_day[day])
            is_repeatable = repeat_days_list
            if len(is_repeatable) > 1:
                is_repeatable = ', '.join(is_repeatable)
            else:
                is_repeatable = is_repeatable[0]
        except Exception as e:
            print(f"Error at display_embeds: {e}")
    else:
        is_repeatable = 'Not repeatable'
    if type == 'task':
        fields = {
            "Name": name, 
            "Description": description, 
            "Links": links, 
            "Start date": start_date,
            "Time": time,
            "Duration": duration,
            "Repeat days": is_repeatable
            }
        
    if type == 'note':
        fields = {"Name": name, "Description": description, "Links": links}
    embed = discord.Embed(colour=color, title=title)
    for field, value in fields.items():
        if not value:
            value = ' '
        embed.add_field(name=field, value=f"```{value}```", inline=False)
    if del_after:
        delete_time = del_after
    else:
        delete_time = DELETE_AFTER
    await channel.send(embed=embed, delete_after=delete_time)
    return
