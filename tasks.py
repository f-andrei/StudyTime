from database.task_operations import save_task_to_database, update_task_in_database
from datetime import datetime
from typing import Optional

class Task:
    def create_task(
            self,
            name: str,
            description: str,
            links: Optional[str],
            start_date_str: str,
            duration: float,
            is_repeatable: int,
            user_id: int
    ) -> None:
        try:
            self.name = name
            self.description = description
            self.links = links
            self.start_date = datetime.strptime(start_date_str, "%d/%m/%Y %H:%M:%S")
            self.duration = duration
            self.is_repeatable = is_repeatable
            self.user_id = user_id
            save_task_to_database(self)

        except Exception as e:
            print(f"Error creating task: {e}")

    def update_task(
        self,
        task_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        links: Optional[str] = None,
        start_date_str: Optional[str] = None,
        duration: Optional[float] = None,
        is_repeatable: Optional[int] = None
    ) -> None:
        try:
            if name is not None:
                self.name = name.strip().capitalize()

            if description is not None:
                self.description = description

            if links is not None:
                self.links = links

            if start_date_str is not None:
                self.start_date = datetime.strptime(start_date_str, "%d/%m/%Y %H:%M:%S")

            if duration is not None:
                self.duration = duration

            if is_repeatable is not None:
                self.is_repeatable = is_repeatable

            update_task_in_database(task_id, self.name, self.description, self.links, self.start_date,
                                    self.duration, self.is_repeatable)

        except Exception as e:
            print(f"Error updating task: {e}")

