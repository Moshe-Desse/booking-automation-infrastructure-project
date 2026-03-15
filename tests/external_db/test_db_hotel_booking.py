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
    def test01_verify_db(self,hotel_booking_flows:HotelBookingFlows,db:DBActions):
        admin_user = db.get_data()
        hotel_booking_flows.navigate_to_login_page()
        hotel_booking_flows.sign_in(admin_user["user_name"],admin_user["password"])
        WebVerify.text(hotel_booking_flows.admin.admin_rooms_header,EXPECTED_ADMIN_HEADER)
        