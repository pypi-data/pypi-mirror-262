"""
Command line interface for interacting with Azure DevOps work items.

Provides commands for fetching work items, listing late and active work items,
and obtaining the work item schema. State, such as fetched work items, is stored
in the click context object and passed between commands.
"""

import click
import os
import logging
from typing import Optional, Callable, Any
from functools import update_wrapper
from .config import load_config
from .log_config import setup_logging
from .report_generator import format_schema
from . import work_item_utils as wiu
import json

logger = logging.getLogger(__name__)

@click.group()
@click.option('--log-level', default='INFO', help='Set the log level.')
@click.option('--test-mode', is_flag=True, help='Enable test mode. Limits fetches to 100 items.')
@click.pass_context
def cli(ctx: click.Context, log_level: str, test_mode: bool) -> None:
    """
    Initializes the CLI application context with configuration and logging.

    Args:
        ctx (click.Context): The click context object.
        log_level (str): Desired logging level (e.g., INFO, DEBUG).
        test_mode (bool): Flag to indicate if the application should run in test mode.
    """
    ctx.ensure_object(dict)
    ctx.obj['LOG_LEVEL'] = log_level.upper()
    ctx.obj['TEST_MODE'] = test_mode

    setup_logging(log_level=ctx.obj['LOG_LEVEL'])
    
    try:
        config = load_config()
        ctx.obj['config'] = config
        ctx.obj['pat'] = os.getenv('ADO_PAT')
        # Ensure organization_url is correctly assigned from the loaded configuration
        ctx.obj['organization_url'] = config['azure_devops']['org_url']  # Corrected assignment
        if not ctx.obj['pat']:
            click.echo("Error: Personal Access Token (PAT) not found in environment variable 'ADO_PAT'", err=True)
            ctx.exit(1)
    except Exception as e:
        click.echo(f"Error loading configuration: {e}", err=True)
        ctx.exit(1)

def ensure_work_items_fetched(f: Optional[Callable] = None, *, max_items: Optional[int] = None) -> Callable:
    """
    Decorator to ensure work items are fetched before executing a command.

    Args:
        f (Optional[Callable]): The CLI command function to decorate.
        max_items (Optional[int]): Maximum number of work items to fetch, overridden in test mode.

    Returns:
        Callable: The decorated CLI command function.
    """
    if f is None:
        return lambda f: ensure_work_items_fetched(f, max_items=max_items)

    def wrapper(ctx: click.Context, *args, **kwargs) -> Any:
        if ctx.obj.get('TEST_MODE'):
            max_items = 100
        if 'work_items' not in ctx.obj or not ctx.obj['work_items']:
            click.echo(f"Fetching {max_items if max_items else 'all'} work items...")
            ctx.invoke(fetch_work_items, max_items=max_items)
        return f(ctx, *args, **kwargs)

    return update_wrapper(wrapper, f)

@cli.command(name='fetch-work-items')
@click.option('--max-items', default=None, type=int, help='Maximum number of work items to fetch. If not specified, all items are fetched.')
@click.pass_context
def fetch_work_items(ctx: click.Context, max_items: Optional[int]) -> None:
    """
    Fetches work items from Azure DevOps and stores them in the CLI context.

    Args:
        ctx: The click context object.
        max_items: Maximum number of work items to fetch.
    """
    work_items = wiu.fetch_and_process_work_items(ctx.obj['config'], ctx.obj['pat'], max_items)
    ctx.obj['work_items'] = work_items

@cli.command(name='list-late-work-items')
@click.pass_context
@ensure_work_items_fetched
def list_late_work_items(ctx: click.Context) -> None:
    """
    Lists work items that are considered late.

    Args:
        ctx: The click context object.
    """
    late_work_items = wiu.filter_late_work_items(ctx.obj['work_items'])
    for work_item in late_work_items:
        click.echo(work_item.summary())

@cli.command(name='get-schema')
@click.pass_context
@ensure_work_items_fetched(max_items=10)
def get_schema(ctx: click.Context) -> None:
    """
    Displays the schema of work items based on the fetched items.

    Args:
        ctx: The click context object.
    """
    schema = wiu.get_work_item_schema(ctx.obj['work_items'])
    pretty_schema = format_schema(schema)
    click.echo(pretty_schema)

@cli.command(name='list-active-work-items')
@click.pass_context
@ensure_work_items_fetched
def list_active_work_items(ctx: click.Context) -> None:
    """
    Lists work items that are currently active.

    Args:
        ctx: The click context object.
    """
    if 'work_items' not in ctx.obj or not ctx.obj['work_items']:
        click.echo("No work items available. Please fetch work items first.")
        return

    active_work_items = wiu.filter_active_work_items(ctx.obj['work_items'])
    if not active_work_items:
        click.echo("No active work items found.")
        return

    for item in active_work_items:
        click.echo(item.summary())

@cli.command(name='list-fields')
@click.option('--namespaces', multiple=True, default=['Microsoft.VSTS.Common', 'Microsoft.VSTS.Scheduling'], help='Namespaces to filter fields by.')
@click.option('--output', default=None, type=str, help='Path to output the results as a JSON file.')
@click.pass_context
def list_fields(ctx: click.Context, namespaces, output) -> None:
    """
    Lists work item fields within specified namespaces from Azure DevOps and optionally outputs to a JSON file.

    Args:
        ctx: The click context object.
        namespaces: Tuple of namespaces to filter the fields by.
        output: Path to the output JSON file.
    """
    organization_url = ctx.obj['config']['azure_devops']['org_url']
    pat = ctx.obj['pat']

    if not organization_url or not pat:
        click.echo("Organization URL or PAT not found in configuration. Please set them up.")
        return

    fields_by_namespace = wiu.get_vsts_fields(ctx, list(namespaces))
    if output:
        with open(output, 'w') as outfile:
            json.dump(fields_by_namespace, outfile, indent=4)
        click.echo(f"Fields by namespace have been output to {output}")
    else:
        for namespace, fields in fields_by_namespace.items():
            click.echo(f"{namespace}:")
            for field in fields:
                click.echo(f"  - {field}")


@cli.command(name='list-all-fields')
@click.option('--namespaces', multiple=True, default=['Microsoft.VSTS.Common', 'Microsoft.VSTS.Scheduling'], help='Namespaces to filter fields by.')
@click.option('--output', default=None, type=str, help='Path to output the results as a JSON file.')
@click.pass_context

def list_fields(ctx: click.Context, namespaces, output) -> None:
    """
    Lists work item fields from Azure DevOps and optionally outputs to a JSON file.

    Args:
        ctx: The click context object.
        namespaces: Ignored in this refactored version, kept for compatibility.
        output: Path to the output JSON file.
    """
    try:
        # Assuming get_all_fields is correctly implemented as per the new specification
        fields_info = wiu.get_all_fields(ctx.obj)

        if output:
            with open(output, 'w') as outfile:
                json.dump(fields_info, outfile, indent=4)
            click.echo(f"Fields information has been output to {output}")
        else:
            for field_name, field_type in fields_info.items():
                click.echo(f"{field_name}: {field_type}")
    except Exception as e:
        click.echo(f"Failed to fetch or output fields: {e}")

if __name__ == '__main__':
    cli(obj={})
