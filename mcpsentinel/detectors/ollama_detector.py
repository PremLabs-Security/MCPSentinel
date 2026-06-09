import aiohttp
import logging
from typing import Dict, Any

class OllamaDetector:
    """Detector for exposed Ollama servers."""

    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    async def detect(self, url: str) -> Dict[str, Any]:
        """
        Check if the given URL is an exposed Ollama server.
        
        Args:
            url: The base URL to check.
            
        Returns:
            A dictionary containing detection results.
        """
        results = {
            "type": "Ollama",
            "url": url,
            "is_exposed": False,
            "details": {}
        }

        # Ollama's default health/version endpoint
        target_url = f"{url.rstrip('/')}/api/tags"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(target_url, timeout=self.timeout) as response:
                    if response.status == 200:
                        try:
                            data = await response.json()
                            if isinstance(data, dict) and "models" in data:
                                results["is_exposed"] = True
                                results["details"] = {
                                    "endpoint": target_url,
                                    "status_code": response.status,
                                    "model_count": len(data.get("models", [])),
                                    "models": [m.get("name") for m in data.get("models", [])]
                                }
                        except Exception:
                            pass
            except Exception as e:
                self.logger.debug(f"Error checking {target_url}: {e}")

        return results
