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

    # This filters out magic methods and methods, adjust the condition as needed


# Example usage:
# work_items = [list of ADOWorkItem instances]
# filtered_items = filter_work_items_by_type(work_items, "Epic")  # Now supports both single and multiple types
# or
# filtered_items = filter_work_items_by_type(work_items, ["Epic", "Feature", "Task"])


# def fetch_work_items_for_reporting(wiql_query: str, max_items: int) -> List[ADOWorkItem]:
#     manager = WorkItemManager('YOUR_ORG_URL', 'YOUR_PAT', 'YOUR_PROJECT_NAME')
#     work_items = manager.fetch_all_and_related_work_items(wiql_query, max_workers=10, chunk_size=max_items)
#     return work_items

# from typing import List, Dict

# def get_active_new_work_items_by_epic(work_items, epic_id=None):
#     """
#     Finds work items that are parented by the specified Epic and are in 'Active' or 'New' state. If no epic_id is provided, it fetches for all epics.

#     Args:
#         work_items (List[ADOWorkItem]): List of all work items to search through.
#         epic_id (int, optional): The ID of the Epic to find related work items for. If None, fetches for all epics.

#     Returns:
#         Dict[int, List[Dict]]: A dictionary where keys are Epic IDs and values are lists of dictionaries, each representing an active or new work item.
#     """
#     # Initialize a dictionary to hold results
#     epic_related_items = {}

#     # Filter for Features or other work item types as needed
#     for item in work_items:
#         state = item.get_field('System.State')
#         parent_id = item.get_field('System.Parent')
        
#         # If filtering for a specific epic or collecting for all
#         if state in ['Active', 'New'] and (parent_id == epic_id or epic_id is None):
#             work_item_details = {
#                 'Name': item.get_field('System.Title', 'N/A')[:80].ljust(80),
#                 'TargetDate': item.get_field('Microsoft.VSTS.Scheduling.TargetDate', 'N/A'),
#                 'ActivatedDate': item.get_field('Microsoft.VSTS.Common.ActivatedDate', 'N/A')
#             }
            
#             if parent_id not in epic_related_items:
#                 epic_related_items[parent_id] = [work_item_details]
#             else:
#                 epic_related_items[parent_id].append(work_item_details)

#     return epic_related_items

# def get_features(work_items):
#     """
#     Filters work items for features and extracts necessary details including Iteration Path.

#     Args:
#         work_items (List): A list of work item objects.

#     Returns:
#         List[Dict]: A list of dictionaries with details of each feature.
#     """
#     features = []
#     for item in work_items:
#         if item.get_field('System.WorkItemType') == 'Feature':
#             feature_details = {
#                 'ID': item.id,
#                 'Name': item.get_field('System.Title', 'N/A')[:80],
#                 'TargetDate': item.get_field('Microsoft.VSTS.Scheduling.TargetDate', 'N/A'),
#                 'ActivatedDate': item.get_field('Microsoft.VSTS.Common.ActivatedDate', 'N/A'),
#                 'Status': item.get_field('System.State', 'N/A'),
#                 'AssignedTo': item.get_field('System.AssignedTo', {}).get('displayName', 'Unassigned'),
#                 'IterationPath': item.get_field('System.IterationPath', 'N/A')  # Extract Iteration Path
#             }
#             features.append(feature_details)
#     return features

# import logging
# from datetime import datetime

# def get_features_with_assessment(work_items):
#     """
#     Extends get_features to include assessment status.

#     Args:
#         work_items (List[Dict]): A list of dictionaries with details of work items.

#     Returns:
#         List[Dict]: Extended feature details including assessment status.
#     """
#     features = []
#     for item in work_items:
#         if item.get_field('System.WorkItemType') == 'Feature':
#             # Assuming you have a function or a way to get activated, target, and closed dates by item ID
#             activated_date = item.get_field('Microsoft.VSTS.Common.ActivatedDate', None)
#             target_date = item.get_field('Microsoft.VSTS.Scheduling.TargetDate', None)
#             closed_date = item.get_field('Microsoft.VSTS.Common.ClosedDate', None)
#             status = item.get_field('System.State', None)

#             # Use assess_work_item_status to get assessment
#             assessment, days = assess_work_item_status(activated_date, target_date, closed_date, status)

#             # Append additional information to feature details
#             feature_details = {
#                 'ID': item.id,
#                 'Name': item.get_field('System.Title', 'N/A')[:80],
#                 'TargetDate': target_date,
#                 'ActivatedDate': activated_date,
#                 'ClosedDate': closed_date,
#                 'Status': status,
#                 'Assessment': assessment,
#                 'Days': days  # Number of days late or early
#             }
#             features.append(feature_details)
#     return features


