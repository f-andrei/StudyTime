from utils.dt_manager import DateTimeManager
import discord
from config import DELETE_AFTER, bot
from tasks.tasks import Tasks
from config import TIMEZONE
from typing import Dict, Any, Literal, Optional
from users.users import User

dt_manager = DateTimeManager(TIMEZONE)

async def display_embed(
        data: Dict[str, Any], 
        type: Optional[Literal["note", "task"]], 
        title: Optional[str] = None, 
        task_id: Optional[int] = None, 
        user_id: Optional[int] = None, 
        del_after: Optional[int] = None, 
        channel_id: Optional[int] = None,
        color=discord.Color.brand_green(),
        ) -> None:
    
    repeat_days = []
    repeat_days_list = []
    
    if type == 'task':
        fields = {
            "Name": data["name"], 
            "Description": data["description"], 
            "Links": data["links"], 
            "Start date": dt_manager.format_datetime(dt=data["start_date"], format="%d/%m/%Y"), 
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
           "Created at": dt_manager.format_datetime(dt=data["created_at"], format="%d/%m/%Y %H:%M:%S"),
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
    
    user = User()
    channel_id = user.get_channel_id(user_id=str(user_id))
    if channel_id:
        channel = bot.get_channel(int(channel_id))
        await channel.send(embed=embed, delete_after=delete_time)
    else:
        return "No channel ID"