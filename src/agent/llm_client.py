from openai import OpenAI
import os

class LLMClient:
    def __init__(self, api_base="http://localhost:1234/v1", api_key="lm-studio"):
        self.client = OpenAI(base_url=api_base, api_key=api_key)
        self.model = "qwen3.5-4b-vision" # default LM Studio model identifier

    def get_action(self, image_base64: str, goal: str, context: list) -> str:
        """
        Sends the current screen image and user goal to the LM, asking for the next action.
        """
        prompt = f"""
        You are an advanced desktop automation AI named NaiveClaw.
        Current Goal: {goal}
        
        You have the following tools available. Respond ONLY with ONE of these formats (do not add conversational padding):
        - CLICK(x, y) - Clicks at specified screen coordinates x, y. Example: `CLICK(300, 450)`
        - TYPE(text) - Types the exact text. Example: `TYPE(Hello World)`
        - PRESS(key) - Presses a key (e.g., enter, tab, space). Example: `PRESS(enter)`
        - SCROLL(amount) - Scrolls the screen (positive or negative int). Example: `SCROLL(-100)`
        - CMD(command) - Runs a terminal command. Example: `CMD(ls -la)`
        - DONE(reason) - If the goal is achieved. Example: `DONE(Task complete.)`
        
        Analyze the provided screen image and determine the single most logical next step.
        """

        messages = [
            {"role": "system", "content": prompt}
        ]
        
        # Append history context if applicable
        for msg in context:
            messages.append(msg)

        # Append current state
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": "This is the current screenshot of the desktop. What is your next move?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1, # Keep it deterministic
            max_tokens=150,
        )

        return response.choices[0].message.content.strip()
