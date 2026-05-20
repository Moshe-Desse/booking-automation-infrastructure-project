import json
import os
import sqlite3
import time
import uuid

import pytest
from appium import webdriver
from google import genai
from dotenv import load_dotenv
from pytest import FixtureRequest
from utils.common_ops import load_config
from workflows.ai.ai_flows import AiFlows # וודא שהנתיב נכון אצלך
from extensions.db_actions import DBActions
from playwright.sync_api import Playwright,Page
from data.api.hotel_booking_hotel_api_data import *
from workflows.ai.ai_agent_flows import AiAgentFlows
from appium.options.android import UiAutomator2Options
from workflows.api.hotel_booking_api_flows import HotelApiFlows
from workflows.web.hotel_booking_flows import  HotelBookingFlows
from utils.fixture_helpers import attach_screenshot, attach_trace, get_browser
from data.web.hotel_booking_data import HOTEL_BOOKING_URL, USER_NAME, PASSWORD

# Load the .env
DOTENV = load_dotenv()

# Load the configuration
CONFIG = load_config()     
CONFIG["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

@pytest.fixture(scope="class")
def page(playwright: Playwright, request:FixtureRequest):
    browser = get_browser(playwright,CONFIG["BROWSER_TYPE"].lower())
    context = browser.new_context(no_viewport=True) 
    context.tracing.start(screenshots=True, snapshots=True, sources=True) # Start tracing for this context.  
    #Listen to console messages       
    page = context.new_page()
    page.set_default_timeout(10000)
    page.set_default_navigation_timeout(10000)
    page.goto(HOTEL_BOOKING_URL)
    yield page    
    test_name = request.node.name
    trace_filename = f"./{CONFIG['TRACES_DIR']}/trace_{test_name}.zip"
    context.tracing.stop(path=trace_filename) # Stop tracing and save the trace to a file.
    #Best practice: Close page before context
    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope="class")
def mobile_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = "QCSGYPS8QWMFBQBI"
    options.browser_name = "Chrome"
    options.no_reset = True
    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )
    yield driver
    driver.quit()

@pytest.fixture
def ai_agent(page, ai_engine):
    return AiAgentFlows(page, ai_engine)

@pytest.fixture
def ai_flows(page, ai_engine):
    return AiFlows(page, ai_engine)

@pytest.fixture
def ai_engine():
    api_key = CONFIG.get("GEMINI_API_KEY")
    if not api_key:
        pytest.fail("שכחת לשים את המפתח בקובץ .env או שלא התקנת python-dotenv")
    client = genai.Client(api_key=api_key)
    return client

@pytest.fixture
def reset_page_before_test(page:Page):
    page.goto(HOTEL_BOOKING_URL)
    yield

@pytest.fixture(scope= "class")
def request_context(playwright: Playwright, request:FixtureRequest):
    request_context=playwright.request.new_context(base_url=BOOKING_BASE_URL)
    yield request_context
    request_context.dispose()

@pytest.fixture(scope="class",autouse=True)
def db(request:FixtureRequest):
    data_base = sqlite3.connect(CONFIG["DB_PATH"])
    db_actions = DBActions(data_base)
    yield db_actions
    db_actions.close_db()

@pytest.fixture(scope="class")
def db_rooms():
    conn = sqlite3.connect(CONFIG["DB_ROOMS_PATH"]) # הנתיב לקובץ ששלחת לי
    actions = DBActions(conn)
    yield actions
    actions.close_db()

@pytest.fixture
def hotel_DB_booking_flows(request_context):
    return 

@pytest.fixture
def hotel_api_flows(request_context):
    return HotelApiFlows(request_context)

@pytest.fixture
def hotel_booking_flows(page):
    return HotelBookingFlows(page)

@pytest.fixture
def logged_in_flows(hotel_booking_flows, page: Page):
    page.goto(HOTEL_BOOKING_URL)    
    hotel_booking_flows.navigate_to_admin_page()    
    user_field = hotel_booking_flows.login.user_name_field    
    try:
        user_field.wait_for(state="visible", timeout=2000)
        hotel_booking_flows.sign_in(USER_NAME, PASSWORD)
    except:
        pass
    return hotel_booking_flows

@pytest.fixture
def calendar_data():
    path = "data/web/hotel_booking_calendar_data.json"
    with open(path, "r") as f:
        return json.load(f)["calendar_data"]
    
#Listen to console messages
def handle_console_message(msg):
    if msg.type == "error":
        print(f"Error detected in console: {msg.text}")
    if "the server responded with a status of 404" in msg.text:
        raise AssertionError(f"Test Failed: 404 Error Detected in Console - {msg.text}")
    
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to attach screenshots, videos, and traces to Allure reports on test failure,
    and log test case names for reporting.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # Attachments (only if the test failed)
        if report.failed:
            page = item.funcargs.get("page")

            if page:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                unique_id = str(uuid.uuid4())[:8]
                base_filename = f"{item.name}_{timestamp}_{unique_id}"

                # Attach screenshot
                screenshot_name = f"{CONFIG['SCREENSHOT_PREFIX']}_{base_filename}.png"
                screenshot_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], screenshot_name)
                attach_screenshot(page, item.name, screenshot_path)
                # Attach trace
                trace_name = f"{CONFIG['TRACE_PREFIX']}_{item.name}_{timestamp}.zip"
                trace_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], trace_name)
                attach_trace(page, item.name, trace_path)