import json

import allure
import pytest
from data.web.hotel_booking_data import *
from utils.common_ops import read_data_from_json
from data.api.hotel_booking_hotel_api_data import *
from extensions.api_verifications import APIVerify
from extensions.web_verifications import WebVerify
from workflows.api.hotel_booking_api_flows import HotelApiFlows

class TestHotelBookingApi:

    @allure.title("Test 01 - Verify Token Is Created Successfully")
    @allure.description("This Test Verify that a token can be created and saved successfully")
    def test_verify_create_token_via_api(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.get_token()
        response_data = response.json()
        APIVerify.json_key_exists(response_data, "token")

    @allure.title("Test 02 - Verify Booking Reservation via API")
    @allure.description("This test verifies that a specific booking reservation can be successfully retrieved via the API.")
    def test02_verify_booking_reservation_via_api(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.get_booking(1)
        APIVerify.status_code(response, EXPECTED_STATUS_SUCCESS_CODE)

    @allure.title("Test 03 - Verify All Bookings via API")
    @allure.description("This test verifies that all bookings can be successfully via the API.")
    def test03_verify_all_bookings_via_api(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.get_all_bookings([1,2])
        APIVerify.status_code(response, EXPECTED_STATUS_SUCCESS_CODE)
         

    @allure.title("Test 04 - Verify Create Room via API")
    @allure.description("This test verifies that a new room can be successfully created via the API")
    def test04_verify_create_room_with_api(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.create_room_with_api(NEW_ROOM_DATA)
        APIVerify.status_code(response, EXPECTED_STATUS_SUCCESS_CODE)

    @allure.title("Test 05 - Verify Room Creation via API (DDT)")
    @allure.description("Data-driven test for creating rooms via API")
    @pytest.mark.parametrize("room_data", read_data_from_json("data/ddt/hotel_booking_rooms_api_data.json"), ids=lambda d: f"{d.get('test_name', 'test')}")
    def test_05_create_room_ddt_via_api(self, hotel_api_flows: HotelApiFlows, room_data: dict):
        expected_status = room_data.pop("expected_status")
        current_test_name = room_data.pop("test_name", "Unknown Test") 
        response = hotel_api_flows.create_room_with_api(room_data)      
        print(f"\nTest name is: {current_test_name}")
        APIVerify.status_code(response, expected_status)



        
