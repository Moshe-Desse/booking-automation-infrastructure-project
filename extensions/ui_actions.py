import allure
from playwright.sync_api import Locator, Page

from utils.common_ops import load_config

CONFIG = load_config()
DEFAULT_TIMEOUT = CONFIG["DEFAULT_COMMAND_TIMEOUT"]

class UIActions:

    @staticmethod
    @allure.step("Navigte to")
    def navigate_to(page:Page,url:str):
        page.goto(url)

    @staticmethod
    @allure.step("Click on element")
    def click(element: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        element.wait_for(state="visible", timeout=timeout)
        element.wait_for(state="attached", timeout=timeout)
        element.click(timeout=timeout)

    @staticmethod
    @allure.step("Force click on element (JS click)")
    def  force_click(element: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        element.wait_for(state="attached", timeout=timeout)
        element.evaluate("el => el.click()")

    @staticmethod
    @allure.step("Get text from element")
    def get_text(element: Locator, timeout: int = DEFAULT_TIMEOUT) -> str:
        element.wait_for(state="visible", timeout=timeout)
        tag_name = element.evaluate("el => el.tagName.toLowerCase()")
        if tag_name in ["input", "textarea"]:
            text = element.input_value(timeout=timeout)
        else:
            text = element.inner_text(timeout=timeout)
        return text.strip()

    @staticmethod
    @allure.step("Select option: {value} - {label}")
    def select_option(element: Locator, value: str = None, label: str = None, timeout: int = DEFAULT_TIMEOUT) -> None:
        element.wait_for(state="visible", timeout=timeout)
        if value:
            element.select_option(value=value)
        elif label:
            element.select_option(label=label)

    @staticmethod
    @allure.step("Update text in element to: '{text}'")
    def update_text(element: Locator, text: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        element.wait_for(state="visible", timeout=timeout)
        element.fill("")  # clear first (more stable)
        element.fill(text, timeout=timeout)


    @staticmethod
    @allure.step("Click all options in element:")
    def click_all(element: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        element.first.wait_for(state="visible", timeout=timeout)
        count = element.count()
        for i in range(count):
            element.nth(i).click(timeout=timeout, force=True)
            element.page.wait_for_timeout(500)
                        
    # @staticmethod
    # @allure.step("Click all delete rooms button element:")
    # def click_all_remove_button(element: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
    #     element.first.wait_for(state="attached", timeout=timeout)
    #     while element.count() > 0:
    #         element.first.click()
    #         element.page.wait_for_timeout(500)

    @staticmethod
    @allure.step("Click to reset page to main page")
    def click_to_reset_page(login_back_button: Locator, main_page_button: Locator, timeout: int = DEFAULT_TIMEOUT):
        try:
            if login_back_button.is_visible(timeout=timeout):
                login_back_button.click(timeout=timeout)
                return
            if main_page_button.is_visible(timeout=timeout):
                main_page_button.click(timeout=timeout)
                return
        except Exception:    
            pass
        login_back_button.page.goto(CONFIG["HOTEL_BOOKING_URL"])

    @staticmethod
    def pick_day_from_datepicker(date_picker:Locator,days_locator:Locator,selected_day):
        date_picker.click()
        days = days_locator.all()
        for day in days:
            if day.inner_text() == selected_day:
                day.click()
                break    

    @staticmethod
    def pick_available_room(rooms_titles:Locator,rooms_locator:Locator,selected_room):
        UIActions.click(rooms_titles)
        rooms = rooms_locator.all()
        for room in rooms:
            if selected_room in room.inner_text():  
                room.locator("a.btn-primary").click()  
                break
        
    
         
    
    