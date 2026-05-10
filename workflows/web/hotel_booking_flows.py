import json
import time
import random
import allure
from playwright.sync_api import Locator
from extensions.ui_actions import UIActions
from playwright.sync_api import APIRequestContext, Page
from page_objects.web.hotel_booking_admin_rooms_page import HotelBookingAdminRooms
from page_objects.web.hotel_booking_booking_page import HotelBooking
from page_objects.web.hotel_booking_main_page import HotelBookingMain
from page_objects.web.hotel_booking_admin_page import HotelBookingAdmin
from page_objects.web.hotel_booking_contact_page import HotelBookingContact
from page_objects.web.hotel_boking_admin_login_page import HotelBookingLogin
from page_objects.web.hotel_booking_reservation_page import HotelBookingReservation
from page_objects.web.hotel_booking_navigation_bar_page import HotelBookingNavigationBar
from utils.common_ops import read_data_from_csv

class HotelBookingFlows:

    def __init__(self,page:Page):
        self.page = page
        self.booking = HotelBooking(page)
        self.main = HotelBookingMain(page)
        self.admin = HotelBookingAdmin(page)
        self.login = HotelBookingLogin(page)
        self.contact = HotelBookingContact(page)
        self.admin_rooms = HotelBookingAdminRooms(page)
        self.reservation = HotelBookingReservation(page)
        self.navigation = HotelBookingNavigationBar(page)

    #==================
    # Sign-in Functions
    #==================

    @allure.step("Sign in:")
    def sign_in(self,username,password)-> None:
        UIActions.update_text(self.login.user_name_field,username)
        UIActions.update_text(self.login.password_field,password)
        UIActions.click(self.login.login_button)

    @allure.step("log_out:")
    def log_out(self)-> None:
        UIActions.click(self.login.log_out_button)

    #=====================
    # Navigation Functions
    #=====================

    @allure.step("Navigate_to_login:")
    def navigate_to_login_page(self)-> None:
        UIActions.click(self.navigation.admin_button)

    @allure.step("Navigate to front:")
    def navigate_to_front_page(self)-> None:
        UIActions.click(self.login.front_page_button)

    @allure.step("Navigate to contact")
    def navigate_to_contact_page(self)-> None:
        UIActions.click(self.navigation.contact_button)

    @allure.step("Navigae to booking:")
    def navigate_to_booking_page(self)-> None:
        UIActions.click(self.navigation.booking_button)

    @allure.step("Navigate to admin:")
    def navigate_to_admin_page(self)-> None:
        UIActions.click(self.navigation.admin_button)

    @allure.step("Rest page:")
    def reset_page(self)-> None:
        UIActions.click_to_reset_page(self.main.main_header,self.login.back_to_main_button)

    @allure.step("Click return home button")
    def click_return_home_button(self)-> None:
        UIActions.click(self.reservation.return_home_page_button)

    @allure.step("Navigate back and forth between pages (stress test)")
    def navigate_back_and_forth(self, actions: list, times: int)->None:
        for i in range(times):
            for action in actions:
                action()

    #==================
    # Select Function
    #==================

    @allure.step("Select past booking dates:")
    def select_past_reservation_booking_dates(self, target_month: str, from_day: str, to_day: str)-> None:
        UIActions.click(self.booking.check_in_calendar) 
        while self.booking.current_month_year.inner_text() != target_month:
            UIActions.force_click(self.booking.previous_month_button)
        UIActions.pick_day_from_datepicker(self.booking.check_in_calendar, self.booking.days, from_day)
        UIActions.click(self.booking.check_out_calendar)
        while self.booking.current_month_year.inner_text() != target_month:
            UIActions.force_click(self.booking.previous_month_button)     
        UIActions.pick_day_from_datepicker(self.booking.check_out_calendar, self.booking.days, to_day)
    
    @allure.step("Select past booking dates:")
    def select_opsite_reservation_booking_dates(self, target_month: str, from_day: str, to_day: str)-> None:
        UIActions.click(self.booking.check_in_calendar) 
        while self.booking.current_month_year.inner_text() != target_month:
            UIActions.force_click(self.booking.next_month_button)
        UIActions.pick_day_from_datepicker(self.booking.check_in_calendar, self.booking.days, from_day)
        UIActions.click(self.booking.check_out_calendar)
        while self.booking.current_month_year.inner_text() != target_month:
            UIActions.force_click(self.booking.next_month_button)     
        UIActions.pick_day_from_datepicker(self.booking.check_out_calendar, self.booking.days, to_day)

    @allure.step("Select booking dates:")
    def select_reservation_booking_dates(self,from_day:str,to_day:str)-> None:
        UIActions.click(self.booking.check_in_calendar) 
        UIActions.force_click(self.booking.next_month_button)
        UIActions.pick_day_from_datepicker(self.booking.check_in_calendar,self.booking.days,from_day)
        UIActions.click(self.booking.check_out_calendar)
        UIActions.force_click(self.booking.next_month_button)
        UIActions.pick_day_from_datepicker(self.booking.check_out_calendar,self.booking.days,to_day)

    @allure.step("Force select a specific date from the past (Jan 2024):")
    def select_specific_past_date(self)-> None:
         self.booking.check_in_calendar()

    #==================
    # Creating Function
    #==================
        
    @allure.step("Create room:")
    def create_new_room(self,room_number,room_price,bed_type,accessible)-> None:
        UIActions.update_text(self.admin_rooms.room_number_field,room_number)
        UIActions.select_option(self.admin_rooms.bed_type_options,value=bed_type)
        UIActions.select_option(self.admin_rooms.accessible_options,value=accessible)
        UIActions.update_text(self.admin_rooms.room_price_field,room_price)
        UIActions.click_all(self.admin_rooms.room_details_button)
        UIActions.click(self.admin_rooms.create_room_button)

    @allure.step("Create multiple rooms from database data")
    def create_rooms_from_db_list(self, rooms_list: list) -> None:
        for i, room in enumerate(rooms_list, 1):
            print(f"\n--- Processing Room {i} ---")
            print(json.dumps(room, indent=4))
            UIActions.update_text(self.admin_rooms.room_number_field,room["room_number"])
            UIActions.select_option(self.admin_rooms.bed_type_options,value=room["bed_type"])
            UIActions.update_text(self.admin_rooms.room_price_field,room["room_price"])       
            UIActions.select_option(self.admin_rooms.accessible_options,value=room["accessible"])
            UIActions.click_random(self.admin_rooms.room_details_button)
            UIActions.click(self.admin_rooms.create_room_button)
            self.page.wait_for_timeout(800)

    @allure.step("Creates multiple rooms based on CSV data:")
    def create_rooms_from_csv(self, file_path)-> None:
        rooms = read_data_from_csv(file_path)
        for room in rooms:
            print(f"--- Attempting to create room number: {room['room_number']} ---")
            self.create_new_room(
                room["room_number"],
                room["room_price"],
                room["bed_type"],
                room["accessible"]
                                )
            self.page.wait_for_timeout(500)
        self.page.wait_for_timeout(1000)
        return len(rooms)
    
    #====================
    # Fill form functions
    #====================

    @allure.step("Fill Contact Information:")
    def fill_contact_field(self,name,email,phone,subject,description)-> None:
        UIActions.update_text(self.contact.contact_name_field,name)
        UIActions.update_text(self.contact.contact_email_field,email)
        UIActions.update_text(self.contact.contact_phone_field,phone)
        UIActions.update_text(self.contact.contact_subject_field,subject) 
        UIActions.update_text(self.contact.contact_discription_field,description)  
        UIActions.click(self.contact.contact_submit_button)    

    @allure.step("Fill reservation information:")
    def fill_reservation_infomation(self,first_name,last_name,email,phone_number)-> None:
        UIActions.click(self.reservation.reserve_now_button)
        UIActions.update_text(self.reservation.first_name_field_button,first_name)
        UIActions.update_text(self.reservation.last_name_field,last_name)
        UIActions.update_text(self.reservation.email_field,email)
        UIActions.update_text(self.reservation.phone_number_field,phone_number)
        UIActions.click(self.reservation.finish_reservation_button)

    @allure.step("Choose available room:")
    def choose_available_room(self)-> None:
        UIActions.click(self.main.booking_room_button.first)

    #===================
    # Get data Functions
    #===================

    @allure.step("Get footer text from main page")
    def get_footer_text(self)-> str:
        footer_info = self.main.footer_container.inner_text()
        print(f"\n{footer_info}")
        return footer_info

    @allure.step("Get all available rooms")
    def get_all_available_rooms(self):
        rooms = UIActions.get_text(self.admin_rooms)
        print(f"\nAll rooms\n: {rooms}")
        return rooms
    
    @allure.step("Get admin rooms page header:")
    def get_admin_rooms_page_header(self)->str:
        header = UIActions.get_text(self.admin.admin_page_header)
        print(f"\nThe header: {header}")
        return header
    
    @allure.step("Get rooms count from admin table")
    def get_rooms_count(self)-> int:
        self.admin_rooms.create_room_button.wait_for(state="visible", timeout=5000)
        total_rooms = self.admin_rooms.room_number_list.count()
        print(f"\nThe total rooms now: {total_rooms}")
        return total_rooms
    
    @allure.step("Get clean total price from locator")
    def get_total_price(self)->int:
        price = self.booking.total_price.inner_text()
        clean_total_price = int(price.replace("£","").strip())
        print(f"\nThe total price:\n {clean_total_price}")
        return clean_total_price

    @allure.step("Get nights count from text")
    def get_nights_from_text(self, locator: Locator) -> int:
        total_nights = locator.inner_text()
        parts = total_nights.split("x")
        nights_part = parts[1]
        clean_nights = int(nights_part.replace("nights","").strip())
        return clean_nights

    @allure.step("Get clean price from locator")
    def get_clean_prices(self,locator: Locator)->int:
        price = locator.inner_text()
        clean_price = int(price.replace("£","").strip())
        print(f"\nThe price:\n {clean_price}")
        return clean_price

    @allure.step("Get text from element {locator}")
    def get_error_message_text(self,locator:Locator, timeout=5000)-> str:
        error_message = locator.inner_text()
        print(f"\n The Error Messge: {error_message}")
        return error_message
    
    #===================
    # Calculate Functions
    #===================

    @allure.step("Verify total booking price logic")
    def booking_calculation(self)-> int:
        price_per_night = self.get_clean_prices(self.booking.room_price_per_night)
        nights_sum = self.get_nights_from_text(self.booking.total_nights)
        clean_cleaning_fee = self.get_clean_prices(self.booking.cleaning_fee)
        clean_service_fee = self.get_clean_prices(self.booking.service_fee)
        total_fee = clean_cleaning_fee + clean_service_fee
        expected_total_price = (price_per_night * nights_sum) + total_fee
        print(f"The total price: {expected_total_price}")
        return expected_total_price

    #===================
    # Remove Functions
    #===================

    @allure.step("Remove all rooms from admin table:")
    def remove_all_rooms(self)-> None:
        self.admin_rooms.remove_room_button.first.wait_for(state="visible")
        rooms = self.admin_rooms.remove_room_button
        while self.admin_rooms.remove_room_button.count() > 0 :
                UIActions.click(rooms.first)
                self.page.wait_for_timeout(500)
        
    #===================
    # Timeing Functions
    #===================.

    @allure.step("UI: Measure Admin Dashboard loading duration")
    def measure_loading_time(self) -> float:        
        start_time = time.time()
        self.page.reload()
        self.page.wait_for_selector("text=Logout") 
        end_time = time.time()
        measure_time = start_time - end_time
        print(f"Measure Time : {measure_time}")
        return end_time - start_time
    
    @allure.step("Measure Dashboard loading time")
    def measure_admin_loading_performance(self) -> float:
        start_time = time.time()
        self.page.reload()      
        self.page.wait_for_selector(self.admin.room_row_locator)
        end_time = time.time()
        duration = end_time - start_time
        print(f"\n[Performance Log] Dashboard loaded in: {duration:.2f} seconds")
        return duration
    

