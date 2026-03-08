from playwright.sync_api import Page

class HotelBookingLogin:

    def __init__(self,page:Page):
        self.page = page
        self.login_header = page.locator("[class='card-header']")
        self.user_name_field = page.locator("[id='username']")
        self.password_field = page.locator("[id='password']")
        self.login_button = page.locator("[id='doLogin']")
        self.log_out_button = page.locator("[class^='btn btn-o']")
        self.front_page_button = page.locator("[id='frontPageLink']")
        self.back_to_main_button = page.locator("[class='navbar-brand']")
        self.error_login_message = page.locator("[class='alert alert-danger']")
        