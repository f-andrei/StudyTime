import requests
from config import DATABASE_API_URL

class User:
    USER_CREATE_USER = "user/create_user"
    USER_GET_USER = "user/get_user"
    USER_UPDATE_USERNAME = "user/update_username"
    USER_GET_CHANNEL_ID = "user/get_channel_id"
    USER_UPDATE_CHANNEL_ID= "user/update_channel_id"


    def create_user(self, user_data: dict):
        url = "{}/{}".format(DATABASE_API_URL, self.USER_CREATE_USER)
        response = requests.post(url, json=user_data)
        return response.json()
    
    def get_user(self, user_id: str):
        url = "{}/{}/{}".format(DATABASE_API_URL, self.USER_GET_USER, user_id)
        response = requests.get(url)
        return response.json()
    
    def update_username(self, username: str, user_id: str):
        url = "{}/{}/{}/{}".format(DATABASE_API_URL, self.USER_UPDATE_USERNAME, user_id, username)
        response = requests.put(url)
        return response.json()
    
    def get_channel_id(self, user_id: str):
        url = "{}/{}/{}".format(DATABASE_API_URL, self.USER_GET_CHANNEL_ID, user_id)
        response = requests.get(url)
        return response.json()

    def update_channel_id(self, channel_id: str, user_id: str):
        url = "{}/{}/{}/{}".format(DATABASE_API_URL, self.USER_UPDATE_CHANNEL_ID, user_id, channel_id)
        response = requests.put(url)
        return response.json()