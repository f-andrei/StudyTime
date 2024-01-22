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


def save_task_to_database(task):
    connection = establish_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {TASK_TABLE} (name, description, start_date, duration, is_repeatable) VALUES (?, ?, ?, ?, ?)",
                       (task.name, task.description, task.start_date, task.duration, task.is_repeatable))
        connection.commit()
        task.task_id = cursor.lastrowid
        print(f"Task '{task.name}' successfully inserted into the database.")
    except Exception as e:
        print(f"Error inserting task into the database: {e}")
    finally:
        connection.close()


def save_repeat_days_to_database(days):
    connection = establish_connection()
    try:
        task_id = get_last_task()
        cursor = connection.cursor()
        for day in days:
            cursor.execute(f"INSERT INTO {REPEAT_DAYS_TABLE} (task_id, day_number) VALUES (?, ?)",
                            (task_id, day))
        connection.commit()
    except Exception as e:
        print(f"Error inserting task days into the database: {e}")
    finally:
        connection.close()


def get_task_by_id(task_id):
    connection = establish_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM {TASK_TABLE} WHERE id=?', (task_id,))
        task_data = cursor.fetchall()
        return task_data
    except Exception as e:
        print(f"Error fetching task from database: {e}")
    finally:
        connection.close()

def get_last_task():
    connection = establish_connection()
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
    finally:
        connection.close()


def update_task_in_database(task_id, name, description, start_date, duration, is_repeatable):
    connection = establish_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            f'UPDATE {TASK_TABLE} SET name=?, description=?, start_date=?, duration=?, '
            'is_repeatable=? WHERE id=?',
            (name, description, start_date, duration, is_repeatable, task_id)
        )
        connection.commit()
    except Exception as e:
        print(f"Error updating task in database: {e}")
    finally:
        connection.close()


def delete_task_from_database(task_id):
    connection = establish_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(f'DELETE FROM {TASK_TABLE} WHERE id = ?', (task_id,))
        connection.commit()
        print(f"Task with ID {task_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting task from the database: {e}")
    finally:
        connection.close()