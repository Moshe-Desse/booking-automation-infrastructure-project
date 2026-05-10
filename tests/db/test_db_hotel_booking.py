import os
import allure
import pytest
from data.web.hotel_booking_data import *
from extensions.db_actions import DBActions
from extensions.web_verifications import WebVerify
from workflows.web.hotel_booking_flows import HotelBookingFlows

class TestDBHotelBooking:
    
    @allure.title("Test 01 - Verify Admin Login via DB")
    @allure.description("This test retrieves admin credentials from an external Database, performs a login via the UI, and verifies the Admin Rooms header text.")
    def test01_verify_db(self,hotel_booking_flows:HotelBookingFlows,db:DBActions,reset_page_before_test):
        admin_user = db.get_data()
        hotel_booking_flows.navigate_to_login_page()
        hotel_booking_flows.sign_in(admin_user["user_name"],admin_user["password"])
        WebVerify.text(hotel_booking_flows.admin.admin_rooms_header,EXPECTED_ADMIN_HEADER)
     

    @allure.title("Create All Rooms From DB")
    def test_create_all_rooms_from_db(self, hotel_booking_flows: HotelBookingFlows, db_rooms: DBActions,reset_page_before_test):
        all_rooms = db_rooms.get_all_rooms_as_dicts()
        hotel_booking_flows.navigate_to_admin_page()
        hotel_booking_flows.sign_in(USER_NAME, PASSWORD)
        hotel_booking_flows.create_rooms_from_db_list(all_rooms)

        