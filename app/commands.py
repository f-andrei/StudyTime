import discord
from config import bot, CHANNEL_ID, DISCORD_ID, DELETE_AFTER
from utils.embed_utils import  display_embed
from database.task_operations import get_tasks_by_user_id
from discord.ext import commands
from discord import app_commands
from time import sleep
from utils.dt_manager import DateTimeManager
from chatbot.chat_llm import invoke_chat
from database.notes_operations import get_notes_by_user_id
from ui.task_modal import  EditTask, TaskModal
from ui.note_modal import EditNote, NoteModal



TIMEZONE = 'America/Sao_Paulo'
dt_manager = DateTimeManager(TIMEZONE)


@bot.command(aliases=['bot', 'studybot', 'study'])
async def greet(ctx):
	try:
		await ctx.send(f'Hey {ctx.author.mention}')
	except Exception as e:
		print(f"Error at greet {e}")


@bot.tree.command(name="create_task", description="Create a task")
@app_commands.guilds(DISCORD_ID)
async def create_task(interaction: discord.Interaction):
    """creates a task"""
    await interaction.response.send_modal(TaskModal(action="create"))

@bot.hybrid_command(name="tasks", description="List, update or delete tasks.")
@app_commands.guilds(DISCORD_ID)
async def all_tasks(ctx: commands.Context) -> None:
	"""List all active tasks"""
	try:
		user_id = ctx.author.id
		# Checks if exist tasks
		channel = bot.get_channel(CHANNEL_ID)
		tasks = get_tasks_by_user_id(user_id)
		if not tasks:
			embed = discord.Embed(colour=discord.Color.red(), title="You don't have any tasks yet!")
			embed.add_field(name=f"Create one using:", value=f"```/create_task```", inline=False)
			await ctx.send(embed=embed)
			return
		await ctx.send("Here's your tasks: ", delete_after=DELETE_AFTER)
		for task in tasks:
			await display_embed(task, title="Task", color=discord.Color.from_rgb(68, 0, 229), type='task')
			view = EditTask(task)
			msg: discord.Message = await channel.send(view=view, delete_after=DELETE_AFTER)
			view.msg_id = msg.id
			sleep(0.4)
		
	except Exception as e:
		print(f"Error in all_tasks(): {e}")


@bot.tree.command(name="create_note", description="Create a note")
@app_commands.guilds(DISCORD_ID)
async def create_note(interaction: discord.Interaction):
    """creates a note"""
    await interaction.response.send_modal(NoteModal(action="create"))


@bot.hybrid_command(name="notes", description="List, update or delete notes.")
@app_commands.guilds(DISCORD_ID)
async def all_notes(ctx):
	try:
		user_id = ctx.author.id
		channel = bot.get_channel(CHANNEL_ID)
		all_notes = get_notes_by_user_id(user_id)
		if all_notes:
			await ctx.send("Here are your notes", delete_after=DELETE_AFTER)

			for note in all_notes:
				await display_embed(note, title="Note", color=discord.Color.from_rgb(68, 0, 229), type='note')
				view = EditNote(note)
				msg: discord.Message = await channel.send(view=view, delete_after=DELETE_AFTER)
				view.msg_id = msg.id
				sleep(0.4)
			return
		else:
			embed = discord.Embed(colour=discord.Color.red(), title="You don't have any notes yet!")
			embed.add_field(name=f"Create one using:", value=f"```/create_note```", inline=False)
			await ctx.send(embed=embed)
	except Exception as e:
		print(f"Error at all_notes(): {e}")


@bot.hybrid_command(name="chat", description="Chat with ChatGPT")
@app_commands.guilds(DISCORD_ID)
async def chat(ctx):
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
		print(f"Error at chat(): {e}")


# sync new commands
@bot.command()
async def sync(ctx):
	await bot.tree.sync(guild=DISCORD_ID)
	print("synced")



