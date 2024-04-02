from utils.dt_manager import DateTimeManager
import discord
from config import DELETE_AFTER
from tasks.tasks import Tasks
from config import TIMEZONE, channel
from typing import Dict, Any

dt_manager = DateTimeManager(TIMEZONE)


async def display_embed(
        data: Dict[str, Any], 
        task_id: int = None, 
        title: str = None, 
        type: str = None, 
        del_after: int = None, 
        user_id: int = None, 
        color=discord.Color.brand_green()
        ) -> None:
    
    repeat_days = []
    repeat_days_list = []
    
    if type == 'task':
        fields = {
            "Name": data["name"], 
            "Description": data["description"], 
            "Links": data["links"], 
            "Start date": data["start_date"], 
            "Time": data["time"], 
            "Duration": data["duration"], 
        }
        number_to_day = {
            6: "Sunday",
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday"
        }
        tasks = Tasks()
        if not task_id:
            task_id = data["id"]
        repeat_days = tasks.get_repeat_days(task_id)
        if repeat_days:
            try:
                for i in range(len(repeat_days)):
                    day = repeat_days[i]["day_number"]
                    repeat_days_list.append(number_to_day[day])

                is_repeatable = repeat_days_list
                if len(is_repeatable) > 1:
                    is_repeatable = ', '.join(is_repeatable)
                else:
                    is_repeatable = is_repeatable[0]
            except Exception as e:
                print(f"Error at display_embeds: {e}")
                raise e
        else:
            is_repeatable = 'Not repeatable'

        fields["Repeat days"] = is_repeatable
        

    if type == 'note':
       fields = {
           "Name": data["name"],
           "Description": data["description"],
           "Links": data["links"],
           "Created at": data["created_at"],
       }

    embed = discord.Embed(colour=color, title=title)
    for field, value in fields.items():
        if not value:
            value = ' '
        embed.add_field(name=field, value=f"```{value}```", inline=False)
    if del_after:
        delete_time = del_after
    else:
        delete_time = DELETE_AFTER
    
    if user_id:
        mention = f"Hey <@{user_id}>"
        await channel.send(mention, delete_after=delete_time)
    await channel.send(embed=embed, delete_after=delete_time)
