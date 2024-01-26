from config import bot
import discord
from discord.ext import tasks
from reminder import TaskScheduler
from database.db_operations import get_task_by_id
import asyncio

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
	

@tasks.loop(seconds=5)
async def remind_tasks():
	channel_id = 1198117804130435092
	channel = bot.get_channel(channel_id)
	#print("Checking for tasks...")
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