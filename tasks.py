from database.db_operations import save_task_to_database, delete_task_from_database, update_task_in_database, get_task_by_id
from datetime import datetime
from typing import Optional, Dict, Union

class Task:
    def create_task(
        self,
        name: str,
        description: str,
        start_date_str: str,
        duration: float,
        is_repeatable: int
    ) -> None:
        try:
            self.name = name
            self.description = description
            self.start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S")
            self.duration = duration
            self.is_repeatable = is_repeatable

            save_task_to_database(self)

        except Exception as e:
            print(f"Error creating task: {e}")

    def retrieve_task(self, task_id: int) -> Dict[str, Union[str, float, int]]:
        task_data = get_task_by_id(task_id)
        return task_data

    def update_task(
        self,
        task_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        start_date_str: Optional[str] = None,
        duration: Optional[float] = None,
        is_repeatable: Optional[int] = None
    ) -> None:
        try:
            if name is not None:
                self.name = name.strip()

            if description is not None:
                self.description = description

            if start_date_str is not None:
                self.start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S")

            if duration is not None:
                self.duration = duration

            if is_repeatable is not None:
                self.is_repeatable = is_repeatable

            update_task_in_database(task_id, self.name, self.description, self.start_date,
                                    self.duration, self.is_repeatable)

        except Exception as e:
            print(f"Error updating task: {e}")

    def delete_task(self, task_id: int) -> None:
        try:
            delete_task_from_database(task_id)

        except Exception as e:
            print(f"Error deleting task: {e}")
