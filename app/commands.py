import discord
from datetime import datetime, timedelta
from config import bot, CHANNEL_ID, DISCORD_ID
from utils.utils import new_task_filter, new_note_filter
from database.task_operations import delete_task_from_database, get_task_by_id
from utils.embed_utils import format_embed, get_all_notes_embed, display_embed
from tasks.tasks import Task
from buttons import DaysToRepeatView
from database.task_operations import get_tasks_by_user_id, get_last_task
from discord.ext import commands
from discord import app_commands
from time import sleep
from utils.dt_manager import DateTimeManager
from chatbot.chat_llm import invoke_chat
from notes.notes import Note
from database.notes_operations import get_notes_by_user_id, get_note_by_id, delete_note_from_database


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

		user_id = msg.author.id
		task = Task()
		filtered_task = new_task_filter(new_task)
		task.create_task(*filtered_task, user_id)
		task_id = get_last_task()
		# If true, will be shown days of the week as buttons to select repeat days
		is_repeatable = filtered_task[5]
		if is_repeatable == 1:
			view=DaysToRepeatView(filtered_task, task_id)
			await ctx.send("Select which days to repeat", view=view)
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
		user_id = ctx.author.id
		# Checks the database for existing tasks
		tasks = get_tasks_by_user_id(user_id)
		if not tasks:
			await ctx.reply("No tasks found.")
			return
		await ctx.send("These are your active tasks: ")

		# Loop through all tasks and append basic info to notify tasks
		for task in tasks:
			await display_embed(task, title="Task")
			sleep(0.3)
		await ctx.send("Which task would you like to update? (Task nº)")

		# Waits for the user's next message containing the task's id to be updated
		while True:
			msg = await bot.wait_for("message")
			if (msg.author == ctx.author):
				task_id = msg.content
				task_id = int(task_id)
				break

		task = get_task_by_id(task_id)
		if not task:
			await ctx.reply(f"Task with ID {task_id} not found.")
			return
		
		await ctx.send("Type in the updated task info:"
				 f"```Study, Study Python, https://discord.com, {dt_manager.format_datetime(one_minute_later)}, 5, 1```\n"
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
		
		if new_task_data:
			# Filters and validate the new task data
			filtered_task = new_task_filter(new_task_data)
			
			task.update_task(
				task_id,
				name=filtered_task[0],
				description=filtered_task[1],
				links=filtered_task[2],
				start_date_str=filtered_task[3],
				duration=filtered_task[4],
				is_repeatable=filtered_task[5]
			)
			await display_embed(filtered_task, title="Task updated sucessfully!")
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
		user_id = ctx.author.id

		# Checks if exist tasks
		tasks = get_tasks_by_user_id(user_id)
		if not tasks:
			embed = discord.Embed(colour=discord.Color.red(), title="You don't have any tasks yet!")
			embed.add_field(name=f"Create one using:", value=f"```/create_task```", inline=False)
			await ctx.send(embed=embed)
		
		for task in tasks:
			await display_embed(task, title="Task")
			sleep(0.3)

	except Exception as e:
		print(f"Error in all_tasks(): {e}")


@bot.hybrid_command(name="chat", description="Chat with ChatGPT")
@app_commands.guilds(DISCORD_ID)
async def chatgpt(ctx):
	"""Calls OpenAI's GPT API"""
	try:
		channel = bot.get_channel(CHANNEL_ID)
		await ctx.send('Conversation with GPT started. To leave the conversation type "leave"')
		while True:
			while True:
				msg = await bot.wait_for("message")
				if (msg.author == ctx.author):
					user_message = msg.content
					user_message = str(user_message)
					break
			
			if not user_message.lower() == 'leave':
				try:
					user_id = msg.author.id
					error_response = 'Agent stopped due to iteration limit or time limit.'
					gpt_response = await invoke_chat(user_message, user_id)
					if gpt_response ==  error_response:
						gpt_response = "Sorry, I could not find an answer."
						await channel.send(gpt_response)
					else:
						await channel.send(gpt_response)
				except Exception as e:
					print(f"Error chat(): {e}")
					
			else:
				await ctx.send("You left the chat.")
				return
	except Exception as e:
		raise e


@bot.hybrid_command(name="create_note", description="Create a note")
@app_commands.guilds(DISCORD_ID)
async def create_note(ctx):
	"""Create a note"""
	try: 
		await ctx.send("Create a note by typing its title and content separated by a comma.")
		await ctx.send("Example: Study, Study python")

		while True:
			msg = await bot.wait_for("message")
			if (msg.author == ctx.author):
				user_message = msg.content
				user_message = str(user_message)
				break

		user_id = msg.author.id
		note = Note()
		filtered_note = new_note_filter(user_message)
		note.create_note(*filtered_note, user_id=user_id)
		await display_embed(filtered_note, title="Note created sucessfully!")
		return
	except Exception as e:
		print(f"Error creating note: {e}")


@bot.hybrid_command(name="notes", description="List all notes")
@app_commands.guilds(DISCORD_ID)
async def all_notes(ctx):
	try:
		user_id = ctx.author.id
		all_notes = get_notes_by_user_id(user_id)
		if all_notes:
			await ctx.send("Here are all your notes")
			all_notes_embeds = get_all_notes_embed(all_notes)
			for note_embed in all_notes_embeds:
				await ctx.send(embed=note_embed)
				sleep(0.3)
		else:
			embed = discord.Embed(colour=discord.Color.red(), title="You don't have any notes yet!")
			embed.add_field(name=f"Create one using:", value=f"```/create_note```", inline=False)
			await ctx.send(embed=embed)
	except Exception as e:
		print(e)


@bot.hybrid_command(name="update_note", description="Update a note by its ID")
@app_commands.guilds(DISCORD_ID)
async def update_note(ctx):
	try:
		user_id = ctx.author.id
		all_notes = get_notes_by_user_id(user_id)
		if not all_notes:
			embed = discord.Embed(colour=discord.Color.red(), title="You don't have any notes yet!")
			embed.add_field(name=f"Create one using:", value=f"```/create_note```", inline=False)
			await ctx.send(embed=embed)

		all_notes_embeds = get_all_notes_embed(all_notes)
		for note_embed in all_notes_embeds:
			await ctx.send(embed=note_embed)
			sleep(0.3)

		await ctx.send("Which note would you like to update? (By ID)")
		while True:
			msg = await bot.wait_for("message")
			if (msg.author == ctx.author):
				user_message = msg.content
				user_message = str(user_message)
				break

		note_id = user_message
		
		await ctx.send("Type in the updated note info:"
				 f"```Delete something, delete that, delete.com```\n"
						"*Ensure that the string above is passed to the program as "
						"a single, continuous sequence with each value separated by commas.*")
		while True:
			msg = await bot.wait_for("message")
			if (msg.author == ctx.author):
				user_message = msg.content
				user_message = str(user_message)
				break
		
		updated_note_data = new_note_filter(user_message)
		note = Note()
		note.update_note(note_id, *updated_note_data)
		await display_embed(updated_note_data, title="Note updated successfully!")
	except Exception as e:
		print(f"Error updating note: {e}")


@bot.hybrid_command(name="delete_note", description="Delete a note by its ID")
@app_commands.guilds(DISCORD_ID)
async def delete_note(ctx, *, note_id):
	"""Deletes a note by its ID"""
	await ctx.defer(ephemeral=True)
	try:
		# Check if task exists before attempting to delete it
		note = get_note_by_id(note_id)
		if not note:
			await ctx.send(f"Note with ID {note_id} does not exist.")
			return
		delete_note_from_database(note_id)
		await ctx.send(f"Note with ID {note_id} deleted sucessfully.")
	except Exception as e:
		print(f"Error in delete_note(): {e}")


# sync new commands
@bot.command()
async def sync(ctx):
	await bot.tree.sync(guild=DISCORD_ID)
	print("synced")