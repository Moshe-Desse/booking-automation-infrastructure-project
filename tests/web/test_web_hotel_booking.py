
import json
import allure
import pytest
from data.web.hotel_booking_data import *
from extensions.api_verifications import APIVerify
from extensions.web_verifications import WebVerify
from workflows.api.hotel_booking_api_flows import HotelApiFlows
from workflows.web.hotel_booking_flows import HotelBookingFlows


class TestHotelBooking:

    
    @allure.title("Test 01 - Administrator Sign-in with Unvalid user name and password")
    @allure.description("This Test Verifies that an administrator cannot sign in with invalid credentials and remains logged out")
    def test01_verify_admin_sign_in_negative(self,hotel_booking_flows:HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.navigate_to_login_page()
        hotel_booking_flows.sign_in(WRONG_USER_NAME,WRONG_PASSWORD)
        WebVerify.text(hotel_booking_flows.login.error_login_message,EXPECTED_FAILAD_LOGIN_MESSAGE)


    @allure.title("Test 02 - Administrator Sign-in with Valid user name and password")
    @allure.description("This test Verify that an administrator can successfully sign in")
    def test02verify_admin_sign_in(self,hotel_booking_flows:HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.navigate_to_login_page()
        hotel_booking_flows.sign_in(USER_NAME,PASSWORD)
        WebVerify.text(hotel_booking_flows.admin.admin_page_header,EXPECTED_ADMIN_HEADER)       


    @allure.title("Test 03 - Verifying booking reservation")
    @allure.description("This Test Verifies that a booking reservation can be created successfully")
    def test03_verify_hotel_reservation(self, hotel_booking_flows: HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.navigate_to_booking_page()
        hotel_booking_flows.select_reservation_booking_dates("17","25")
        hotel_booking_flows.choose_available_room()
        hotel_booking_flows.fill_reservation_infomation(GUSSE_FIRST_NAME,GUSSE_LAST_NAME,GUSSE_EMAIL,GUSSE_PHONE_NUMBER)
        WebVerify.text(hotel_booking_flows.reservation.confirmed_reservation_message,EXPECTED_CONFIRMED_BOOKING_MESSAGE)


    @allure.title("Test 04 - Admin Creates a New Room")
    @allure.description("This test verifies that an administrator can create a new room from the Admin Dashboard")
    def test04_verify_createing_room_possitive(self,logged_in_flows:HotelBookingFlows, hotel_api_flows: HotelApiFlows):
        logged_in_flows.create_new_room(ROOM_NUMBER,ROOM_PRICE,BED_TYPE,ACCESSIBLE)    
        room_data = hotel_api_flows.get_room_details_by_number(ROOM_NUMBER)
        APIVerify.json_contains(room_data, {"roomName": ROOM_NUMBER})


    @allure.title("Test 05 - Admin Delete a Room")
    @allure.description("This test verifies that an administrator can delete a room from the Admin Dashboard")
    def test05_verify_remove_room_possitive(self,logged_in_flows:HotelBookingFlows,hotel_api_flows: HotelApiFlows):
        logged_in_flows.remove_all_rooms()
        response_data = hotel_api_flows.get_rooms_response_data()
        APIVerify.json_value_equals(response_data, "rooms", [])


    @allure.title("Test 06 - Send Contact Message")
    @allure.description("This test verifies that a user can successfully send a contact message")
    def test06_verify_send_contact_message(self,hotel_booking_flows:HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.navigate_to_contact_page()
        hotel_booking_flows.fill_contact_field(CONTACT_NAME,CONTACT_EMAIL,CONTACT_PHONE,CONTACT_SUBJECT,CONTACT_DESCRIPTION)
        WebVerify.text(hotel_booking_flows.contact.contact_thanks_message,EXPECTED_CONTACAT_MESSAGE)


    @allure.title("Test 07 - Verify double booking prevention")
    @allure.description("Verify double booking prevention for the same room on the same dates")
    def test07_verify_double_booking_prevention(self, hotel_booking_flows: HotelBookingFlows, reset_page_before_test):
        hotel_booking_flows.navigate_to_booking_page()
        hotel_booking_flows.select_reservation_booking_dates("17","25")
        hotel_booking_flows.choose_available_room()
        hotel_booking_flows.fill_reservation_infomation(GUSSE_FIRST_NAME,GUSSE_LAST_NAME,GUSSE_EMAIL,GUSSE_PHONE_NUMBER)
        hotel_booking_flows.click_return_home_button()
        hotel_booking_flows.navigate_to_booking_page()
        hotel_booking_flows.select_reservation_booking_dates("17","25")
        hotel_booking_flows.choose_available_room()
        hotel_booking_flows.fill_reservation_infomation(GUSSE_FIRST_NAME,GUSSE_LAST_NAME,GUSSE_EMAIL,GUSSE_PHONE_NUMBER)
        WebVerify.text(hotel_booking_flows.reservation.confirmed_reservation_message,EXPECTED_CONFIRMED_BOOKING_MESSAGE)



    