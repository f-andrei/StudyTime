from config import bot
import discord
from discord.ext import tasks, commands
from reminder import TaskScheduler
from database.db_operations import get_task_by_id
import asyncio


class Events(commands.Cog):
	REMIND_LOOP_INTERVAL = 5
	STATUS_LOOP_INTERVAL = 10
	TASK_POSTPONE_INTERVAL = 295
	CHANNEL_ID = 1198117804130435092

	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot
		self.task_scheduler = TaskScheduler()
		
	async def on_ready(self) -> None:
		servers_count = 0
		for server in self.bot.guilds:
			print(f"- {server.id} (name: {server.name})")
			servers_count = servers_count + 1

			print(f"StudyTime bot is in {servers_count} servers!")
			self.remind_tasks.start()
			self.statusloop.start()

	async def notify_tasks(self, tasks) -> None:
		try:
			channel = bot.get_channel(self.CHANNEL_ID)
			if tasks:
				for task_index, task_data in enumerate(tasks, start=1):
					embed = discord.Embed(colour=discord.Color.green(), title=f"Active task {task_index + 1}:")
					for key, value in task_data.items():
						embed.add_field(name=f"{key}", value=value, inline=False)
					await asyncio.gather(
						channel.send(embed=embed),
						asyncio.sleep(self.TASK_POSTPONE_INTERVAL))
			self.task_scheduler.on_off(stop='true')
		except IndexError as e:
			print(f"Error in remind_tasks(): {e}")

	@tasks.loop(seconds=REMIND_LOOP_INTERVAL)
	async def remind_tasks(self) -> None:
		print("Checking for tasks...")
		try:
			await self.task_scheduler.update_schedule()
			due_task_ids = await self.task_scheduler.get_due_task_ids()
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
			await self.notify_tasks(notify_tasks)
		except IndexError as e:
			print(f"Error in remind_tasks(): {e}")

	@tasks.loop(seconds=STATUS_LOOP_INTERVAL)
	async def statusloop(self) -> None:
		await self.bot.wait_until_ready()
		await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f".help"))
		await asyncio.sleep(10)
		await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"you study..."))
		await asyncio.sleep(10)