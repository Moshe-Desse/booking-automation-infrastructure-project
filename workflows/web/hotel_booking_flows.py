import json
import time

import allure

from extensions.ui_actions import UIActions
from playwright.sync_api import APIRequestContext, Page
from page_objects.web.hotel_booking_admin_rooms_page import HotelBookingAdminRooms
from page_objects.web.hotel_booking_page import HotelBooking
from page_objects.web.hotel_booking_main_page import HotelBookingMain
from page_objects.web.hotel_booking_admin_page import HotelBookingAdmin
from page_objects.web.hotel_booking_contact_page import HotelBookingContact
from page_objects.web.hotel_boking_admin_login_page import HotelBookingLogin
from page_objects.web.hotel_booking_reservation_page import HotelBookingReservation
from page_objects.web.hotel_booking_navigation_bar_page import HotelBookingNavigationBar

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


    #@allure.step("Sign in:")
    def sign_in(self,username,password):
        UIActions.update_text(self.login.user_name_field,username)
        UIActions.update_text(self.login.password_field,password)
        UIActions.click(self.login.login_button)

    #@allure.step("log_out:")
    def log_out(self):
        UIActions.click(self.login.log_out_button)

    #@allure.step("Navigate_to_login:")
    def navigate_to_login_page(self):
        UIActions.click(self.navigation.admin_button)

    #@allure.step("Navigate to front:")
    def navigate_to_front_page(self):
        UIActions.click(self.login.front_page_button)

    #@allure.step("Navigate to contact")
    def navigate_to_contact_page(self):
        UIActions.click(self.navigation.contact_button)

    #@allure.step("Navigae to booking:")
    def navigate_to_booking_page(self):
        UIActions.click(self.navigation.booking_button)

    #@allure.step("Navigate to admin:")
    def navigate_to_admin_page(self):
        UIActions.click(self.navigation.admin_button)

    #@allure.step("Navigate to contact:")
    def navigate_to_contact_page(self):
        UIActions.click(self.navigation.contact_button)

    #@allure.step("Rest page:")
    def reset_page(self):
        UIActions.click_to_reset_page(self.main.main_header,self.login.back_to_main_button)

    #@allure.step("Click return home button")
    def click_return_home_button(self):
        UIActions.click(self.reservation.return_home_page_button)

    #@allure.step("Create room:")
    def create_new_room(self,room_number,room_price,bed_type,accessible):
        UIActions.update_text(self.admin_rooms.room_number_field,room_number)
        UIActions.select_option(self.admin_rooms.bed_type_options,value=bed_type)
        UIActions.select_option(self.admin_rooms.accessible_options,value=accessible)
        UIActions.update_text(self.admin_rooms.room_price_field,room_price)
        UIActions.click_all(self.admin_rooms.room_details_button)
        UIActions.click(self.admin_rooms.create_room_button)

    #@allure.step("Select booking dates:")
    def select_reservation_booking_dates(self,from_day:str,to_day:str=None):
        UIActions.click(self.booking.check_in_calendar) 
        UIActions.force_click(self.booking.next_month_button)
        UIActions.pick_day_from_datepicker(self.booking.check_in_calendar,self.booking.days,from_day)
        UIActions.click(self.booking.check_out_calendar)
        UIActions.force_click(self.booking.next_month_button)
        UIActions.pick_day_from_datepicker(self.booking.check_out_calendar,self.booking.days,to_day)

    #@allure.step("Fill Contact Information:")
    def fill_contact_field(self,name,email,phone,subject,description):
        UIActions.update_text(self.contact.contact_name_field,name)
        UIActions.update_text(self.contact.contact_email_field,email)
        UIActions.update_text(self.contact.contact_phone_field,phone)
        UIActions.update_text(self.contact.contact_subject_field,subject) 
        UIActions.update_text(self.contact.contact_discription_field,description)  
        UIActions.click(self.contact.contact_submit_button)    

    #@allure.step("Choose available room:")
    def choose_available_room(self):
        UIActions.click(self.main.booking_room_button.first)

    #@allure.step("Fill reservation information:")
    def fill_reservation_infomation(self,first_name,last_name,email,phone_number):
        UIActions.click(self.reservation.reserve_now_button)
        UIActions.update_text(self.reservation.first_name_field_button,first_name)
        UIActions.update_text(self.reservation.last_name_field,last_name)
        UIActions.update_text(self.reservation.email_field,email)
        UIActions.update_text(self.reservation.phone_number_field,phone_number)
        UIActions.click(self.reservation.finish_reservation_button)

    @allure.step("Get all available rooms")
    def get_all_available_rooms(self):
        UIActions.get_text(self.admin_rooms.all_rooms_list)

    def remove_all_rooms(self):
        self.admin_rooms.remove_room_button.first.wait_for(state="visible")
        rooms = self.admin_rooms.remove_room_button
        while self.admin_rooms.remove_room_button.count() > 0 :
                UIActions.click(rooms.first)
                self.page.wait_for_timeout(500)
    
    def get_admin_rooms_page_header(self):
        UIActions.get_text(self.admin.admin_page_header)