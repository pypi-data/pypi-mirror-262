"""
Command line interface for interacting with Azure DevOps work items.

Provides commands for fetching work items and listing detailed information.
"""
import click
import os
import logging
from .config import load_config
from .log_config import setup_logging
from .work_item_utils import * 
from .legacy_report_generator import *
from .report_generator.csv_report import  CSVReportGenerator  # Adjust import paths as necessary
from .report_generator.table_report import TableReportGenerator  # Adjust import paths as necessary
#from .work_item_utils import get_work_items_without_target_date, count_work_items_without_activated_date, get_active_new_work_items_by_epic, get_features, get_features_with_assessment

logger = logging.getLogger(__name__)

def fetch_work_items(ctx, max_items):
    logger.info(f"Fetching work items{' with a limit of ' + str(max_items) if max_items else ''}...")
    work_items = fetch_and_process_work_items(ctx.obj['config'], ctx.obj['pat'], max_items)
    if work_items:
        ctx.obj['work_items'] = work_items
        click.echo(f"Fetched {len(work_items)} work items.")
    else:
        click.echo("No work items fetched.")
    return work_items

@click.group()
@click.option('--log-level', default='INFO', help='Set the log level.')
@click.option('--pat', envvar='ADO_PAT', help='Personal Access Token for Azure DevOps.', required=True)
@click.option('--report-format', default='table', type=click.Choice(['table', 'csv']), help='Output format for reports')
@click.pass_context
def cli(ctx, log_level, pat, report_format):
    """
    CLI tool for managing Azure DevOps work items.
    """
    setup_logging(log_level=log_level)
    ctx.ensure_object(dict)
    config = load_config()
    ctx.obj['config'] = config
    ctx.obj['pat'] = pat
    ctx.obj['report_format'] = report_format

@cli.command()
@click.option('--max-items', default=None, type=int, help='Maximum number of work items to fetch. If not specified, all items are fetched.')
@click.pass_context
def fetch(ctx, max_items):
    fetch_work_items(ctx, max_items)

@cli.command()
@click.option('--max-items', default=None, type=int, help='Maximum number of work items to fetch. If not specified, all items are fetched.')
@click.option('--state', multiple=True, default=['New'], help='Work item state(s) to count. Multiple states can be specified.')
@click.option('--all-states', is_flag=True, help='Count work items for all states: Active, Closed, New, Removed, Resolved.')
@click.pass_context
def count(ctx, max_items, state, all_states):
    """
    Counts the number of work items in given states, or all states if --all-states is specified.
    """
    # Define all states
    ALL_STATES = ['Active', 'Closed', 'New', 'Removed', 'Resolved']

    if 'work_items' not in ctx.obj or not ctx.obj['work_items']:
        click.echo("No work items in context, fetching work items...")
        fetch_work_items(ctx, max_items)

    work_items = ctx.obj.get('work_items', [])
    if not work_items:
        click.echo("No work items fetched. Please check your WIQL query.")
        return

    if max_items is not None:
        work_items = work_items[:max_items]

    # Use ALL_STATES if --all-states is specified, otherwise use the states provided by --state
    states_to_count = ALL_STATES if all_states else state

    state_counts = count_work_items_by_state(work_items, states_to_count)

    for each_state in states_to_count:
        count = state_counts.get(each_state, 0)  # Use .get to handle case where a state might not be present
        click.echo(f"Found {count} work items in the '{each_state}' state.")

@cli.command()
@click.option('--max-items', default=None, type=int, help='Maximum number of work items to fetch. If not specified, all items are fetched.')
@click.option('--work-item-type', multiple=True, default=['Strategic Theme'], help='Work item type(s) to return. Multiple types can be specified.')
@click.option('--all-types', is_flag=True, help='Return work items for all Types: Strategic Theme, Epic, User Story, Task, Bug, Story Blocker.')
@click.pass_context
def get_work_item_types(ctx, max_items, work_item_type, all_types):
    """
    Counts the number of work items in given states, or all states if --all-states is specified.
    """
    # Define all states
    ALL_TYPES = ['Strategic Theme', 'Epic', 'User Story', 'Task', 'Bug', 'Story Blocker']

    if 'work_items' not in ctx.obj or not ctx.obj['work_items']:
        click.echo("No work items in context, fetching work items...")
        fetch_work_items(ctx, max_items)

    work_items = ctx.obj.get('work_items', [])
    if not work_items:
        click.echo("No work items fetched. Please check your WIQL query.")
        return

    if max_items is not None:
        work_items = work_items[:max_items]

    types_to_return = ALL_TYPES if all_types else work_item_type

    work_items = filter_work_items_by_type(work_items, types_to_return)
    logger.info(f"Found {len(work_items)} work items matching types: {', '.join(types_to_return)}")
    
    report_format = ctx.obj['report_format']
    logger.info(f"Generating report in {report_format} format")

    if work_items:
        fields = extract_fields_from_work_item(work_items[0])
        logger.info(f"Extracted fields: {', '.join(fields)}")

    else:
        click.echo("No work items to report on.")
        return

    # Generate report
    if report_format == 'table':

        report_generator_instance = TableReportGenerator(fields)
    else:
        # Assuming there's logic here to choose CSVReportGenerator or others as needed
        pass

    # Generate and display the report
    report = report_generator_instance.generate_report(work_items)
    click.echo(report)



