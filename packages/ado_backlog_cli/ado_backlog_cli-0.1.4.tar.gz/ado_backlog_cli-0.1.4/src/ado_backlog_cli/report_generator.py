import logging
from typing import Dict
from termcolor import colored

logger = logging.getLogger(__name__)

def format_schema(schema: Dict[str, str]) -> str:
    """
    Formats a schema dictionary into a colorized, pretty-printed string.

    The function iterates through the schema dictionary, applying colorization
    based on the value type of each schema item. It supports basic Python types
    such as string, integer, float, list, and dictionary.

    Args:
        schema (Dict[str, str]): The schema dictionary to format, where keys are
            the field names and values are the type names as strings.

    Returns:
        str: A colorized, formatted string representation of the schema.
    """
    # Start the output with an opening curly brace.
    output_lines = ["{"]
    
    # Iterate through the schema items to format each line.
    for key, value_type in schema.items():
        # Colorize the key.
        key_str = colored(f'    "{key}": ', "grey")
        
        # Apply colorization based on the type of the value.
        if value_type == "str":
            value_str = colored('"String"', "blue")
        elif value_type == "int":
            value_str = colored('"Integer"', "red")
        elif value_type == "float":
            value_str = colored('"Float"', "cyan")
        elif value_type == "list":
            value_str = colored('"List"', "magenta")
        elif value_type == "dict":
            value_str = colored('"Dictionary"', "yellow")
        else:
            # Default colorization for types not explicitly handled.
            value_str = colored(f'"{value_type}"', "white")
        
        # Add the formatted and colorized schema item to the output.
        output_lines.append(f"{key_str}{value_str},")
    
    # Remove the trailing comma from the last item to maintain valid JSON syntax.
    output_lines[-1] = output_lines[-1].rstrip(',')
    
    # Close the output with a closing curly brace.
    output_lines.append("}")
    
    # Join all lines into a single string to return.
    return "\n".join(output_lines)
