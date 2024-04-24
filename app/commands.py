import discord
from buttons import WrongChannelView
from notes.notes import Notes
from users.users import User
from config import bot, DELETE_AFTER, TIMEZONE, MESSAGE_DELAY
from utils.embed_utils import  display_embed
from discord.ext import commands
from time import sleep
from utils.dt_manager import DateTimeManager
from chatbot.chat_llm import invoke_chat
from ui.task_modal import  EditTask, TaskModal
from ui.note_modal import EditNote, NoteModal
from tasks.tasks import Tasks
from typing import Optional, Literal
from users.users import User


dt_manager = DateTimeManager(TIMEZONE)


@bot.command(aliases=['bot', 'studybot', 'study'])
async def greet(ctx: commands.Context) -> None:
	try:
		await ctx.send(f'Hey {ctx.author.mention}')
	except Exception as e:
		print(f"Error at greet {e}")


@bot.hybrid_command(name="help", description="Lists all commands")
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
		name="**Register**", value="```/register```", inline=False
		)
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
async def create_task(interaction: discord.Interaction) -> None:
	"""creates a task"""
	user_id = interaction.user.id
	await interaction.response.send_modal(TaskModal(action="create", user_id=user_id))


@bot.hybrid_command(name="tasks", description="List, update or delete tasks.")
async def all_tasks(ctx: commands.Context) -> None:
	"""List all active tasks"""
	try:
		user_id = ctx.author.id
		tasks = Tasks()
		tasks = tasks.get_all_tasks(user_id=user_id)

		user = User()
		current_channel_id = ctx.channel.id
		if current_channel_id != int(user.get_channel_id(user_id=str(user_id))):
			embed = discord.Embed(
				title="Incorrect channel",
				description="This is not your preferred channel. Would you like to change it?",
				color=discord.Color.orange()
			)
			view = WrongChannelView()
			await ctx.send(embed=embed, view=view)
			await bot.wait_for(
				'interaction', 
				check=lambda interaction: interaction.data["component_type"] == 2 
				and "custom_id" in interaction.data.keys()
				)
			if view.confirmation:
				user.update_channel_id(channel_id=current_channel_id, user_id=user_id)

		channel_id = user.get_channel_id(user_id=user_id)
		channel = bot.get_channel(int(channel_id))

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
			await channel.send(embed=embed)
		
		await channel.send(
			embed=discord.Embed(
				title="Here are your tasks:", 
				color=discord.Color.dark_blue()), 
				delete_after=DELETE_AFTER
				)
		for task in tasks:
			await display_embed(
				data=task, 
				title="Task", 
				task_id=task["id"],
				user_id=user_id,
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
async def create_note(interaction: discord.Interaction) -> None:
	"""creates a note"""
	user_id = interaction.user.id
	await interaction.response.send_modal(NoteModal(action="create", user_id=user_id))


@bot.hybrid_command(name="notes", description="List, update or delete notes.")
async def all_notes(ctx: commands.Context) -> None:
	try:
		user_id = ctx.author.id
		notes = Notes()
		all_notes = notes.get_all_notes(user_id)

		user = User()
		current_channel_id = ctx.channel.id
		if current_channel_id != int(user.get_channel_id(user_id=str(user_id))):
			embed = discord.Embed(
				title="Incorrect channel",
				description="This is not your preferred channel. Would you like to change it?",
				color=discord.Color.orange()
			)
			view = WrongChannelView()
			await ctx.send(embed=embed, view=view)
			await bot.wait_for(
				'interaction', 
				check=lambda interaction: interaction.data["component_type"] == 2 
				and "custom_id" in interaction.data.keys()
				)
			if view.confirmation:
				user.update_channel_id(channel_id=current_channel_id, user_id=user_id)

		channel_id = user.get_channel_id(user_id=user_id)
		channel = bot.get_channel(int(channel_id))

		if all_notes:
			await channel.send(
				embed=discord.Embed(
					title="Here are your notes:", 
					color=discord.Color.blurple()), 
					delete_after=DELETE_AFTER
					)

			for note in all_notes:
				await display_embed(
					data=note, 
					title="Note", 
					task_id=note["id"], 
					color=discord.Color.from_rgb(68, 0, 229), 
					type='note',
					user_id=user_id
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
			await channel.send(embed=embed, ephemeral=True)
	except Exception as e:
		print(f"Error at all_notes(): {e}")


@bot.hybrid_command(name="register", description="Create")
async def register(ctx: commands.Context) -> None:
	try:
		user = User()
		user_data = {
			"id": str(ctx.author.id),
			"username": str(ctx.author.name),
			"channel_id": str(ctx.channel.id),
			"server_id": str(ctx.guild.id)
		}

		user = user.create_user(user_data)
		if user:
			embed = discord.Embed(
					colour=discord.Color.green(), 
					title="User registered successfully!"
					)
			
			embed.add_field(name=f"Username", value=f"```{user['username']}```", inline=False)
			embed.add_field(name=f"Server", value=f"```{ctx.guild.name}```", inline=False)
			embed.add_field(name=f"Preferred channel", value=f"```{ctx.channel.name}```", inline=False)
			await ctx.send(embed=embed, ephemeral=True)

	except Exception as e:
		print(f"Error at register(): {e}")


@bot.hybrid_command(name="chat", description="Chat with ChatGPT")
async def chat(ctx: commands.Context) -> None:
	"""Calls OpenAI's GPT API"""
	try:
		await ctx.send('Conversation started. Type "leave" to exit conversation.', ephemeral=True)
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
						await ctx.send(gpt_response, ephemeral=True)
					else:
						await ctx.send(gpt_response, ephemeral=True)
				except Exception as e:
					print(f"Agent error: {e}")
					
			else:
				await ctx.send("You left the chat.", ephemeral=True)
	except Exception as e:
		print(f"Error at chat(): {e}")


# Sync new commands
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
	ctx: commands.Context, 
	guilds: commands.Greedy[discord.Object], 
	spec: Optional[Literal["~", "*", "^"]] = None
	) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

# Delete global commands and sync
@bot.command()
async def delete_commands(ctx: commands.Context):
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
    await ctx.send('Commands deleted.')



