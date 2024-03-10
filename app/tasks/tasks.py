import requests
from app.config import DATABASE_API_URL

class Tasks:
    TASK_CREATE_ENDPOINT = "task/create_task"
    TASK_GET_ENDPOINT = "task/get_task"
    TASK_GET_ALL_ENDPOINT = "task/get_all_tasks"
    TASK_UPDATE_ENDPOINT = "task/update_task"
    TASK_DELETE_ENDPOINT = "task/delete_task"
    REPEAT_DAYS_ADD_ENDPOINT = "task/add_repeat_days"
    REPEAT_DAYS_GET_ENDPOINT = "task/get_repeat_days"
    
    api_url = DATABASE_API_URL

    def create_task(self, task_data: dict):
        url = "{}/{}".format(self.api_url, self.TASK_CREATE_ENDPOINT)
        response = requests.post(url, json=task_data)
        return response.json()

    def get_task(self, task_id: int):
        url = "{}/{}/{}".format(self.api_url, self.TASK_GET_ENDPOINT, task_id)
        response = requests.get(url)
        return response.json()
    
    def get_all_tasks(self, user_id: int):
        url = "{}/{}/{}".format(self.api_url, self.TASK_GET_ALL_ENDPOINT, user_id)
        response = requests.get(url)
        return response.json()
    
    def update_task(self, task_data: dict, task_id: int):
        url = "{}/{}/{}".format(self.api_url, self.TASK_UPDATE_ENDPOINT, task_id)
        response = requests.put(url, json=task_data)
        return response.json()
    
    def delete_task(self, task_id: int):
        url = "{}/{}/{}".format(self.api_url, self.TASK_DELETE_ENDPOINT, task_id)
        response = requests.delete(url)
        return response.json()
    
    def add_repeat_days(self, task_id: int, repeat_days: dict):
        url = "{}/{}/{}".format(self.api_url, self.REPEAT_DAYS_ADD_ENDPOINT, task_id)
        response = requests.post(url, json=repeat_days)
        return response.json()
    
    def get_repeat_days(self, task_id: int):
        url = "{}/{}/{}".format(self.api_url, self.REPEAT_DAYS_GET_ENDPOINT, task_id)
        response = requests.get(url)
        return response.json()
