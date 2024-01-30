import discord
from datetime import datetime, timedelta
from config import bot, CHANNEL_ID
from utils import new_task_filter
from tasks import Task
from buttons import DaysToRepeatView
from database.db_operations import get_all_tasks
from time import sleep

@bot.command(aliases=['bot', 'studybot', 'study'])
async def greet(ctx):
	try:
		await ctx.send(f'Hey {ctx.author.mention}')
	except Exception as e:
		print(f"Error at greet {e}")

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
		channel = bot.get_channel(CHANNEL_ID)
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
async def all_tasks(ctx) -> None:
	try:
		channel = bot.get_channel(CHANNEL_ID)
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
		
