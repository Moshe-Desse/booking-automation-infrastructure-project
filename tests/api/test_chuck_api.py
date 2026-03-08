from data.api.chuck_api_data import *
from extensions.api_verifications import APIVerify
from workflows.api.hotel_booking_api_flows import HotelApiFlows


class TestHotelsApi:

    def test01_verify_joke(self,hotel_api_flows:HotelApiFlows):
        print(hotel_api_flows.login())

