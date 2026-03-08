from playwright.sync_api import Page
from extensions.ui_actions import UIActions
from page_objects.web.grafana_home_page import GrafanaHomePage
from page_objects.web.grafana_login_page import GrafanaLoginPage

class GrafanaWebFlows:

    def __init__(self,page:Page):
        self.page = page
        self.login = GrafanaLoginPage(page)
        self.home  = GrafanaHomePage(page)

    def fill_login_fields(self,username,password):
        self.login.user_name_field.fill(username)
        self.login.password_field.fill(password)

    def click_on_login_button(self):
        self.login.login_button.click()

    def click_on_skip_button(self):
        self.login.skip_update_password_button.click()

    def get_failed_login_message(self):
        failed_message = self.login.failed_login_message.inner_text()
        print(f"\nThe login negative message: {failed_message}")
        return failed_message

    def get_home_page_header(self):
        header = self.home.header.inner_text()
        print(f"\nThe Home Page header: {header}")
        return header   

    def creat_new_dashboard(self):
        UIActions.click(self.home.plus_button)
        UIActions.click(self.home.new_dashboard_button) 
        UIActions.click(self.home.add_visualization_button)
        UIActions.click(self.home.save_dashboard_button)
        UIActions.click(self.home.source_test_data)
        UIActions.update_text(self.home.title_field)

    def get_login_failed_message(self):
        failed_login = self.login.failed_login_message
        print(f"\nFailed Login Message: {failed_login}")
        return failed_login
    
 