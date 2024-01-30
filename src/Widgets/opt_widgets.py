from __future__ import annotations

import gc
import logging
import os

from PySide6.QtCore import QFileSystemWatcher, QObject, Signal, Qt, QEvent, QSize
from PySide6.QtWidgets import QWidget, QListWidget, QLabel, QListWidgetItem, QFileDialog, QDialog, \
    QHBoxLayout, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy

from OpenPhotogrammetryToolkit import opt_helper_funcs as h_func

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".ico")

WIDGET_TEXTS = h_func.import_json_as_dict(os.path.join(os.path.dirname(os.path.abspath(__file__)), "widget_texts.json"))


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
        self._itemRef = None

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


class _FileAddedSignal(QObject):
    """Signal for when a single file has changed."""
    fileAdded = Signal(str)


class _FileRemovedSignal(QObject):
    """Signal for when a single file has changed."""
    fileRemoved = Signal(str)


class _WatcherInitializedSingal(QObject):
    """Signal for when multiple files have changed."""
    watcherInitialized = Signal(list)


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

        self.fileAdded = _FileAddedSignal()
        self.fileRemoved = _FileRemovedSignal()
        self.watcherInitialized = _WatcherInitializedSingal()
        self.primarySelectionChanged = _PrimarySelectionSignal()
        self.secondarySelectionChanged = _SecondarySelectionSignal()

        self.curr_file_paths = {}

        self.layout = QVBoxLayout(self)
        self.listWidget = _ClickableListWidget(parent=self)
        self.layout.addWidget(self.listWidget)

        self.curr_folder_path = None
        self.watched_directory = None

    def set_watched_directory(self, dir_path):
        """Set the directory for the widget to monitor.

        :param dir_path: The path to the directory to monitor
        :type dir_path: str
        """
        self.curr_folder_path = dir_path
        self.intialize_file_list()

        self.watcher = QFileSystemWatcher([self.curr_folder_path])
        self.watcher.directoryChanged.connect(self.update_file)

    def get_primary_selection(self):
        """
        Retrieves the primary selected file path object.

        :return: The primary selected file path object if it exists, otherwise None.
        :rtype: _FilePathObject or None
        """
        if self._primary_sel is None:
            return None

        return self._primary_sel

    def get_secondary_selection(self):
        """
        Retrieves the secondary selected file path object.

        :return: The secondary selected file path object if it exists, otherwise None.
        :rtype: _FilePathObject or None
        """
        if self._secondary_sel is None:
            return None

        return self._secondary_sel

    def set_primary_selection(self, selection, broadcast_change=True):
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
            if broadcast_change:
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

        if broadcast_change:
            self.primarySelectionChanged.primarySelectionChanged.emit(self._primary_sel.file_path)

    def set_secondary_selection(self, selection, broadcast_change=True):
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
            if broadcast_change:
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

        if broadcast_change:
            self.secondarySelectionChanged.secondarySelectionChanged.emit(self._secondary_sel.file_path)

    def get_fpo_from_current(self, path) -> _FilePathObject:
        """
        Retrieves the file path object (_FilePathObject) corresponding to the given path from the current file paths.

        :param path: The path for which to retrieve the file path object.
        :type path: str
        :return: The file path object if found, otherwise None.
        :rtype: _FilePathObject or None
        :raises KeyError: If the selected object does not exist.
        """
        if os.path.isfile(path):
            path = os.path.basename(path)

        try:
            return self.curr_file_paths[path]
        except KeyError:
            logging.warning("Selected Object does not exist!")
            return None

    def intialize_file_list(self):
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
                self._add_fpo_to_view(fpo)

        self.watcherInitialized.watcherInitialized.emit(list(self.curr_file_paths.values()))

    def _add_fpo_to_view(self, fpo):
        """
        Adds a file path object to the list widget view.

        :param fpo: The file path object to add to the view.
        :type fpo: _FilePathObject
        """
        if fpo.label not in self.curr_file_paths.keys():
            # Create a QListWidgetItem for the list
            item = QListWidgetItem(self.listWidget)
            # Set the FilePathObject as the item's widget
            fpo._itemRef = item
            self.listWidget.setItemWidget(item, fpo)
            # Add the item to the list
            self.listWidget.addItem(item)

            self.curr_file_paths[fpo.label] = fpo

    def _remove_fpo_from_view(self, fpo):
        """
        Removes a file path object from the list widget view.

        :param fpo: The file path object to be removed.
        :type fpo: _FilePathObject
        """
        if fpo.label in self.curr_file_paths.keys():
            # Unselect if selected
            if fpo == self.get_primary_selection():
                self._primary_sel.change_style_unselected()
                self._primary_sel = None
            elif fpo == self.get_secondary_selection():
                self._secondary_sel.change_style_unselected()
                self._secondary_sel = None

            idx = self.listWidget.indexFromItem(fpo._itemRef)
            item = self.listWidget.takeItem(idx.row())
            self.curr_file_paths.pop(fpo.label)

            del fpo
            del item

    def update_file(self, dir_path):
        """Update the list with a single file change.

        :param dir_path: The path to the updated directory
        :type file_path: str
        """
        files = set()

        for file_name in os.listdir(dir_path):
            if any(file_name.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                full_path = os.path.join(dir_path, file_name)
                files.add(full_path)

        # We track changes and operate on the end to not change the dict during iteration
        fpos = set(f.file_path for f in self.curr_file_paths.values())

        added = list(files - fpos)
        removed = list(fpos - files)

        for a in added:
            print("Added {}".format(a))
            self._file_added(a)

        for r in removed:
            print("Deleted {}".format(r))
            self._file_removed(r)

    def _file_added(self, file):
        """
        Handles the addition of a file to the view.

        :param file: The path of the file that has been added.
        :type file: str
        """
        fpo = _FilePathObject(file, parent=self)
        self._add_fpo_to_view(fpo)
        self.fileAdded.fileAdded.emit(file)

    def _file_edited(self, file):
        """
        Handles the editing of a file in the view. This is currently a placeholder with no implementation.

        :param file: The path of the file that has been edited.
        :type file: str
        """
        # do nothing
        # emit nothing
        pass

    def _file_removed(self, file):
        """
        Handles the removal of a file from the view.

        :param file: The path of the file that has been removed.
        :type file: str
        """
        fpo = self.curr_file_paths[os.path.basename(file)]
        self._remove_fpo_from_view(fpo)
        self.fileRemoved.fileRemoved.emit(file)


class _SquareButton(QPushButton):
    """
    A QPushButton that maintains a square shape and ensures equal width and height.

    :param text: The button text.
    :type text: str, optional
    :param parent: The parent widget.
    :type parent: QWidget or None, optional
    """
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)

    def sizeHint(self):
        """
        Reimplemented sizeHint to make the width and height equal.

        :return: The recommended size for the button, which is square.
        :rtype: QSize
        """
        size = super(_SquareButton, self).sizeHint()
        dimension = max(size.width(), size.height())
        return QSize(dimension, dimension)


