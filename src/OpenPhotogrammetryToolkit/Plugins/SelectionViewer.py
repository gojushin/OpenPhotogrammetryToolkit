"""
Selection Viewer Plugin.

This module provides a SelectionViewer class and a custom QLabel class (_SquareLabel)
to display and compare two images side by side.
Each image is displayed in a square label, maintaining its aspect ratio and centered
against a black background.

Classes:
    _SquareLabel: A custom QLabel that maintains square dimensions and centers its pixmap.
    SelectionViewer: Widget-Plugin for displaying and comparing two images with labels.

Usage:
    This file should be placed in the "OpenPhotogrammetryToolkit/Plugins"
    folder to add an image preview for the current selections.
"""

import os

from OpenPhotogrammetryToolkit import PluginWidgetBase

from PySide6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import QSize, Qt, Slot

PLUGIN_NAME = "Selection Viewer"
PLUGIN_DESCRIPTION = "Shows both the primary and secondary selection."
PLUGIN_AUTHOR = "Nico Breycha"
VERSION = "0.0.1"


class _SquareLabel(QLabel):
    """
    A QLabel subclass that maintains a square aspect ratio and updates its
    displayed pixmap to always fit its dimensions, centered with a black background
    if necessary.

    :param parent: The parent widget of this label, defaults to None.
    :type parent: QWidget, optional
    """
    def __init__(self, parent=None):
        """
        Initialize the _SquareLabel with a default black pixmap and preferred size policy.
        """
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Initial Black Pixmap
        self.pixmap = QPixmap(1, 1)
        self.pixmap.fill(Qt.black)
        self.setPixmap(self.pixmap)

    def sizeHint(self):
        """
        Provides a square size hint for the label based on the maximum of its width and height.

        :return: The size hint as a square dimension.
        :rtype: QSize
        """
        # Providing a square size hint
        size = super().sizeHint()
        side = max(size.width(), size.height())
        return QSize(side, side)

    def resizeEvent(self, event):
        """
        Handles the resize event by updating the pixmap to fit the new size.

        :param event: The resize event.
        :type event: QResizeEvent
        """
        # Enforce the widget to be square
        self.updatePixmap()

    def setPixmap(self, pixmap):
        """
        Sets the pixmap for the label and updates it to fit the label's size with a black background.

        :param pixmap: The pixmap to display.
        :type pixmap: QPixmap
        """
        if pixmap and isinstance(pixmap, QPixmap):
            self.pixmap = pixmap
        else:
            # If None or invalid, create a black pixmap
            self.pixmap = QPixmap(1, 1)
            self.pixmap.fill(Qt.black)

        self.updatePixmap()

    def updatePixmap(self):
        """
        Updates the pixmap to fit the label's current size, maintaining the aspect ratio,
        and centering it against a black background.
        """
        if self.pixmap and isinstance(self.pixmap, QPixmap):
            # Scale the pixmap while maintaining aspect ratio
            scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio)

            # Create a new pixmap for the background
            final_pixmap = QPixmap(self.size())
            final_pixmap.fill(Qt.black)  # Fill the pixmap with black color

            # Paint the scaled image onto the final pixmap
            painter = QPainter(final_pixmap)
            x = (final_pixmap.width() - scaled_pixmap.width()) / 2
            y = (final_pixmap.height() - scaled_pixmap.height()) / 2
            painter.drawPixmap(x, y, scaled_pixmap)
            painter.end()

            # Call base class setPixmap with the new pixmap
            super().setPixmap(final_pixmap)
        else:
            # Directly fill with black if no valid pixmap
            final_pixmap = QPixmap(self.size())
            final_pixmap.fill(Qt.black)
            super().setPixmap(final_pixmap)

    def paintEvent(self, event):
        """
        Custom paint event to handle the drawing of the pixmap or a black background if no pixmap is set.

        :param event: The paint event.
        :type event: QPaintEvent
        """
        if self.pixmap:
            # If a pixmap exists, let the QLabel handle painting
            super().paintEvent(event)
        else:
            # If no pixmap, fill the background with black
            painter = QPainter(self)
            painter.fillRect(self.rect(), Qt.black)


class SelectionViewer(PluginWidgetBase):
    """
    A widget to show two selected images side by side for reference and comparison
    using custom square labels.

    :param parent: The applications main window.
    :type parent: QWidget
    :param identifier: The name identifier for this plugin widget.
    :type identifier: str
    """
    def __init__(self, parent, identifier=PLUGIN_NAME):
        """
        Initializes the SelectionViewer with two square labels and vertical layouts
        for displaying primary and secondary selected images.
        """
        super().__init__(opt_main_window=parent, identifier=identifier)

        self.primary_selection_file_path = None
        self.secondary_selection_file_path = None

        self.setMinimumSize(QSize(300, 150))

        self.layout = QHBoxLayout()

        self.prim_layout = QVBoxLayout()
        self.seco_layout = QVBoxLayout()

        self.primary_img_label = _SquareLabel(self)
        self.secondary_img_label = _SquareLabel(self)

        self.prim_layout.addWidget(QLabel("Reference"))
        self.prim_layout.addWidget(self.primary_img_label)

        self.seco_layout.addWidget(QLabel("Comparison"))
        self.seco_layout.addWidget(self.secondary_img_label)

        self.layout.addLayout(self.prim_layout)
        self.layout.addLayout(self.seco_layout)

        self.setLayout(self.layout)

    def primary_selection_changed(self, selection: str):
        """
        Updates the primary selection and loads the corresponding image.

        :param selection: The file path to the primary image.
        :type selection: str
        """
        self.primary_selection_file_path = selection
        self.load_image(selection, self.primary_img_label)

    def secondary_selection_changed(self, selection: str):
        """
        Updates the secondary selection and loads the corresponding image.

        :param selection: The file path to the secondary image.
        :type selection: str
        """
        self.secondary_selection_file_path = selection
        self.load_image(selection, self.secondary_img_label)

    def start(self):
        """
        Is called once the application starts, and all the plugins are loaded.
        Initiates the viewer by loading the primary and secondary selections,
        if they are available and valid file paths.
        """
        primary_fpo = self.fplw.get_primary_selection()
        secondary_fpo = self.fplw.get_secondary_selection()

        if primary_fpo:
            primary_fp = primary_fpo.file_path
            if os.path.isfile(primary_fp):
                self.load_image(primary_fp, self.primary_img_label)

        if secondary_fpo:
            secondary_fp = secondary_fpo.file_path
            if os.path.isfile(secondary_fp):
                self.load_image(secondary_fp, self.secondary_img_label)

    @staticmethod
    def load_image(img_path, label):
        """
        Loads an image from a given path and sets it to the provided label. If the path is invalid,
        sets the label to a default black pixmap.

        :param img_path: The path to the image to load.
        :type img_path: str
        :param label: The label to set the image on.
        :type label: _SquareLabel
        """
        if not img_path or not os.path.isfile(img_path):
            label.setPixmap(QPixmap())
            return

        pixmap = QPixmap(img_path)
        label.setPixmap(pixmap)
