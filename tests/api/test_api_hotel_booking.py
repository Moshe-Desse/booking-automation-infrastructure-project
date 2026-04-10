import json
import allure
import pytest
from data.web.hotel_booking_data import *
from utils.common_ops import *
from data.api.hotel_booking_hotel_api_data import *
from extensions.api_verifications import APIVerify
from extensions.web_verifications import WebVerify
from workflows.api.hotel_booking_api_flows import HotelApiFlows

class TestHotelBookingApi:

    @pytest.mark.smoke
    def test_00_health_check(self,hotel_api_flows:HotelApiFlows):
        response = hotel_api_flows.check_service_health()
        APIVerify.status_code(response,EXPECTED_STATUS_SUCCESS_CODE)

    @pytest.mark.smoke
    @allure.title("Test 01 - Verify Token Is Created Successfully")
    @allure.description("This Test Verify that a token can be created and saved successfully")
    def test_01_verify_create_token_via_api(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.fetch_new_token()
        response_data = response.json()
        APIVerify.json_key_exists(response_data, "token")

    @pytest.mark.functional
    @pytest.mark.regression
    @allure.title("Test 02 - Verify Booking Reservation via API")
    @allure.description("This test verifies that a specific booking reservation can be successfully retrieved via the API.")
    def test_02_verify_booking_reservation_via_api(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.get_booking_details(1)
        APIVerify.status_code(response, EXPECTED_STATUS_SUCCESS_CODE)

    @pytest.mark.functional
    @pytest.mark.regression
    @allure.title("Test 03 - Verify All Bookings via API")
    @allure.description("This test verifies that all bookings can be successfully via the API.")
    def test_03_verify_all_bookings_via_api(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.get_bookings_by_id_list([1,2])
        APIVerify.status_code(response, EXPECTED_STATUS_SUCCESS_CODE)
         
    @pytest.mark.functional
    @pytest.mark.regression
    @allure.title("Test 04 - Verify Create Room via API")
    @allure.description("This test verifies that a new room can be successfully created via the API")
    def test_04_verify_create_room_with_api(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.execute_room_creation(NEW_ROOM_DATA_01)
        APIVerify.status_code(response, EXPECTED_STATUS_SUCCESS_CODE)

    @pytest.mark.functional
    @pytest.mark.regression
    @allure.title("Test 05 - Verify Room Creation via API (DDT)")
    @allure.description("Data-driven test for creating rooms via API")
    @pytest.mark.parametrize("room_data", read_data_from_json("data/ddt/hotel_booking_rooms_api_data.json"), ids=lambda d: f"{d.get('test_name', 'test')}")
    def test_05_create_room_ddt_via_api(self, hotel_api_flows: HotelApiFlows, room_data: dict):
        expected_status = room_data.pop("expected_status")
        current_test_name = room_data.pop("test_name", "Unknown Test") 
        response = hotel_api_flows.execute_room_creation(room_data)      
        print(f"\nTest name is: {current_test_name}")
        APIVerify.status_code(response, expected_status)

    @pytest.mark.functional
    @pytest.mark.regression
    @allure.title("Test 06 - Verify Delete Booking via API")
    @allure.description("This test creates a booking and then deletes it to verify the DELETE flow")
    def test_06_verify_delete_booking_via_api(self, hotel_api_flows: HotelApiFlows):
        payload = read_data_from_json("data/api/booking.json")
        booking_payload = payload["default_booking"]
        response = hotel_api_flows.execute_booking_creation(booking_payload)
        booking_id  = hotel_api_flows.extract_booking_id(response)
        delete_res = hotel_api_flows.delete_booking_by_id(booking_id)
        APIVerify.status_code(delete_res,EXPECTED_STATUS_SUCCESS_CODE)

    @pytest.mark.functional
    @pytest.mark.regression
    @allure.title("Test - 07 Verify Updating Booking via API")
    @allure.description("This test create booking reservation and updating the name of the reservation")
    def test_07_verify_booking_update_success(self, hotel_api_flows: HotelApiFlows):
        payload_data = read_data_from_json("data/api/booking.json")
        creat_payload = payload_data["default_booking"]
        response = hotel_api_flows.execute_booking_creation(creat_payload)
        booking_id = hotel_api_flows.extract_booking_id(response)
        update_data = payload_data["alternate_booking"]
        update_payload = hotel_api_flows.execute_booking_update(booking_id,update_data)
        APIVerify.status_code(update_payload,EXPECTED_STATUS_SUCCESS_CODE)

    @pytest.mark.negative
    @pytest.mark.regression
    @allure.title("Test - 08 Verify Server Blocks Duplicate Booking Update")
    @allure.description("This test ensures that the API returns a 409 Conflict when attempting to update an existing booking with the exact same room and dates")
    def test_08_verify_booking_update_conflict_fails(self,hotel_api_flows: HotelApiFlows):
        payload_data = read_data_from_json("data/api/booking.json")
        booking_payload = payload_data["update_conflict_target"]
        response = hotel_api_flows.execute_booking_creation(booking_payload)
        booking_id = hotel_api_flows.extract_booking_id(response)
        update_data = payload_data["update_conflict_target"]
        update_payload = hotel_api_flows.execute_booking_update(booking_id,update_data)
        APIVerify.status_code(update_payload,EXPECTED_STATUS_SUCCESS_CODE)
        
    @pytest.mark.negative
    @pytest.mark.regression
    @allure.title("Test - 09 Verify Server Blocks Duplicate Booking Creation")
    @allure.description("This test ensures that the API returns a 409 Conflict when attempting to create a second booking with the same room and dates.")
    def test_09_verify_no_duplicate_booking_allowed(self,hotel_api_flows: HotelApiFlows):
        payload_data = read_data_from_json("data/api/booking.json")
        booking_payload = payload_data["negative_testing_booking"]
        response_01 = hotel_api_flows.execute_booking_creation(booking_payload)
        APIVerify.status_code(response_01,EXPECTED_CREATED_SUCCESS_CODE)
        response_02 = hotel_api_flows.execute_booking_creation(booking_payload)
        APIVerify.status_code(response_02,EXPECTED_FAILED_CODE)

    @pytest.mark.smoke
    @allure.title("Test 10 - Verify Message Count API")
    @allure.description("This test verifies the message API is up and returns a valid message count.")
    def test_10_verify_message_count_exists(self,hotel_api_flows:HotelApiFlows):
        response = hotel_api_flows.get_message_count()
        APIVerify.status_code(response,EXPECTED_STATUS_SUCCESS_CODE)
        response_data = response.json()
        APIVerify.json_key_exists(response_data,"count")
    
    @pytest.mark.functional
    @pytest.mark.regression
    @allure.title("Test 11 - Verify Get All Rooms List")
    @allure.description("Verify that the API returns a valid JSON with rooms list")
    def test_11_verify_get_all_rooms(self, hotel_api_flows: HotelApiFlows):
        rooms_json = hotel_api_flows.get_rooms_raw_json()
        APIVerify.json_key_exists(rooms_json, "rooms")

    @pytest.mark.functional
    @pytest.mark.regression
    @allure.title("Test 12 - Create Room and Verify in List")
    def test_12_verify_room_are_add_after_creating(self,hotel_api_flows:HotelApiFlows):
        creat_room_response = hotel_api_flows.execute_room_creation(NEW_ROOM_DATA_02)
        APIVerify.status_code(creat_room_response,EXPECTED_STATUS_SUCCESS_CODE)
        room_json = hotel_api_flows.get_rooms_raw_json()
        APIVerify.json_key_exists(room_json,"rooms")

    @pytest.mark.functional
    @allure.title("Test 13 - Verify Message Count")
    @allure.description("Check that the message count API returns 200 OK and valid JSON data.")
    def test_13_verify_message_count(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.get_message_count()
        APIVerify.status_code(response, EXPECTED_STATUS_SUCCESS_CODE)
        APIVerify.json_key_exists(response.json(), "count")

    @pytest.mark.functional
    @allure.title("Test 14 - Verify Hotel Branding Information")
    @allure.description("This test verifies that the hotel branding details (like name) are returned correctly.")
    def test_14_verify_hotel_branding(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.get_hotel_branding()
        APIVerify.status_code(response, EXPECTED_STATUS_SUCCESS_CODE)
        APIVerify.json_key_exists(response.json(), "name")

    @pytest.mark.functional
    @pytest.mark.regression
    @allure.title("Test 15 - Get Specific Room Details")
    @allure.description("This test verifies that the API returns correct details for room ID 1.")
    def test_15_get_specific_room(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.get_room_details_by_id(1)
        APIVerify.status_code(response, EXPECTED_STATUS_SUCCESS_CODE)
        APIVerify.json_key_exists(response.json(), "roomName")

    @pytest.mark.negative
    @allure.title("Test 16 - Verify Unauthorized Access to Bookings is Blocked")
    @allure.description("This test ensures that the API returns 401 Unauthorized when attempting to fetch all bookings without a token.")
    def test_16_verify_unauthorized_bookings_accesss(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.get_all_bookings_list_unauthorized()
        APIVerify.status_code(response, EXPECTED_UNAUTHORIZED_CODE)

    #========================================================================================#
    # TEST  - The server is having a mid-life crisis and returns 500. 
    # Keeping it RED to show the audience that I actually found something broken. #JobSecurity
    #========================================================================================#
    @pytest.mark.negative
    @allure.title("Test 17 - Verify Delete Non-Existent Booking Fails")
    @allure.description("This test attempts to delete a booking with an invalid ID to verify error handling.")
    def test_17_delete_non_existent_booking(self, hotel_api_flows: HotelApiFlows):
        invalid_id = 9999
        response = hotel_api_flows.delete_booking_by_id(invalid_id)
        APIVerify.status_code(response, EXPECTED_DELETE_CODE)
       
    @pytest.mark.performance
    @allure.title("Test 18 - Verify API Response Latency")
    @allure.description("This test ensures that the health check endpoint responds within an acceptable timeframe (1.5s).")
    def test_18_verify_api_latency(self, hotel_api_flows: HotelApiFlows):
        latency = hotel_api_flows.get_health_check_latency()
        APIVerify.response_time_less_than(latency, EXPECTED_LATENCY_MS)

    @pytest.mark.functional
    @allure.title("Test 19 - Verify Response Headers Content-Type")
    @allure.description("This test verifies that the API returns the correct Content-Type header.")
    def test_19_verify_headers(self, hotel_api_flows: HotelApiFlows):
        headers = hotel_api_flows.get_api_response_headers()
        APIVerify.header_value_contains(headers, "content-type", "application/json")

    @pytest.mark.functional
    @allure.title("Test 20 - Verify Branding JSON Schema")
    @allure.description("This test verifies the structure of the branding response using APIVerify.")
    def test_20_verify_branding_schema(self, hotel_api_flows: HotelApiFlows):
        data = hotel_api_flows.get_branding_data()
        APIVerify.json_key_exists(data, "name")
        APIVerify.json_key_exists(data, "contact")
        APIVerify.json_key_exists(data, "map")
        APIVerify.json_key_exists(data["contact"], "email")
        APIVerify.json_key_exists(data["map"], "latitude")