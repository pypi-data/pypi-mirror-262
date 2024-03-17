import logging
from typing import Any, Dict
logger = logging.getLogger(__name__)

class ADOWorkItem:
    """
    Represents a work item from Azure DevOps, allowing dynamic access to its fields,
    including a custom get method for attribute access.
    """

    def __init__(self, work_item_data: Dict[str, Any], organization_url: str, project_name: str) -> None:
        """
        Initializes a WorkItem instance with data and configuration.
        
        Args:
            work_item_data (Dict[str, Any]): The data retrieved from Azure DevOps for a single work item.
            organization_url (str): The URL of the Azure DevOps organization.
            project_name (str): The name of the Azure DevOps project.
        """
        self.id = work_item_data.get('id')
        self.organization_url = organization_url
        self.project_name = project_name
        self.fields = work_item_data.get('fields', {})
    
    def get_field(self, key: str, default: Any = None) -> Any:
        """
        Gets the value of a field, or a default value if the field is not present.

        Args:
            key (str): The field name.
            default (Any): The default value to return if the field is not present.

        Returns:
            Any: The field value or the default value.
        """
        return self.fields.get(key, default)
    
    @property
    def hyperlink(self) -> str:
        """Generates a hyperlink to the work item in Azure DevOps."""
        return f"{self.organization_url}/{self.project_name}/_workitems/edit/{self.id}"

    def summary(self) -> str:
        """Returns a summary string for the work item, including its ID, title, and state."""
        title = self.fields.get('System.Title', 'N/A')[:80]
        state = self.fields.get('System.State', 'Unknown')
        return f"ID {self.id}: {title} (State: {state})"

    def set_additional_info(self, key, value):
        setattr(self, key, value)

