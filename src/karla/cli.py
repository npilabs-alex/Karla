"""Karla CLI - Command line interface for Karla."""

import typer
from rich.console import Console
from rich.table import Table

from karla.jobs import JobManager

app = typer.Typer(
    name="karla",
    help="Agentic websearch and scraping system for regional data collection.",
    no_args_is_help=True,
)
console = Console()
job_manager = JobManager()


# Job commands
job_app = typer.Typer(help="Manage scraping jobs")
app.add_typer(job_app, name="job")


@job_app.command("create")
def job_create(
    name: str = typer.Argument(..., help="Name for this job"),
    query: str = typer.Option(..., "--query", "-q", help="What to search for"),
    region: str = typer.Option(..., "--region", "-r", help="Target region (e.g., india, europe)"),
    cities: str = typer.Option(None, "--cities", "-c", help="Comma-separated list of cities"),
    schema: str = typer.Option("default", "--schema", "-s", help="Schema to use"),
):
    """Create a new scraping job."""
    city_list = [c.strip() for c in cities.split(",")] if cities else []

    job = job_manager.create(
        name=name,
        query=query,
        region=region,
        cities=city_list,
        schema_name=schema,
    )

    console.print(f"[green]✓[/green] Job '[bold]{name}[/bold]' created")
    console.print(f"  Query: {query}")
    console.print(f"  Region: {region}")
    if city_list:
        console.print(f"  Cities: {', '.join(city_list)}")


@job_app.command("list")
def job_list():
    """List all jobs."""
    jobs = job_manager.list_all()

    if not jobs:
        console.print("[dim]No jobs found. Create one with:[/dim] karla job create <name>")
        return

    table = Table(title="Jobs")
    table.add_column("Name", style="cyan")
    table.add_column("Query")
    table.add_column("Region")
    table.add_column("Status")

    for job in jobs:
        status_style = {
            "pending": "dim",
            "running": "yellow",
            "completed": "green",
            "failed": "red",
        }.get(job.status, "dim")

        table.add_row(
            job.name,
            job.query[:40] + "..." if len(job.query) > 40 else job.query,
            job.region,
            f"[{status_style}]{job.status}[/{status_style}]",
        )

    console.print(table)


@job_app.command("show")
def job_show(name: str = typer.Argument(..., help="Job name")):
    """Show details of a job."""
    job = job_manager.get(name)

    if not job:
        console.print(f"[red]✗[/red] Job '[bold]{name}[/bold]' not found")
        raise typer.Exit(1)

    console.print(f"[bold]{job.name}[/bold]")
    console.print(f"  Query:   {job.query}")
    console.print(f"  Region:  {job.region}")
    console.print(f"  Cities:  {', '.join(job.cities) if job.cities else 'All'}")
    console.print(f"  Schema:  {job.schema_name}")
    console.print(f"  Status:  {job.status}")
    console.print(f"  Created: {job.created}")


@job_app.command("delete")
def job_delete(
    name: str = typer.Argument(..., help="Job name"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a job."""
    job = job_manager.get(name)

    if not job:
        console.print(f"[red]✗[/red] Job '[bold]{name}[/bold]' not found")
        raise typer.Exit(1)

    if not force:
        confirm = typer.confirm(f"Delete job '{name}'?")
        if not confirm:
            raise typer.Abort()

    job_manager.delete(name)
    console.print(f"[green]✓[/green] Job '[bold]{name}[/bold]' deleted")


# Sources command
@app.command("sources")
def sources(
    job_name: str = typer.Argument(..., help="Job name to show sources for"),
):
    """List recommended sources for a job."""
    job = job_manager.get(job_name)

    if not job:
        console.print(f"[red]✗[/red] Job '[bold]{job_name}[/bold]' not found")
        raise typer.Exit(1)

    # For now, return static sources based on region
    # Later this will be dynamic based on source scoring
    sources_by_region = {
        "india": [
            ("Google Maps", 7.1, "Best coverage + contact info"),
            ("Zomato", 6.9, "Good data, needs in-region"),
            ("JustDial", 6.8, "Excellent contacts"),
            ("LBB", 6.6, "Best music specificity"),
            ("TripAdvisor", 6.0, "Good reviews, geo-blocked"),
            ("GigHub", 5.8, "Curated but sparse"),
        ],
    }

    region_sources = sources_by_region.get(job.region.lower(), [])

    if not region_sources:
        console.print(f"[dim]No sources configured for region '{job.region}'[/dim]")
        return

    table = Table(title=f"Sources for '{job_name}' ({job.region})")
    table.add_column("Source", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Notes")

    for source, score, notes in region_sources:
        table.add_row(source, f"{score:.1f}", notes)

    console.print(table)


# Scrape command (placeholder)
@app.command("scrape")
def scrape(
    job_name: str = typer.Argument(..., help="Job name to run"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be done"),
):
    """Run a scraping job."""
    job = job_manager.get(job_name)

    if not job:
        console.print(f"[red]✗[/red] Job '[bold]{job_name}[/bold]' not found")
        raise typer.Exit(1)

    if dry_run:
        console.print(f"[dim]Dry run for job '{job_name}'[/dim]")
        console.print(f"  Would scrape: {job.query}")
        console.print(f"  Region: {job.region}")
        console.print(f"  Cities: {', '.join(job.cities) if job.cities else 'All'}")
        return

    console.print(f"[yellow]⚡[/yellow] Scraping not yet implemented")
    console.print(f"  Job: {job_name}")
    console.print(f"  Run with --dry-run to see planned actions")


# Status command
@app.command("status")
def status(job_name: str = typer.Argument(..., help="Job name")):
    """Show status of a job."""
    job = job_manager.get(job_name)

    if not job:
        console.print(f"[red]✗[/red] Job '[bold]{job_name}[/bold]' not found")
        raise typer.Exit(1)

    status_emoji = {
        "pending": "⏳",
        "running": "🔄",
        "completed": "✅",
        "failed": "❌",
    }.get(job.status, "❓")

    console.print(f"{status_emoji} [bold]{job.name}[/bold]: {job.status}")


if __name__ == "__main__":
    app()
