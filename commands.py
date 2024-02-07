import discord
from datetime import datetime, timedelta
from config import bot, CHANNEL_ID, DISCORD_ID
from utils import new_task_filter, format_embed, create_embed
from database.db_operations import delete_task_from_database, get_task_by_id
from tasks import Task
from buttons import DaysToRepeatView
from database.db_operations import get_all_tasks
from discord.ext import commands
from discord import app_commands
from time import sleep
from dt_manager import DateTimeManager

TIMEZONE = 'America/Sao_Paulo'
dt_manager = DateTimeManager(TIMEZONE)

@bot.command(aliases=['bot', 'studybot', 'study'])
async def greet(ctx):
	try:
		await ctx.send(f'Hey {ctx.author.mention}')
	except Exception as e:
		print(f"Error at greet {e}")

@bot.hybrid_command(name="create_task", description="Create a new task")
@app_commands.guilds(DISCORD_ID)
async def create_task(ctx):
	"""Create task command"""
	await ctx.defer(ephemeral=True)
	try:
		# Creates an embed exampling a task creation
		await ctx.send(embed=discord.Embed(
			title="Create Task",
			colour=discord.Color.yellow(),
			description=format_embed()))
		await ctx.send("Waiting for your message containing the required fields...")
		
		# Waits for the user's next message containing a single string with all task data
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

		# If true, will be shown days of the week as buttons to select repeat days
		if is_repeatable == 1:
			view=DaysToRepeatView()
			await ctx.send("Select which days to repeat", view=view)
		else:
			await ctx.send('Task created sucessfully.')
		return
	except Exception as e:
		print(f"Error in create_task(): {e}")


@bot.hybrid_command(name="update_task", description="Update an existing task")
@app_commands.guilds(DISCORD_ID)
async def update_task(ctx):
	"""Update task command"""
	await ctx.defer(ephemeral=True)
	try:
		current_time = datetime.now()
		one_minute_later = current_time + timedelta(minutes=1)
		channel = bot.get_channel(CHANNEL_ID)

		# Checks the database for existing tasks
		tasks = get_all_tasks()
		if not tasks:
			await ctx.reply("No tasks found.")
			return
		notify_tasks = []
		await channel.send("These are your active tasks: ")

		# Loop through all tasks and append basic info to notify tasks
		for task in tasks:
			task_data = {
				"Task nº": f"```{task[0]}```",
				"Name": f"```{task[1]}```",
				"Start Date": f"```{task[3]}```",
			}
			notify_tasks.append(task_data)

		# Create an embed for each task in notify_tasks
		embeds = create_embed(notify_tasks)
		for embed in embeds:
			await channel.send(embed=embed)
			sleep(0.3)
		await channel.send("Which task would you like to update? (Task nº)")

		# Waits for the user's next message containing the task's id to be updated
		while True:
			msg = await bot.wait_for("message")
			if (msg.author == ctx.author):
				task_id = msg.content
				task_id = int(task_id)
				break
		await channel.send("Type in the updated task info:"
				 f"```Study, Study Python, {one_minute_later}, 30, 1```\n"
						"*Ensure that the string above is passed to the program as "
						"a single, continuous sequence with each value separated by commas.*")
		# Waits for the user's next message containing the new task data as a single string
		while True:
			task_msg = await bot.wait_for("message")
			if (task_msg.author == ctx.author):
				new_task_data = task_msg.content
				new_task_data = str(new_task_data)
				break

		task = Task()
		
		if task_data:
			# Filters and validate the new task data
			filtered_task = new_task_filter(new_task_data)
			
			task.update_task(
				task_id,
				name=filtered_task[0],
				description=filtered_task[1],
				start_date_str=filtered_task[2],
				duration=filtered_task[3],
				is_repeatable=filtered_task[4]
			)
			
			await ctx.send(f'Task with ID {task_id} updated successfully.')
		else:
			await ctx.send(f'Task with ID {task_id} not found.')

	except Exception as e:
		print(f"Error in update_task(): {e}")


@bot.hybrid_command(name="delete_task", description="Delete a task by its ID")
@app_commands.guilds(DISCORD_ID)
async def delete_task(ctx, *, task_id):
	"""Deletes a task by its ID"""
	await ctx.defer(ephemeral=True)
	try:
		# Check if task exists before attempting to delete it
		task = get_task_by_id(task_id)
		if not task:
			await ctx.send(f"Task with ID {task_id} does not exist.")
			return
		delete_task_from_database(task_id)
		await ctx.send(f"Task with ID {task_id} deleted sucessfully.")
	except Exception as e:
		print(f"Error in delete_task(): {e}")


@bot.hybrid_command(name="tasks", description="List all active tasks")
@app_commands.guilds(DISCORD_ID)
async def all_tasks(ctx: commands.Context) -> None:
	"""List all active tasks"""
	await ctx.defer(ephemeral=True)
	try:
		# Checks if exist tasks
		tasks = get_all_tasks()
		if not tasks:
			await ctx.reply("No tasks found.")
		notify_tasks = []
		
		# Appends each embed to notify tasks
		for task in tasks:
			task_data = format_embed(task)
			notify_tasks.append(task_data)

		# Create an embed for each task
		embeds = create_embed(notify_tasks)
		for embed in embeds:
			await ctx.send(embed=embed)
			sleep(0.3)

	except Exception as e:
		print(f"Error in all_tasks(): {e}")

# sync new commands
@bot.command()
async def sync(ctx):
	await bot.tree.sync(guild=DISCORD_ID)
	print("synced")