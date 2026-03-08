from playwright.sync_api import Page

class HotelBookingNavigationBar:

    def __init__(self,page:Page):
        self.page = page
        self.navigations_buttons = page.locator("[class='nav-item']")
        self.rooms_button = page.locator("//a[@class='nav-link' and text()='Rooms']")
        self.booking_button = page.locator("//a[@class='nav-link' and text()='Booking']")
        self.amnities_button = page.locator("//a[@class='nav-link' and text()='Amenities']")
        self.location_button = page.locator("//a[@class='nav-link' and text()='Location']")
        self.contact_button = page.locator("//a[@class='nav-link' and text()='Contact']")
        self.admin_button = page.locator("//a[@class='nav-link' and text()='Admin']")

