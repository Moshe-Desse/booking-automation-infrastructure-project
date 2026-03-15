# 🏨 Hotel Booking Automation Project

A comprehensive hybrid automation framework for testing the **Restful Booker Platform**. This project integrates **Web (UI)**, **API**, and **Database** testing into a single unified architecture, utilizing advanced Design Patterns.

## 🛠 Technologies Used
* **Language:** Python 3.x
* **Framework:** Pytest
* **UI Automation:** Playwright
* **API Testing:** Playwright Request Context
* **Database:** SQLite
* **Reporting:** Allure Reports
* **Design Pattern:** Page Object Model (POM) & Workflows
* **AI Integration:** Google Gemini API

---

## 🏗 Architecture & Project Structure
The project is built modularly to separate test logic from technical implementation:

* **`pages/`**: Implementation of the Page Object Model. Each page is represented by a class containing only its Locators.
* **`workflows/`**: The Business Logic layer. Contains application "flows" (e.g., login, booking process) that combine multiple actions.
* **`extensions/`**: A wrapper over Playwright and DB operations. Includes `UIActions`, `APIVerify`, and `WebVerify` classes for reusability and clean code.
* **`data/`**: External data management (DDT) using JSON and CSV files.
* **`tests/`**: Test files categorized by domain (Web, API, DB).
* **`utils/`**: Helper functions for loading configurations and file management.

---

## 🧪 Key Test Scenarios

### Web (UI) Tests
* **Booking Management:** Full room reservation process, including date selection from a calendar, form submission, and confirmation message validation.
* **Double Booking Prevention:** Verifying that the system prevents booking the same room for the same dates twice.
* **Admin Dashboard:** Administrative login, creating new rooms, and deleting existing rooms.
* **Contact Us:** Testing the integrity of the contact form submission and verifying the "Thank You" response.

### API Tests
* **Authentication:** Token generation and secure login verification.
* **Room Management:** Creating, retrieving, and updating rooms via POST and GET requests.
* **DDT API:** Running a series of room creation tests with varying data sets (valid and invalid) from an external JSON file.

### Database & Integration Tests
* **DB Login:** Retrieving encrypted admin credentials directly from the database to perform a UI Login.
* **E2E Validation:** Creating a room via the UI and validating its data using a direct API call.

---

## 🌟 Advanced Features
- **Soft Assertions:** Collecting multiple errors during a test run and displaying them at the end, preventing the test from stopping at the first failure.
- **AI-Powered Locators:** Integration with Gemini API for smart selector discovery from HTML content.
- **Smart Wait Mechanism:** Built-in Playwright waiters within `UIActions` for maximum stability (Flaky-free tests).
- **Allure Reporting:** Detailed visual reports including screenshots and full API request/response logs.

---

## 🚀 How to Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
# 2. Install Playwright Browsers
playwright install

# 3. Run Tests
pytest --alluredir=allure-results

# 4. View Reports
allure serve allure-results

# Project Maintainer: [Moshe Desse] | QA Automation Engineer