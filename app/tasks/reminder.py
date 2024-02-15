import asyncio
from database.task_operations import get_due_tasks, get_due_tasks_days
from typing import List

class TaskScheduler:
    SLEEP_DURATION: float = 0.5

    def __init__(self) -> None:
        self.due_task_ids: set[int] = set()
        self.due_task_ids_lock: asyncio.Lock = asyncio.Lock()
        self.running: bool = True

    async def job(self, day: int, task_id: int) -> None:
        async with self.due_task_ids_lock:
            self.due_task_ids.add(task_id)

    async def schedule_job(self, task_id: int, days: list) -> None:
        for day in days:
            await self.job(day, task_id)

    async def update_schedule(self) -> None:
        while self.running:
            self.due_task_ids.clear()
            due_tasks = get_due_tasks()
            tasks_dict = {}
            
            for task in due_tasks:
                task_id, _, _, _, _, _, _, _ = task
                task_days = await asyncio.to_thread(get_due_tasks_days, task_id)
                tasks_dict.setdefault(task_id, {'days': []})
                tasks_dict[task_id]['days'].extend(day[1] for day in task_days)

            for task_id, data in tasks_dict.items():
                await self.schedule_job(task_id, data['days'])

            await asyncio.sleep(self.SLEEP_DURATION)
            self.running = False

    async def main(self) -> None:
        try:
            await self.update_schedule()
        except Exception as e:
            print(f"An error occurred in main: {e}")

    async def get_due_task_ids(self) -> List[int]:
        async with self.due_task_ids_lock:
            return list(self.due_task_ids)

    def toggle_scheduler(self, stop: bool):
        self.running = stop

if __name__ == "__main__":
    task_scheduler = TaskScheduler()
    asyncio.run(task_scheduler.main())
