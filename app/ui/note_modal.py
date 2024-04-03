from discord import ui
import discord
from notes.notes import Notes
from config import DELETE_AFTER, BLURPLE_STYLE, RED_STYLE
from utils.embed_utils import display_embed
from utils.dt_manager import DateTimeManager

notes = Notes()
dt_manager = DateTimeManager("America/Sao_Paulo")

class NoteModal(ui.Modal, title='Create note'):
    def __init__(self, action: str, note_id: int = None, channel_id: int = None) -> None:
        super().__init__()
        self.action = action
        self.note_id = note_id
        self.channel_id = channel_id

    name = ui.TextInput(label='Name', placeholder="Replace batteries",
                        style=discord.TextStyle.short, 
                        max_length=50, required=False
                        )
    description = ui.TextInput(label='Description', placeholder='Replace my mouse battery',
                        style=discord.TextStyle.paragraph, 
                        max_length=1000, required=False
                        )
    links = ui.TextInput(label='Links', placeholder="https://google.com",
                        style=discord.TextStyle.short, 
                        required=False
                        )
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=self.title, color = discord.Color.blue())
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        
        user_id = interaction.user.id
        
        note_data = {
            "name": str(self.name),
            "description": str(self.description),
            "links": str(self.links),
            "created_at": dt_manager.get_formatted_datetime_now(),
            "user_id": str(user_id)
        }
        
        if self.action == 'create':
            embed_2 = discord.Embed(title=None, color=discord.Color.red())
            for i, item in enumerate(note_data):
                if item is None:
                    embed_2.title="Unable to create note. Missing fields on invalid data."
                    await interaction.response.send_message(
                                                    embed=embed_2, 
                                                    delete_after=DELETE_AFTER,
                                                    ephemeral=True
                                                    )
                    return

            note_created = notes.create_note(note_data)
            if not note_created:
                embed_2.title = "Unable to create note. Missing fields or invalid data."
                await interaction.response.send_message(
                                                embed=embed_2, 
                                                delete_after=DELETE_AFTER,
                                                ephemeral=True
                                                )
                return
            
            await display_embed(
                channel_id=self.channel_id, 
                data=note_data, 
                type='note', 
                title="Note created sucessfully!"
                )
            await interaction.response.defer()

        if self.action == 'update':
            note_data = {}
            field_names = ["name", "description", "links"]
            fields_values = [self.name, self.description, self.links]

            for field_name, field_value in zip(field_names, fields_values):
                field_value = str(field_value)
                if field_value is not None and field_value.strip() != "":
                    note_data[field_name] = field_value

            note_updated = notes.update_note(note_data=note_data, note_id=self.note_id)

            if not note_updated:
                embed.title = "Unable to update note. Invalid data."
                embed.description = None
                await interaction.response.send_message(
                                                embed=embed, 
                                                delete_after=DELETE_AFTER,
                                                ephemeral=True
                                                )
            else:
                embed.title = "Note updated!"
                embed.description = None
                await interaction.response.send_message(
                                                embed=embed, 
                                                delete_after=DELETE_AFTER,
                                                ephemeral=True
                                                )


class EditNote(discord.ui.View):
    button: discord.ui.Button
    msg_id = None

    def __init__(self, note_data) -> None:	
        super().__init__()
        self.note_data: dict = note_data
        self.note_id: int = note_data["id"]
        self.note = notes.get_note(self.note_id)
        self.embed = discord.Embed()

    @discord.ui.button(label="Edit", style=BLURPLE_STYLE)
    async def edit(self, interaction: discord.Interaction, button) -> None:
        if self.note:
            note_modal = NoteModal(action='update', note_id=self.note_id)
            button.disabled = True
            await interaction.response.send_modal(note_modal)
            await interaction.followup.delete_message(self.msg_id)
        else:
            self.embed.title = "Note not found."
            await interaction.response.send_message(embed=self.embed, ephemeral=True)
            
    @discord.ui.button(label="Delete", style=RED_STYLE)
    async def delete(self, interaction: discord.Interaction, button) -> None:
        if self.note:
            deleted = notes.delete_note(self.note_id)
            if deleted:
                self.embed.title = "Note sucessfully deleted!"
                self.embed.color = discord.Color.red()
            else:
                self.embed.title = "Unable to delete note!"
        else:
            self.embed.title = f"Note doesn't exist or is already deleted."
            self.embed.color = discord.Color.red()
            
        button.disabled = True
        await interaction.response.send_message(embed=self.embed, ephemeral=True)
        await interaction.followup.delete_message(self.msg_id)