import time
import logging
import random
import json
import os

logger = logging.getLogger("ChaosMonkey")

# Shared state for metrics
METRICS_FILE = "var/metrics.json"

def update_metrics(metrics: dict):
    """Writes current metrics to a file (simulating an endpoint)."""
    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f)

def scenario_db_connection_failure():
    """Simulates a database connection failure with intermittent 500 errors."""
    metrics = {"cpu_usage": 45.0, "memory_usage": 512, "active_connections": 100, "error_rate": 0.0}
    
    logger.info("Application starting up...")
    time.sleep(1)
    logger.info("Connected to Postgres at localhost:5432")
    
    iteration = 0
    while True:
        iteration += 1
        
        # Normal operation
        if iteration < 10:
            logger.info(f"Processed request_id={random.randint(1000,9999)} status=200 duration={random.randint(20, 100)}ms")
            metrics["error_rate"] = 0.01
        
        # The Incident Begins
        else:
            if random.random() < 0.7:
                logger.error("ConnectionRefusedError: [Errno 111] Connection refused to postgres:5432")
                logger.error("sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server: Connection refused")
                metrics["error_rate"] = 0.85
                metrics["active_connections"] = 0
            else:
                logger.info(f"Processed request_id={random.randint(1000,9999)} status=200 duration={random.randint(20, 100)}ms")
        
        update_metrics(metrics)
        time.sleep(0.5)

def scenario_memory_leak():
    """Simulates a memory leak leading to OOM."""
    metrics = {"cpu_usage": 30.0, "memory_usage": 200, "error_rate": 0.0}
    
    logger.info("Worker process started. PID: 1234")
    
    while True:
        # Memory grows linearly
        metrics["memory_usage"] += random.randint(10, 50)
        
        if metrics["memory_usage"] > 1000:
            logger.critical("MemoryError: Out of memory. Killing process.")
            logger.info("Worker process restarting...")
            metrics["memory_usage"] = 200 # Reset
        elif metrics["memory_usage"] > 800:
            logger.warning(f"High memory usage detected: {metrics['memory_usage']}MB")
        else:
            logger.info(f"Job processed. Queue size: {random.randint(0, 5)}")
            
        update_metrics(metrics)
        time.sleep(0.5)

SCENARIOS = {
    "db_crash": scenario_db_connection_failure,
    "memory_leak": scenario_memory_leak
}
