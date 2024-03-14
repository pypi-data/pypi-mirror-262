import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class WorkItem:
    """
    Represents a work item from Azure DevOps, allowing dynamic access to its fields.

    Attributes:
        id (int): The ID of the work item.
        fields (Dict[str, Any]): Dictionary containing all fields of the work item.
        organization_url (str): URL of the Azure DevOps organization.
        project_name (str): Name of the Azure DevOps project.
    """

    def __init__(self, work_item_data: Any, organization_url: str, project_name: str) -> None:
        """
        Initializes a WorkItem instance with data and configuration.

        Args:
            work_item_data (Any): The data retrieved from Azure DevOps for a single work item.
                                  Expected to have 'id' and 'fields' attributes.
            organization_url (str): The URL of the Azure DevOps organization.
            project_name (str): The name of the Azure DevOps project.
        """
        self.id: int = work_item_data.id
        self.fields: Dict[str, Any] = work_item_data.fields
        self.organization_url: str = organization_url
        self.project_name: str = project_name

    def __getattr__(self, item: str) -> Any:
        """
        Allows dynamic access to work item fields as if they were attributes.

        Args:
            item (str): The field name of the work item.

        Returns:
            Any: The value of the requested field.

        Raises:
            AttributeError: If the requested field is not found in the work item fields.
        """
        if item in self.fields:
            return self.fields[item]
        else:
            raise AttributeError(f"'WorkItem' object has no attribute '{item}'")

    @property
    def hyperlink(self) -> str:
        """
        Generates a hyperlink to the work item in Azure DevOps.

        Returns:
            str: A URL string pointing to the work item in Azure DevOps.
        """
        return f"{self.organization_url}/{self.project_name}/_workitems/edit/{self.id}"

    def summary(self) -> str:
        """
        Returns a summary string for the work item, including its ID, title, and state.

        Returns:
            str: A summary of the work item.
        """
        title: str = self.fields.get('System.Title', 'N/A')[:80]
        state: str = self.fields.get('System.State', 'Unknown')
        return f"ID {self.id}: {title} (State: {state})"
    
    def get_fields(self) -> Dict[str, str]:
        """
        Returns a dictionary of fields and their types for the work item.

        Returns:
            Dict[str, str]: A dictionary where keys are field names and values are the type names of their values.
        """
        return {key: type(value).__name__ for key, value in self.fields.items()}
