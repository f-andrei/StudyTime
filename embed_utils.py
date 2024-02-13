from datetime import datetime
from dt_manager import DateTimeManager
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
                    ***Start Date***\n```06/02/2024 12:00:00```\n
                    ***Duration in minutes (min 5)***\n```5```\n
                    ***Is Repeatable (1 or 0) for True or False***\n```1```\n
                    ***Example Usage***\n
                    ```Study, Study Python, {formatted_dt}, 5, 1```\n
                    *Ensure that the string above is passed to the program as 
                    a single, continuous sequence with each value separated by commas.*"""
        return description
    formatted_task_data = {
        "Task nº": f"```{task_data[0]}```",
        "Name": f"```{task_data[1]}```",
        "Description": f"```{task_data[2]}```",
        "Start Date": f"```{task_data[3]}```",
        "Duration": f"```{task_data[4]}```",
        "Is Repeatable": f"```{task_data[5]}```"
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