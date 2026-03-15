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
            "username": USER_NAME,
            "password": PASSWORD
                  }        
        url = BOOKING_BASE_URL + LOGIN_RESOURCE
        response = self.api.post(url, payload)
        return response
    

    def get_token_only_one_time(self):
            if not self.token:
                response = self.login()
                self.token = response.json().get("token")
            return self.token


    def get_token(self):
        response = self.login()
        self.token = response.json().get("token")  # שולף את הטוקן מה-body
        print("\nThe token is:")
        print(json.dumps({"token": self.token}, indent=4))  # מדפיס בטור מסודר JSON
        return response
    

    def get_booking(self, booking_id: int):
        token = self.get_token()  
        url = f"{BOOKING_BASE_URL}booking/{booking_id}"
        headers = {
            "Cookie": f"token={self.token}"  
                  }
        response = self.api.get(url, headers=headers)
        print(json.dumps(response.json(), indent=4))
        return response
    

    def get_all_bookings(self, booking_ids: list[int]):
        token = self.get_token_only_one_time()
        headers = {"Cookie": f"token={token}"}
        for booking_id in booking_ids:
            url = f"{BOOKING_BASE_URL}booking/{booking_id}"
            response = self.api.get(url, headers=headers)
            print(f"\nBooking {booking_id}:")
            print(json.dumps(response.json(), indent=4))
            return response

        
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

    def create_booking_api(self, checkin: str, checkout: str, room_id: int = 1):
        url = f"{BOOKING_BASE_URL}booking/"
        payload = {
            "bookingid": 0,
            "roomid": room_id,
            "firstname": "Yossi",
            "lastname": "Automation",
            "depositpaid": True,
            "bookingdates": {
                "checkin": checkin,
                "checkout": checkout
            },
            "email": "test@example.com",
            "phone": "05012345678"
                  }
        headers = {"Content-Type": "application/json", "Accept": "*/*"}
        response = self.api.post(url, payload=payload, headers=headers)                
        print(f"\n--- Creating Booking for Room {room_id} ---")
        print(json.dumps(response.json(), indent=4))        
        return response

    def get_room_details_by_number(self, room_number: str):
        url = f"{BOOKING_BASE_URL}room/"
        response = self.api.get(url)        
        rooms = response.json().get("rooms", [])
        for room in rooms:
            if str(room.get("roomName")) == str(room_number):
                print(json.dumps(room))
                return room
              
    # פלואו: API (בתוך מחלקת HotelApiFlows)
    def get_all_rooms_list(self):
        url = f"{BOOKING_BASE_URL}room/"
        response = self.api.get(url)
        print(f"\nAPI Response Status: {response.status}")
        print(f"API Response Body: {response.text()}")
        rooms = response.json().get("rooms", [])
        return rooms

    def get_rooms_response_data(self):
        url = f"{BOOKING_BASE_URL}room/"
        response = self.api.get(url)
        print(f"\nResponse {response}")
        print(f"\nApi response status{response.status}")
        return response.json()
    
