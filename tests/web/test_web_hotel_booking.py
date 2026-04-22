
import json
import allure
import pytest
from data.web.hotel_booking_data import *
from extensions.api_verifications import APIVerify
from extensions.web_verifications import WebVerify
from utils.common_ops import read_data_from_csv
from workflows.api.hotel_booking_api_flows import HotelApiFlows  
from workflows.web.hotel_booking_flows import HotelBookingFlows


class TestHotelBooking:

    @pytest.mark.security
    @allure.title("Test 01 - Administrator Sign-in with Unvalid user name and password")
    @allure.description("This Test Verifies that an administrator cannot sign in with invalid credentials and remains logged out")
    def test_01_verify_admin_sign_in_negative(self,hotel_booking_flows:HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.navigate_to_login_page()
        hotel_booking_flows.sign_in(WRONG_USER_NAME,WRONG_PASSWORD)
        WebVerify.text(hotel_booking_flows.login.error_login_message,EXPECTED_FAILAD_LOGIN_MESSAGE)

    @pytest.mark.smoke
    @allure.title("Test 02 - Administrator Sign-in with Valid user name and password")
    @allure.description("This test Verify that an administrator can successfully sign in")
    def test_02_verify_admin_sign_in(self,hotel_booking_flows:HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.navigate_to_login_page()
        hotel_booking_flows.sign_in(USER_NAME,PASSWORD)
        WebVerify.text(hotel_booking_flows.admin.admin_page_header,EXPECTED_ADMIN_HEADER)       

    @pytest.mark.functional
    @allure.title("Test 03 - Verifying booking reservation")
    @allure.description("This Test Verifies that a booking reservation can be created successfully")
    def test_03_verify_hotel_reservation(self, hotel_booking_flows: HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.navigate_to_booking_page()
        hotel_booking_flows.select_reservation_booking_dates(CHECK_IN_DATES,CHECK_OUT_DATES)
        hotel_booking_flows.choose_available_room()
        hotel_booking_flows.fill_reservation_infomation(GUSSE_FIRST_NAME,GUSSE_LAST_NAME,GUSSE_EMAIL,GUSSE_PHONE_NUMBER)
        WebVerify.text(hotel_booking_flows.reservation.confirmed_reservation_message,EXPECTED_CONFIRMED_BOOKING_MESSAGE)

    @pytest.mark.regression
    @allure.title("Test 04 - Admin Creates a New Room")
    @allure.description("This test verifies end-to-end room creation by creating a room via the Admin Dashboard UI "
                        "and validating the room data via API")
    def test_04_verify_createing_room_possitive(self,logged_in_flows:HotelBookingFlows, hotel_api_flows: HotelApiFlows):
        logged_in_flows.create_new_room(ROOM_NUMBER,ROOM_PRICE,BED_TYPE,ACCESSIBLE)    
        room_data = hotel_api_flows.get_room_details_by_number(ROOM_NUMBER)
        APIVerify.json_contains(room_data, {"roomName": ROOM_NUMBER})

    @pytest.mark.api_integration
    @allure.title("Test 05 - Admin Delete a Room")
    @allure.description("This test verifies that an administrator can delete a room from the Admin Dashboard")
    def test_05_verify_remove_room_possitive(self,logged_in_flows:HotelBookingFlows,hotel_api_flows: HotelApiFlows):
        logged_in_flows.remove_all_rooms()
        response_data = hotel_api_flows.get_rooms_raw_json()
        APIVerify.json_value_equals(response_data, "rooms", [])

    @pytest.mark.ui_only
    @allure.title("Test 06 - Send Contact Message")
    @allure.description("This test verifies that a user can successfully send a contact message")
    def test_06_verify_send_contact_message(self,hotel_booking_flows:HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.navigate_to_contact_page()
        hotel_booking_flows.fill_contact_field(CONTACT_NAME,CONTACT_EMAIL,CONTACT_PHONE,CONTACT_SUBJECT,CONTACT_DESCRIPTION)
        WebVerify.text(hotel_booking_flows.contact.contact_thanks_message,EXPECTED_CONTACAT_MESSAGE)

    @pytest.mark.complex_logic
    @allure.title("Test 07 - Verify double booking prevention")
    @allure.description("Verify double booking prevention for the same room on the same dates")
    def test_07_verify_double_booking_prevention(self, hotel_booking_flows: HotelBookingFlows, reset_page_before_test):
        hotel_booking_flows.navigate_to_booking_page()
        hotel_booking_flows.select_reservation_booking_dates(CHECK_IN_DATES,CHECK_OUT_DATES)
        hotel_booking_flows.choose_available_room()
        hotel_booking_flows.fill_reservation_infomation(GUSSE_FIRST_NAME,GUSSE_LAST_NAME,GUSSE_EMAIL,GUSSE_PHONE_NUMBER)
        hotel_booking_flows.click_return_home_button()
        hotel_booking_flows.navigate_to_booking_page()
        hotel_booking_flows.select_reservation_booking_dates(CHECK_IN_DATES,CHECK_OUT_DATES)
        hotel_booking_flows.choose_available_room()
        hotel_booking_flows.fill_reservation_infomation(GUSSE_FIRST_NAME,GUSSE_LAST_NAME,GUSSE_EMAIL,GUSSE_PHONE_NUMBER)
        WebVerify.text(hotel_booking_flows.reservation.confirmed_reservation_message,EXPECTED_CONFIRMED_BOOKING_MESSAGE)

    @pytest.mark.data_driven
    @allure.title("Test 08 - Data Driven: Create Rooms from CSV")
    @allure.description("Validates room creation by importing data from a CSV file and verifying the updated room count.")
    def test_08_verify_create_rooms_from_csv(self,logged_in_flows:HotelBookingFlows,reset_page_before_test):
        before_count = logged_in_flows.get_rooms_count()
        added_rooms = logged_in_flows.create_rooms_from_csv("data/web/rooms.csv")
        after_count = logged_in_flows.get_rooms_count()
        WebVerify.strings_are_equal(before_count + added_rooms, after_count)

    @pytest.mark.sanity
    @allure.title("Test 09 - Verify Footer Information")
    @allure.description("Verifies that all footer contact details and branding information are correctly displayed.")
    def test_09_verify_footer_text_are_visible(self, hotel_booking_flows:HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.get_footer_text()
        WebVerify.soft_is_visible(hotel_booking_flows.main.footer_container,"ERROR: Footer is not visible!")
        WebVerify.soft_all()   

    @pytest.mark.negative
    @allure.title("Test 10 - Prevent Reservation in Past Dates")
    @allure.description("Verifies that the system blocks room reservations for dates that have already passed.")
    def test_10_verify_past_date_reservation_blocking(self, hotel_booking_flows: HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.navigate_to_booking_page()
        hotel_booking_flows.select_past_reservation_booking_dates(OLD_MONTH_YEAR,OLD_CHECK_IN_DATES,OLD_CHECK_OUT_DATES)
        hotel_booking_flows.choose_available_room()
        hotel_booking_flows.fill_reservation_infomation(GUSSE_FIRST_NAME,GUSSE_LAST_NAME,GUSSE_EMAIL,GUSSE_PHONE_NUMBER)
        WebVerify.text(hotel_booking_flows.reservation.confirmed_reservation_message,EXPECTED_FAILED_BOOKING_MESSAGE)

    @pytest.mark.negative
    @allure.title("Test 11 - Verify Error for Invalid Date Selection")
    @allure.description("This test validates that the system prevents hotel bookings when the checkout date is set before the check-in date")
    def test_11_verify_booking_error_on_invalid_date_range(self, hotel_booking_flows: HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.navigate_to_booking_page()
        hotel_booking_flows.select_opsite_reservation_booking_dates(WRONG_MONTH_YEAR,WRONG_CHECK_IN,WRONG_CHECK_OUT)
        hotel_booking_flows.choose_available_room()
        try:
            hotel_booking_flows.fill_reservation_infomation(GUSSE_FIRST_NAME, GUSSE_LAST_NAME, GUSSE_EMAIL, GUSSE_PHONE_NUMBER)
            WebVerify.text(hotel_booking_flows.reservation.confirmed_reservation_message,EXPECTED_FAILED_BOOKING_MESSAGE)
        except Exception as e:
            current_url = hotel_booking_flows.page.url
            if WRONG_CHECK_IN in current_url and WRONG_CHECK_OUT in current_url:
                raise AssertionError(f"\nCRITICAL BUG IDENTIFIED: The site crashed or got stuck.\n URL at failure: :{current_url}")
                    

            
