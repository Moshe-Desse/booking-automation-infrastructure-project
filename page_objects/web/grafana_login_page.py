from playwright.sync_api import Page

class GrafanaLoginPage:

    def __init__(self,page:Page):
        self.page = page
        self.user_name_field = page.locator("[id=':r0:']")
        self.password_field = page.locator("[id=':r1:']")
        self.login_button = page.locator("[data-testid^='data-testid L']") 
        self.rest_password_button = page.locator("[class^='css-1pd']")
        self.show_password_on_screen_button = page.locator("[aria-controls=':r1:']")
        self.skip_update_password_button = page.locator("[data-testid^='data-testid S']")
        self.failed_login_message = page.locator("[class='css-91zald']")