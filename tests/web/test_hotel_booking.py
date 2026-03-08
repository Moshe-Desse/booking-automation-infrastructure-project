import allure
import pytest
from typing import Any
from urllib import response
from data.web.hotel_booking_data import *
from utils.common_ops import read_data_from_json
from extensions.api_verifications import APIVerify
from extensions.web_verifications import WebVerify
from data.api.hotel_booking_hotel_api_data import *
from workflows.api.hotel_booking_api_flows import HotelApiFlows
from workflows.web.hotel_booking_flows import HotelBookingFlows


class TestHotelBooking:

    
    @allure.title("Test 01 - Administrator Sign-in with Valid user name and password")
    @allure.description("This test Verify that an administrator can successfully sign in and log out")
    def test01_verify_admin_sign_in_and_log_out_possitive(self,hotel_booking_flows:HotelBookingFlows):
        hotel_booking_flows.admin_sgin_in_and_log_out(USER_NAME,PASSWORD)
        WebVerify.text(hotel_booking_flows.main.main_header,EXPECTED_MAIN_HEADER)


    @allure.title("Test 02 - Administrator Sign-in with Unvalid user name and password")
    @allure.description("This Test Verifies that an administrator cannot sign in with invalid credentials and remains logged out")
    def test02_verify_admin_sign_in_negative(self,hotel_booking_flows:HotelBookingFlows):
        hotel_booking_flows.admin_sgin_in_with_invalid_credentials(WRONG_USER_NAME,WRONG_PASSWORD)
        WebVerify.text(hotel_booking_flows.login.error_login_message,EXPECTED_FAILAD_LOGIN_MESSAGE)
        

    @allure.title("Test 03 - Verifying booking reservation")
    @allure.description("This Test Verifies that a booking reservation can be created successfully")
    def test03_verify_hotel_reservation(self, hotel_booking_flows: HotelBookingFlows):
        hotel_booking_flows.select_reservation_booking_dates("17","25")
        hotel_booking_flows.choose_available_room()
        hotel_booking_flows.fill_reservation_infomation(GUSSE_FIRST_NAME,GUSSE_LAST_NAME,GUSSE_EMAIL,GUSSE_PHONE_NUMBER)
        WebVerify.text(hotel_booking_flows.reservation.confirmed_reservation_message,EXPECTED_CONFIRMED_BOOKING_MESSAGE)


    @allure.title("Test 04 - Admin Creates a New Room")
    @allure.description("This test verifies that an administrator can create a new room from the Admin Dashboard")
    def test04_verify_createing_room_possitive(self,hotel_booking_flows:HotelBookingFlows):
        hotel_booking_flows.admin_sgin_in(USER_NAME,PASSWORD)
        hotel_booking_flows.create_new_room(ROOM_NUMBER,ROOM_PRICE,BED_TYPE,ACCESSIBLE)
       

    
    @allure.title("Test 05 - Admin Delete a Room")
    @allure.description("This test verifies that an administrator can delete a room from the Admin Dashboard")
    def test05_verify_delete_room_possitive(self,hotel_booking_flows:HotelBookingFlows):
        hotel_booking_flows.admin_sgin_in(USER_NAME,PASSWORD)
        hotel_booking_flows.delete_available_room_from_admin()


    @allure.title("Test 06 - Send Contact Message")
    @allure.description("This test verifies that a user can successfully send a contact message")
    def test06_verify_send_contact_message(self,hotel_booking_flows:HotelBookingFlows):
        hotel_booking_flows.fill_contact_field(CONTACT_NAME,CONTACT_EMAIL,CONTACT_PHONE,CONTACT_SUBJECT,CONTACT_DESCRIPTION)
        WebVerify.text(hotel_booking_flows.contact.contact_thanks_message,EXPECTED_CONTACAT_MESSAGE)


    @allure.title("Test 07 - Verify Token Is Created Successfully")
    @allure.description("This Test Verify that a token can be created and saved successfully")
    def test_verify_create_token_via_api(self, hotel_api_flows: HotelApiFlows):
        hotel_api_flows.get_token()
    

    @allure.title("Test 08 - Verify Booking Reservation via API")
    @allure.description("This test verifies that a specific booking reservation can be successfully retrieved via the API.")
    def test08_verify_booking_reservation_via_api(self, hotel_api_flows: HotelApiFlows):
        hotel_api_flows.get_booking(1)


    @allure.title("Test 09 - Verify All Bookings via API")
    @allure.description("This test verifies that all bookings can be successfully via the API.")
    def test09_verify_all_bookings_via_api(self, hotel_api_flows: HotelApiFlows):
        hotel_api_flows.get_all_bookings([1])


    @allure.title("Test 10 - Verify Create Room via API")
    @allure.description("This test verifies that a new room can be successfully created via the API and the response status code matches the expected success code")
    def test10_verify_create_room_with_api(self, hotel_api_flows:HotelApiFlows):
        response = hotel_api_flows.create_room_with_api(NEW_ROOM_DATA)
        APIVerify.status_code(response,EXPECTED_STATUS_SUCCESS_CODE)


    @allure.title("Test 11 - Verify Room Creation via API with Multiple Data Sets (DDT)")
    @allure.description("This data-driven test verifies that rooms can be created via the API using multiple sets of input data. Each dataset checks that the response status code matches the expected value.")
    @pytest.mark.parametrize("room_data", read_data_from_json("data/ddt/hotel_booking_rooms_api_data.json"), ids=lambda d: f"{d.get('test_name', 'test')}")
    def test_11_create_room_ddt_via_api(self, hotel_api_flows: HotelApiFlows, room_data: dict):
        # API של Body- שולפים את הסטטוס הצפוי ושם הטסט מהמילון כדי שלא יישלחו ב
        expected_status = room_data.pop("expected_status")
        current_test_name = room_data.pop("test_name", "Unknown Test") 
        # באמת מצפה לקבל API - מכיל רק את השדות שה room data - פה ה 
        response = hotel_api_flows.create_room_with_api(room_data)      
        print(f"\nTest name is: {current_test_name}")
        APIVerify.soft_assert_status_code(response ,expected_status)
           

    @allure.title("Test - 12 ")
    def test12_verify_no_rooms_exist_via_api(self, hotel_api_flows: HotelApiFlows):
        response = hotel_api_flows.get_all_rooms()
        rooms = response["rooms"]
        assert len(rooms) > 0

