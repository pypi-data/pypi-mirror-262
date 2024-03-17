import logging
from typing import List, Dict, Optional
import re
from .work_item_manager import WorkItemManager
from pympler import asizeof
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections.abc import Iterable
from typing import List
from .work_item_manager import WorkItemManager
from .work_item_ado_wrapper import ADOWorkItem


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
    iteration_path = config['azure_devops']['iteration_path']

    manager = WorkItemManager(org_url=org_url, personal_access_token=personal_access_token, project_name=project_name)
    # SELECT [System.Id], [System.Title], [System.State]
    wiql_query = f"""
    SELECT *
    FROM WorkItems
    WHERE [System.TeamProject] = '{project_name}'
    AND [System.IterationPath] UNDER '{iteration_path}'
    ORDER BY [System.CreatedDate] DESC
    """
    try:
        logger.info(f"With max items of {max_items} if specified.")
        work_items = manager.fetch_all_and_related_work_items(wiql_query, max_items=max_items)
        if work_items is None:
            logger.info("No work items found.")
            return []

        all_work_items = list(work_items)  # Start with the initially fetched work items

        logger.info(f"Fetched {len(all_work_items)} work items including related items.")
        logger.info(f"Results from ADO is: {asizeof.asizeof(all_work_items) / 1000000} megabytes.")
        return all_work_items
    except Exception as e:
        logger.error(f"Error fetching work items: {e}")
        return []

from typing import List

# In work_item_utils.py or a similar module

def count_work_items_by_state(work_items, states):
    """
    Counts work items by the specified states.

    Args:
        work_items (List[ADOWorkItem]): A list of ADOWorkItem instances.
        states (List[str]): The states of work items to count.

    Returns:
        Dict[str, int]: A dictionary with each state and its corresponding count of work items.
    """
    state_counts = {state: 0 for state in states}
    for item in work_items:
        item_state = item.get_field('System.State')
        if item_state in state_counts:
            state_counts[item_state] += 1
    return state_counts

def filter_work_items(work_items, item_types=None, states=None):
    """
    Filters work items by the specified item types and states.

    Args:
        work_items (List[ADOWorkItem]): A list of ADOWorkItem instances to filter.
        item_types (List[str] or str, optional): A list of item types to filter by or a single item type as a string. 
                                                 Valid types include "Strategic Theme", "Epic", "Feature", "Task", "Bug", "Story", "Blocker".
        states (List[str] or str, optional): A list of states to filter by or a single state as a string.

    Returns:
        List[ADOWorkItem]: A list of filtered ADOWorkItem instances.
    """
    logger.dev(f"item_types before adjustment: {item_types}")  # Debugging line
    logger.dev(f"states before adjustment: {states}")  # Debugging line
    
    # Ensure item_types and states are lists for single string inputs
    if isinstance(item_types, str):
        item_types = [item_types]
    if isinstance(states, str):
        states = [states]
    
    logger.dev(f"item_types after adjustment: {item_types}")  # Debugging line
    logger.dev(f"states after adjustment: {states}")  # Debugging line

    # If both item_types and states are None (or empty), return all work items
    if not item_types and not states:
        return work_items
    
    # Filter logic
    filtered_work_items = []
    for item in work_items:
        item_type = item.get_field('System.WorkItemType')
        state = item.get_field('System.State')
        
        # Check if item matches the specified types and states
        if (not item_types or item_type in item_types) and (not states or state in states):
            filtered_work_items.append(item)

    return filtered_work_items
def filter_work_items_by_type(work_items, item_types):
    """
    Filters work items by the specified item types.

    Args:
        work_items (List[ADOWorkItem]): A list of ADOWorkItem instances to filter.
        item_types (List[str] or str): A list of item types to filter by or a single item type as a string. 
                                        Valid types include "Strategic Theme", "Epic", "Feature", "Task", "Bug", "Story", "Blocker".

    Returns:
        List[ADOWorkItem]: A list of filtered ADOWorkItem instances.
    """
    # Ensure item_types is a list for single string inputs

    logger.dev(f"item_types before adjustment: {item_types}")  # Debugging line
    if isinstance(item_types, str):
        item_types = [item_types]
    logger.dev(f"item_types after adjustment: {item_types}")  # Debugging line

    if isinstance(item_types, str):
        item_types = [item_types]
        logger.dev(f"is insance of list: {isinstance(item_types, list)}")
        logger.dev(f"item_types: {item_types}")
    
    # Mapping of high-level types to their corresponding System.WorkItemType values in Azure DevOps
    type_mapping = {
        "Strategic Theme": "Strategic Theme",
        "Epic": "Epic",
        "Feature": "Feature",
        "Task": "Task",
        "Bug": "Bug",
        "Story": "User Story",  # Assuming "Story" maps to "User Story"
        "Blocker": "Blocker"  # Adjust based on your Azure DevOps setup
    }

    # Resolve the item_types to their System.WorkItemType values
    azure_devops_types = [type_mapping[item_type] for item_type in item_types if item_type in type_mapping]

    # Filter work items
    filtered_work_items = [item for item in work_items if item.get_field('System.WorkItemType') in azure_devops_types]

    return filtered_work_items

def extract_fields_from_work_item(work_item):
    return list(work_item.fields.keys())

def fetch_work_item_history_util(manager: WorkItemManager, work_item_id: int) -> List[ADOWorkItem]:
    """
    Utilizes the WorkItemManager to fetch the history of a specified work item.

    Args:
        manager (WorkItemManager): An instance of WorkItemManager.
        work_item_id (int): The ID of the work item for which to fetch the history.

    Returns:
        List[ADOWorkItem]: A list of ADOWorkItem instances representing the revision history of the work item.
    """
    
    return manager.fetch_work_item_history(work_item_id)

def count_iteration_path_changes(manager: WorkItemManager, work_item_id: int) -> int:
    """
    Counts the number of times the iteration path of a work item has changed.

    Args:
        manager (WorkItemManager): An instance of WorkItemManager to fetch work item history.
        work_item_id (int): The ID of the work item.

    Returns:
        int: The number of times the iteration path has changed.
    """
    history = manager.fetch_work_item_history(work_item_id)
    iteration_paths = [revision.fields.get("System.IterationPath", "") for revision in history]

    # Count the changes in iteration path
    changes = sum(1 for i in range(1, len(iteration_paths)) if iteration_paths[i] != iteration_paths[i-1])

    return changes