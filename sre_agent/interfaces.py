from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LogProvider(ABC):
    @abstractmethod
    def fetch_logs(self, start_time: float, end_time: float) -> List[str]:
        """Fetch logs between two timestamps."""
        pass

class MetricProvider(ABC):
    @abstractmethod
    def fetch_metrics(self, metric_name: str, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """Fetch metrics for a specific name between two timestamps."""
        pass

class CodebaseProvider(ABC):
    @abstractmethod
    def get_relevant_code(self, error_signature: str) -> str:
        """Retrieve code snippets relevant to a specific error."""
        pass
