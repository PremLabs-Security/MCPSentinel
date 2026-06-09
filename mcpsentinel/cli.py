import asyncio
import click
import logging
from .scanner import Scanner
from .reporter import Reporter

@click.command()
@click.option('--target', '-t', multiple=True, help='Target URL to scan (can be used multiple times)')
@click.option('--file', '-f', type=click.Path(exists=True), help='File containing target URLs (one per line)')
@click.option('--output', '-o', type=click.Path(), help='Path to save JSON results')
@click.option('--concurrency', '-c', default=10, help='Number of concurrent scans')
@click.option('--timeout', default=5, help='Timeout for each request in seconds')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(target, file, output, concurrency, timeout, verbose):
    """MCPSentinel: Detect exposed MCP and Ollama endpoints."""
    
    # Configure logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Collect targets
    targets = list(target)
    if file:
        with open(file, 'r') as f:
            targets.extend([line.strip() for line in f if line.strip()])
    
    if not targets:
        click.echo("Error: No targets specified. Use --target or --file.")
        return

    # Initialize scanner and reporter
    scanner = Scanner(timeout=timeout, concurrency=concurrency)
    reporter = Reporter()

    click.echo(f"[*] Starting scan on {len(targets)} targets...")
    
    # Run scan
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(scanner.scan_targets(targets))
    
    # Report results
    reporter.display_results(results)
    
    if output:
        reporter.export_json(results, output)

if __name__ == "__main__":
    main()
