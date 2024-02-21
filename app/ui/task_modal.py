from __future__ import annotations
from discord import ui
import discord
from utils.dt_manager import DateTimeManager
from buttons import DaysToRepeatView
from tasks.tasks import Task
from database.task_operations import delete_task_from_database, get_last_task, get_task_by_id, save_repeat_days_to_database
from config import DELETE_AFTER
from utils.embed_utils import display_embed

dt_manager = DateTimeManager('America/Sao_Paulo')
five_from_dt_now = dt_manager.calculate_datetime(dt_manager.get_current_time(), 5)
five_from_dt_now = dt_manager.format_datetime(five_from_dt_now)

class TaskModal(ui.Modal, title="Create task"):
	def __init__(self, action: str, task_id: int = None) -> None:
		super().__init__()
		self.action = action
		self.task_id = task_id
	name = ui.TextInput(label='Name', placeholder="Study",
								style=discord.TextStyle.short,
								max_length=50, required=False)
	description = ui.TextInput(label='Description', placeholder="Study Tensor Flow",
										style=discord.TextStyle.paragraph,
										max_length=1000, required=False)
	links = ui.TextInput(label='Links', placeholder="https://www.discord.com",
								style=discord.TextStyle.short,
								required=False)
	start_date = ui.TextInput(label='Start Date',
									style=discord.TextStyle.short,
									min_length=19, max_length=19,
									placeholder=five_from_dt_now, required=False)
	duration = ui.TextInput(label='Duration (minutes)',
									style=discord.TextStyle.short,
									min_length=1, max_length=3,
									placeholder="60", required=False)

	async def on_submit(self, interaction: discord.Interaction):
			embed = discord.Embed(title=self.title, color = discord.Color.blue())
			embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
			task = Task()
			user_id = interaction.user.id
			
			task_data = [self.name, self.description, self.links, self.start_date, self.duration]
			for i, item in enumerate(task_data):
				if len(str(item)) >= 1:
					task_data[i] = str(item)
				else:
					task_data[i] = None

			if self.action == 'create':
				embed_2 = discord.Embed(title="Would you like to make this task repeat on multiple days?", color=discord.Color.blue())
				for i, item in enumerate(task_data):
					if item is None:
						embed_2.title="Unable to create task. Missing fields or invalid data format."
						await interaction.response.send_message(embed=embed_2, delete_after=DELETE_AFTER)
						return
			
				task_created = task.create_task(*task_data, user_id)
				if not task_created:
					embed_2.title = "Unable to create task. Missing fields or invalid data format."
					await interaction.response.send_message(embed=embed_2, delete_after=DELETE_AFTER)
					return
				
				button_view=IsRepeatable(embed_2, task_data, self.task_id, self.start_date)
				await interaction.response.defer(thinking=True)
				msg:discord.Message = await interaction.followup.send(embed=embed_2, view=button_view)
				button_view.msg_id = msg.id

			if self.action == 'update':
				task_updated = task.update_task(self.task_id, *task_data)
				if not task_updated:
					embed.title = "Unable to update task. Invalid data format."
					embed.description = None
					await interaction.response.send_message(embed=embed, delete_after=DELETE_AFTER)
				else:
					embed.title = "Task updated!"
					embed.description = None
					await interaction.response.send_message(embed=embed, delete_after=DELETE_AFTER)


class IsRepeatable(discord.ui.View):
	SUCCESS_STYLE = discord.ButtonStyle.success
	GRAY_STYLE = discord.ButtonStyle.gray
	msg_id = None
	def __init__(self, embed, task_data, task_id, start_date) -> None:
		super().__init__()
		self.is_repeatable = False
		self.embed = embed
		self.task_data = task_data
		self.task_id = task_id
		self.start_date = start_date

	@discord.ui.button(label="Yes!", style=SUCCESS_STYLE)
	async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.is_repeatable = True
		button.disabled = True
		last_task_created = get_last_task()
		last_task_id = last_task_created
		days_button_view = DaysToRepeatView(self.task_data, last_task_id, self.msg_id)
		self.embed.title = "Which days would you like it to repeat?"
		await interaction.response.edit_message(embed=self.embed, delete_after=DELETE_AFTER)
		await interaction.followup.edit_message(message_id=self.msg_id, embed=self.embed, view=days_button_view)

	
	@discord.ui.button(label="No, thanks!", style=GRAY_STYLE)
	async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.is_repeatable = False
		button.disabled = True
		day_number = dt_manager.get_day_number(str(self.start_date))
		save_repeat_days_to_database([day_number])
		last_task_created = get_last_task()
		last_task_id = last_task_created
		await display_embed(self.task_data, last_task_id, title="Task created sucessfully!", del_after=86400, type='task')
		await interaction.response.edit_message(view=self.clear_items())
		await interaction.followup.delete_message(self.msg_id)

class EditTask(discord.ui.View):
	BLURPLE_STYLE = discord.ButtonStyle.blurple
	RED_STYLE = discord.ButtonStyle.red
	SUCCESS_STYLE = discord.ButtonStyle.success

	def __init__(self, task_data) -> None:	
		super().__init__()
		self.task_data = task_data
		self.task_id = task_data[0]
		self.task = get_task_by_id(self.task_id)
		self.embed = discord.Embed()
	
	@discord.ui.button(label="Edit", style=BLURPLE_STYLE)
	async def edit(self, interaction: discord.Interaction, button: discord.ui.Button):
		task_modal = TaskModal(action='update', task_id=self.task_id)
		button.disabled = True
		await interaction.response.send_modal(task_modal)

	@discord.ui.button(label="Delete", style=RED_STYLE)
	async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
		if self.task:
			deleted = delete_task_from_database(self.task_id)
			if deleted:
				self.embed.title = "Task sucessfully deleted!"
				self.embed.color = discord.Color.red()
			else:
				self.embed.title = "Unable to delete task!"
		else:
			self.embed.title = f"Task doesn't exist or is already deleted."
			self.embed.color = discord.Color.red()
		button.disabled = True
		await interaction.response.send_message(embed=self.embed)
		await interaction.followup.delete_message(self.msg_id)