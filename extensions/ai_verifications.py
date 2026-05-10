import allure
from google.genai import types


class AiVerify:

    @staticmethod
    @allure.step("AI Verify: expected text '{expected_text}' exists")
    def verify_text_exists(actual_text: str, expected_text: str):

        print("\nAI Extracted Text:\n", actual_text)

        assert expected_text.lower() in actual_text, (
            f"\n❌ AI Verification Failed"
            f"\nExpected: {expected_text}"
            f"\nActual: {actual_text}")
        