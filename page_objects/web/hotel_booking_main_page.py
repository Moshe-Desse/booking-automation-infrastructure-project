from playwright.sync_api import Page

class HotelBookingMain:

    def __init__(self,page:Page):
        self.page = page
        self.header = page.locator("[class^='navbar-b'] span")
        self.book_now_button = page.locator("[class^='btn btn-primary b']")
        self.main_header = page.locator("[class='display-4 fw-bold mb-4']")
        self.booking_room_button = page.locator("//a[contains(@href,'/reservation/') and contains(@class,'btn-primary')]") 


        