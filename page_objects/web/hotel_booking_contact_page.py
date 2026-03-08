from playwright.sync_api import Page

class HotelBookingContact:

    def __init__(self,page:Page):
        self.page = page
        self.contact_name_field = page.locator("[data-testid='ContactName']")
        self.contact_email_field = page.locator("[data-testid='ContactEmail']")
        self.contact_phone_field = page.locator("[data-testid='ContactPhone']")
        self.contact_subject_field = page.locator("[data-testid='ContactSubject']")
        self.contact_discription_field = page.locator("[id='description']")
        self.contact_thanks_message = page.locator("//*[@id='contact']/div//h3")
        self.contact_submit_button = page.locator("//*[@id='contact']/div//button")