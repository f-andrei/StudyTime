import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio
from dotenv import load_dotenv
import os
import sqlite3
from pytz import timezone
from tasks import Task
from pathlib import Path
from utils import new_task_filter
from database.db_operations import get_task_by_id, save_repeat_days_to_database, get_all_tasks, get_due_tasks
from time import sleep
from reminder import TaskScheduler


load_dotenv()
token = os.getenv('DISCORD_TOKEN')


ROOT_DIR = Path(__file__).parent.parent
DB_DIR = 'database'
DB_NAME = 'studytime.sqlite3'
DB_FILE = ROOT_DIR / DB_DIR / DB_NAME
BOT_NICKNAMES = ['.bot', '.study', '.studytime']
REPEAT_TIMES = [5, 10, 15] # How many times message will repeat before starting it
REPEAT_AFTER = 300 # How many seconds between repeat times

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

task_scheduler = TaskScheduler()

@bot.event
async def on_ready():
	servers_count = 0
	for server in bot.guilds:
		print(f"- {server.id} (name: {server.name})")
		servers_count = servers_count + 1

	print("StudyTime bot is in " + str(servers_count) + " servers.")
	remind_tasks.start()
	statusloop.start()
	

@bot.event
async def on_message(message):
	if any(nickname.lower() in message.content.lower() for nickname in BOT_NICKNAMES):
		print(message.content)
		await message.channel.send(f"hey {message.author.mention}")

	await bot.process_commands(message)


@bot.command()
async def create_task(ctx):
	try:
		current_time = datetime.now()
		five_minutes_later = current_time + timedelta(minutes=5)
		formatted_datetime = five_minutes_later.strftime("%Y-%m-%dT%H:%M:%S")
		await ctx.send(embed=discord.Embed(
			title="Create Task",
			colour=discord.Color.yellow(),
			description="**Required Fields**\n"
						"***Name***\n```Study```\n"
						"***Description***\n```Study Python```\n"
						"***Start Date***\n```2024-01-21T21:00:00```\n"
						"***Duration (minutes)***\n```30```\n"
						"***Is Repeatable (1 or 0) for True or False***\n```1```\n"
						"***Example Usage***\n"
						f"```Study, Study Python, {formatted_datetime}, 30, 1```\n"
						"*Ensure that the string above is passed to the program as "
						"a single, continuous sequence with each value separated by commas.*"))
		await ctx.send("Waiting for your message containing the required fields...")
		while True:
			msg = await bot.wait_for("message")
			if (msg.author == ctx.author):
				new_task = msg.content
				new_task = str(new_task)
				break
		task = Task()
		filtered_task = new_task_filter(new_task)
		task.create_task(*filtered_task)
		_, _, _, _, is_repeatable = filtered_task
		if is_repeatable == 1:
			view=DaysToRepeatView()
			await ctx.send("Select which days to repeat", view=view)
		else:
			await ctx.send('Task created sucessfully.')
		return
	except Exception as e:
		print(f"Error in create_task(): {e}")


@bot.command()
async def update_task(ctx):
	try:
		channel_id = 1198117804130435092
		channel = bot.get_channel(channel_id)
		tasks = get_all_tasks()
		if not tasks:
			await channel.send("No tasks found.")
		notify_tasks = []
		await channel.send("These are your active tasks: ")

		for task in tasks:
			task_data = {
				"Task nº": f"```{task[0]}```",
				"Name": f"```{task[1]}```",
				"Start Date": f"```{task[3]}```",
			}
			notify_tasks.append(task_data)

		for i, task_data in enumerate(notify_tasks):
			embed = discord.Embed(colour=discord.Color.green(), title=f"Active task {i + 1}:")
			for key, value in task_data.items():
				embed.add_field(name=f"{key}", value=value, inline=False)
			await channel.send(embed=embed)
			sleep(0.5)

		await ctx.send("Please send the task id (Task nº)")
		while True:
			msg = await bot.wait_for("message")
			if (msg.author == ctx.author):
				task_id = msg.content
				task_id = int(task_id)
				break
		await channel.send("Type in the updated task info:"
				 f"```Study, Study Python, asdasdad, 30, 1```\n"
						"*Ensure that the string above is passed to the program as "
						"a single, continuous sequence with each value separated by commas.*")

		while True:
			task_msg = await bot.wait_for("message")
			if (task_msg.author == ctx.author):
				new_task_data = task_msg.content
				new_task_data = str(new_task_data)
				break
		await ctx.send(f"You typed {new_task_data}")
		task = Task()
		
		if task_data:
			filtered_task = new_task_filter(new_task_data)
			
			task.update_task(
				task_id,
				name=filtered_task[0],
				description=filtered_task[1],
				start_date=filtered_task[2],
				duration=filtered_task[3],
				is_repeatable=filtered_task[4]
			)
			
			await ctx.send(f'Task with ID {task_id} updated successfully.')
		else:
			await ctx.send(f'Task with ID {task_id} not found.')

	except Exception as e:
		print(f"Error in update_task(): {e}")


