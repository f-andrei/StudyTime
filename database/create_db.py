import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DB_DIR = 'database'
DB_NAME = 'studytime.sqlite3'
DB_FILE = ROOT_DIR / DB_DIR / DB_NAME

TASKS = 'tasks'
REPEAT_DAYS = 'repeat_days'


def initialize_database():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()

            # Clear existing data from tables
            clear_tables(cur, TASKS)
            clear_tables(cur, REPEAT_DAYS)

            # Clear all ids
            cur.execute('VACUUM')
            conn.commit()

            # Create parent table
            create_table(cur, TASKS, [
                ('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
                ('name', 'TEXT'),
                ('description', 'TEXT'),
                ('start_date', 'TEXT'),
                ('duration', 'FLOAT'),
                ('is_repeatable', 'INTEGER')
            ])

            # Create child table
            create_table(cur, REPEAT_DAYS, [
                ('task_id', 'INTEGER'),
                ('day_number', 'INTEGER'),
                ('PRIMARY KEY', '(task_id)'),
                (f'FOREIGN KEY (task_id) REFERENCES {TASKS} (id)', '')
            ])

    except Exception as e:
        print(f"Error: {e}")


def clear_tables(cursor, table_name):
    cursor.execute(f'DELETE FROM {table_name}')


def create_table(cursor, table_name, columns):
    columns_str = ', '.join([f"{name} {data_type}" for name, data_type in columns])
    query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})'
    cursor.execute(query)


if __name__ == "__main__":
    initialize_database()
