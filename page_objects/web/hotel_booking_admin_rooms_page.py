from playwright.sync_api import Page

class HotelBookingAdminRooms:

    def __init__(self,page:Page):
        self.page = page
        self.rooms_information_list = page.locator("[data-testid='roomlisting']")
        self.room_details = page.locator("[id^='details']")
        self.room_number_list = page.locator("div.col-sm-1 p[id^='roomName']")
        self.room_number_field = page.locator("[data-testid='roomName']")
        self.bed_type_options = page.locator("[id='type']")
        self.accessible_options = page.locator("[id='accessible']")
        self.room_price_field = page.locator("[id='roomPrice']")
        self.create_room_button = page.locator("[id='createRoom']")
        self.room_details_button = page.locator("//*[@class='form-check-input']")
        self.remove_room_button = page.locator("[class='fa fa-remove roomDelete']")

