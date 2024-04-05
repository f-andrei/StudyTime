from __future__ import annotations
from discord import ui
import discord
from utils.dt_manager import DateTimeManager
from buttons import DaysToRepeatView
from tasks.tasks import Tasks
from config import DELETE_AFTER, TIMEZONE, BLURPLE_STYLE, GRAY_STYLE, RED_STYLE, SUCCESS_STYLE
from utils.embed_utils import display_embed

dt_manager = DateTimeManager(TIMEZONE)
task = Tasks()
five_from_dt_now = dt_manager.calculate_datetime(dt_manager.get_current_time(), 5)
five_from_dt_now = dt_manager.format_datetime(dt=five_from_dt_now, format="%d/%m/%Y %H:%M:%S")


class TaskModal(ui.Modal, title="Create task"):
	def __init__(self, action: str, task_id: int = None, channel_id = None) -> None:
		super().__init__()
		self.action = action
		self.task_id = task_id
		self.channel_id = channel_id

	name = ui.TextInput(label='Name', placeholder="Study",
						style=discord.TextStyle.short,
						max_length=50, required=False
						)
	description = ui.TextInput(label='Description', placeholder="Study Tensor Flow",
							    style=discord.TextStyle.paragraph,
								max_length=1000, required=False
								)
	links = ui.TextInput(label='Links', placeholder="https://www.discord.com",
						style=discord.TextStyle.short,
						required=False
						)
	start_date = ui.TextInput(label='Start Date',
							style=discord.TextStyle.short,
							min_length=19, max_length=19,
							placeholder=five_from_dt_now, required=False
							)
	duration = ui.TextInput(label='Duration (minutes)',
							style=discord.TextStyle.short,
							min_length=1, max_length=3,
							placeholder="60", required=False
							)

	async def on_submit(self, interaction: discord.Interaction) -> None:
			embed = discord.Embed(title=self.title, color = discord.Color.blue())
			embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)

			user_id = interaction.user.id

			if self.action == "create":
				self.start_date = str(self.start_date)
				self.start_date = self.start_date.split(" ")
				self.time = self.start_date[1]
				self.start_date = self.start_date[0]
				task_data = {
					"name": str(self.name),
					"description": str(self.description),
					"links": str(self.links),
					"start_date": str(self.start_date),
					"time": str(self.time),
					"duration": float(str(self.duration)),
					"user_id": str(user_id)
				}

				embed_2 = discord.Embed(
					title="Would you like to make this task repeat on multiple days?", 
					color=discord.Color.blue()
					)
				for i, item in enumerate(task_data):
					if item is None:
						embed_2.title="Unable to create task. Missing fields or invalid data."
						await interaction.response.send_message(
														embed=embed_2, 
														delete_after=DELETE_AFTER,
														ephemeral=True
														)
						return
			
				task_created = task.create_task(task_data=task_data)
				if 'detail' in task_created and task_created['detail'][0]['ctx']['error']:
					embed_2.title = "Unable to create task. Missing fields or invalid data."
					print(f"Error creating task: {task_created['detail'][0]['ctx']['error']}")
					await interaction.response.send_message(
													embed=embed_2, 
													delete_after=DELETE_AFTER, 
													ephemeral=True
													)
					return
				print(task_created)
				self.task_id = task_created["id"]
				button_view=IsRepeatable(embed_2, task_data, self.task_id, self.start_date, self.channel_id)
				await interaction.response.defer(thinking=True)
				msg:discord.Message = await interaction.followup.send(
																	embed=embed_2, 
																	view=button_view, 
																	ephemeral=True
																	)
				button_view.msg_id = msg.id

			if self.action == 'update':
				task_data = {}
				time = None
				field_names = ["name", "description", "links", "start_date", "duration"]
				fields_values = [
					self.name, 
					self.description, 
					self.links, 
					self.start_date, 
					self.duration
					]

				for field_name, field_value in zip(field_names, fields_values):
					field_value = str(field_value)
					if field_value is not None and field_value.strip() != "":
						if field_name == "start_date":
							start_date, time = field_value.split(" ")
							task_data["start_date"] = start_date
							task_data["time"] = time
						else:
							task_data[field_name] = field_value

				task_updated = task.update_task(task_data=task_data, task_id=self.task_id)


				if not task_updated:
					embed.title = "Unable to update task. Invalid data format."
					embed.description = None
					await interaction.response.send_message(
														embed=embed, 
														delete_after=DELETE_AFTER,
														ephemeral=True
														)
				else:
					embed.title = "Task updated!"
					embed.description = None
					await interaction.response.send_message(
													embed=embed, 
													delete_after=DELETE_AFTER,
													ephemeral=True
													)
					

class IsRepeatable(discord.ui.View):
	msg_id = None
	button: discord.ui.Button

	def __init__(self, embed, task_data, task_id, start_date, channel_id) -> None:
		super().__init__()
		self.is_repeatable = False
		self.embed = embed
		self.task_data = task_data
		self.task_id = task_id
		self.start_date = start_date
		self.channel_id = channel_id

	@discord.ui.button(label="Yes!", style=SUCCESS_STYLE)
	async def yes(self, interaction: discord.Interaction, button) -> None:
		self.is_repeatable = True
		button.disabled = True
		days_button_view = DaysToRepeatView(self.task_data, self.task_id, self.msg_id, self.channel_id)
		self.embed.title = "Which days would you like it to repeat?"
		await interaction.response.edit_message(
										embed=self.embed, 
										delete_after=DELETE_AFTER
										)
		await interaction.followup.edit_message(
										message_id=self.msg_id, 
										embed=self.embed, 
										view=days_button_view
										)

	
	@discord.ui.button(label="No, thanks!", style=GRAY_STYLE)
	async def no(self, interaction: discord.Interaction, button) -> None:
		self.is_repeatable = False
		button.disabled = True
		day_number = dt_manager.get_day_number(str(self.start_date))
		task.add_repeat_days(
			task_id=self.task_id, 
			repeat_days={"day_number": [day_number]}
			)
		last_task_id = self.task_id
		await display_embed(
			channel_id=self.channel_id,
			data=self.task_data, 
			task_id=last_task_id, 
			title="Task created sucessfully!", 
			del_after=86400, 
			type='task'
			)
		await interaction.response.edit_message(view=self.clear_items())
		await interaction.followup.delete_message(self.msg_id)


class EditTask(discord.ui.View):
	def __init__(self, task_data) -> None:	
		super().__init__()
		self.task_data = task_data
		self.task_id = task_data["id"]
		self.task = task.get_task(self.task_id)
		self.embed = discord.Embed()
	
	@discord.ui.button(label="Edit", style=BLURPLE_STYLE)
	async def edit(self, interaction: discord.Interaction, button) -> None:
		task_modal = TaskModal(action='update', task_id=self.task_id)
		button.disabled = True
		await interaction.response.send_modal(task_modal)

	@discord.ui.button(label="Delete", style=RED_STYLE)
	async def delete(self, interaction: discord.Interaction, button) -> None:
		if self.task:
			deleted = task.delete_task(self.task_id)
			if deleted:
				self.embed.title = "Task sucessfully deleted!"
				self.embed.color = discord.Color.red()
			else:
				self.embed.title = "Unable to delete task!"
		else:
			self.embed.title = f"Task doesn't exist or is already deleted."
			self.embed.color = discord.Color.red()
		button.disabled = True
		await interaction.response.send_message(embed=self.embed, ephemeral=True)
		await interaction.followup.delete_message(self.msg_id)