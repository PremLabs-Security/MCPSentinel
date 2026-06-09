import aiohttp
import logging
from typing import Dict, Any, Optional

class MCPDetector:
    """Detector for exposed Model Context Protocol (MCP) endpoints."""

    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    async def detect(self, url: str) -> Dict[str, Any]:
        """
        Check if the given URL is an exposed MCP endpoint.
        
        Args:
            url: The base URL to check.
            
        Returns:
            A dictionary containing detection results.
        """
        results = {
            "type": "MCP",
            "url": url,
            "is_exposed": False,
            "details": {}
        }

        # Common MCP endpoints to check
        endpoints = ["/mcp", "/api/mcp", "/v1/mcp"]
        
        async with aiohttp.ClientSession() as session:
            for endpoint in endpoints:
                target_url = f"{url.rstrip('/')}{endpoint}"
                try:
                    async with session.get(target_url, timeout=self.timeout) as response:
                        if response.status == 200:
                            # Attempt to parse as JSON and look for MCP indicators
                            try:
                                data = await response.json()
                                if isinstance(data, dict) and ("protocol_version" in data or "methods" in data):
                                    results["is_exposed"] = True
                                    results["details"] = {
                                        "endpoint": target_url,
                                        "status_code": response.status,
                                        "version": data.get("protocol_version", "unknown"),
                                        "methods": data.get("methods", [])
                                    }
                                    break
                            except Exception:
                                # Not JSON, but still a 200 on an MCP-like path
                                results["is_exposed"] = True
                                results["details"] = {
                                    "endpoint": target_url,
                                    "status_code": response.status,
                                    "note": "Endpoint returned 200 but response was not JSON"
                                }
                                break
                except Exception as e:
                    self.logger.debug(f"Error checking {target_url}: {e}")

        return results
