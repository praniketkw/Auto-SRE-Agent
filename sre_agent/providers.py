import json
import os
from typing import List, Dict, Any
from .interfaces import LogProvider, MetricProvider

class FileLogProvider(LogProvider):
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path

    def fetch_logs(self, start_time: float, end_time: float) -> List[str]:
        """
        Reads the last N lines of the log file. 
        In a real impl, we'd parse timestamps. 
        For demo, we just grab the last 50 lines.
        """
        if not os.path.exists(self.log_file_path):
            return []
        
        with open(self.log_file_path, 'r') as f:
            lines = f.readlines()
            return lines[-50:] # Return last 50 lines for context

class FileMetricProvider(MetricProvider):
    def __init__(self, metric_file_path: str):
        self.metric_file_path = metric_file_path

    def fetch_metrics(self, metric_name: str, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """
        Reads the current state from the metrics json file.
        """
        if not os.path.exists(self.metric_file_path):
            return []
            
        try:
            with open(self.metric_file_path, 'r') as f:
                data = json.load(f)
                # Return as a list of one data point since our simulator overwrites
                return [{"timestamp": time.time(), "value": data.get(metric_name)}] 
        except Exception:
            return []
            
import time
