from playwright.sync_api import Page

class HotelBookingAdmin:

    def __init__(self,page:Page):
        self.page = page
        self.admin_rooms_header = page.locator("[class='navbar-brand'][href='/']")
        self.admin_room_button = page.locator("//*[@id='navbarSupportedContent']/ul[1]/li[1]")
        self.admin_report_button = page.locator("[id='reportLink']")
        self.admin_branding_button = page.locator("[id='brandingLink']")
        self.admin_message_button = page.locator("//*[@id='navbarSupportedContent']//li[4]/a")
        self.admin_page_header = page.locator("//a[text()='Restful Booker Platform Demo']")
