import discord
from notes.notes import Notes
from config import bot, DISCORD_ID, DELETE_AFTER, TIMEZONE, MESSAGE_DELAY, CHANNEL_ID
from utils.embed_utils import  display_embed
from discord.ext import commands
from discord import app_commands
from time import sleep
from utils.dt_manager import DateTimeManager
from chatbot.chat_llm import invoke_chat
from ui.task_modal import  EditTask, TaskModal
from ui.note_modal import EditNote, NoteModal
from tasks.tasks import Tasks


dt_manager = DateTimeManager(TIMEZONE)
channel = bot.get_channel(CHANNEL_ID)

@bot.command(aliases=['bot', 'studybot', 'study'])
async def greet(ctx) -> None:
	try:
		await ctx.send(f'Hey {ctx.author.mention}')
	except Exception as e:
		print(f"Error at greet {e}")


@bot.hybrid_command(name="help", description="Lists all commands")
@app_commands.guilds(DISCORD_ID)
async def help(ctx: commands.Context) -> None:
	embed = discord.Embed(
		title="StudyTime", 
		color=discord.Color.dark_purple(), 
		description="""**Welcome to *StudyTime*!  
		I'm here to assist you in managing your tasks and notes. 
		You can also have a chat with ChatGPT-4 for free!	
		These are the commands available:**""",
		url="https://github.com/f-andrei/StudyTime")
	
	embed.add_field(
		name="**Create a task**", value="```/create_task```", inline=False
		)
	embed.add_field(
		name="**Create a note**", value="```/create_note```", inline=False
		)
	embed.add_field(
		name="**List, update or delete tasks**", value="```/tasks```", inline=False
		)
	embed.add_field(
		name="**List, update or delete notes****", value="```/notes```", inline=False
		)
	embed.add_field(
		name="**Have a chat with GPT**", value="```/chat```", inline=False
		)
	
	embed.set_image(url="https://i.ibb.co/P9r1r6K/Study.png")
	embed.set_thumbnail(url="https://i.ibb.co/rvZh9FC/studytime.png")
	embed.set_footer(
		text="By @andrei.f on Discord.", 
		icon_url="https://i.ibb.co/nLsLSjH/gorilla.png"
		)
	await ctx.send(embed=embed)


@bot.tree.command(name="create_task", description="Create a task")
@app_commands.guilds(DISCORD_ID)
async def create_task(interaction: discord.Interaction) -> None:
    """creates a task"""
    await interaction.response.send_modal(TaskModal(action="create"))


@bot.hybrid_command(name="tasks", description="List, update or delete tasks.")
@app_commands.guilds(DISCORD_ID)
async def all_tasks(ctx: commands.Context) -> None:
	"""List all active tasks"""
	try:
		user_id = ctx.author.id
		tasks = Tasks()
		tasks = tasks.get_all_tasks(user_id=user_id)
		if not tasks:
			embed = discord.Embed(
				colour=discord.Color.red(), 
				title="You don't have any tasks yet!"
				)
			embed.add_field(
				name=f"Create one using:", 
				value=f"```/create_task```", 
				inline=False
				)
			await ctx.send(embed=embed)
			return
		
		await ctx.send("Here's your tasks: ", delete_after=DELETE_AFTER)

		for task in tasks:
			await display_embed(
				task, 
				title="Task", 
				task_id=task["id"], 
				color=discord.Color.from_rgb(68, 0, 229), 
				type='task'
				)
			view = EditTask(task)
			msg: discord.Message = await channel.send(
													view=view, 
													delete_after=DELETE_AFTER
													)
			view.msg_id = msg.id
			sleep(MESSAGE_DELAY)
		
	except Exception as e:
		print(f"Error in all_tasks(): {e}")


@bot.tree.command(name="create_note", description="Create a note")
@app_commands.guilds(DISCORD_ID)
async def create_note(interaction: discord.Interaction) -> None:
    """creates a note"""
    await interaction.response.send_modal(NoteModal(action="create"))


@bot.hybrid_command(name="notes", description="List, update or delete notes.")
@app_commands.guilds(DISCORD_ID)
async def all_notes(ctx) -> None:
	try:
		user_id = ctx.author.id
		notes = Notes()
		all_notes = notes.get_all_notes(user_id)
		if all_notes:
			await ctx.send("Here are your notes", delete_after=DELETE_AFTER)

			for note in all_notes:
				await display_embed(
					note, 
					title="Note", 
					task_id=note["id"], 
					color=discord.Color.from_rgb(68, 0, 229), 
					type='note'
					)
				view = EditNote(note)
				msg: discord.Message = await channel.send(
														view=view, 
														delete_after=DELETE_AFTER
														)
				view.msg_id = msg.id
				sleep(MESSAGE_DELAY)
			return
		else:
			embed = discord.Embed(
				colour=discord.Color.red(), 
				title="You don't have any notes yet!"
				)
			embed.add_field(
				name=f"Create one using:", value=f"```/create_note```", inline=False
				)
			await ctx.send(embed=embed)
	except Exception as e:
		print(f"Error at all_notes(): {e}")


@bot.hybrid_command(name="chat", description="Chat with ChatGPT")
@app_commands.guilds(DISCORD_ID)
async def chat(ctx) -> None:
	"""Calls OpenAI's GPT API"""
	try:
		await ctx.send('Conversation started. Type "leave" to exit conversation.')
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
					print(f"Agent error: {e}")
					
			else:
				await ctx.send("You left the chat.")
				return
	except Exception as e:
		print(f"Error at chat(): {e}")


# sync new commands
@bot.command()
async def sync(ctx) -> None:
	await bot.tree.sync(guild=DISCORD_ID)
	print("synced")




