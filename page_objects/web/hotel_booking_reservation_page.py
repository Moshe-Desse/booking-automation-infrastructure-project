from playwright.sync_api import Page

class HotelBookingReservation:

    def __init__(self,page:Page):
        self.page = page
        self.reserve_now_button = page.locator("[id='doReservation']")
        self.finish_reservation_button = page.locator("[class='btn btn-primary w-100 mb-3']")
        self.cancel_reservation_button = page.locator("[class='btn btn-secondary w-100 mb-3']")
        self.first_name_field_button = page.locator("[class^='form-control room-f']")
        self.last_name_field = page.locator("[class^='form-control room-l']")
        self.email_field = page.locator("[class^='form-control room-e']")
        self.phone_number_field = page.locator("[class^='form-control room-p']")
        self.confirmed_reservation_message = page.locator("//*[@id='root-container']//div[2]//div[2]//h2")
        self.return_home_page_button = page.locator("[class='btn btn-primary w-100 mb-3 mt-3']")
        