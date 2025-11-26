import time
import json
from .interfaces import LogProvider, MetricProvider, CodebaseProvider
from .llm import LLMClient

class SREAgent:
    def __init__(self, log_provider: LogProvider, metric_provider: MetricProvider, llm_client: LLMClient):
        self.log_provider = log_provider
        self.metric_provider = metric_provider
        self.llm_client = llm_client

    def analyze_incident(self) -> str:
        """
        Main workflow:
        1. Fetch logs/metrics
        2. Detect anomalies (simplified: just pass everything to LLM)
        3. Generate report
        """
        print("🤖 SRE Agent: Waking up...")
        
        # 1. Gather Context
        logs = self.log_provider.fetch_logs(0, 0)
        metrics_snapshot = self.metric_provider.fetch_metrics("all", 0, 0)
        
        print(f"    Found {len(logs)} log lines.")
        
        # 2. Construct Prompt
        context = {
            "logs": logs,
            "metrics": metrics_snapshot
        }
        
        print("    Asking LLM to analyze root cause...")
        report = self.llm_client.analyze_incident(context)
        
        return report

if __name__ == "__main__":
    pass
