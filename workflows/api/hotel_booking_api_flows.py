import json
import time
import allure
from extensions.api_actions import APIActions
from data.api.hotel_booking_hotel_api_data import *
from playwright.sync_api import APIRequestContext, APIResponse


class HotelApiFlows:
    
    def __init__(self,request_context:APIRequestContext):
        self.api = APIActions(request_context)
        self.token = None

    #=======================
    # Authentication Section 
    #=======================

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

    #====================
    # GET Request Section
    #====================

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
        print(f"\nRooms JSON Response:\n{json.dumps(response.json(), indent=4)}")
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

    @allure.step("API Step: Get Message Count")
    def get_message_count_json(self) -> dict:
        url = f"{BOOKING_BASE_URL}message/count"
        response = self.api.get(url)
        print(f"\nMessage Count JSON:\n{json.dumps(response.json(),indent=4)}")
        return response

    @allure.step("API Step: Get Hotel Branding Details")
    def get_hotel_branding(self):
        url = f"{BOOKING_BASE_URL}branding/"
        response = self.api.get(url)
        response_data = response.json()
        print("\nHotel Branding:")
        print(f"\n{json.dumps(response.json(),indent=4)}")
        return response

    @allure.step("API Step: Get Room Details by ID: {room_id}")
    def get_room_details_by_id(self, room_id: int) -> APIResponse:
        url = f"{BOOKING_BASE_URL}room/{room_id}"
        response = self.api.get(url)
        response_data = response.json()
        print("\nRoom Details by ID:")
        print(f"\n{json.dumps(response.json(),indent=4)}")
        print(response_data)
        return response

    @allure.step("API Step: Get All Bookings List (Unauthorized Check)")
    def get_all_bookings_list_unauthorized(self) -> APIResponse:
        url = f"{BOOKING_BASE_URL}booking/"
        response = self.api.get(url) 
        print("\nNegative Test - Unauthorized Access Result:")
        try:
            print(f"\n{json.dumps(response.json(), indent=4)}")
        except:
            print(f"\nResponse Body: {response.text()}")          
        return response
    
    @allure.step("API Step: Measure Health Check Latency")
    def get_health_check_latency(self) -> float:
        start_time = time.time()    
        response = self.api.get(f"{BOOKING_BASE_URL}auth/actuator/health") 
        end_time = time.time()
        duration_ms = (end_time - start_time) 
        print(f"\nHealth Check Latency: {duration_ms:.2f}ms")
        return duration_ms

    @allure.step("API Step: Get API Headers")
    def get_api_response_headers(self) -> dict:
        url = f"{BOOKING_BASE_URL}branding/"
        response = self.api.get(url)
        headers = dict(response.headers)
        print("\nResponse Headers:")
        print(f"\n{json.dumps(headers, indent=4)}")
        return headers

    @allure.step("API Step: Get Branding Data")
    def get_branding_data(self) -> dict:
        url = f"{BOOKING_BASE_URL}branding/"
        response = self.api.get(url)
        data = response.json()
        print("\nBranding Data Received:")
        print(json.dumps(data, indent=4))
        return data

    #=====================
    # POST Request Section
    #=====================

    @allure.step("API: Create mass rooms for performance - Count: {count}")
    def create_multiple_rooms(self, count: int):
        for i in range(count):
            room_data = {
                "roomName": f"LoadTest{100 + i}",
                "type": "Double",
                "accessible": True,
                "image": "https://example.com/room.jpg",
                "description": "Mass creation for load test",
                "features": ["WiFi", "TV"],
                "roomPrice": 200
                        }
            self.execute_room_creation(room_data)


    # def execute_room_creation(self, room_data: dict) -> APIResponse:
    #     data = room_data.copy()
    #     expected_status = data.pop("expected_status", None)
    #     test_name = data.pop("test_name", "Unknown Test")
    #     self._last_expected_status = expected_status
    #     self._last_test_name = test_name
    #     token = self.get_valid_token()
    #     url = f"{BOOKING_BASE_URL}room/"
    #     headers = {
    #         "Cookie": f"token={token}",
    #         "Content-Type": "application/json",
    #         "accept": "*/*"
    #     }
    #     response = self.api.post(url, payload=data, headers=headers)
    #     print("\nCreating rooms list:")
    #     print(json.dumps(response.json(), indent=4))
    #     return response

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

    #=======================
    # DELETE Request Section 
    #=======================

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

    #====================
    # PUT Request Section 
    #====================

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

    #================
    # Message Section
    #================

    def get_message_count(self) -> APIResponse:
        url = f"{BOOKING_BASE_URL}/message/count"
        response = self.api.get(url)
        try:
            print(f"\nMessage Count Response: {json.dumps(response.json(), indent=4)}")
        except:
            print(f"\nMessage Count Response (Text): {response.text()}")
        return response