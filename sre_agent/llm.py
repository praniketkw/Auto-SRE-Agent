import os
import anthropic

class LLMClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if not self.api_key:
            # Fallback to env var if not passed explicitly, though main.py should pass it
            self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        
        if not self.api_key:
             raise ValueError("ANTHROPIC_API_KEY is required for the SRE Agent to function.")

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def run_agent_step(self, messages: list, tools: list) -> dict:
        """
        Sends messages to Claude with available tools.
        Returns the response message (which might be a tool call or text).
        """
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        return response
