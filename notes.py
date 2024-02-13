from dt_manager import DateTimeManager
import discord
import json
from time import sleep

dt_manager = DateTimeManager('America/Sao_Paulo')
notes_path = 'database/notes.json'

def create_note(note_data):
    """Creates a note"""
    note = note_data.split(', ')
    note.append(dt_manager.format_datetime(dt_manager.get_current_time()))
    note_dict = {}
    note_dict["title"] = note[0]
    note_dict["description"] = note[1]
    note_dict["created_at"] = note[2]
    try:
        with open(notes_path, 'r') as file:
            try:
                notes = json.load(file)
                if not isinstance(notes, list):
                    raise ValueError("Invalid data type in JSON file")
            except (json.JSONDecodeError, ValueError):
                notes = []  
    except FileNotFoundError:
        notes = []

    notes.append(note_dict)

    with open(notes_path, 'w') as file:
        json.dump(notes, file, indent=4, separators=(',', ':'), ensure_ascii=True)
    
    return note


def get_notes():
    try:
        with open(notes_path, 'r') as file:
            notes = json.load(file)
            return notes
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error: {e}")


def get_all_notes_embed():
    try:
        all_notes = get_notes()
        if all_notes:
            embeds = []
            for note in all_notes:
                embed = discord.Embed(colour=discord.Color.magenta(), title="Note")
                embed.add_field(name=f"Title", value=f"```{note['title']}```", inline=False)
                embed.add_field(name=f"Description", value=f"```{note['description']}```", inline=False)
                embed.add_field(name=f"Created at", value=f"```{note['created_at']}```", inline=False)
                embeds.append(embed)
            return embeds      
    except Exception as e:
         ...