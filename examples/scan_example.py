import asyncio
from mcpsentinel.scanner import Scanner
from mcpsentinel.reporter import Reporter

async def main():
    # List of targets to scan
    targets = [
        "http://localhost:11434",  # Default Ollama port
        "http://localhost:8000",   # Common MCP/Proxy port
        "https://example-mcp-server.com"
    ]

    print(f"[*] Initializing MCPSentinel Scanner...")
    scanner = Scanner(timeout=3, concurrency=5)
    reporter = Reporter()

    print(f"[*] Scanning {len(targets)} targets...")
    results = await scanner.scan_targets(targets)

    print("\n[*] Scan Complete. Results:")
    reporter.display_results(results)

if __name__ == "__main__":
    asyncio.run(main())
