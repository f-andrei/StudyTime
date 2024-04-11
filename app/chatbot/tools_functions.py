import sqlite3
from config import DB_FILE


def analyze_all_tables():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()

        result = []
        for table in tables:
            table_name = table[0]
            result.append(get_table_info(table_name))
      

    return '\n'.join(result)

def analyze_table(table_name):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table_name})")
        table_info = cur.fetchall()

        # List of tuples containing name, data type, and additional information of each attribute
        column_info = []
        for column in table_info:
            column_name = column[1]
            data_type = column[2]
            if column_name == 'is_repeatable':
                additional_info = "1 or 0 (1 for true/yes, 0 for false/no)"
            if column_name == 'day_number':
                additional_info = "Day of the week (0: Sunday, 1: Monday, 2: tuesday, 3: wednesday, 4: thursday, 5: friday, 6: saturday)"
            else:
                additional_info = None
            column_info.append((column_name, data_type, additional_info))

    return column_info

def get_table_info(table_name):
    table_info = []
    columns_info = analyze_table(table_name)
    column_names = [column[0] for column in columns_info]
    column_data_types = [column[1] for column in columns_info]
    additional_info = [column[2] for column in columns_info]

    # Add start_date format if exists
    if 'start_date' in column_names:
        start_date_index = column_names.index('start_date')
        start_date_data_type = column_data_types[start_date_index]
        if start_date_data_type.lower() == 'text':
            start_date_format = 'DD/MM/YYYY HH:MM:SS'
            additional_info[start_date_index] = f"Start Date Format: {start_date_format}"

    for name, data_type, info in zip(column_names, column_data_types, additional_info):
        table_info.append(f"{name}: {data_type}" + (f" ({info})" if info else ""))

    table_info_str = f"Table: {table_name}\n"
    table_info_str += "\n".join(table_info)
    return table_info_str


