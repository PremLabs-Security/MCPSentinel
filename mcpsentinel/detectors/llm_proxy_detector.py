import aiohttp
import logging
from typing import Dict, Any

class LLMProxyDetector:
    """Detector for exposed LLM proxies (e.g., LiteLLM, vLLM)."""

    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    async def detect(self, url: str) -> Dict[str, Any]:
        """
        Check if the given URL is an exposed LLM proxy.
        
        Args:
            url: The base URL to check.
            
        Returns:
            A dictionary containing detection results.
        """
        results = {
            "type": "LLM Proxy",
            "url": url,
            "is_exposed": False,
            "details": {}
        }

        # Common LLM proxy endpoints
        endpoints = ["/v1/models", "/health", "/metrics"]
        
        async with aiohttp.ClientSession() as session:
            for endpoint in endpoints:
                target_url = f"{url.rstrip('/')}{endpoint}"
                try:
                    async with session.get(target_url, timeout=self.timeout) as response:
                        if response.status == 200:
                            try:
                                data = await response.json()
                                # Check for common patterns in /v1/models response
                                if endpoint == "/v1/models" and isinstance(data, dict) and "data" in data:
                                    results["is_exposed"] = True
                                    results["details"] = {
                                        "endpoint": target_url,
                                        "status_code": response.status,
                                        "model_ids": [m.get("id") for m in data.get("data", []) if isinstance(m, dict)]
                                    }
                                    break
                                # Check for metrics or health status
                                elif endpoint in ["/health", "/metrics"]:
                                    results["is_exposed"] = True
                                    results["details"] = {
                                        "endpoint": target_url,
                                        "status_code": response.status,
                                        "type": "health_or_metrics"
                                    }
                                    break
                            except Exception:
                                pass
                except Exception as e:
                    self.logger.debug(f"Error checking {target_url}: {e}")

        return results
