import json
import allure
from extensions.api_actions import APIActions
from data.api.hotel_booking_hotel_api_data import *
from playwright.sync_api import APIRequestContext, APIResponse


class HotelApiFlows:
    
    def __init__(self,request_context:APIRequestContext):
        self.api = APIActions(request_context)
        self.token = None

    # --- Authentication Section ---

    @allure.step("API Step: Check Service Health (Ping)")
    def check_service_health(self)-> APIResponse:
        url = f"{BOOKING_BASE_URL}auth/actuator/health"
        response = self.api.get(url)
        print(f"\nHealth Check Response: {response.text()}")
        return response
    
    @allure.step("API Step: Authenticate User and Get Response")
    def authenticate(self) -> APIResponse:
        payload = {
            "username": USER_NAME,
            "password": PASSWORD
                  }        
        url = BOOKING_BASE_URL + LOGIN_RESOURCE
        response = self.api.post(url, payload)
        return response
    
    @allure.step("API Step: Get Valid Authentication Token")
    def get_valid_token(self)-> str:
        if not self.token:
            response = self.authenticate()
            self.token = response.json().get("token")
        return self.token

    @allure.step("API Step: Fetch and Print New Token")
    def fetch_new_token(self)-> APIResponse:
        response = self.authenticate()
        self.token = response.json().get("token")  # שולף את הטוקן מה-body
        print("\nThe token is:")
        print(json.dumps({"token": self.token}, indent=4))  # מדפיס בטור מסודר JSON
        return response

    # --- GET Request Section ---

    @allure.step("API Step: Get Details for Booking ID: {booking_id}")
    def get_booking_details(self, booking_id: int)-> APIResponse: 
        token = self.get_valid_token()  
        url = f"{BOOKING_BASE_URL}booking/{booking_id}"
        headers = {
            "Cookie": f"token={token}"  
                  }
        response = self.api.get(url, headers=headers)
        print(json.dumps(response.json(), indent=4))
        return response
    
    @allure.step("API Step: Get Details for Multiple Bookings: {booking_ids}")
    def get_bookings_by_id_list(self, booking_ids: list[int])-> APIResponse:
        token = self.get_valid_token()
        headers = {"Cookie": f"token={token}"}
        for booking_id in booking_ids:
            url = f"{BOOKING_BASE_URL}booking/{booking_id}"
            response = self.api.get(url, headers=headers)
            print(f"\nBooking {booking_id}:")
            print(json.dumps(response.json(), indent=4))
            return response
    
    @allure.step("API Step: Get All Rooms Data (JSON)")
    def get_all_rooms_data(self)-> dict:
        url = f"{BOOKING_BASE_URL}room"
        response = self.api.get(url)
        return response.json()

    @allure.step("API Step: Get List of All Rooms")
    def get_all_rooms_list(self)-> list:
        url = f"{BOOKING_BASE_URL}room/"
        response = self.api.get(url)
        print(f"\nAPI Response Status: {response.status}")
        print(f"API Response Body: {response.text()}")
        rooms = response.json().get("rooms", [])
        return rooms

    @allure.step("API Step: Get Raw JSON for All Rooms")
    def get_rooms_raw_json(self)-> dict:
        url = f"{BOOKING_BASE_URL}room/"
        response = self.api.get(url)
        print(f"\nResponse {response}")
        print(f"\nApi response status{response.status}")
        return response.json()

    @allure.step("API Step: Find Room Details by Number: {room_number}")
    def get_room_details_by_number(self, room_number: str) -> dict:
        url = f"{BOOKING_BASE_URL}room/"
        response = self.api.get(url)        
        rooms = response.json().get("rooms", [])
        for room in rooms:
            if str(room.get("roomName")) == str(room_number):
                print(json.dumps(room))
                return room

    # --- POST Request Section ---

    @allure.step("API Step: Create New Room with Data: {room_data}")
    def execute_room_creation(self, room_data: dict)-> APIResponse:
        token = self.get_valid_token()
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
    
    @allure.step("API Step: Create New Booking Reservation")
    def execute_booking_creation(self, payload: dict) -> APIResponse:
        url = f"{BOOKING_BASE_URL}booking/"
        headers = {"Content-Type": "application/json", "Accept": "*/*"}
        print(f"\n--- Creating Booking Reservation ---")
        print(json.dumps(payload, indent=4))        
        response = self.api.post(url, payload=payload, headers=headers)       
        print("\n--- Response received ---")
        print(f"Status Code :{response.status}) ")
        try:
            print(json.dumps(response.json(), indent=4))          
        except:
            print(response.text())
        return response
    
    # --- DELETE Request Section ---

    @allure.step("API Step: Delete Booking ID: {booking_id}")
    def delete_booking_by_id(self,booking_id:int) -> APIResponse:
        token = self.get_valid_token()
        url = f"{BOOKING_BASE_URL}booking/{booking_id}"
        headers = { "Cookie":f"token={token}","Content-Type":"application/json","Accept":"application/json"}
        response = self.api.delete(url,headers=headers)
        print(f"\n --- Delete Booking - {booking_id} ---")
        return response
    
    @allure.step("API Step: Extract Booking ID from Response")
    def extract_booking_id(self, response:APIResponse) -> int:
        extract = response.json().get("bookingid")
        print(f"\nThe extract id is: {extract}")
        return extract

        # --- PUT Request Section ---

    @allure.step("API Step: Update Booking ID: {booking_id}")
    def execute_booking_update(self,booking_id:int, payload:dict) -> APIResponse:
        token = self.get_valid_token()
        url = f"{BOOKING_BASE_URL}booking/{booking_id}"
        headers = {"Cookie": f"token={token}","Content-Type":"application/json","Accept":"application/json"}
        print(f"\n --- Updating Booking Reservation ID: {booking_id} --- ")
        print(json.dumps(payload,indent=4))
        response = self.api.put(url,payload=payload,headers=headers)
        print("\n --- Response received --- ")
        try:
            print(json.dumps(response.json(), indent=4))
        except: 
            print(response.text())
        return response
    
        # --- Message Section ---

    def get_message_count(self) -> APIResponse:
        url = f"{BOOKING_BASE_URL}/message/count"
        response = self.api.get(url)
        try:
            print(f"\nMessage Count Response: {json.dumps(response.json(), indent=4)}")
        except:
            print(f"\nMessage Count Response (Text): {response.text()}")
        return response