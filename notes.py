from dt_manager import DateTimeManager
from database.notes_operations import save_note_to_database, update_note_in_database
import json
from typing import Optional

dt_manager = DateTimeManager('America/Sao_Paulo')
notes_path = 'database/notes.json'


class Note:
    def create_note(
            self,
            name: str, 
            description: str, 
            links: Optional[str],
            user_id: int,  
    ) -> None:
        try:
            self.user_id = user_id
            self.name = name
            self.description = description
            self.links = links
            self.status = 'Active'
            self.created_at = dt_manager.get_formatted_datetime_now()
            save_note_to_database(self)
        except Exception as e:
            print(f"Error creating task: {e}")

    def update_note(
            self,
            note_id: int,
            name: Optional[str] = None,
            description: Optional[str] = None,
            links: Optional[str] = None,
        ) -> None:

        try:
            if name is not None:
                self.name = name.strip().capitalize()

            if description is not None:
                self.description = description

            if links is not None:
                self.links = links

            update_note_in_database(
                note_id, 
                self.name, 
                self.description, 
                self.links)
            
        except Exception as e:
            print(f"Error updating note: {e}")  

