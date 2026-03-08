import json
from urllib import response
from extensions.api_actions import APIActions
from data.api.hotel_booking_hotel_api_data import *
from playwright.sync_api import APIRequestContext, APIResponse


class HotelApiFlows:
    
    def __init__(self,request_context:APIRequestContext):
        self.api = APIActions(request_context)
        self.token = None


    def login(self) -> APIResponse:
        payload = {
            "username": USERNAME,
            "password": PASSWORD
                  }        
        url = BOOKING_BASE_URL + LOGIN_RESOURCE
        response = self.api.post(url, payload)
        return response
    
    
    def get_all_rooms(self):
         response = self.hotel_api_requests.get_all_rooms()
         return response.json()
    

    def get_token_only_one_time(self):
            if not self.token:
                response = self.login()
                self.token = response.json().get("token")
            return self.token


    def get_token(self):
        response = self.login()
        token = response.json().get("token")  # שולף את הטוקן מה-body
        print("\nThe token is:")
        print(json.dumps({"token": token}, indent=4))  # מדפיס בטור מסודר JSON
        return token
    

    def get_booking(self, booking_id: int):
        token = self.get_token()  # שולף את הטוקן
        url = f"{BOOKING_BASE_URL}booking/{booking_id}"
        headers = {
            "Cookie": f"token={token}"  
                  }
        response = self.api.get(url, headers=headers)
        print(json.dumps(response.json(), indent=4))
        return response
    

    def get_all_bookings(self, booking_ids: list[int]):
        token = self.get_token()
        headers = {"Cookie": f"token={token}"}
        for booking_id in booking_ids:
            url = f"{BOOKING_BASE_URL}booking/{booking_id}"
            response = self.api.get(url, headers=headers)
            print(f"\nBooking {booking_id}:")
            print(json.dumps(response.json(), indent=4))

        
    def create_room_with_api(self, room_data: dict):
        token = self.get_token_only_one_time()
        url = f"{BOOKING_BASE_URL}room/"
        headers = {
            "Cookie": f"token={token}",
            "Content-Type": "application/json",
            "accept": "*/*"
                  }
        payload = room_data.copy()
        payload.pop("expected_status", None)
        payload.pop("test_name", None)
        response = self.api.post(url, payload=room_data, headers=headers)
        print("\nCreateing rooms list:")
        print(json.dumps(response.json(), indent=4))
        return response
    
    def get_all_rooms(self):
        url = f"{BOOKING_BASE_URL}room"
        response = self.api.get(url)
        return response.json()