# from datetime import datetime

# def parse_iso_datetime(date_str):
#     """
#     Parses an ISO 8601 formatted date string, handling 'Z' for UTC.
    
#     Args:
#         date_str (str): ISO 8601 formatted date string.
    
#     Returns:
#         datetime: A datetime object representing the given date and time in UTC.
#     """
#     if date_str and date_str.endswith('Z'):
#         date_str = date_str[:-1] + '+00:00'  # Replace 'Z' with '+00:00' for UTC offset
#     return datetime.fromisoformat(date_str) if date_str else None

# def assess_work_item_status(activated_date_str, target_date_str, closed_date_str, status):
#     """
#     Assesses a work item's timeliness based on its dates and status, for ISO 8601 formatted date strings.
    
#     Args:
#         activated_date_str (str): The activation date in ISO 8601 format. None if not available.
#         target_date_str (str): The target completion date in ISO 8601 format. None if not available.
#         closed_date_str (str): The closure date in ISO 8601 format. None if not available.
#         status (str): The current status of the work item (new, active, closed, removed).

#     Returns:
#         tuple: An assessment and the number of days late or early.
#     """
#     # Parse date strings into datetime objects
#     activated_date = parse_iso_datetime(activated_date_str)
#     target_date = parse_iso_datetime(target_date_str)
#     closed_date = parse_iso_datetime(closed_date_str)

#     if not target_date:
#         logger.info("Target date not provided; cannot assess work item status.")
#         return ('Assessment Not Available', 0)

#     if activated_date and activated_date > target_date:
#         days_late = (activated_date - target_date).days
#         return ('Started Late', days_late)

#     if status in ['closed', 'removed'] and closed_date:
#         if closed_date > target_date:
#             days_late = (closed_date - target_date).days
#             return ('Finished Late', days_late)
#         else:
#             days_early = (target_date - closed_date).days
#             return ('On Time', -days_early)

#     return ('Assessment Not Available', 0)

# def get_work_items_without_target_date(work_items):
#     """
#     Filters work items that do not have a target date or due date, as applicable,
#     and sets 'Should Be' information using the ADOWorkItem's set_additional_info method.
#     """
#     filtered_items = []
#     for item in work_items:
#         work_item_type = item.get_field('System.WorkItemType')
#         iteration_path = item.get_field('System.IterationPath')
#         sprint_start, sprint_end, sprint_no = extract_sprint_details(iteration_path)
        
#         if sprint_end is None:
#             continue  # Skip items without a valid sprint end date in their iteration path

#         date_field = 'Microsoft.VSTS.Scheduling.DueDate' if work_item_type == 'Task' else 'Microsoft.VSTS.Scheduling.TargetDate'
        
#         if not item.get_field(date_field):
#             #should_be_action = "Set " + ("DueDate" if work_item_type == "Task" else "TargetDate")
#             #item.set_additional_info('should_be', should_be_action + f" to {sprint_end.strftime('%Y-%m-%d')}")
#             item.set_additional_info('should_be', sprint_end)
            
#             filtered_items.append(item)

#     return filtered_items


# import re
# from datetime import datetime

# def extract_sprint_details(iteration_path):
#     """
#     Extracts sprint start date, end date, and sprint number from the iteration path,
#     only if the iteration path contains the word 'Sprint'.

#     Args:
#         iteration_path (str): Iteration path string.

#     Returns:
#         tuple: sprint_start (datetime), sprint_end (datetime), sprint_no (int), or
#                None values if 'Sprint' not in iteration path.
#     """
#     if 'Sprint' not in iteration_path:
#         return None, None, None

#     pattern = re.compile(r'(\d{2}\.\d{2}\.\d{4}) - (\d{2}\.\d{2}\.\d{4}) - Sprint (\d+)')
#     match = pattern.search(iteration_path)

#     if not match:
#         raise ValueError(f"Unable to extract sprint details from iteration path: {iteration_path}")

#     start_date_str, end_date_str, sprint_no_str = match.groups()
#     sprint_start = datetime.strptime(start_date_str, '%m.%d.%Y')
#     sprint_end = datetime.strptime(end_date_str, '%m.%d.%Y')
#     sprint_no = int(sprint_no_str)

#     logger.debug(f"Extracted sprint {sprint_no} from {iteration_path}, starting {sprint_start} and ending {sprint_end}.")

#     return sprint_start, sprint_end, sprint_no
