import logging
from typing import List, Dict, Optional
from .work_item_manager import WorkItemManager
from pympler import asizeof
from concurrent.futures import ThreadPoolExecutor, as_completed
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

logger = logging.getLogger(__name__)

def fetch_and_process_work_items(config: Dict, personal_access_token: str, max_items: Optional[int] = None) -> List:
    """
    Fetches work items from Azure DevOps and processes them to include related work items.

    Args:
        config (Dict): Configuration details including Azure DevOps organization and project name.
        personal_access_token (str): Personal Access Token for Azure DevOps access.
        max_items (Optional[int]): Maximum number of work items to fetch. If None, fetches all available items.

    Returns:
        List: A list of WorkItem objects, including both primary and related work items.
    """
    logger.info("Starting to fetch work items...")
    org_url = config['azure_devops']['org_url']
    project_name = config['azure_devops']['project_name']

    manager = WorkItemManager(org_url=org_url, personal_access_token=personal_access_token, project_name=project_name)

    wiql_query = f"""
    SELECT [System.Id], [System.Title], [System.State]
    FROM WorkItems
    WHERE [System.TeamProject] = '{project_name}'
    ORDER BY [System.CreatedDate] DESC
    """
    try:
        work_items = manager.query_work_items(wiql_query, max_items)
        if work_items is None:
            logger.info("No work items found.")
            return []

        all_work_items = list(work_items)  # Start with the initially fetched work items

        with ThreadPoolExecutor() as executor:
            future_to_work_item = {
                executor.submit(manager.fetch_related_work_items, work_item.id): work_item
                for work_item in work_items
            }

            for future in as_completed(future_to_work_item):
                work_item = future_to_work_item[future]
                try:
                    related_items = future.result()
                    all_work_items.extend(related_items)
                except Exception as e:
                    logger.error(f"Error fetching related items for work item {work_item.id}: {e}")

        logger.info(f"Fetched {len(all_work_items)} work items including related items.")
        logger.info(f"Results from ADO is: {asizeof.asizeof(all_work_items) / 1000000} megabytes.")
        return all_work_items
    except Exception as e:
        logger.error(f"Error fetching work items: {e}")
        return []

def filter_late_work_items(work_items: List) -> List:
    """
    Filters work items to find ones that are late.

    Currently, this function does not implement any filtering logic and always returns an empty list.
    Future implementations should add the logic based on specific criteria for what constitutes "late".

    Args:
        work_items (List): The list of WorkItem objects to filter.

    Returns:
        List: A list of WorkItem objects that are late.
    """
    late_work_items = []
    # Implementation goes here
    return late_work_items

def get_work_item_schema(work_items: List) -> Dict:
    """
    Generates a schema based on the first work item in the list, showing fields and their types.

    Args:
        work_items (List): The list of WorkItem objects.

    Returns:
        Dict: A dictionary representing the schema of a work item, with keys as field names and values as types.
    """
    if not work_items:
        return {}

    sample_item = work_items[0]
    schema = sample_item.get_fields()

    return schema

def get_vsts_fields(ctx: Dict, namespaces: Optional[List[str]] = None) -> Dict[str, List[str]]:
    """
    Retrieves a list of work item fields from Azure DevOps within specified namespaces.

    Args:
        ctx (Dict): The context object containing configuration and state.
        namespaces (Optional[List[str]]): List of namespaces to filter fields by. Defaults to common VSTS namespaces.

    Returns:
        Dict[str, List[str]]: A dictionary with namespace as keys and lists of field references as values.
    """
    organization_url = ctx.obj.get('organization_url')
    personal_access_token = ctx.obj.get('pat')
    namespaces = namespaces or ['Common', 'Microsoft.VSTS.Common', 'Microsoft.VSTS.Scheduling']
    fields_by_namespace = {namespace: [] for namespace in namespaces}
    
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    wit_client = connection.clients.get_work_item_tracking_client()
    
    fields = wit_client.get_fields()
    
    for field in fields:
        for namespace in namespaces:
            if field.reference_name.startswith(namespace):
                fields_by_namespace[namespace].append(field.reference_name)
    
    return fields_by_namespace

def get_all_fields(ctx: Dict) -> Dict[str, str]:
    """
    Retrieves a dictionary of work item fields from Azure DevOps, mapping field names to their types.

    Args:
        ctx (Dict): The context object containing configuration and state.

    Returns:
        Dict[str, str]: Dictionary where keys are field references and values are field types.
    """
    organization_url = ctx.get('organization_url')
    personal_access_token = ctx.get('pat')
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    wit_client = connection.clients.get_work_item_tracking_client()
    
    fields = wit_client.get_fields()

    field_info = {field.reference_name: field.type for field in fields}
    
    return field_info
