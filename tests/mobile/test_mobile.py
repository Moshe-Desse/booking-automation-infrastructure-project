import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data.web.hotel_booking_data import HOTEL_BOOKING_URL

class TestMobileUi:

    def test_01_verify_open_restful_booker(self, mobile_driver):
        mobile_driver.get(HOTEL_BOOKING_URL)
        print(f"\nTitle is:\n {mobile_driver.title}")
        assert "Restful-booker-platform demo" in mobile_driver.title

