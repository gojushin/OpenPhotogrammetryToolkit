from __future__ import annotations

import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QLabel, QListWidgetItem
from PySide6.QtCore import QFileSystemWatcher, QObject, Signal, Qt
import logging

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".ico")


class _FilePathObject(QLabel):
    """Represents a file path with an associated UI label.

    :param file_path: The path to the file this object represents.
    :type file_path: str
    :param parent: The parent widget.
    :type parent: QWidget
    """
    def __init__(self, file_path, parent=None):
        if not parent:
            logging.warning("FPO did NOT receive a parent!")

        super().__init__(parent=parent)

        # Resolve Symlinks
        if os.path.islink(file_path):
            self.file_path = os.path.realpath(file_path)
            logging.info("Resolved Symlink {} to {}".format(file_path, self.file_path))
        else:
            self.file_path = file_path

        # Normalize and resolve file_path
        file_path = os.path.normpath(os.path.abspath(file_path)).replace(r"\\", "/")

        if not os.path.isfile(file_path):
            raise FileExistsError("{} does not exist!".format(self.file_path))

        self.label = os.path.basename(file_path)

        self.setText(self.label)
        self.change_style_unselected()

    def change_style_unselected(self):
        """Style the label as unselected (plain and black)."""
        self.setStyleSheet("QLabel { color: black; font-weight: normal; }")

    def change_style_primary(self):
        """Style the label as selected primary (thick and blue)."""
        self.setStyleSheet("QLabel { color: blue; font-weight: bold; }")

    def change_style_secondary(self):
        """Style the label as selected secondary (thick and orange)."""
        self.setStyleSheet("QLabel { color: orange; font-weight: bold; }")


class _FileChangedSignal(QObject):
    """Signal for when a single file has changed."""
    fileHasChanged = Signal(str)


class _FilesChangedSignal(QObject):
    """Signal for when multiple files have changed."""
    filesHaveChanged = Signal(list)


class _PrimarySelectionSignal(QObject):
    """Signal for when the primary selection has changed."""
    primarySelectionChanged = Signal(str)


class _SecondarySelectionSignal(QObject):
    """Signal for when the secondary selection has changed."""
    secondarySelectionChanged = Signal(str)


