import json


def import_json_as_dict(json_file_path):
    """
    Imports a JSON file as a dictionary.

    Args:
    json_file_path (str): The file path of the JSON file.

    Returns:
    dict: The dictionary representation of the JSON file.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("File not found. Please check the path and try again.")
    except json.JSONDecodeError:
        print("File is not a valid JSON. Please check the file and try again.")
    except Exception as e:
        print("An error occurred: {}".format(e))
