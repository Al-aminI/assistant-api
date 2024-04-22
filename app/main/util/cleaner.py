import json


def replace_outer_quotes(data):
    """
    This function replaces outer quotes in a given data structure with double quotes.
    It uses the json module to convert the data to a string and back to a data structure.

    Parameters:
        data (any): The data structure to process.

    Returns:
        any: The processed data structure.

    """
    result = json.dumps(data)
    result = json.loads(result)

    return result