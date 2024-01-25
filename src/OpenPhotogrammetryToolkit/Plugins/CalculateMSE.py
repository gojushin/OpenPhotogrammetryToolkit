"""
Calculate MSE Action.

This module provides a SelectionViewer class and a custom QLabel class (_SquareLabel)
to display and compare two images side by side.
Each image is displayed in a square label, maintaining its aspect ratio and centered
against a black background.

Classes:
    CalculateMSE: Action-Plugin to calculate the MSE between two images.

Usage:
    The plugin retrieves the primary and secondary image file paths,
    loads the images, calculates the MSE, and displays the result.
"""

import cv2
import numpy as np
from PySide6.QtWidgets import QMessageBox

from OpenPhotogrammetryToolkit import PluginActionBase

PLUGIN_NAME = "CalculateMSE"
PLUGIN_DESCRIPTION = "Calculates the MSE between the reference and the comparison picture."
PLUGIN_AUTHOR = "Nico Breycha"
VERSION = "0.0.1"


class CalculateMSE(PluginActionBase):
    """
    An Action to calculate the Mean Squared Error between the two selected images.

    :param parent: The applications main window.
    :type parent: QWidget
    :param identifier: The name identifier for this plugin widget.
    :type identifier: str
    """

    def __init__(self, parent, identifier=PLUGIN_NAME):
        super().__init__(opt_main_window=parent, identifier=identifier)

    def on_triggered(self):
        """
        Executes the main functionality of the plugin. It retrieves the primary and secondary
        image file paths, loads the images, calculates the MSE, and displays the result.

        :raises ValueError: If either of the images is not selected, invalid or if they do not match in size.
        """
        primary_fpo = self.primarySelection
        secondary_fpo = self.secondarySelection

        if not primary_fpo or not secondary_fpo:
            raise ValueError("Need to have selected both elements to calculate MSE.")

        primary_fp = primary_fpo.file_path
        secondary_fp = secondary_fpo.file_path

        prim_img = cv2.imread(primary_fp, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        sec_img = cv2.imread(secondary_fp, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

        if prim_img is None or sec_img is None:
            raise ValueError("Both elements need to be valid pictures.")

        if prim_img.shape[:2] != sec_img.shape[:2]:
            raise ValueError("Both elements need to match in height and width!")

        prim_img = cv2.cvtColor(prim_img, cv2.COLOR_BGR2RGB)
        sec_img = cv2.cvtColor(sec_img, cv2.COLOR_BGR2RGB)

        mse = np.mean((prim_img - sec_img) ** 2)

        msg_box = QMessageBox()
        msg_box.setText("MSE between Ref and Comp is: {}".format(mse))
        msg_box.exec()