class _StartupSignal(QObject):
    """Signal for when a single file has changed."""
    dirSelected = Signal(str)


class StartupDialog(QDialog):
    """
    Dialog for initial setup tasks such as opening or creating a directory.

    :param QDialog: Inherits QDialog
    """
    def __init__(self):
        """
        Constructor for StartupDialog, initializes the dialog and its components.
        """
        super().__init__()
        # Setting Widget Size
        self.setFixedSize(400, 250)

        self.dirSelectedSignal = _StartupSignal()

        # Generic reusable Spacer. We need a function to create new instances, because this otherwise makes problems
        # when deconstructing the QDialog
        def expanding_spacer(): return QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Create and fit all layouts.
        layout = QVBoxLayout()

        greeting_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        hint_layout = QHBoxLayout()

        layout.addLayout(greeting_layout)
        layout.addLayout(button_layout)
        layout.addLayout(hint_layout)

        # Greeting
        greeting = QLabel(WIDGET_TEXTS["StartupDialogWelcomeText"])
        greeting.setAlignment(Qt.AlignCenter)

        # Greeting Arrangement
        greeting_layout.addItem(expanding_spacer())
        greeting_layout.addWidget(greeting)
        greeting_layout.addItem(expanding_spacer())

        # Button to open a directory
        self.open_dir_btn = _SquareButton("Open")
        self.open_dir_btn.clicked.connect(self.open_directory)

        # Button to create a directory
        self.create_dir_btn = _SquareButton("Create")
        self.create_dir_btn.clicked.connect(self.create_directory)

        # Setting up hover events for buttons
        self.open_dir_btn.installEventFilter(self)
        self.create_dir_btn.installEventFilter(self)

        # Button Arrangement
        button_layout.addItem(expanding_spacer())
        button_layout.addWidget(self.open_dir_btn)
        button_layout.addItem(expanding_spacer())
        button_layout.addWidget(self.create_dir_btn)
        button_layout.addItem(expanding_spacer())

        # Explanation Label
        self.explanation_label = QLabel("")
        self.explanation_label.setAlignment(Qt.AlignCenter)

        # Hint Arrangement
        hint_layout.addItem(expanding_spacer())
        hint_layout.addWidget(self.explanation_label)
        hint_layout.addItem(expanding_spacer())

        # Set dialog layout
        self.setLayout(layout)

    def open_directory(self):
        """
        Opens a dialog to select a directory and emits dirSelected signal with the selected path.

        :return: None
        """
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.dirSelectedSignal.dirSelected.emit(dir_path)

    def create_directory(self):
        """
        Opens a dialog to create a new directory. This is currently a placeholder and will be implemented later.

        :return: None
        """
        dir_path = QFileDialog.getExistingDirectory(self, "Create Directory")
        if dir_path:
            pass  # TODO Implement shallow working dirs in the future using symlinks.

    def eventFilter(self, obj, event):
        """
        Filters events to respond to hover events over buttons.

        :param obj: The object that generated the event.
        :type obj: QObject
        :param event: The event that occurred.
        :type event: QEvent
        :return: Whether the event was handled here.
        :rtype: bool
        """
        # Check for hover event
        if event.type() == QEvent.Enter:
            if obj == self.open_dir_btn:
                self.explanation_label.setText(WIDGET_TEXTS["StartupDiaOpenDirHint"])
            elif obj == self.create_dir_btn:
                self.explanation_label.setText(WIDGET_TEXTS["StartupDiaCreateDirHint"])
        elif event.type() == QEvent.Leave:
            self.explanation_label.setText("")

        return super().eventFilter(obj, event)
