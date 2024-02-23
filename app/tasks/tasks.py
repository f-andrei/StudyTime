from database.task_operations import save_task_to_database, update_task_in_database, get_task_by_id
from datetime import datetime
from typing import Optional

class Task:
    def create_task(
            self,
            name: str,
            description: str,
            links: Optional[str],
            start_date: str,
            duration: float,
            user_id: int
    ) -> None:
        try:
            start_date = datetime.strptime(start_date, "%d/%m/%Y %H:%M:%S")
            start_date = datetime.strftime(start_date, "%d/%m/%Y %H:%M:%S")
            start_date = start_date.split(' ')
            date = start_date[0]
            time = start_date[1]
            self.name = name
            self.description = description
            self.links = links
            self.start_date = date
            self.time = time
            self.duration = duration
            self.user_id = user_id
            save_task_to_database(self)
            return True
        except Exception as e:
            print(f"Error creating task: {e}")
            return False

    def update_task(
        self,
        task_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        links: Optional[str] = None,
        start_date: Optional[str] = None,
        duration: Optional[float] = None,
    ) -> bool:
        try:
            self.name = name
            self.description = description
            self.links = links
            if start_date:
                start_date = datetime.strptime(start_date, "%d/%m/%Y %H:%M:%S")
                start_date = datetime.strftime(start_date, "%d/%m/%Y %H:%M:%S")
                start_date = start_date.split(' ')
                date = start_date[0]
                time = start_date[1]
                self.start_date = date
            else:
                self.start_date = start_date
            
            self.time = time
            self.duration = duration
            
            existing_task = get_task_by_id(task_id)
            existing_task = existing_task[0]

            if name is None:
                self.name = existing_task[1]

            if description is None:
                self.description = existing_task[2]

            if links is None:
                self.links = existing_task[3]

            if start_date is None:
                self.start_date = existing_task[4]
                self.time = existing_task[5]

            if duration is None:
                self.duration = existing_task[6]

            update_task_in_database(task_id, self.name, self.description, self.links, self.start_date, time,
                                    self.duration)
            return True
        except Exception as e:
            print(f"Error updating task: {e}")
            return False
