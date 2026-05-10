import re
import json
from google.genai import types
from playwright.sync_api import Page


class AiAgentFlows:

    def __init__(self, page: Page, ai_engine):
        self.page = page
        self.ai_model = ai_engine

    def ask_ai_next_action(self, user_goal: str):
        screenshot_bytes = self.page.screenshot(type="png")
        prompt = f"""You are a UI automation agent.
        User goal:
        {user_goal}
        Analyze the screenshot and decide the NEXT action only.
        Return ONLY valid JSON.
        Do not wrap the JSON with markdown.
        Supported actions:
        - click
        - fill
        JSON format:
        {{
          "action": "click",
          "target": "Login button"
        }}
        OR
        {{
          "action": "fill",
          "target": "Username field",
          "value": "admin"
        }}
        """
        response = self.ai_model.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=screenshot_bytes,
                    mime_type="image/png")])
        ai_text = response.text.strip()
        ai_text = re.sub(r"```json|```", "", ai_text).strip()
        print("\nAI RESPONSE:")
        print(ai_text)
        return json.loads(ai_text)
        
    
    def execute_action(self, action_data):
        action = action_data["action"]
        
        if action == "click":
            target = action_data["target"]
            self.page.get_by_text(target).click()
            print(f"\nClicked on: {target}")
       
        elif action == "fill":
            target = action_data["target"]
            value = action_data["value"]
            self.page.get_by_label(target).fill(value)
            print(f"\nFilled '{target}' with '{value}'")

    def run_flow(self, goal: str):
        MAX_STEPS = 5
        for step in range(MAX_STEPS):
            action = self.ask_ai_next_action(goal)
            print(f"\nSTEP {step + 1}: {action}")
            if action.get("action") == "done":
                break
            self.execute_action(action)