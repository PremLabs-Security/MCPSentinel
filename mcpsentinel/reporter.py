import json
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table

class Reporter:
    """Handles formatting and displaying scan results."""

    def __init__(self):
        self.console = Console()

    def display_results(self, results: List[Dict[str, Any]]):
        """
        Display scan results in a formatted table.
        
        Args:
            results: A list of detection results.
        """
        if not results:
            self.console.print("[bold green]No exposed endpoints detected.[/bold green]")
            return

        table = Table(title="MCPSentinel - Detection Results")
        table.add_column("Type", style="cyan")
        table.add_column("Target URL", style="magenta")
        table.add_column("Status", style="bold red")
        table.add_column("Details", style="white")

        for res in results:
            details_str = str(res.get("details", {}))
            if len(details_str) > 50:
                details_str = details_str[:47] + "..."
            
            table.add_row(
                res["type"],
                res["url"],
                "EXPOSED",
                details_str
            )

        self.console.print(table)

    def export_json(self, results: List[Dict[str, Any]], output_path: str):
        """
        Export scan results to a JSON file.
        
        Args:
            results: A list of detection results.
            output_path: The path to save the JSON file.
        """
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=4)
        self.console.print(f"[bold green]Results exported to {output_path}[/bold green]")
