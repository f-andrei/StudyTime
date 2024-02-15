from config import bot, CHANNEL_ID
import discord
from discord.ext import tasks, commands
from tasks.reminder import TaskScheduler
from database.task_operations import get_task_by_id
import asyncio
from typing import List
from utils.embed_utils import create_embed, format_embed


class Events(commands.Cog):
	REMIND_LOOP_INTERVAL = 5
	STATUS_LOOP_INTERVAL = 10
	TASK_POSTPONE_INTERVAL = 295

	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot
		self.task_scheduler = TaskScheduler()
	
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


	async def notify_tasks(self, tasks: List[str], durations: List[float]) -> None:
		"""Task notifier (sends a message with an embed)"""
		try:
			channel = bot.get_channel(CHANNEL_ID)
			if tasks:
				print('NOTIFY')
				embeds = create_embed(tasks)
				for i, embed in enumerate(embeds):
					await channel.send(embed=embed)
					# right now it's blocking new tasks from notifying. Has to be fixed.
					duration = durations[i-1] * 60
					await asyncio.sleep(duration)
					# needs to be implemented
					await channel.send("duration")

			self.task_scheduler.toggle_scheduler(True)
		except IndexError as e:
			print(f"Error in remind_tasks(): {e}")

	@tasks.loop(seconds=REMIND_LOOP_INTERVAL)
	async def remind_tasks(self) -> None:
		"""Checks for new tasks every {REMIND_LOOP_INTERVAL}"""
		self.task_scheduler.running = True
		try:
			await self.task_scheduler.update_schedule()
			due_task_ids = await self.task_scheduler.get_due_task_ids()
			notify_tasks = []
			durations = []
			if due_task_ids:
				for task_id in due_task_ids:
					try:
						task_data = await asyncio.to_thread(get_task_by_id, task_id)
						task_data = task_data[0]
						formatted_task_data = format_embed(task_data=task_data)

						notify_tasks.append(formatted_task_data)
						durations.append(task_data[5])
					except IndexError:
						# Since this program is supposed to run continuously, the user may
						# decide to delete a task, in this case to avoid crashes, said
						# task will be removed from due tasks.
						due_task_ids.remove(task_id)
						self.task_scheduler.due_task_ids.clear()
						print(f"IndexError: Task with ID {task_id} not found.")
						if not due_task_ids:
							break
			await self.notify_tasks(notify_tasks, durations)
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
				name=f".help"))
		await asyncio.sleep(10)
		
		await self.bot.change_presence(
			status=discord.Status.online,
			activity=discord.Activity(
				type=discord.ActivityType.watching,
				name=f"you study..."))
		await asyncio.sleep(10)