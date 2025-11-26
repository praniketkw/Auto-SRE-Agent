import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sre_agent.agent import SREAgent
from sre_agent.providers import FileLogProvider, FileMetricProvider
from sre_agent.llm import LLMClient

def main():
    # Paths to simulated data
    log_path = "var/logs/app.log"
    metric_path = "var/metrics.json"
    
    # Initialize dependencies
    log_provider = FileLogProvider(log_path)
    metric_provider = FileMetricProvider(metric_path)
    llm_client = LLMClient() # No API key needed for demo mode
    
    # Initialize Agent
    agent = SREAgent(log_provider, metric_provider, llm_client)
    
    # Run Analysis
    report = agent.analyze_incident()
    
    print("\n" + "="*30)
    print(report)
    print("="*30 + "\n")
    
    # Save report
    with open("var/report.md", "w") as f:
        f.write(report)
    print("Report saved to var/report.md")

if __name__ == "__main__":
    main()
