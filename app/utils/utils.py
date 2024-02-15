from datetime import datetime
from utils.dt_manager import DateTimeManager
from typing import List
import json


dt_manager = DateTimeManager('America/Sao_Paulo')
dt_now = datetime.now()

def new_task_filter(new_task: str) -> List[str]:
    """Splits a single string (new_task) into task parameters"""
    filtered_task = new_task.split(", ")
    if len(filtered_task) == 5:
        try:
            filtered_task[3] = float(filtered_task[3]) 
            filtered_task[4] = int(filtered_task[4])
            return filtered_task
        except ValueError as e:
            invalid_value = filtered_task[3] if 'could not convert string to float' in str(e) else filtered_task[4]
            return f'Invalid data type. {invalid_value} must be int or float'
    else:
        try:
            filtered_task[4] = float(filtered_task[4]) 
            filtered_task[5] = int(filtered_task[5])
            return filtered_task
        except ValueError as e:
            invalid_value = filtered_task[3] if 'could not convert string to float' in str(e) else filtered_task[4]
            return f'Invalid data type. {invalid_value} must be int or float'


def new_note_filter(new_note: str) -> List[str]:
    """Splits a single string (new_note) into note parameters"""
    filtered_note = new_note.split(", ")
    return filtered_note

def save_session():
    context_path = 'app\database\context.json'
    history_path = 'app\database\history.json'
    try:
        with open(context_path, 'r') as context_file:
            context = json.load(context_file)
    except (FileNotFoundError, json.JSONDecodeError):
        context = []

    with open(context_path, 'w') as context_file:
        context_file.write('')

    context.append(datetime.now().isoformat())

    try:
        with open(history_path, 'r') as history_file:
            history = json.load(history_file)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(context)
    with open(history_path, 'w') as history_file:
        json.dump(history, history_file, indent=2, separators=(',', ':'), ensure_ascii=True)


