from discord import ui
import discord
from datetime import datetime
from utils.dt_manager import DateTimeManager
from notes.notes import Note
from database.notes_operations import get_note_by_id, save_note_to_database, delete_note_from_database
from config import DELETE_AFTER
from utils.embed_utils import display_embed


class NoteModal(ui.Modal, title='Create note'):
    def __init__(self, action: str, note_id: int = None):
        super().__init__()
        self.action = action
        self.note_id = note_id
    name = ui.TextInput(label='Name', placeholder="Replace batteries",
                        style=discord.TextStyle.short, 
                        max_length=50, required=False)
    description = ui.TextInput(label='Description', placeholder='Replace my mouse battery',
                        style=discord.TextStyle.paragraph, 
                        max_length=1000, required=False)
    links = ui.TextInput(label='Links', placeholder="https://google.com",
                        style=discord.TextStyle.short, 
                        required=False)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.title, color = discord.Color.blue())
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        note = Note()
        user_id = interaction.user.id
        
        note_data = [str(self.name), str(self.description), str(self.links)]
        
        for i, item in enumerate(note_data):
            if not len(item) >= 1:
                note_data[i] = None

        if self.action == 'create':
            embed_2 = discord.Embed(title=None, color=discord.Color.red())
            for i, item in enumerate(note_data):
                if item is None:
                    embed_2.title="Unable to create note. Missing fields on invalid data."
                    await interaction.response.send_message(embed=embed_2, delete_after=DELETE_AFTER)
                    return

            note_created = note.create_note(*note_data, user_id)
            if not note_created:
                embed_2.title = "Unable to create note. Missing fields or invalid data format."
                await interaction.response.send_message(embed=embed_2, delete_after=DELETE_AFTER)
                return
            
            await display_embed(note_data, type='note', title="Note created sucessfully!")
            await interaction.response.defer()

        if self.action == 'update':
            note_updated = note.update_note(self.note_id, *note_data)
            if not note_updated:
                embed.title = "Unable to update note. Invalid data format."
                embed.description = None
                await interaction.response.send_message(embed=embed, delete_after=DELETE_AFTER)
            else:
                embed.title = "Note updated!"
                embed.description = None
                await interaction.response.send_message(embed=embed, delete_after=DELETE_AFTER)


class EditNote(discord.ui.View):
    BLURPLE_STYLE = discord.ButtonStyle.blurple
    RED_STYLE = discord.ButtonStyle.red
    SUCCESS_STYLE = discord.ButtonStyle.success
    msg_id = None
    def __init__(self, note_data) -> None:	
        super().__init__()
        self.note_data = note_data
        self.note_id = note_data[0]
        self.note = get_note_by_id(self.note_id)
        self.embed = discord.Embed()

    @discord.ui.button(label="Edit", style=BLURPLE_STYLE)
    async def edit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.note:
            note_modal = NoteModal(action='update', note_id=self.note_id)
            button.disabled = True
            await interaction.response.send_modal(note_modal)
            await interaction.followup.delete_message(self.msg_id)
        else:
            self.embed.title = "Note not found."
            await interaction.response.send_message(embed=self.embed)
            
    @discord.ui.button(label="Delete", style=RED_STYLE)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if self.note:
            deleted = delete_note_from_database(self.note_id)
            if deleted:
                self.embed.title = "Note sucessfully deleted!"
                self.embed.color = discord.Color.red()
            else:
                self.embed.title = "Unable to delete note!"
        else:
            self.embed.title = f"Note doesn't exist or is already deleted."
            self.embed.color = discord.Color.red()
        button.disabled = True
        await interaction.response.send_message(embed=self.embed)
        await interaction.followup.delete_message(self.msg_id)