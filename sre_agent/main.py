import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sre_agent.agent import SREAgent
from sre_agent.providers import FileLogProvider, FileMetricProvider
from sre_agent.llm import LLMClient
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Paths to simulated data
    log_path = "var/logs/app.log"
    metric_path = "var/metrics.json"
    
    # Initialize dependencies
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  Warning: ANTHROPIC_API_KEY not found in environment variables.")
        print("   Please set it via: export ANTHROPIC_API_KEY='your-key-here'")
        # We let the LLMClient raise the error if it's critical, or we could exit here.
    
    try:
        llm_client = LLMClient(api_key=api_key)
    except ValueError as e:
        print(f"❌ Error: {e}")
        return
    
    # Initialize Agent
    agent = SREAgent(llm_client)
    
    # Start Monitoring
    try:
        agent.monitor()
    except KeyboardInterrupt:
        print("\nStopping SRE Agent.")

if __name__ == "__main__":
    main()
