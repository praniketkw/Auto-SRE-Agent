import requests
import os

LOG_FILE = "var/logs/app.log"
APP_URL = "http://localhost:8000"

def read_log_file(lines: int = 20) -> str:
    """Reads the last N lines from the application log file."""
    if not os.path.exists(LOG_FILE):
        return "Log file not found."
    
    try:
        with open(LOG_FILE, "r") as f:
            all_lines = f.readlines()
            return "".join(all_lines[-lines:])
    except Exception as e:
        return f"Error reading log file: {str(e)}"

def check_server_health() -> str:
    """Checks the health of the server by pinging the /health endpoint."""
    try:
        response = requests.get(f"{APP_URL}/health", timeout=2)
        if response.status_code == 200:
            return "Server is HEALTHY."
        else:
            return f"Server is UNHEALTHY. Status Code: {response.status_code}. Content: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Server is UNREACHABLE. Error: {str(e)}"

def restart_server() -> str:
    """
    Restarts the server (simulated by calling the reset endpoint).
    In a real scenario, this might issue a 'systemctl restart' command.
    """
    try:
        response = requests.post(f"{APP_URL}/admin/reset", timeout=2)
        if response.status_code == 200:
            return "Server successfully restarted (state reset)."
        else:
            return f"Failed to restart server. Status: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Failed to call reset endpoint. Error: {str(e)}"

TOOLS = [
    {
        "name": "read_log_file",
        "description": "Reads the last N lines of the application log. Use this to see recent errors.",
        "input_schema": {
            "type": "object",
            "properties": {
                "lines": {"type": "integer", "description": "Number of lines to read (default 20)"}
            }
        }
    },
    {
        "name": "check_server_health",
        "description": "Checks if the server is running and healthy.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "restart_server",
        "description": "Restarts the server application to fix crash states.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]

TOOL_MAP = {
    "read_log_file": read_log_file,
    "check_server_health": check_server_health,
    "restart_server": restart_server
}
