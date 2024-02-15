from datetime import datetime
from utils.dt_manager import DateTimeManager
import discord
from typing import List, Dict



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


def create_embed(notify_tasks) -> List[discord.Embed]:
    """Creates a Discord embed from given tasks"""
    embeds = []
    for i, task_data in enumerate(notify_tasks):
        embed = discord.Embed(colour=discord.Color.green(), title=f"Active task {i + 1}")
        for key, value in task_data.items():
            embed.add_field(name=f"{key}", value=value, inline=False)
        embeds.append(embed)
    return embeds


def creation_success_embed(data, title=None):
    if len(data) == 6:
        name, description, links, start_date, duration, is_repeatable = data
        embed = discord.Embed(colour=discord.Color.brand_green(), title=title)
        embed.add_field(name=f"Title", value=f"```{name}```", inline=False)
        embed.add_field(name=f"Description", value=f"```{description}```", inline=False)
        embed.add_field(name=f"Links", value=f"```{links}```", inline=False)
        embed.add_field(name=f"Start date", value=f"```{start_date}```", inline=False)
        embed.add_field(name=f"Duration", value=f"```{duration}```", inline=False)
        embed.add_field(name=f"Is repeatable", value=f"```{is_repeatable}```", inline=False)
        return embed
    else:
        name, description, links = data
        embed = discord.Embed(colour=discord.Color.brand_green(), title=title)
        embed.add_field(name=f"Title", value=f"```{name}```", inline=False)
        embed.add_field(name=f"Description", value=f"```{description}```", inline=False)
        embed.add_field(name=f"Links", value=f"```{links}```", inline=False)
        return embed

def get_all_notes_embed(all_notes):
    try:
        if all_notes:
            embeds = []
            for note in all_notes:
                embed = discord.Embed(colour=discord.Color.magenta(), title="Note")
                embed.add_field(name=f"ID", value=f"```{note[0]}```", inline=False)
                embed.add_field(name=f"Title", value=f"```{note[1]}```", inline=False)
                embed.add_field(name=f"Description", value=f"```{note[2]}```", inline=False)
                embed.add_field(name=f"Links", value=f"```{note[3]}```", inline=False)
                embed.add_field(name=f"Status", value=f"```{note[4]}```", inline=False)
                embed.add_field(name=f"Created at", value=f"```{note[5]}```", inline=False)
                embeds.append(embed)
            return embeds      
    except Exception as e:
         ...