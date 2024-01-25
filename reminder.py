import asyncio
from datetime import datetime, timedelta
import schedule
from queue import Queue
from pytz import timezone
from database.db_operations import get_due_tasks, get_due_tasks_days

class TaskScheduler:
    def __init__(self):
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
        self.stop_scheduler = True

    async def job(self, task_id, hour):
        self.due_task_ids.add(task_id)
        return task_id

    def schedule_job(self, task_id, day, hour):
        asyncio.create_task(self.job(task_id, hour))

    async def update_schedule(self):
        while self.stop_scheduler:
            self.due_task_ids.clear()
            due_tasks = get_due_tasks()
            tasks_dict = {}

            for task in due_tasks:
                task_id, _, _, task_datetime, _, _ = task
                task_hour = self.parse_task_datetime(task_datetime).strftime('%H:%M:%S')
                task_days = get_due_tasks_days(task_id)

                tasks_dict.setdefault(task_id, {'days': [], 'hours': []})
                tasks_dict[task_id]['days'].extend(day[1] for day in task_days)
                tasks_dict[task_id]['hours'].append(task_hour)

            for task_id, data in tasks_dict.items():
                for day, hour in zip(data['days'], data['hours']):
                    self.schedule_job(task_id, day, hour)

            await asyncio.sleep(0.5)
            self.stop_scheduler = False

    async def main(task_scheduler):
        scheduler = asyncio.create_task(task_scheduler.update_schedule())
        await scheduler

    def parse_task_datetime(self, datetime_str):
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    async def get_due_task_ids(self):
        async with self.due_task_ids_lock:
            return list(self.due_task_ids)
    
    def on_off(self, stop: str):
        if stop == 'false':
            self.stop_scheduler = False
        if stop == 'true':
            self.stop_scheduler = True

if __name__ == "__main__":
    task_scheduler = TaskScheduler()
    asyncio.run(task_scheduler.main())
    
