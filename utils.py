def new_task_filter(new_task):
    filtered_task = new_task.split(", ")
    filtered_task[3] = float(filtered_task[3]) 
    filtered_task[4] = int(filtered_task[4]) 
    return filtered_task
