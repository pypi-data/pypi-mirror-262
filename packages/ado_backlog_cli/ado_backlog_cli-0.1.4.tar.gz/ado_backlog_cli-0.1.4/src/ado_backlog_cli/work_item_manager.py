import logging
import os
from typing import List, Optional
import psutil
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking.models import Wiql
from concurrent.futures import ThreadPoolExecutor, as_completed
from .work_item import WorkItem

logger = logging.getLogger(__name__)

class WorkItemManager:
    """
    Manages querying and fetching Azure DevOps work items, supporting concurrent operations.
    """

    def __init__(self, org_url: str, personal_access_token: str, project_name: str) -> None:
        """
        Initializes a WorkItemManager instance with Azure DevOps organization info.

        Args:
            org_url (str): The URL of the Azure DevOps organization.
            personal_access_token (str): Personal access token for Azure DevOps.
            project_name (str): Name of the Azure DevOps project.
        """
        self.organization_url = org_url
        self.personal_access_token = personal_access_token
        self.project_name = project_name
        self.connection = self._create_connection()

    def _create_connection(self) -> Connection:
        """Creates and returns a connection to Azure DevOps with the provided credentials."""
        credentials = BasicAuthentication('', self.personal_access_token)
        return Connection(base_url=self.organization_url, creds=credentials)

    def _chunk_list(self, lst: List[int], chunk_size: int) -> List[List[int]]:
        """Yields successive n-sized chunks from lst."""
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

    def fetch_work_item_details(self, ids: List[int], wit_client) -> List[WorkItem]:
        """
        Fetches details for a list of work item IDs.

        Args:
            ids (List[int]): A list of work item IDs.
            wit_client: Azure DevOps work item tracking client.

        Returns:
            List[WorkItem]: A list of WorkItem instances with detailed information.
        """
        try:
            work_items_data = wit_client.get_work_items(ids=ids, expand='All')
            return [WorkItem(work_item_data=item, organization_url=self.organization_url, project_name=self.project_name) for item in work_items_data]
        except Exception as e:
            logger.error(f"Error fetching work item details for IDs {ids}: {e}")
            return []

    def query_work_items(self, wiql_query: str, max_items: Optional[int] = None, max_workers: int = 300, chunk_size: int = 50) -> List[WorkItem]:
        """
        Queries work items using WIQL and fetches their details.

        Args:
            wiql_query (str): The WIQL query string.
            max_items (Optional[int]): Maximum number of work items to query.
            max_workers (int): Maximum number of threads for concurrent fetching.
            chunk_size (int): Number of work item IDs to fetch in each batch.

        Returns:
            List[WorkItem]: A list of fetched WorkItem instances.
        """
        logger.info("Querying Azure DevOps for work items...")
        wit_client = self.connection.clients.get_work_item_tracking_client()
        query_result = wit_client.query_by_wiql(Wiql(query=wiql_query))
        work_item_references = query_result.work_items[:max_items] if max_items is not None else query_result.work_items
        ids = [ref.id for ref in work_item_references]
        ids_chunks = list(self._chunk_list(ids, chunk_size))

        work_items: List[WorkItem] = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_chunk = {
                executor.submit(self.fetch_work_item_details, chunk, wit_client): chunk
                for chunk in ids_chunks
            }

            for future in as_completed(future_to_chunk):
                try:
                    data = future.result()
                    work_items.extend(data)
                except Exception as e:
                    logger.error(f"Error processing chunk {future_to_chunk[future]}: {e}")

        return work_items

    def fetch_related_work_items(self, work_item_id: int, max_workers: int = 300, chunk_size: int = 100) -> List[WorkItem]:
        """
        Fetches related work items for a given work item ID.

        Args:
            work_item_id (int): The ID of the work item to fetch related items for.
            max_workers (int): Maximum number of threads for concurrent fetching.
            chunk_size (int): Number of related work item IDs to fetch in each batch.

        Returns:
            List[WorkItem]: A list of related WorkItem instances.
        """
        wit_client = self.connection.clients.get_work_item_tracking_client()
        work_item = wit_client.get_work_item(work_item_id, expand='Relations')
        related_work_items: List[WorkItem] = []

        if not hasattr(work_item, 'relations'):
            return related_work_items

        related_ids = [
            int(relation.url.split('/').pop())
            for relation in work_item.relations
            if relation.rel in ['System.LinkTypes.Hierarchy-Forward', 'System.LinkTypes.Related']
        ]

        ids_chunks = self._chunk_list(related_ids, chunk_size)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.fetch_work_item_details, chunk, wit_client)
                for chunk in ids_chunks
            ]

            for future in as_completed(futures):
                related_work_items_batch = future.result()
                related_work_items.extend(related_work_items_batch)

        return related_work_items
