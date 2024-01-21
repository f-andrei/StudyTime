import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DB_DIR = 'database'
DB_NAME = 'studytime.sqlite3'
DB_FILE = ROOT_DIR / DB_DIR / DB_NAME

TASKS = 'tasks'
REPEAT_DAYS = 'repeat_days'

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()


try:
    # Clear existing data from tables
    cur.execute(f'DELETE FROM {TASKS}')
    conn.commit()

    # Clear all ids
    cur.execute('VACUUM')
    conn.commit()
except Exception as e:
    print(f"Error: {e}")

# Create parent table
cur.execute(
    f'CREATE TABLE IF NOT EXISTS {TASKS}'
    '('
    'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    'name TEXT, '
    'description TEXT, '
    'start_date TEXT, '
    'duration FLOAT, '
    'is_repeatable INTEGER'
    ')'
)

cur.execute(
    f'CREATE TABLE IF NOT EXISTS {REPEAT_DAYS}'
    '('
    'task_id INTEGER, '
    'day_number INTEGER, '
    'PRIMARY KEY (task_id, day_number), '
    f'FOREIGN KEY (task_id) REFERENCES {REPEAT_DAYS} (task_id)'
    ')'
)
conn.commit()
conn.close()