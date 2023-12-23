import os
import tempfile
import pytest
import shutil

from PySide6.QtWidgets import QApplication
from Widgets import FilePathObject, FilePathListWidget

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

@pytest.fixture(scope="module")
def qapp():
    return QApplication([])


def test_FilePathObject_initialization_fakepath(qapp):
    """Test that the FilePathObject initializes correctly."""
    with pytest.raises(FileExistsError) as excinfo:
        test_path = "C:/fakepath/fakefile.txt"
        fpo = FilePathObject(test_path)


def test_FilePathObject_initialization_realpath(qapp):
    """Test that the FilePathObject initializes correctly."""
    temp_dir = tempfile.mkdtemp()
    target_file = os.path.join(temp_dir, "target.txt")

    with open(target_file, "w") as f:
        f.write("Hello")

    fpo = FilePathObject(target_file)

    assert fpo.file_path == target_file
    assert fpo.label == os.path.basename(target_file)

    os.remove(target_file)


def test_FilePathObject_symlink_resolution(qapp, tmp_path):  # Will fail under Windows due to ! Run in Docker.
    """Test resolution of symlink."""
    # Setup: Create a temporary file and a symlink pointing to it
    target_file = tmp_path / "target.txt"
    symlink_path = tmp_path / "symlink.lnk"

    target_file.write_text("Hello Test!")

    # Attempt to create a symlink. Skip test if not permitted (common in Windows without admin rights).
    try:
        os.symlink(str(target_file), str(symlink_path))
    except OSError as e:
        pytest.skip("Skipped Test since privileges for creating Symlinks are not granted or not supported on this OS.")

    # Test: Initialize FilePathObject with the symlink
    fpo = FilePathObject(str(symlink_path))

    assert os.path.realpath(fpo.file_path) == os.path.realpath(str(target_file))


def test_FilePathListWidget_file_changed_signal(qapp, qtbot, tmp_path):
    """Test the fileHasChanged signal."""
    widget = FilePathListWidget()
    test_file = tmp_path / "test.txt"
    test_file.write_text("Initial text.")

    with qtbot.waitSignal(widget.fileHasChanged.fileHasChanged, timeout=1000) as blocker:
        test_file.write_text("Modified text.")  # Modify the file to trigger signal
        widget.update_file(str(test_file))  # Simulate the file update call

    assert blocker.signal_triggered
    assert blocker.args == [str(test_file)]


def test_FilePathListWidget_files_changed_signal(qapp, qtbot, tmp_path):
    """Test the filesHaveChanged signal."""
    widget = FilePathListWidget()
    widget.set_watched_directory(str(tmp_path))  # Set to the temporary directory

    with qtbot.waitSignal(widget.filesHaveChanged.filesHaveChanged, timeout=1000) as blocker:
        # Copy files from IMAGE_DIR to tmp_path. Adding Files should trigger a signal.
        for file_name in os.listdir(IMAGE_DIR):
            source = os.path.join(IMAGE_DIR, file_name)
            destination = tmp_path / file_name
            shutil.copy(source, destination)  # Triggers the update
            break  # Testing for more is pointless

    assert blocker.signal_triggered


def test_FilePathListWidget_primary_selection_signal(qapp, qtbot):
    """Test the primarySelectionChanged signal."""
    widget = FilePathListWidget()
    widget.set_watched_directory(IMAGE_DIR)  # Set to the predefined directory with images
    widget.update_file_list()  # Refresh to include the new files

    fpo = next(iter(widget.curr_file_paths.values()))

    with qtbot.waitSignal(widget.primarySelectionChanged.primarySelectionChanged, timeout=1000) as blocker:
        widget.set_primary_selection(fpo)  # Simulate primary selection

    assert blocker.signal_triggered
    assert blocker.args[0] == fpo.file_path
    assert IMAGE_DIR in blocker.args[0]


def test_FilePathListWidget_secondary_selection_signal(qapp, qtbot):
    """Test the secondarySelectionChanged signal."""
    widget = FilePathListWidget()
    widget.set_watched_directory(IMAGE_DIR)   # Set to the predefined directory with images
    widget.update_file_list()  # Refresh to include the new files

    fpo = next(iter(widget.curr_file_paths.values()))

    with qtbot.waitSignal(widget.secondarySelectionChanged.secondarySelectionChanged, timeout=1000) as blocker:
        widget.set_secondary_selection(fpo)  # Simulate secondary selection

    assert blocker.signal_triggered
    assert blocker.args[0] == fpo.file_path
    assert IMAGE_DIR in blocker.args[0]