@bot.command()
async def delete_task(ctx, *, task_id):
	try:
		task = Task()
		task.delete_task(task_id)
		await ctx.send(f"Task deleted sucessfully.")
	except Exception as e:
		print(f"Error in delete_task(): {e}")


@bot.command(name='tasks')
async def all_tasks(ctx):
	try:
		channel_id = 1198117804130435092
		channel = bot.get_channel(channel_id)
		tasks = get_all_tasks()
		if not tasks:
			await channel.send("No tasks found.")
		notify_tasks = []
		for task in tasks:
			task_data = {
				"Task nº": f"```{task[0]}```",
				"Name": f"```{task[1]}```",
				"Description": f"```{task[2]}```",
				"Start Date": f"```{task[3]}```",
				"Duration": f"```{task[4]}```",
				"Is Repeatable": f"```{task[5]}```"
			}
			notify_tasks.append(task_data)

		for i, task_data in enumerate(notify_tasks):
			embed = discord.Embed(colour=discord.Color.green(), title=f"Active task {i + 1}:")
			for key, value in task_data.items():
				embed.add_field(name=f"{key}", value=value, inline=False)
			await channel.send(embed=embed)
			sleep(0.5)
	except Exception as e:
		print(f"Error in all_tasks(): {e}")



@tasks.loop(seconds=5)
async def remind_tasks():
	channel_id = 1198117804130435092
	channel = bot.get_channel(channel_id)
	print("Checking for tasks...")
	try:
		await task_scheduler.update_schedule()
		due_task_ids = await task_scheduler.get_due_task_ids()
		notify_tasks = []
		if due_task_ids:
			for task_id in due_task_ids:
				try:
					task_data = get_task_by_id(task_id)
					task_data = task_data[0]
					task_data = {
						"Task nº": f"```{task_data[0]}```",
						"Name": f"```{task_data[1]}```",
						"Description": f"```{task_data[2]}```",
						"Start Date": f"```{task_data[3]}```",
						"Duration": f"```{task_data[4]}```",
						"Is Repeatable": f"```{task_data[5]}```"
					}
					notify_tasks.append(task_data)
				except IndexError:
					due_task_ids.remove(task_id)
					print(f"IndexError: Task with ID {task_id} not found.")
		if notify_tasks:
			for i, task_data in enumerate(notify_tasks):
				embed = discord.Embed(colour=discord.Color.green(), title=f"Active task {i + 1}:")
				for key, value in task_data.items():
					embed.add_field(name=f"{key}", value=value, inline=False)
				await channel.send(embed=embed)
				await asyncio.sleep(295)
		task_scheduler.on_off(stop='true')
	except Exception as e:
		print(f"Error in remind_tasks(): {e}")


@tasks.loop(seconds=10)
async def statusloop():
	await bot.wait_until_ready()
	await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f".help"))
	await asyncio.sleep(10)
	await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"you study..."))
	await asyncio.sleep(10)


class DaysToRepeatView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.days = []

    @discord.ui.button(label="Monday", style=discord.ButtonStyle.blurple)
    async def monday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(1)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Tuesday", style=discord.ButtonStyle.blurple)
    async def tuesday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(2)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Wednesday", style=discord.ButtonStyle.blurple)
    async def wednesday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(3)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Thursday", style=discord.ButtonStyle.blurple)
    async def thursday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(4)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Friday", style=discord.ButtonStyle.blurple)
    async def friday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(5)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Saturday", style=discord.ButtonStyle.blurple)
    async def saturday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(6)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Sunday", style=discord.ButtonStyle.blurple)
    async def sunday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(0)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Reset All", style=discord.ButtonStyle.red)
    async def reset_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.clear()
        for child in self.children:
            if isinstance(child, discord.ui.Button) and child.label != "Reset All":
                child.disabled = False
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Send", style=discord.ButtonStyle.success)
    async def send(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel_id = 1198117804130435092
        channel = bot.get_channel(channel_id)
        save_repeat_days_to_database(self.days)
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)
        await channel.send(f"Task created successfully.")




bot.run(token)

