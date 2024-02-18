from datetime import datetime
from utils.dt_manager import DateTimeManager
import discord
from typing import Dict
from config import CHANNEL_ID, bot
from database.task_operations import get_due_tasks_days

dt_manager = DateTimeManager('America/Sao_Paulo')
dt_now = datetime.now()


def format_embed(task_data=None) -> str | Dict[str, str]:
    """Formats a static or dynamic Discord embed"""
    if not task_data:
        dt_one_min_added = dt_manager.calculate_datetime(dt_now, 1)
        formatted_dt = dt_manager.format_datetime(dt_one_min_added)
        description=f"""**Required Fields**\n
                    ***Name***\n```Study```\n
                    ***Description***\n```Study Python```\n
                    ***Links***\n```https://www.discord.com```\n
                    ***Start Date***\n```06/02/2024 12:00:00```\n
                    ***Duration in minutes (min 5)***\n```5```\n
                    ***Is Repeatable (1 or 0) for True or False***\n```1```\n
                    ***Example Usage***\n
                    ```Study, Study Python, https://www.discord.com, {formatted_dt}, 5, 1```\n
                    *Ensure that the string above is passed to the program as 
                    a single, continuous sequence with each value separated by commas.*"""
        return description
    formatted_task_data = {
        "Task nº": f"```{task_data[0]}```",
        "Name": f"```{task_data[1]}```",
        "Description": f"```{task_data[2]}```",
        "Links": f"```{task_data[3]}```",
        "Start Date": f"```{task_data[4]}```",
        "Duration": f"```{task_data[5]}```",
        "Is Repeatable": f"```{task_data[6]}```"
						}
    return formatted_task_data


async def display_embed(data, id=None, title=None, color=discord.Color.brand_green()):
    channel = bot.get_channel(CHANNEL_ID)
    name = ""
    description = ""
    links = ""
    start_date = ""
    duration = ""
    is_repeatable = ""
    repeat_days = []
    repeat_days_list = []
    match len(data):
        case 8:
            id, name, description, links, start_date, duration, is_repeatable, is_repeatable = data
        case 7:
            name, description, links, start_date, duration, is_repeatable, repeat_days = data
        case 6:
            name, description, links, start_date, duration, is_repeatable = data
        case 5:
            name, description, links, status, created_at = data
        case 3:
            name, description, links = data
        case n if n > 8:
            id, name, description, links, start_date, duration, is_repeatable, *repeat_days = data

    number_to_day = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday"
    }

    repeat_days = get_due_tasks_days(id)
    if repeat_days:
        try:
            for _, day in repeat_days:
                repeat_days_list.append(number_to_day[day])
            is_repeatable = repeat_days_list
            if len(is_repeatable) > 1:
                is_repeatable = ', '.join(is_repeatable)
            else:
                is_repeatable = is_repeatable[0]
        except Exception as e:
            print(e)
    else:
        is_repeatable = 'Not repeatable'
    if len(data) > 5:
        fields = {
            "ID": id,
            "Title": name, 
            "Description": description, 
            "Links": links, 
            "Start date": start_date, 
            "Duration": duration,
            "Repeat days": is_repeatable
            }
    else:
        fields = {"Title": name, "Description": description, "Links": links}
    embed = discord.Embed(colour=color, title=title)
    for field, value in fields.items():
        embed.add_field(name=field, value=f"```{value}```", inline=False)
    await channel.send(embed=embed)
    return 'success'

def get_all_notes_embed(all_notes):
    try:
        if all_notes:
            embeds = []
            for note in all_notes:
                embed = discord.Embed(colour=discord.Color.magenta(), title="Note")
                fields = ["ID", "Title", "Description", "Links", "Status", "Created at"]
                for i, field in enumerate(fields):
                    embed.add_field(name=field, value=f"```{note[i]}```", inline=False)
                embeds.append(embed)
            return embeds      
    except Exception as e:
        print(f"Error at get_all_notes_embed(): {e}")