from utils.dt_manager import DateTimeManager
from database.notes_operations import get_note_by_id, save_note_to_database, update_note_in_database
from config import TIMEZONE
from typing import Optional

dt_manager = DateTimeManager(TIMEZONE)
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
            self.created_at = dt_manager.get_formatted_datetime_now()
            save_note_to_database(self)
            return True
        except Exception as e:
            print(f"Error creating note: {e}")
            return False
    def update_note(
            self,
            note_id: int,
            name: Optional[str] = None,
            description: Optional[str] = None,
            links: Optional[str] = None,
        ) -> None:

        try:
            self.name = name
            self.description = description
            self.links = links

            existing_note = get_note_by_id(note_id)
            existing_note = existing_note[0]
            
            if name is None:
                self.name = existing_note[1]

            if description is None:
                self.description = existing_note[2]

            if links is None:
                self.links = existing_note[3]

            update_note_in_database(
                note_id, 
                self.name, 
                self.description, 
                self.links)
            return True
        except Exception as e:
            print(f"Error updating note: {e}")  
            return False