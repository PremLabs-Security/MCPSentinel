import asyncio
import logging
from typing import List, Dict, Any
from .detectors.mcp_detector import MCPDetector
from .detectors.ollama_detector import OllamaDetector
from .detectors.llm_proxy_detector import LLMProxyDetector

class Scanner:
    """Main scanner engine for MCPSentinel."""

    def __init__(self, timeout: int = 5, concurrency: int = 10):
        self.timeout = timeout
        self.concurrency = concurrency
        self.detectors = [
            MCPDetector(timeout=timeout),
            OllamaDetector(timeout=timeout),
            LLMProxyDetector(timeout=timeout)
        ]
        self.logger = logging.getLogger(__name__)

    async def scan_target(self, url: str) -> List[Dict[str, Any]]:
        """
        Scan a single target URL using all available detectors.
        
        Args:
            url: The target URL to scan.
            
        Returns:
            A list of detection results.
        """
        tasks = [detector.detect(url) for detector in self.detectors]
        results = await asyncio.gather(*tasks)
        return [res for res in results if res["is_exposed"]]

    async def scan_targets(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Scan multiple target URLs with concurrency control.
        
        Args:
            urls: A list of target URLs to scan.
            
        Returns:
            A flattened list of all positive detection results.
        """
        semaphore = asyncio.Semaphore(self.concurrency)
        all_results = []

        async def bounded_scan(url: str):
            async with semaphore:
                results = await self.scan_target(url)
                all_results.extend(results)

        tasks = [bounded_scan(url) for url in urls]
        await asyncio.gather(*tasks)
        return all_results
