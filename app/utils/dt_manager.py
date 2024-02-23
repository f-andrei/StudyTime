from datetime import datetime, timedelta
from pytz import timezone
from typing import Optional, Tuple
import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DB_DIR = 'database'
DB_NAME = 'studytime.sqlite3'
DB_FILE = ROOT_DIR / DB_DIR / DB_NAME
TASK_TABLE = 'tasks'
REPEAT_DAYS_TABLE = 'repeat_days'



# Create a connection to the SQLite database
def establish_connection():
    """Establish a connection to the SQLite database."""
    connection = sqlite3.connect(str(DB_FILE))
    return connection

def get_last_task():
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM {TASK_TABLE} ORDER BY id DESC LIMIT 1')
            task = cursor.fetchone()
            if task:
                return task[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching task from database: {e}")



def save_repeat_days_to_database(days):
    with establish_connection() as connection:
        try:
            task_id = get_last_task()
            cursor = connection.cursor()
            for day in days:
                cursor.execute(f"INSERT INTO {REPEAT_DAYS_TABLE} (task_id, date) VALUES (?, ?)",
                                (task_id, day))
            connection.commit()
        except Exception as e:
            print(f"Error inserting task days into the database: {e}")

def save_task_to_database(name, description, links, start_date, time, duration, user_id):
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO {TASK_TABLE} (name, description, links, start_date, time, duration, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (name, description, links, start_date, time, duration, user_id))
            connection.commit()
            
            print(f"Task '{name}' successfully inserted into the database.")
        except Exception as e:
            print(f"Error inserting task into the database: {e}")



class DateTimeManager:
    def __init__(self, tz: Optional[str] = None):
        self.tz = tz
        self.datetime_format = "%d/%m/%Y %H:%M:%S"
 
    def get_current_time(self) -> datetime:
        datetime_now = datetime.utcnow()
        if self.tz:
            new_tz = timezone(self.tz)
            datetime_now = datetime_now.replace(tzinfo=timezone('UTC')).astimezone(new_tz)
        return datetime_now

    def get_day_number(self, datetime_str):
        dt_obj = datetime.strptime(datetime_str, "%d/%m/%Y")
        day_number = dt_obj.weekday()
        return (day_number + 1) % 7

    def get_formatted_datetime_now(self) -> str:
        datetime_now = self.get_current_time()
        formatted_datetime_now = datetime_now.strftime(self.datetime_format)
        return formatted_datetime_now

    def format_datetime(self, dt: datetime) -> str:
        formatted_datetime = dt.strftime(self.datetime_format)
        return formatted_datetime

    def get_due_tasks_time_range(self) -> Tuple[datetime, datetime]:
        current_time = self.get_current_time()
        end_time_range = current_time - timedelta(minutes=1, seconds=30)
        start_time_range = current_time + timedelta(seconds=10)

        end_time_range_str = end_time_range.strftime('%d/%m/%Y %H:%M:%S')
        start_time_range_str = start_time_range.strftime('%d/%m/%Y %H:%M:%S')

        _, end_time_range = end_time_range_str.split(' ')
        _, start_time_range = start_time_range_str.split(' ')

        return end_time_range, start_time_range

    def calculate_datetime(self, time: datetime, addendum: int) -> datetime:
        new_datetime = time + timedelta(minutes=addendum)
        return new_datetime






    