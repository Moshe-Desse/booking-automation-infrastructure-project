from playwright.sync_api import Page

class HotelBookingAdmin:

    def __init__(self,page:Page):
        self.page = page
        self.admin_room_button = page.locator("//*[@id='navbarSupportedContent']/ul[1]/li[1]")
        self.admin_report_button = page.locator("[id='reportLink']")
        self.admin_branding_button = page.locator("[id='brandingLink']")
        self.admin_message_button = page.locator("//*[@id='navbarSupportedContent']//li[4]/a")
        self.admin_page_header = page.locator("//a[text()='Restful Booker Platform Demo']")
        self.fill_room_number_field = page.locator("[data-testid='roomName']")
        self.bed_type_options = page.locator("[id='type']")
        self.accessible_options = page.locator("[id='accessible']")
        self.room_price_field = page.locator("[id='roomPrice']")
        self.all_room_details = page.locator("//*[@class='form-check-input']")
        self.create_room_button = page.locator("[id='createRoom']")
        self.remove_room_button = page.locator("//span[contains(@class,'roomDelete')]")
        self.rew_room_ditails_header = page.locator("[class='col-sm-5 rowHeader']")
        self.delete_room_button = page.locator("//*[@class='col-sm-1']/span")

