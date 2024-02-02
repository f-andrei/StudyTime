


from datetime import datetime, timedelta
from pytz import timezone


def new_task_filter(new_task):
    filtered_task = new_task.split(", ")
    filtered_task[3] = float(filtered_task[3]) 
    filtered_task[4] = int(filtered_task[4]) 
    return filtered_task

def get_current_time():
    sao_paulo_tz = timezone('America/Sao_Paulo')
    current_time_utc = datetime.utcnow()
    sao_paulo_now = current_time_utc.replace(tzinfo=timezone('UTC')).astimezone(sao_paulo_tz)
    formatted_sao_paulo_now = sao_paulo_now.strftime("%d/%m/%Y %H:%M:%S")

    end_time_range = sao_paulo_now - timedelta(minutes=15)
    start_time_range = sao_paulo_now + timedelta(seconds=10)
    return end_time_range, start_time_range