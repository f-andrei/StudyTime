import discord
from discord.ext import tasks, commands
from tasks.reminder import TaskScheduler
from config import REMIND_LOOP_INTERVAL, STATUS_LOOP_INTERVAL
import asyncio
from typing import List
from utils.embed_utils import display_embed
from tasks.tasks import Tasks

class Events(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot
		self.task_scheduler = TaskScheduler()
		self.task = Tasks()

	async def on_ready(self) -> None:
		"""Starts status loop and task reminder when ready."""
		servers_count = 0
		for server in self.bot.guilds:
			print(f"- {server.id} (name: {server.name})")
			servers_count = servers_count + 1
			print(f"StudyTime bot is in {servers_count} servers!")

			# Starts task status loop (discord status)
			if not self.statusloop.is_running():
				self.statusloop.start()
			# Starts task reminder
			if not self.remind_tasks.is_running():
				self.remind_tasks.start()


	async def notify_tasks(self, task: dict, duration: List[float]) -> None:
		"""Task notifier (sends a message with an embed)"""
		try:
			if task:
				print('NOTIFY')
				duration = duration[0] * 60
				await display_embed(
					data=task, 
					title="Task is due!", 
					user_id=task["user_id"], 
					del_after=duration, 
					color=discord.Color.from_rgb(255, 92, 80),
					type='task',
					)
				await asyncio.sleep(duration)

				title="Task ended."
				
				await display_embed(
					data=task, 
					title=title, 
					user_id=task["user_id"], 
					color=discord.Color.from_rgb(46, 204, 113),
					del_after=86400, 
					type='task',
					)

			self.task_scheduler.toggle_scheduler(True)
		except IndexError as e:
			print(f"Error in notify_tasks(): {e}")

	@tasks.loop(seconds=REMIND_LOOP_INTERVAL)
	async def remind_tasks(self) -> None:
		"""Checks for new tasks every {REMIND_LOOP_INTERVAL}"""
		self.task_scheduler.running = True
		try:
			await self.task_scheduler.update_schedule()
			due_task_ids = await self.task_scheduler.get_due_task_ids()
			notify_tasks = []
			duration = []
			if due_task_ids:
				for task_id in due_task_ids:
					try:
						task_data = await asyncio.to_thread(self.task.get_task, task_id)
						if task_data:
							notify_tasks.append(task_data)
							duration.append(task_data["duration"])
					except IndexError:
						due_task_ids.remove(task_id)
						self.task_scheduler.due_task_ids.clear()
						print(f"IndexError: Task with ID {task_id} not found.")
						if not due_task_ids:
							break
			if notify_tasks:
				await self.notify_tasks(task=notify_tasks[0], duration=duration)
		except IndexError as e:
			print(f"Error in remind_tasks(): {e}")


	@tasks.loop(seconds=STATUS_LOOP_INTERVAL)
	async def statusloop(self) -> None:
		"""Discord status loop"""
		await self.bot.wait_until_ready()
		await self.bot.change_presence(
			status=discord.Status.online,
			activity=discord.Activity(
				type=discord.ActivityType.watching,
				name=f".help"
				)
			)
		await asyncio.sleep(10)
		
		await self.bot.change_presence(
			status=discord.Status.online,
			activity=discord.Activity(
				type=discord.ActivityType.watching,
				name=f"you study..."
				)
			)
		await asyncio.sleep(10)