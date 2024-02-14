import sqlite3
from pathlib import Path
from dt_manager import DateTimeManager

ROOT_DIR = Path(__file__).parent.parent
DB_DIR = 'database'
DB_NAME = 'studytime.sqlite3'
DB_FILE = ROOT_DIR / DB_DIR / DB_NAME
TASK_TABLE = 'tasks'
REPEAT_DAYS_TABLE = 'repeat_days'

dt_manager = DateTimeManager('America/Sao_Paulo')

# Create a connection to the SQLite database
def establish_connection():
    """Establish a connection to the SQLite database."""
    connection = sqlite3.connect(str(DB_FILE))
    return connection


def save_task_to_database(task):
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO {TASK_TABLE} (name, description, links, start_date, duration, is_repeatable, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (task.name, task.description, task.links, task.start_date, task.duration, task.is_repeatable, task.user_id))
            connection.commit()
            task.task_id = cursor.lastrowid
            print(f"Task '{task.name}' successfully inserted into the database.")
        except Exception as e:
            print(f"Error inserting task into the database: {e}")


def save_repeat_days_to_database(days):
    with establish_connection() as connection:
        try:
            task_id = get_last_task()
            cursor = connection.cursor()
            for day in days:
                cursor.execute(f"INSERT INTO {REPEAT_DAYS_TABLE} (task_id, day_number) VALUES (?, ?)",
                                (task_id, day))
            connection.commit()
        except Exception as e:
            print(f"Error inserting task days into the database: {e}")


def get_task_by_id(task_id):
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM {TASK_TABLE} WHERE id=?', (task_id,))
            task_data = cursor.fetchall()
            return task_data
        except Exception as e:
            print(f"Error fetching task from database: {e}")


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


def get_tasks_by_user_id(user_id):
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {TASK_TABLE} WHERE user_id=?", (user_id,))
            tasks_data = cursor.fetchall()
            return tasks_data
        except Exception as e:
            print(f"Error fetching tasks from database: {e}")
            


def update_task_in_database(task_id, name, description, links, start_date, duration, is_repeatable):
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                f'UPDATE {TASK_TABLE} SET name=?, description=?, links=?, start_date=?, duration=?, '
                'is_repeatable=? WHERE id=?',
                (name, description, links, start_date, duration, is_repeatable, task_id)
            )
            connection.commit()
        except Exception as e:
            print(f"Error updating task in database: {e}")


def delete_task_from_database(task_id):
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f'DELETE FROM {TASK_TABLE} WHERE id = ?', (task_id,))
            connection.commit()
            print(f"Task with ID {task_id} deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting task from the database: {e}")


def get_due_tasks():
    end_time_range, start_time_range = dt_manager.get_due_tasks_time_range()
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tasks WHERE start_date BETWEEN ? AND ?",
                           (end_time_range, start_time_range))
            due_tasks = cursor.fetchall()
        except Exception as e:
            print(e)
    return due_tasks


def get_due_tasks_days(task_id):
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM repeat_days WHERE task_id=?', (task_id,))
            task_days = cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
    return task_days
