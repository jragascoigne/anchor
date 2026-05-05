"""
cli.py
Anchor CLI entry point.
Usage:
    anchor check --config anchor.config.json
    anchor check --file ./components/UserCard.tsx --endpoint getUser
"""

import sys
import json
import click
from pathlib import Path

from anchor.parser import parse_file, parse_directory
from anchor.fetcher import fetch_and_flatten
from anchor.checker import check_bindings
from anchor.reporter import report


def load_config(config_path: str) -> dict:
    path = Path(config_path)
    if not path.exists():
        click.echo(f"Error: config file '{config_path}' not found.", err=True)
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


@click.group()
def cli():
    """Anchor — keep your API bindings from drifting."""
    pass


@cli.command()
@click.option("--config", default="anchor.config.json", help="Path to anchor.config.json")
@click.option("--file", "ts_file", default=None, help="Check a single TS/TSX file")
@click.option("--endpoint", default=None, help="Use a specific named endpoint from config")
def check(config, ts_file, endpoint):
    """Check @Expects annotations against live API responses."""

    cfg = load_config(config)
    endpoints = cfg.get("endpoints", [])
    watch_dirs = cfg.get("watch", [])

    if not endpoints:
        click.echo("No endpoints defined in config.", err=True)
        sys.exit(1)

    # Filter to a specific endpoint if requested
    if endpoint:
        endpoints = [e for e in endpoints if e["name"] == endpoint]
        if not endpoints:
            click.echo(f"Endpoint '{endpoint}' not found in config.", err=True)
            sys.exit(1)

    # Collect bindings
    if ts_file:
        bindings = parse_file(ts_file)
    else:
        bindings = []
        for d in watch_dirs:
            bindings.extend(parse_directory(d))

    if not bindings:
        click.echo("No @Expects annotations found.", err=True)
        sys.exit(0)

    # Run check against each endpoint
    overall_exit = 0
    for ep in endpoints:
        click.echo(f"Fetching {ep['url']}...")
        try:
            flat = fetch_and_flatten(ep["url"], ep.get("method", "GET"))
        except Exception as e:
            click.echo(f"Failed to fetch {ep['name']}: {e}", err=True)
            overall_exit = 1
            continue

        results = check_bindings(bindings, flat)
        exit_code = report(results, ep["name"])
        if exit_code != 0:
            overall_exit = 1

    sys.exit(overall_exit)


if __name__ == "__main__":
    cli()