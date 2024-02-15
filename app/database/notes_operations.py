import sqlite3
from pathlib import Path
from utils.dt_manager import DateTimeManager

ROOT_DIR = Path(__file__).parent.parent
DB_DIR = 'database'
DB_NAME = 'studytime.sqlite3'
DB_FILE = ROOT_DIR / DB_DIR / DB_NAME
TASK_TABLE = 'tasks'
REPEAT_DAYS_TABLE = 'repeat_days'
NOTES_TABLE = 'notes'
USER_TABLE = 'user'

dt_manager = DateTimeManager('America/Sao_Paulo')

# Create a connection to the SQLite database
def establish_connection():
    """Establish a connection to the SQLite database."""
    connection = sqlite3.connect(str(DB_FILE))
    return connection


def save_note_to_database(note):
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO {NOTES_TABLE} (name, description, links, status, created_at, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                        (note.name, note.description, note.links, note.status, note.created_at, note.user_id))
            connection.commit()
            note.note_id = cursor.lastrowid
            print(f"Note '{note.name}' successfully inserted into the database.")
        except Exception as e:
            print(f"Error inserting note into the database: {e}")


def update_note_in_database(note_id, name, description, links):
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                f'UPDATE {NOTES_TABLE} SET name=?, description=?, links=? '
                'WHERE id=?',
                (name, description, links, note_id)
            )
            connection.commit()
        except Exception as e:
            print(f"Error updating task in database: {e}")


def get_notes_by_user_id(user_id):
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {NOTES_TABLE} WHERE user_id=?", (user_id,))
            notes_data = cursor.fetchall()
            return notes_data
        except Exception as e:
            print(f"Error fetching notes from database: {e}")


def get_note_by_id(note_id):
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM {NOTES_TABLE} WHERE id=?', (note_id,))
            note_data = cursor.fetchall()
            return note_data
        except Exception as e:
            print(f"Error fetching note from database: {e}")


def delete_note_from_database(note_id):
    with establish_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f'DELETE FROM {NOTES_TABLE} WHERE id = ?', (note_id,))
            connection.commit()
            print(f"Note with ID {note_id} deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting note from the database: {e}")