import requests
from app.config import DATABASE_API_URL
from typing import Dict, Any

class Notes:
    NOTE_CREATE_ROUTE = "note/create_note"
    NOTE_GET_ROUTE = "note/get_note"
    NOTE_GET_ALL_ROUTE = "note/get_all_notes"
    NOTE_UPDATE_ROUTE = "note/update_note"
    NOTE_DELETE_ROUTE = "note/delete_note"
    
    api_url = DATABASE_API_URL


    def create_note(self, note_data: Dict[str, Any]) -> Dict[str, Any]:
        url = "{}/{}".format(self.api_url, self.NOTE_CREATE_ROUTE)
        response = requests.post(url, json=note_data)
        return response.json()
    
    def get_note(self, note_id: int) -> Dict[str, Any]:
        url = "{}/{}/{}".format(self.api_url, self.NOTE_GET_ROUTE, note_id)
        response = requests.get(url)
        return response.json()
    
    def get_all_notes(self, user_id: int) -> Dict[str, Any]:
        url = "{}/{}/{}".format(self.api_url, self.NOTE_GET_ALL_ROUTE, user_id)
        response = requests.get(url)
        return response.json()
    
    def update_note(self, note_data: Dict[str, Any], note_id: int) -> Dict[str, Any]:
        url = "{}/{}/{}".format(self.api_url, self.NOTE_UPDATE_ROUTE, note_id)
        response = requests.put(url, json=note_data)
        return response.json()
        
    def delete_note(self, note_id: int) -> Dict[str, Any]:
        url = "{}/{}/{}".format(self.api_url, self.NOTE_DELETE_ROUTE, note_id)
        response = requests.delete(url)
        return response.json()