import asyncio
from datetime import datetime
import schedule
from database.db_operations import get_due_tasks, get_due_tasks_days
from typing import List

class TaskScheduler:
    SLEEP_DURATION = 0.5

    def __init__(self) -> None:
        self.day_mapping = {
            0: schedule.every().sunday,
            1: schedule.every().monday,
            2: schedule.every().tuesday,
            3: schedule.every().wednesday,
            4: schedule.every().thursday,
            5: schedule.every().friday,
            6: schedule.every().saturday,
        }

        self.due_task_ids = set()
        self.due_task_ids_lock = asyncio.Lock()
        self.running = True

    async def job(self, task_id: int) -> int:
        self.due_task_ids.add(task_id)
        return task_id

    def schedule_job(self, task_id: int) -> None:
        asyncio.create_task(self.job(task_id))

    async def update_schedule(self) -> None:
        while self.running:
            print('running')
            self.due_task_ids.clear()
            due_tasks = get_due_tasks()
            tasks_dict = {}

            for task in due_tasks:
                task_id, _, _, task_datetime, _, _ = task
                task_hour = self.parse_task_datetime_str(task_datetime).strftime('%H:%M:%S')
                task_days = get_due_tasks_days(task_id)

                tasks_dict.setdefault(task_id, {'days': [], 'hours': []})
                tasks_dict[task_id]['days'].extend(day[1] for day in task_days)
                tasks_dict[task_id]['hours'].append(task_hour)

            for task_id, data in tasks_dict.items():
                for day, hour in zip(data['days'], data['hours']):
                    self.schedule_job(task_id)

            await asyncio.sleep(self.SLEEP_DURATION)
            self.toggle_scheduler(False)

    async def main(self, task_scheduler) -> None:
        try:
            await asyncio.create_task(task_scheduler.update_schedule())
        except Exception as e:
            print(f"An error occurred in main: {e}")

    def parse_task_datetime_str(self, datetime_str) -> str:
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    async def get_due_task_ids(self) -> List:
        async with self.due_task_ids_lock:
            return list(self.due_task_ids)
    
    def toggle_scheduler(self, stop: bool):
        self.running = not stop

if __name__ == "__main__":
    task_scheduler = TaskScheduler()
    asyncio.run(task_scheduler.main(task_scheduler))