class _ClickableListWidget(QListWidget):
    """
    A subclass of QListWidget that handles mouse press events to determine if the click is left or right.

    :param parent: The parent widget of this list widget. Defaults to None.
    :type parent: QWidget or None
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def mousePressEvent(self, event):  # We handle the mouse press event here, so we only need it one time.
        """
        Handle mouse press events to determine if the click is left or right.

        Overrides the default mouse press event to add functionality for detecting
        left and right-clicks on the items of the list. It then delegates the action to the parent widget.

        :param event: The mouse event that occurred.
        :type event: QMouseEvent
        """
        super().mousePressEvent(event)  # Invoke the default functionality

        # Determine which item is selected
        selection = self.currentItem()

        if not selection:
            return  # No item was clicked

        selected_item: _FilePathObject = self.itemWidget(selection)

        if event.button() == Qt.LeftButton:  # If the click is a left click
            self.parent.set_primary_selection(selected_item)
        elif event.button() == Qt.RightButton:  # If the click is a right click
            self.parent.set_secondary_selection(selected_item)


class FilePathListWidget(QWidget):
    """A widget that displays a list of file paths as clickable labels.

    This widget watches a directory and updates the file list when changes are detected.

    :param parent: The parent widget. Defaults to None.
    :type parent: QWidget or None
    """
    def __init__(self, parent=None):
        """Initialize the file path list widget."""
        super().__init__(parent)

        self._primary_sel: _FilePathObject = None
        self._secondary_sel: _FilePathObject = None

        self.fileHasChanged = _FileChangedSignal()
        self.filesHaveChanged = _FilesChangedSignal()
        self.primarySelectionChanged = _PrimarySelectionSignal()
        self.secondarySelectionChanged = _SecondarySelectionSignal()

        self.curr_file_paths = {}
        self.curr_folder_path = None

        self.layout = QVBoxLayout(self)
        self.listWidget = _ClickableListWidget(parent=self)
        self.layout.addWidget(self.listWidget)

        self.watcher = None

    def set_watched_directory(self, dir_path):
        """Set the directory for the widget to monitor.

        :param dir_path: The path to the directory to monitor
        :type dir_path: str
        """
        self.curr_folder_path = dir_path
        self.update_file_list()

        self.watcher = QFileSystemWatcher([self.curr_folder_path])
        self.watcher.directoryChanged.connect(self.update_file_list)
        self.watcher.fileChanged.connect(self.update_file)

    def set_primary_selection(self, selection):
        """Set the primary selected file.

        :param selection: the selection
        :type selection: str | _FilePathObject
        """
        # If FPO is provided, we can just operate on that and return early.
        if isinstance(selection, _FilePathObject):
            if selection is self._primary_sel:
                return

            if selection is self._secondary_sel:
                self._secondary_sel = None

                # Clear previous selection
            if self._primary_sel:
                self._primary_sel.change_style_unselected()

            selection.change_style_primary()
            self._primary_sel = selection
            self.primarySelectionChanged.primarySelectionChanged.emit(self._primary_sel.file_path)
            return

        # In case label is provided
        if os.path.isfile(selection):
            selection = os.path.basename(selection)

        # Get the FPO
        fpo: _FilePathObject = self.get_fpo_from_current(selection)

        if fpo is self._primary_sel:
            return

        if fpo is self._secondary_sel:
            self._secondary_sel = None

        # Clear previous selection
        if self._primary_sel:
            self._primary_sel.change_style_unselected()

        fpo.change_style_primary()
        self._primary_sel = fpo
        self.primarySelectionChanged.primarySelectionChanged.emit(self._primary_sel.file_path)

    def set_secondary_selection(self, selection):
        """Set the secondary selected file.

        :param selection: the selection
        :type selection: str | _FilePathObject
        """
        # If FPO is provided, we can just operate on that and return early.
        if isinstance(selection, _FilePathObject):
            if selection is self._secondary_sel:
                return

            if selection is self._primary_sel:
                self._primary_sel = None

            # Clear previous selection
            if self._secondary_sel:
                self._secondary_sel.change_style_unselected()

            selection.change_style_secondary()
            self._secondary_sel = selection
            self.secondarySelectionChanged.secondarySelectionChanged.emit(self._secondary_sel.file_path)
            return

        # In case label is provided
        if os.path.isfile(selection):
            selection = os.path.basename(selection)

        # Get the FPO
        fpo: _FilePathObject = self.get_fpo_from_current(selection)

        if fpo is self._secondary_sel:
            return

        if fpo is self._primary_sel:
            self._primary_sel = None

        # Clear previous selection
        if self._secondary_sel:
            self._secondary_sel.change_style_unselected()

        fpo.change_style_secondary()
        self._secondary_sel = fpo
        self.secondarySelectionChanged.secondarySelectionChanged.emit(self._secondary_sel.file_path)

    def get_fpo_from_current(self, path) -> _FilePathObject:
        if os.path.isfile(path):
            path = os.path.basename(path)

        try:
            return self.curr_file_paths[path]
        except KeyError:
            logging.warning("Selected Object does not exist!")
            return None

    def update_file_list(self):
        """Updates the displayed list of files in the monitored directory.

        This method clears the existing list and repopulates it based on the files
        found in the currently watched directory. Only processes image files.
        """
        self.listWidget.clear()

        for file_name in os.listdir(self.curr_folder_path):
            if any(file_name.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                full_path = os.path.join(self.curr_folder_path, file_name)
                # Create a FilePathObject for each file
                fpo = _FilePathObject(full_path, parent=self)
                self.curr_file_paths[fpo.label] = fpo
                # Create a QListWidgetItem for the list
                item = QListWidgetItem(self.listWidget)
                # Set the FilePathObject as the item's widget
                self.listWidget.setItemWidget(item, fpo)
                # Add the item to the list
                self.listWidget.addItem(item)

        self.filesHaveChanged.filesHaveChanged.emit(list(self.curr_file_paths.values()))

    def update_file(self, file_path):
        """Update the list with a single file change.

        :param file_path: The path to the updated file
        :type file_path: str
        """
        fpo = _FilePathObject(file_path, parent=self)
        self.curr_file_paths[fpo.label] = fpo
        self.fileHasChanged.fileHasChanged.emit(file_path)

