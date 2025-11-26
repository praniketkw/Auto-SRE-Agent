import time
import logging
import random
import argparse
from .scenarios import SCENARIOS

def setup_logging():
    logging.basicConfig(
        filename='var/logs/app.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def run_scenario(scenario_name: str):
    if scenario_name not in SCENARIOS:
        print(f"Unknown scenario: {scenario_name}")
        return

    print(f"Starting scenario: {scenario_name}")
    scenario_func = SCENARIOS[scenario_name]
    
    try:
        scenario_func()
    except KeyboardInterrupt:
        print("Stopping simulation.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chaos Monkey Simulator")
    parser.add_argument("--scenario", type=str, required=True, help="Name of the scenario to run")
    args = parser.parse_args()
    
    # Ensure log and metric directory exists
    import os
    os.makedirs('var/logs', exist_ok=True)
    
    setup_logging()
    run_scenario(args.scenario)
