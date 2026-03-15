from playwright.sync_api import Page

class HotelBooking:

    def __init__(self,page:Page):
        self.page = page
        self.check_in_calendar = page.locator("[class='react-datepicker__input-container']").first 
        self.check_out_calendar = page.locator("[class='react-datepicker__input-container']").last
        self.days = page.locator("[class*='react-datepicker__day'][aria-label]")
        self.next_month_button = page.locator("[class^='react-datepicker__navigation-icon react-datepicker__navigation-icon--next']")
        self.previous_month_button = page.locator("[class^='react-datepicker__navigation-icon react-datepicker__navigation-icon--p']")
        self.availability_button = page.locator("[class^='btn btn-primary w']")
        self.in_day = page.locator("[aria-label='Choose Sunday, 1 March 2026']") 
        self.rooms_full_cards = page.locator("[class='[class='card h-100 shadow-sm room-card']']")
        