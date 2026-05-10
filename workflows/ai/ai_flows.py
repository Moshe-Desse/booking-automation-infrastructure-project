from google.genai import types
from playwright.sync_api import Page
from page_objects.web.hotel_booking_booking_page import HotelBooking
from page_objects.web.hotel_booking_main_page import HotelBookingMain
from page_objects.web.hotel_booking_admin_page import HotelBookingAdmin
from page_objects.web.hotel_booking_contact_page import HotelBookingContact
from page_objects.web.hotel_boking_admin_login_page import HotelBookingLogin
from page_objects.web.hotel_booking_admin_rooms_page import HotelBookingAdminRooms
from page_objects.web.hotel_booking_reservation_page import HotelBookingReservation
from page_objects.web.hotel_booking_navigation_bar_page import HotelBookingNavigationBar

class AiFlows:

    def __init__(self,page:Page,ai_engine):
        self.page = page
        self.ai_model = ai_engine
        self.booking = HotelBooking(page)
        self.main = HotelBookingMain(page)
        self.admin = HotelBookingAdmin(page)
        self.login = HotelBookingLogin(page)
        self.contact = HotelBookingContact(page)
        self.admin_rooms = HotelBookingAdminRooms(page)
        self.reservation = HotelBookingReservation(page)
        self.navigation = HotelBookingNavigationBar(page)

    def extract_text_from_screen(self) -> str:
        screenshot_bytes = self.page.screenshot(type="png")
        prompt = """
        Extract all visible text from this screenshot.
        Return only the text.
        """
        response = self.ai_model.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=screenshot_bytes,
                    mime_type="image/png")])
        return response.text.lower()

    def verify_room_exists_in_admin(self, expected_room_name: str) -> bool:
        screenshot_bytes = self.page.screenshot(type="png")
        prompt = f"""
        You are analyzing an admin hotel rooms table.
        Task:
        Check if the room with name "{expected_room_name}" exists in the table.
        Return ONLY:
        - "Yes" if the room exists
        - "No" if it does not exist
        """
        response = self.ai_model.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=screenshot_bytes,
                    mime_type="image/png")])
        result = response.text.strip().lower()
        print(f"\nAI Admin Check Result: {result}")

    