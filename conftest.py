import json
import os
import time
import uuid
import pytest
from pytest import FixtureRequest
from data.api.chuck_api_data import *
from data.web.sauce_demo_data import *
from workflows.web.sauce_flows import *
from utils.common_ops import load_config
from playwright.sync_api import Playwright
from workflows.api.chuck_api_flows import ChuckApiFlows
from data.web.hotel_booking_data import HOTEL_BOOKING_URL
from workflows.web.grafana_web_flows import GrafanaWebFlows
from workflows.api.hotel_booking_api_flows import HotelApiFlows
from workflows.web.hotel_booking_flows import  HotelBookingFlows
from data.api.hotel_booking_hotel_api_data import BOOKING_BASE_URL
from utils.fixture_helpers import attach_screenshot, attach_trace, get_browser

# Load the configuration
CONFIG = load_config()     

@pytest.fixture(scope="class")
def page(playwright: Playwright, request:FixtureRequest):
    browser = get_browser(playwright,CONFIG["BROWSER_TYPE"].lower())
    context = browser.new_context(no_viewport=True) 
    context.tracing.start(screenshots=True, snapshots=True, sources=True) # Start tracing for this context.  
    #Listen to console messages       
    page = context.new_page()
    page.goto(HOTEL_BOOKING_URL)
    yield page    
    test_name = request.node.name
    trace_filename = f"./{CONFIG["TRACES_DIR"]}/trace_{test_name}.zip"
    context.tracing.stop(path=trace_filename) # Stop tracing and save the trace to a file.
    #Best practice: Close page before context
    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope= "class")
def request_context(playwright: Playwright, request:FixtureRequest):
    request_context=playwright.request.new_context(base_url=BOOKING_BASE_URL)
    yield request_context
    request_context.dispose()


@pytest.fixture
def sauce_flows(page):
    return GrafanaWebFlows(page)


@pytest.fixture
def chuck_flows(request_context):
    return ChuckApiFlows(request_context)

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



@pytest.fixture
def hotel_api_flows(request_context):
    return HotelApiFlows(request_context)


@pytest.fixture
def hotel_booking_flows(page):
    return HotelBookingFlows(page)


@pytest.fixture
def calendar_data():
    path = "data/web/hotel_booking_calendar_data.json"
    with open(path, "r") as f:
        return json.load(f)["calendar_data"]