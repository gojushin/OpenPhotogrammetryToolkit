import importlib.util
import json
import os
import sys


def get_class_name(module):
    """
    Retrieve the name of the class that has the same name as the module file.

    :param module: The module from which to retrieve the class name
    :type module: ModuleType
    :return: The name of the class found in the module
    :rtype: str
    :raises AttributeError: If no class named as the module file is found in the module
    """
    module_file = os.path.basename(module.__file__)

    file_name = os.path.splitext(module_file)[0]

    # Check if the class exists in the module
    if hasattr(module, file_name):
        return file_name
    else:
        raise AttributeError("No class named {} found in module {}".format(file_name, module.__name__))


def import_module(file_location):
    """
    Import a module from a given file location.

    :param file_location: The file location of the module to import
    :type file_location: str
    :return: The module that is imported
    :rtype: ModuleType
    """
    module_name = os.path.splitext(os.path.basename(file_location))[0]

    # Find the module specification from the import system
    spec = importlib.util.spec_from_file_location(module_name, file_location)

    module = importlib.util.module_from_spec(spec)

    # Load it into sys.modules
    sys.modules[module_name] = module

    # Execute the module
    spec.loader.exec_module(module)

    return module


def find_files_by_type(directory, file_type, sort=True):
    """
    Find files of a specified type in a given directory, optionally sorted by filename.

    :param directory: The path to the directory where the search should be performed
    :type directory: str
    :param file_type: The extension of the files to find, e.g., 'txt' for text files
    :type file_type: str
    :param sort: Whether to return the files sorted by filename, defaults to True
    :type sort: bool, optional
    :return: A list of paths to the files found with the specified extension
    :rtype: list
    """
    matched_files = []
    # Ensure the directory exists and is a directory, else return empty list
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return matched_files

    # Normalize the file type to ensure it does not start with a period
    if file_type.startswith('.'):
        file_type = file_type[1:]

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check the file extension and add to the list if it matches
            if file.endswith('.' + file_type):
                matched_files.append(os.path.join(root, file))

    if sort:
        matched_files.sort(key=lambda x: os.path.basename(x))

    return matched_files


def import_json_as_dict(json_file_path):
    """
    Import a JSON file as a dictionary.

    :param json_file_path: The file path of the JSON file
    :type json_file_path: str
    :return: The dictionary representation of the JSON file
    :rtype: dict
    :raises FileNotFoundError: If the JSON file is not found at the specified path
    :raises JSONDecodeError: If the file is not a valid JSON
    :raises Exception: For other exceptions that may occur
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError as e:
        print("File not found. Please check the path and try again.")
        raise e
    except json.JSONDecodeError as e:
        print("File is not a valid JSON. Please check the file and try again.")
        raise e
    except Exception as e:
        print("An error occurred: {}".format(e))
