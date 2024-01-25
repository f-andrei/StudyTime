def new_task_filter(new_task):
    filtered_task = new_task.split(", ")
    filtered_task[3] = float(filtered_task[3]) 
    filtered_task[4] = int(filtered_task[4]) 
    name, description, start_date, duration, is_repeatable = filtered_task
    return filtered_task
