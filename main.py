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
from database.db_operations import get_task_by_id, save_repeat_days_to_database, get_last_task

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


@bot.event
async def on_ready():
	servers_count = 0
	for server in bot.guilds:
		print(f"- {server.id} (name: {server.name})")
		servers_count = servers_count + 1

	print("StudyTime bot is in " + str(servers_count) + " servers.")
	check_tasks.start()
	statusloop.start()
	

@bot.event
async def on_message(message):
	if any(nickname.lower() in message.content.lower() for nickname in BOT_NICKNAMES):
		print(message.content)
		await message.channel.send(f"hey {message.author.mention}")

	if message.content == '.tasks':
		await message.channel.send(f"Hey {message.author.mention}, here are your tasks:")
		await check_tasks()

	await bot.process_commands(message)


@bot.command()
async def create_task(ctx):
	try:
		await ctx.send(embed=discord.Embed(
			title="Create Task",
			description="**Required Fields**\n"
						"***Name***\n```Study```\n"
						"***Description***\n```Study Python```\n"
						"***Start Date***\n```2024-01-21T21:00:00```\n"
						"***Duration (minutes)***\n```30```\n"
						"***Is Repeatable (1 or 0) for True or False***\n```1```\n"
						"***Example Usage***\n"
						"```Study, Study Python, 2024-01-21T21:00:00, 30, 1```\n"
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
		await ctx.send(f"An error occurred: {e}")


@bot.command()
async def update_task(ctx, task_id: int, *, new_task):
	try:
		task_data = get_task_by_id(task_id)
		task = Task()
		
		if task_data:
			filtered_task = new_task_filter(new_task)
			
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
		await ctx.send(f"An error occurred: {e}")


@bot.command()
async def delete_task(ctx, *, task_id):
	try:
		task = Task()
		task.delete_task(task_id)
		await ctx.send(f"Task deleted sucessfully.")
	except Exception as e:
		await ctx.send(f"An error occured: {e}")


@tasks.loop(seconds=300)
async def check_tasks():
	sao_paulo = timezone('America/Sao_Paulo')
	current_time_utc = datetime.utcnow()
	current_time_sao_paulo = current_time_utc.replace(tzinfo=timezone('UTC')).astimezone(sao_paulo)

	channel_id = 1198117804130435092
	channel = bot.get_channel(channel_id)
	print("Checking for tasks...")
	# Connect to the database
	with sqlite3.connect('database/studytime.sqlite3') as connection:
		try:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM tasks WHERE start_date BETWEEN ? AND ?",
				   (current_time_sao_paulo - timedelta(minutes=15), current_time_sao_paulo))
			due_tasks = cursor.fetchall()
			notify_tasks = []
			for task in due_tasks:
				task_data = f"""
					Task nº: {task[0]}
					Name: {task[1]}
					Description: {task[2]}
					Start date: {task[3]}
					Duration: {task[4]}
					Is repeatable: {task[5]}
				"""
				notify_tasks.append(task_data)
				await channel.send(f"""Reminder:
					Active tasks:
					{''.join(notify_tasks)}""")
		except Exception as e:
			await channel.send(f"An error occurred: {e}")


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
        save_repeat_days_to_database(self.days)
        await interaction.response.send_message(f"Task created sucessfully.")


bot.run(token)