# Assuming you have a function or a CLI command setup like this
@click.command()
@click.option('--work-item-id', required=True, type=int, help='ID of the work item to fetch history for.')
@click.pass_context
def fetch_history(ctx, work_item_id):
    
    if 'work_items' not in ctx.obj or not ctx.obj['work_items']:
        click.echo("No work items in context, fetching work items...")
        fetch_work_items(ctx, max_items=None)

    work_items = ctx.obj.get('work_items', [])
    if not work_items:
        click.echo("No work items fetched. Please check your WIQL query.")
        return

    org_url = ctx.obj['config']['azure_devops']['org_url']  
    project_name = ctx.obj['config']['azure_devops']['project_name']
    personal_access_token =  ctx.obj['pat']

    manager = WorkItemManager(org_url, personal_access_token, project_name)

    history = fetch_work_item_history_util(manager, work_item_id)

    # Display the fetched history, for example:
    for revision in history:
        logger.debug(f"Revision ID: {revision.id}, Fields: {revision.fields}")
    
    columns = ['Work Item Type', 'State', 'Reason', 'Created Date', 'Changed Date', 'Title']

    # Prepare the data for the report
    report_data = []
    for revision in history:
        fields = revision.fields  # Accessing the fields attribute directly
        report_row = {
            'Work Item Type': fields.get('System.WorkItemType', 'N/A'),
            'State': fields.get('System.State', 'N/A'),
            'Reason': fields.get('System.Reason', 'N/A'),
            'Created Date': fields.get('System.CreatedDate', 'N/A'),
            'Changed Date': fields.get('System.ChangedDate', 'N/A'),
            'Title': fields.get('System.Title', 'N/A')
        }
        report_data.append(report_row)

    # Instantiate and use the TableReportGenerator
    report_generator = TableReportGenerator(fields=columns)
    report = report_generator.generate_report(report_data)
    click.echo(report)

    changes_count = count_iteration_path_changes(manager, work_item_id)
    click.echo(changes_count)

@cli.command()
@click.option('--max-items', default=None, type=int, help='Maximum number of work items to fetch. If not specified, all items are fetched.')
@click.option('--work-item-type', multiple=True, default=['Strategic Theme'], help='Work item type(s) to include in the report. Multiple types can be specified.')
@click.option('--work-item-state', multiple=True, default=['Active'], help='Work item state(s) to include in the report. Multiple states can be specified.')
@click.pass_context
def report_work_item_changes(ctx, max_items, work_item_type, work_item_state):
    """
    Reports work items of specified types and states, and their iteration path changes.
    """
    if 'work_items' not in ctx.obj or not ctx.obj['work_items']:
        click.echo("No work items in context, fetching work items...")
        fetch_work_items(ctx, max_items)

    work_items = ctx.obj.get('work_items', [])
    if not work_items:
        click.echo("No work items fetched. Please check your WIQL query.")
        return

    # Correctly use the work_item_state variable
    # Filter work items by specified types and states
    filtered_work_items = filter_work_items(work_items, work_item_type, work_item_state)

    # Setup for reporting
    org_url = ctx.obj['config']['azure_devops']['org_url']
    project_name = ctx.obj['config']['azure_devops']['project_name']
    personal_access_token = ctx.obj['pat']
    manager = WorkItemManager(org_url, personal_access_token, project_name)
    
    report_data = []
    for item in filtered_work_items:
        item_id = item.id
        changes_count = count_iteration_path_changes(manager, item_id)
        if changes_count > 0:
            item_data = {
                'ID': item_id,
                'Title': item.fields.get('System.Title', 'N/A'),
                'Type': item.fields.get('System.WorkItemType', 'N/A'),
                'State': item.fields.get('System.State', 'N/A'),
                'Sprints': changes_count
            }
            report_data.append(item_data)

    if not report_data:
        click.echo("No work items with iteration path changes were found.")
        return

    # Define columns for the report
    columns = ['ID', 'Title', 'Type', 'State', 'Sprints']
    report_generator = TableReportGenerator(fields=columns, centered_columns=['State', 'Type', 'Sprints'])

    report = report_generator.generate_report(report_data)
    
    click.echo(report)




if __name__ == '__main__':
    cli.add_command(fetch)
    cli.add_command(count)
    cli.add_command(get_work_item_types)
    cli.add_command(fetch_history)
    cli.add_command(report_work_item_changes)
    cli(obj={})
