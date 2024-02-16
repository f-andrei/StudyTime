import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DB_DIR = 'database'
DB_NAME = 'studytime.sqlite3'
DB_FILE = ROOT_DIR / DB_DIR / DB_NAME

TASKS = 'tasks'
REPEAT_DAYS = 'repeat_days'
NOTES = 'notes'
USER = 'user'

def initialize_database():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()

            #Clear existing data from tables
            # clear_tables(cur, TASKS)
            # clear_tables(cur, REPEAT_DAYS)
            # clear_tables(cur, 'sqlite_sequence')

            # #Clear all ids
            # cur.execute('VACUUM')
            # conn.commit()

            create_table(cur, USER, [
                ('id', 'INTEGER PRIMARY KEY'),
                ('username', 'TEXT'),
                ('discriminator', 'INTEGER'),
                ('guilds', 'TEXT'),
                
            ])

            # Create parent table
            create_table(cur, TASKS, [
                ('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
                ('name', 'TEXT'),
                ('description', 'TEXT'),
                ('links', 'TEXT'),
                ('start_date', 'DATETIME'),
                ('duration', 'FLOAT'),
                ('is_repeatable', 'INTEGER'),
                ('user_id', 'INTEGER'),
                (f'FOREIGN KEY (user_id) REFERENCES {USER} (id)', '')
            ])

            # Create child table
            create_table(cur, REPEAT_DAYS, [
                ('task_id', 'INTEGER'),
                ('day_number', 'INTEGER'),
                (f'FOREIGN KEY (task_id) REFERENCES {TASKS} (id)', ''),
            ])


            create_table(cur, NOTES, [
                ('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
                ('name', 'TEXT'),
                ('description', 'TEXT'),
                ('links', 'TEXT'),
                ('status', 'TEXT'),
                ('created_at', 'DATETIME'),
                ('user_id', 'INTEGER'),
            ])
    except Exception as e:
        raise e


def clear_tables(cursor, table_name):
    cursor.execute(f'DELETE FROM {table_name}')


def create_table(cursor, table_name, columns):
    columns_str = ', '.join([f"{name} {data_type}" for name, data_type in columns])
    query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})'
    cursor.execute(query)


if __name__ == "__main__":
    initialize_database()
