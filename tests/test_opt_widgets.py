import os
import tempfile

import pytest
import shutil

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QMouseEvent
from Widgets import FilePathObject, FilePathListWidget, StartupDialog, _SquareButton, _WidgetTexts

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")


@pytest.fixture(scope="function")
def file_path_widget():
    fpw = FilePathListWidget()
    yield fpw
    fpw.close()


@pytest.fixture(scope="function")
def square_button():
    return _SquareButton()


@pytest.fixture(scope="function")
def startup_dialog():
    """Fixture to create and return a fresh instance of StartupDialog for each test"""
    diag = StartupDialog()
    yield diag
    diag.close()


def test_FilePathObject_initialization_fakepath(qapp):
    """
    Test FilePathObject initialization with a fake path.

    Ensures that initializing FilePathObject with a non-existent file path raises a FileExistsError.
    """
    with pytest.raises(FileExistsError) as excinfo:
        test_path = "C:/fakepath/fakefile.txt"
        fpo = FilePathObject(test_path)


def test_FilePathObject_initialization_realpath():
    """
    Test FilePathObject initialization with a real path.

    Ensures that initializing FilePathObject with an actual file path correctly sets up its properties.
    """
    temp_dir = tempfile.mkdtemp()
    target_file = os.path.join(temp_dir, "target.txt")

    with open(target_file, "w") as f:
        f.write("Hello")

    fpo = FilePathObject(target_file)

    assert fpo.file_path == target_file
    assert fpo.label == os.path.basename(target_file)

    os.remove(target_file)


def test_FilePathObject_symlink_resolution(tmp_path):  # Will fail under Windows due to ! Run in Docker.
    """
    Test FilePathObject symlink resolution.

    Ensures that FilePathObject resolves symlinks to their target paths and initializes correctly.
    """
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


def test_FilePathListWidget_file_changed_signal(qtbot, tmp_path, file_path_widget):
    """
    Test the fileHasChanged signal of FilePathListWidget.

    Ensures that modifying a file triggers the fileHasChanged signal with the correct file path as argument.
    """
    widget = file_path_widget
    test_file = tmp_path / "test.txt"
    test_file.write_text("Initial text.")

    with qtbot.waitSignal(widget.fileHasChanged.fileHasChanged, timeout=100) as blocker:
        test_file.write_text("Modified text.")  # Modify the file to trigger signal
        widget.update_file(str(test_file))  # Simulate the file update call

    assert blocker.signal_triggered
    assert blocker.args == [str(test_file)]


def test_FilePathListWidget_files_changed_signal(qtbot, tmp_path, file_path_widget):
    """
    Test the filesHaveChanged signal of FilePathListWidget.

    Ensures that adding files to the watched directory triggers the filesHaveChanged signal.
    """
    widget = file_path_widget
    widget.set_watched_directory(str(tmp_path))  # Set to the temporary directory

    with qtbot.waitSignal(widget.filesHaveChanged.filesHaveChanged, timeout=100) as blocker:
        # Copy files from IMAGE_DIR to tmp_path. Adding Files should trigger a signal.
        for file_name in os.listdir(IMAGE_DIR):
            source = os.path.join(IMAGE_DIR, file_name)
            destination = tmp_path / file_name
            shutil.copy(source, destination)  # Triggers the update
            break  # Testing for more is pointless

    assert blocker.signal_triggered


def test_FilePathListWidget_primary_selection_signal(qtbot, file_path_widget):
    """
    Test the primarySelectionChanged signal of FilePathListWidget.

    Ensures that setting a primary selection triggers the primarySelectionChanged signal with the correct file path.
    """
    widget = file_path_widget
    widget.set_watched_directory(IMAGE_DIR)  # Set to the predefined directory with images
    widget.update_file_list()  # Refresh to include the new files

    fpo = next(iter(widget.curr_file_paths.values()))

    with qtbot.waitSignal(widget.primarySelectionChanged.primarySelectionChanged, timeout=100) as blocker:
        widget.set_primary_selection(fpo)  # Simulate primary selection

    assert blocker.signal_triggered
    assert blocker.args[0] == fpo.file_path
    assert IMAGE_DIR in blocker.args[0]


def test_FilePathListWidget_secondary_selection_signal(qtbot, file_path_widget):
    """
    Test the secondarySelectionChanged signal of FilePathListWidget.

    Ensures that setting a secondary selection triggers the secondarySelectionChanged signal with the correct file path.
    """
    widget = file_path_widget
    widget.set_watched_directory(IMAGE_DIR)  # Set to the predefined directory with images
    widget.update_file_list()  # Refresh to include the new files

    fpo = next(iter(widget.curr_file_paths.values()))

    with qtbot.waitSignal(widget.secondarySelectionChanged.secondarySelectionChanged, timeout=100) as blocker:
        widget.set_secondary_selection(fpo)  # Simulate secondary selection

    assert blocker.signal_triggered
    assert blocker.args[0] == fpo.file_path
    assert IMAGE_DIR in blocker.args[0]


def test_SquareButton_size_hint(square_button):
    """
    Test the sizeHint method of _SquareButton.

    Ensures that the width and height returned by sizeHint are equal, maintaining a square aspect ratio.
    """
    size_hint = square_button.sizeHint()
    assert size_hint.width() == size_hint.height(), "The button is not square."


def test_StartupDialog_signal_emission(qtbot, startup_dialog):
    """
        Test the dirSelected signal emission of StartupDialog.

        Ensures that the dirSelected signal emits the directory path when triggered.
        """
    with qtbot.waitSignal(startup_dialog.dirSelectedSignal.dirSelected, timeout=100) as blocker:
        startup_dialog.dirSelectedSignal.dirSelected.emit(IMAGE_DIR)

    assert blocker.signal_triggered
    assert blocker.args[0] == IMAGE_DIR


def test_StartupDialog_eventFilter_hover(startup_dialog):
    """
    Test the hover event filter of StartupDialog.

    Ensures that hovering over the open directory and create directory buttons updates the explanation label text accordingly.
    """
    # Simulate hover enter event for open_dir_btn
    enter_event = QMouseEvent(QEvent.Enter, startup_dialog.open_dir_btn.pos(), Qt.NoButton, Qt.NoButton, Qt.NoModifier)
    QApplication.sendEvent(startup_dialog.open_dir_btn, enter_event)
    assert startup_dialog.explanation_label.text() == _WidgetTexts["StartupDiaOpenDirHint"]

    # Simulate hover leave event for open_dir_btn
    leave_event = QMouseEvent(QEvent.Leave, startup_dialog.open_dir_btn.pos(), Qt.NoButton, Qt.NoButton, Qt.NoModifier)
    QApplication.sendEvent(startup_dialog.open_dir_btn, leave_event)
    assert startup_dialog.explanation_label.text() == ""

    enter_event_create = QMouseEvent(QEvent.Enter, startup_dialog.create_dir_btn.pos(), Qt.NoButton, Qt.NoButton,
                                     Qt.NoModifier)
    QApplication.sendEvent(startup_dialog.create_dir_btn, enter_event_create)
    # Assert for create_dir_btn hover event
    assert startup_dialog.explanation_label.text() == _WidgetTexts["StartupDiaCreateDirHint"]

    # Simulate hover leave event for create_dir_btn
    leave_event_create = QMouseEvent(QEvent.Leave, startup_dialog.create_dir_btn.pos(), Qt.NoButton, Qt.NoButton,
                                     Qt.NoModifier)
    QApplication.sendEvent(startup_dialog.create_dir_btn, leave_event_create)
    assert startup_dialog.explanation_label.text() == ""
