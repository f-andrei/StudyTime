from database.db_operations import save_task_to_database, delete_task_from_database, update_task_in_database, get_task_by_id
from datetime import datetime
from typing import Optional

class Task:
    def create_task(self, name: str, description: str, start_date: str, duration: float, is_repeatable: int) -> None:
        self.name = name
        self.description = description
        self.start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        self.duration = duration
        self.is_repeatable = is_repeatable

        save_task_to_database(self)

        return self

    def get_task(self, task_id) -> str:
        task_data = get_task_by_id(task_id)
        return task_data
    
    def update_task(
        self,
        task_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[str] = None,
        duration: Optional[float] = None,
        is_repeatable: Optional[int] = None
    ) -> None:
        if name is not None:
            self.name = name.strip()

        if description is not None:
            self.description = description

        if start_date is not None:
            self.start_date = start_date

        if duration is not None:
            self.duration = duration

        if is_repeatable is not None:
            self.is_repeatable = is_repeatable

        update_task_in_database(task_id, self.name, self.description, self.start_date,
                                self.duration, self.is_repeatable)

    def delete_task(self, task_id: int):
        delete_task_from_database(task_id)