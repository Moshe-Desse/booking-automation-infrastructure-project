
import json
import time
import allure
import pytest
from utils.common_ops import *
from data.web.hotel_booking_data import *
from extensions.ai_verifications import AiVerify
from extensions.api_verifications import APIVerify
from extensions.web_verifications import WebVerify
from workflows.ai.ai_agent_flows import AiAgentFlows
from workflows.ai.ai_flows import AiFlows
from workflows.api.hotel_booking_api_flows import HotelApiFlows  
from workflows.web.hotel_booking_flows import HotelBookingFlows
from playwright.sync_api import Locator

class TestHotelBooking:

    @pytest.mark.security
    @allure.title("Test 01 - Administrator Sign-in with Unvalid user name and password")
    @allure.description("This Test Verifies that an administrator cannot sign in with invalid credentials and remains logged out")
    def test_01_verify_admin_sign_in_negative(self,hotel_booking_flows:HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.navigate_to_admin_page()
        hotel_booking_flows.sign_in(WRONG_USER_NAME,WRONG_PASSWORD)
        WebVerify.text(hotel_booking_flows.login.error_login_message,EXPECTED_FAILAD_LOGIN_MESSAGE)

    @pytest.mark.smoke
    @allure.title("Test 02 - Administrator Sign-in with Valid user name and password")
    @allure.description("This test Verify that an administrator can successfully sign in")
    def test_02_verify_admin_sign_in(self,hotel_booking_flows:HotelBookingFlows,reset_page_before_test):
        hotel_booking_flows.navigate_to_admin_page()
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
    @allure.description("This test verifies end-to-end room creation by creating a room via Admin UI Dashboard  "
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
    def test_08_verify_create_rooms_from_csv(self,logged_in_flows:HotelBookingFlows):
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
                    
    @pytest.mark.logic
    @allure.title("Test 12 - Verify Booking Total Price Calculation")
    @allure.description("Calculates (Price per Night * Nights) and compares it with the UI total price.")
    def test_12_verify_booking_price_logic(self, hotel_booking_flows: HotelBookingFlows, reset_page_before_test):
        hotel_booking_flows.navigate_to_booking_page()
        hotel_booking_flows.select_reservation_booking_dates(CHECK_IN_DATES,CHECK_OUT_DATES)
        hotel_booking_flows.choose_available_room()
        actual_price = hotel_booking_flows.booking_calculation()
        expected_price = hotel_booking_flows.get_total_price()
        WebVerify.strings_are_equal(actual_price,expected_price)

    @pytest.mark.performance
    @allure.title("Test 13 - Performance: System Load Test")
    @allure.description("Measures Admin Dashboard loading time under a load of 50 rooms created via API.")
    def test_13_verify_performance_load(self, logged_in_flows: HotelBookingFlows, hotel_api_flows: HotelApiFlows):
        hotel_api_flows.create_multiple_rooms(count=50)
        duration = logged_in_flows.measure_loading_time()
        WebVerify.strings_are_equal(duration < 5, True,f"Performance fail: Loading took {duration:.2f}s")

    @allure.title("Test 14 - Testing invalid data in the booking form")
    @allure.description("This test runs many scenarios with wrong info to make sure the website shows error messages.")
    @pytest.mark.parametrize("data", read_data_from_json("data/ddt/contact_form_negative_data.json"), ids=lambda d: d["test_name"])
    def test_14_verify_reservation_negative_validation_ddt(self, hotel_booking_flows:HotelBookingFlows, data, reset_page_before_test):
        expected_error = data.pop("expected_error")
        hotel_booking_flows.navigate_to_booking_page()
        hotel_booking_flows.select_reservation_booking_dates(CHECK_IN_DATES,CHECK_OUT_DATES) 
        hotel_booking_flows.choose_available_room()
        hotel_booking_flows.fill_reservation_infomation( data["first_name"], data["last_name"], data["email"], data["phone_number"])
        actual_text = hotel_booking_flows.get_error_message_text(hotel_booking_flows.reservation.error_messages_container)       
        WebVerify.contains_string(actual_text,expected_error,f"The error message is {expected_error}")

    @pytest.mark.negative
    @allure.title("Test 15 - ")
    @allure.description(" ")
    @pytest.mark.parametrize ("data",read_data_from_csv("data/ddt/contact_form_negative_data.csv"), ids=lambda d: d["test_name"])
    def test_15_verify_invalid_data_in_the_contac_form(self,hotel_booking_flows:HotelBookingFlows,data,reset_page_before_test):
        expected_error = data.pop("expected_error")
        hotel_booking_flows.navigate_to_contact_page()
        hotel_booking_flows.fill_contact_field(data["name"], data["email"],data["phone"], data["subject"],data["message"])
        actual_text = hotel_booking_flows.get_error_message_text(hotel_booking_flows.contact.contact_error_message)
        WebVerify.contains_string(actual_text,expected_error,f"The error message is {expected_error}")

    @pytest.mark.stability
    @allure.title("Test 16 - Navigation Stress and Stability Between Pages")
    @allure.description("This test verifies the stability and reliability of navigation between different pages ")
    def test_16_multiple_navigation_back_and_forth(self, hotel_booking_flows:HotelBookingFlows,reset_page_before_test):
        expected_header = hotel_booking_flows.booking.booking_page_header
        hotel_booking_flows.navigate_back_and_forth(actions=[
        hotel_booking_flows.navigate_to_booking_page,
        hotel_booking_flows.navigate_to_admin_page,
        hotel_booking_flows.navigate_to_front_page],times=10)
        WebVerify.text(expected_header, BOOKING_PAGE_HEADER)
        
    @pytest.mark.security
    @pytest.mark.negative_test
    @allure.title("Test 17 - SQL Injection Attempt in Room Creation")
    @allure.description("Check that the system blocks SQL injection in the room name and shows an error.")
    def test_17_room_name_sql_injection(self, logged_in_flows:HotelBookingFlows,reset_page_before_test):
        error_message = logged_in_flows.create_new_room(SQL_INVALID_DATA, SQL_ROOM_NUMBER, SQL_ROOM_TYPE, TRUE)
        WebVerify.text(error_message, INVALID_INPUT)     
                
    @pytest.mark.ui
    @pytest.mark.ai_vision
    @allure.title("Test 18 - Visual Verification of Password Field on Login Screen via AI")
    @allure.description("Use AI to scan the screen and make sure the word 'password' appears on the login page.")
    def test_18_login_screen_contains_password(self,ai_flows:AiFlows,hotel_booking_flows:HotelBookingFlows):
        hotel_booking_flows.navigate_to_admin_page()
        actual_text = ai_flows.extract_text_from_screen()
        AiVerify.verify_text_exists(actual_text=actual_text,expected_text=EXPECTET_TEXT_FOR_AI)

    def test_login_with_ai_agent(ai_agent:AiAgentFlows, hotel_booking_flows:HotelBookingFlows):
        hotel_booking_flows.navigate_to_admin_page()
        ai_agent.run_flow("Login to admin system")
        
