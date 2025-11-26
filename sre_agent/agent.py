import time
import json
from .llm import LLMClient
from .tools import TOOLS, TOOL_MAP, check_server_health

class SREAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def monitor(self):
        """
        Continuously monitors the server health.
        """
        print("🤖 SRE Agent: Monitoring started...")
        while True:
            health_status = check_server_health()
            if "UNHEALTHY" in health_status or "UNREACHABLE" in health_status:
                print(f"🚨 ALERT: {health_status}")
                self.investigate(health_status)
                # Wait a bit after fixing before checking again
                time.sleep(5)
            else:
                print(".", end="", flush=True)
                time.sleep(2)

    def investigate(self, initial_issue: str):
        """
        Runs the agent loop to investigate and fix the issue.
        """
        print("\n🔍 Investigating...")
        
        messages = [
            {
                "role": "user", 
                "content": f"The server is reporting an issue: {initial_issue}. Please investigate the logs, find the root cause, and fix it if possible."
            }
        ]

        # Agent Loop (Think -> Act -> Observe)
        for _ in range(10): # Max 10 steps
            response = self.llm_client.run_agent_step(messages, TOOLS)
            
            # Add assistant response to history
            messages.append({"role": "assistant", "content": response.content})

            # Check if tool use is required
            if response.stop_reason == "tool_use":
                for block in response.content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input
                        tool_use_id = block.id
                        
                        print(f"🛠️  Agent calls tool: {tool_name}({tool_input})")
                        
                        # Execute Tool
                        if tool_name in TOOL_MAP:
                            tool_func = TOOL_MAP[tool_name]
                            tool_result = tool_func(**tool_input)
                        else:
                            tool_result = f"Error: Tool {tool_name} not found."
                        
                        print(f"    Result: {str(tool_result)[:100]}...")

                        # Add tool result to history
                        messages.append({
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_use_id,
                                    "content": str(tool_result)
                                }
                            ]
                        })
            else:
                # Final answer or just text
                print(f"🤖 Agent: {response.content[0].text}")
                break
