import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DB_DIR = 'database'
DB_NAME = 'studytime.sqlite3'
DB_FILE = ROOT_DIR / DB_DIR / DB_NAME

TASKS = 'tasks'

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Clear existing data from tables
cur.execute(f'DELETE FROM {TASKS}')
conn.commit()

# Clear all ids
cur.execute('VACUUM')
conn.commit()


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
conn.commit()
conn.close()