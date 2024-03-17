import logging
import os
from typing import List, Optional
import psutil
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking.models import Wiql

from concurrent.futures import ThreadPoolExecutor, as_completed
from .work_item_ado_wrapper import ADOWorkItem 

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


    def fetch_all_and_related_work_items(self, wiql_query: str, max_workers: int = 300, chunk_size: int = 100,
                                          max_items: Optional[int] = None  ) -> List[ADOWorkItem]:
        """
        Fetches work items based on a WIQL query and their related work items,
        respecting the max_items limit if specified.

        Args:
            wiql_query (str): WIQL query to select work items.
            max_workers (int): Maximum number of threads for concurrent fetching.
            chunk_size (int): Number of work item IDs to fetch in each batch.
            max_items (Optional[int]): Maximum number of initial work items to fetch.

        Returns:
            List[ADOWorkItem]: List of queried and related ADOWorkItem instances.
        """
        logger.info("Querying and fetching work items and their related items...")
        logger.info(f"Max Itemes: {max_items}")
        wit_client = self.connection.clients.get_work_item_tracking_client()

        # Step 1: Query work items using WIQL
        query_result = wit_client.query_by_wiql(Wiql(query=wiql_query), top=max_items)
        work_item_refs = query_result.work_items
        ids = [ref.id for ref in work_item_refs][:max_items] if max_items else [ref.id for ref in work_item_refs]

        # Step 2: Fetch details of queried work items concurrently
        queried_work_items = self._fetch_work_items_concurrently(ids, wit_client, max_workers, chunk_size)

        # Collect and deduplicate all related work item IDs
        all_related_ids: Set[int] = set()
        for work_item in queried_work_items:
            if hasattr(work_item, 'related_work_items'):
                related_ids = [int(relation.url.split('/').pop()) for relation in work_item.related_work_items]
                all_related_ids.update(related_ids)

        # Optional: Apply max_items limit to related items as well
        # This step is optional and depends on how you want to apply the max_items limit
        all_related_ids = list(all_related_ids)[:max_items] if max_items else list(all_related_ids)

        # Step 3: Fetch details for all related work items concurrently
        related_work_items = self._fetch_work_items_concurrently(all_related_ids, wit_client, max_workers, chunk_size)

        # Create a mapping of work item ID to ADOWorkItem for quick lookup
        id_to_related_item = {item.id: item for item in related_work_items}

        # Step 4: Associate related work items with their corresponding queried work items
        for work_item in queried_work_items:
            if hasattr(work_item, 'related_work_items'):
                work_item.related_work_items = [id_to_related_item[int(relation.url.split('/').pop())] for relation in work_item.related_work_items if int(relation.url.split('/').pop()) in id_to_related_item]

        return queried_work_items

    
    
    def _fetch_work_items_concurrently(self, ids: List[int], wit_client, max_workers: int, chunk_size: int) -> List[ADOWorkItem]:
        """
        Helper method to fetch work item details concurrently.

        Args:
            ids (List[int]): List of work item IDs to fetch.
            wit_client: Azure DevOps work item tracking client.
            max_workers (int): Maximum number of concurrent threads.
            chunk_size (int): Chunk size for batching work item ID requests.

        Returns:
            List[ADOWorkItem]: A list of fetched ADOWorkItem instances.
        """
        ids_chunks = list(self._chunk_list(ids, chunk_size))
        all_work_items = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.fetch_work_item_details, chunk, wit_client) for chunk in ids_chunks]
            for future in as_completed(futures):
                try:
                    batch_work_items = future.result()
                    all_work_items.extend(batch_work_items)
                except Exception as e:
                    logger.error(f"Error fetching work item details: {e}")
        return all_work_items

    def fetch_work_item_details(self, ids: List[int], wit_client, max_items: Optional[int] = None) -> List[ADOWorkItem]:
        """
        Fetches details for a list of work item IDs up to a maximum number of items if specified.
        
        Args:
            ids (List[int]): A list of work item IDs.
            wit_client: Azure DevOps work item tracking client.
            max_items (Optional[int]): Maximum number of work items to fetch.

        Returns:
            List[ADOWorkItem]: A list of ADOWorkItem instances with detailed information.
        """
        try:
            # If max_items is specified and less than the length of ids, reduce ids to max_items
            if max_items is not None and len(ids) > max_items:
                ids = ids[:max_items]
            
            work_items_data = wit_client.get_work_items(ids=ids, expand='All')
            logger.debug(f"Fetched {len(work_items_data)} work items.")
            
            adoworkitems = [ADOWorkItem(work_item_data={'id': ado_item.id, 'fields': ado_item.fields if hasattr(ado_item, 'fields') else {}},
                                        organization_url=self.organization_url,
                                        project_name=self.project_name) for ado_item in work_items_data]
            
            return adoworkitems
        except Exception as e:
            logger.error(f"Error fetching work item details for IDs {ids}: {e}")
            return []

    def fetch_work_item_history(self, work_item_id: int) -> List[ADOWorkItem]:
        """
        Fetches the revision history of a work item.
        """
        wit_client = self.connection.clients.get_work_item_tracking_client()

        # Adjusting the method call according to the correct usage
        revisions = wit_client.get_revisions(work_item_id)

        # Convert each revision to an ADOWorkItem instance (or handle as needed)
        history = [ADOWorkItem(work_item_data={'id': rev.id, 'fields': rev.fields if hasattr(rev, 'fields') else {}},
                               organization_url=self.organization_url,
                               project_name=self.project_name) for rev in revisions]

        return history


    # def fetch_work_item_history(self, work_item_id: int) -> List[ADOWorkItem]:
    #     """
    #     Fetches the revision history of a work item.

    #     Args:
    #         work_item_id (int): The ID of the work item to fetch history for.

    #     Returns:
    #         List[ADOWorkItem]: A list of ADOWorkItem instances representing the revision history of the work item.
    #     """
    #     wit_client = self.connection.clients.get_work_item_tracking_client()
    #     revisions = wit_client.get_revisions(work_item_id=work_item_id, expand='All')

    #     # Convert each revision to an ADOWorkItem instance
    #     history = [ADOWorkItem(work_item_data={'id': rev.id, 'fields': rev.fields if hasattr(rev, 'fields') else {}},
    #                            organization_url=self.organization_url,
    #                            project_name=self.project_name) for rev in revisions]

    #     return history
