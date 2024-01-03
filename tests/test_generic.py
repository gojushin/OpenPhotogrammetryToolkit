import json
import os

import pytest

from OpenPhotogrammetryToolkit.opt_helper_funcs import (get_class_name, import_module, find_files_by_type,
                                                        import_json_as_dict)

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")


def test_get_class_name_valid(tmp_path):
    """
    Test the get_class_name function with a valid mock module.

    Ensures that the function correctly returns the class name when
    the class name matches the file name.
    """
    dummy_module = tmp_path / "dummy_module.py"
    dummy_module.write_text("class dummy_module: pass")

    class MockModule:
        pass

    mocked_module = MockModule()
    mocked_module.__file__ = str(dummy_module)
    setattr(mocked_module, 'dummy_module', MockModule)  # Simulate the class named as the file
    assert get_class_name(mocked_module) == 'dummy_module'


def test_get_class_name_invalid(tmp_path):
    """
    Test the get_class_name function with an invalid mock module.

    Ensures that the function raises an AttributeError when the class name
    does not match the file name.
    """
    dummy_module = tmp_path / "dummy_module.py"
    dummy_module.write_text("")

    class MockModule:
        pass

    mocked_module = MockModule()
    mocked_module.__file__ = str(dummy_module)
    with pytest.raises(AttributeError):
        get_class_name(mocked_module)


def test_import_module_valid(tmp_path):
    """
    Test the import_module function with a valid module file.

    Verifies that the function correctly imports a Python file as a module
    and recognizes its name.
    """
    module_file = tmp_path / "temp_module.py"
    module_file.write_text("# Temporary module file")
    assert import_module(str(module_file)).__name__ == 'temp_module'


def test_import_module_invalid():
    """
    Test the import_module function with a non-existent module file.

    Ensures that the function raises a FileNotFoundError when attempting
    to import a non-existent module file.
    """
    with pytest.raises(FileNotFoundError) as e:
        import_module("non_existent_module.py")


def test_find_files_by_type():
    """
    Test the find_files_by_type function.

    Verifies that the function correctly identifies and returns all files
    of a specific type within a given directory.
    """
    file1 = os.path.join(IMAGE_DIR, "test_img1.jpg")
    file2 = os.path.join(IMAGE_DIR, "test_img2.jpg")
    file3 = os.path.join(IMAGE_DIR, "test_img3.jpg")
    file4 = os.path.join(IMAGE_DIR, "test_img4.jpg")

    assert find_files_by_type(str(IMAGE_DIR), 'jpg') == [file1, file2, file3, file4]


def test_import_json_as_dict_valid(tmp_path):
    """
    Test the import_json_as_dict function with a valid JSON file.

    Ensures that the function correctly imports a JSON file as a dictionary.
    """
    data = {"key": "value"}
    json_file = tmp_path / "temp.json"
    json_file.write_text(json.dumps(data))
    assert import_json_as_dict(str(json_file)) == data


def test_import_json_as_dict_file_not_found():
    """
    Test the import_json_as_dict function for a non-existent file.

    Ensures that the function raises a FileNotFoundError when the specified
    JSON file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        import_json_as_dict("non_existent.json")


def test_import_json_as_dict_invalid_json(tmp_path):
    """
    Test the import_json_as_dict function with an invalid JSON file.

    Ensures that the function raises a JSONDecodeError when the file content
    is not a valid JSON format.
    """
    non_json_file = tmp_path / "file.txt"
    non_json_file.write_text("Not a JSON content")
    with pytest.raises(json.JSONDecodeError):
        import_json_as_dict(str(non_json_file))
