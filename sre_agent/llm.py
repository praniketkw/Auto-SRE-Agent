import json

class LLMClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def analyze_incident(self, context: dict) -> str:
        """
        Simulates an LLM call. In a real app, this would call OpenAI/Gemini.
        For this demo, we use a heuristic to generate a "fake" LLM response 
        based on the log content, so the user sees it working without an API key.
        """
        logs = "".join(context['logs'])
        
        report = "# 🚨 Incident Report\n\n"
        
        if "ConnectionRefusedError" in logs:
            report += "## 🔴 Critical Issue: Database Connection Failure\n"
            report += "**Root Cause:** The application cannot connect to the Postgres database at `localhost:5432`.\n\n"
            report += "**Evidence:**\n- Multiple `ConnectionRefusedError` logs.\n- `sqlalchemy.exc.OperationalError` detected.\n\n"
            report += "**Recommended Actions:**\n1. Check if the Postgres service is running.\n2. Verify firewall rules.\n3. Check database credentials in environment variables."
            
        elif "MemoryError" in logs or "High memory usage" in logs:
            report += "## ⚠️ Performance Issue: Memory Leak Detected\n"
            report += "**Root Cause:** The worker process is consuming excessive memory, leading to OOM kills.\n\n"
            report += "**Evidence:**\n- `MemoryError` logs.\n- Metrics show memory usage > 800MB.\n\n"
            report += "**Recommended Actions:**\n1. Profile the worker process.\n2. Check for unclosed file handles or large data structures in loops."
            
        else:
            report += "## ✅ System Status: Healthy\n"
            report += "No critical errors detected in the recent logs."
            
        return report
