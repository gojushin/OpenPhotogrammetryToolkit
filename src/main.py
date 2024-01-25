import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QDockWidget

from OpenPhotogrammetryToolkit.opt_helper_funcs import find_files_by_type, get_class_name, import_module
from Widgets import *

PLUGIN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "OpenPhotogrammetryToolkit/Plugins")

if PLUGIN_DIR not in sys.path:
    sys.path.append(PLUGIN_DIR)


class OPTMainWindow:
    """
    Main window class for the OpenPhotogrammetryToolkit (OPT). Handles the initialization and
    dynamic loading of plugins, and sets up the primary interface and interactions.
    """
    def __init__(self):
        self.startup_dialog = StartupDialog()
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("OPT")

        self.plugin_files = []
        self.loaded_plugins = []

        self.fplw = FilePathListWidget()
        self.main_window.setCentralWidget(self.fplw)

        self.startup_dialog.dirSelectedSignal.dirSelected.connect(self.start)
        self.startup_dialog.show()

    def start(self, dir_path):
        """
        Begins the main application process after a directory is selected in the startup dialog.
        Sets up the file path list widget, loads and starts plugins, and displays the main window.

        :param dir_path: Path of the directory selected by the user.
        :type dir_path: str
        """
        self.fplw.set_watched_directory(dir_path)
        self.startup_dialog.close()
        self.startup_dialog.deleteLater()

        self.load_plugins()
        self.instantiate_plugins()
        self.add_plugins_to_view()
        self.start_plugins()

        self.main_window.show()

    def load_plugins(self):
        """
        Searches for and loads all Python plugin files found in the specified plugin directory.
        """
        # Use the find_files_by_type function to get all Python files in the PLUGIN_DIR
        plugin_files = find_files_by_type(PLUGIN_DIR, "py")

        for plugin_file in plugin_files:
            module = import_module(plugin_file)

            if module:
                self.plugin_files.append(module)

    def instantiate_plugins(self):
        """
        Instantiates each plugin class found in the plugin files, handling any errors and
        keeping track of successfully loaded plugins.
        """
        for plugin in self.plugin_files:
            class_name = get_class_name(plugin)
            try:
                PluginClass = getattr(plugin, class_name)
                self.loaded_plugins.append(PluginClass(parent=self.main_window))
            except Exception as e:
                print("Failed to call {}\n{}".format(class_name, e))  # TODO Log Error later

                continue

            print("Loaded Plugin: {}!".format(class_name))

    def add_plugins_to_view(self):
        """
        Adds each loaded plugin to the main window's view. This method handles different types of plugins,
        including those that are QWidget-based or QAction-based.
        """
        for plugin in self.loaded_plugins:
            if isinstance(plugin, QWidget):
                dw = QDockWidget(plugin.identifier, self.main_window)
                dw.setWidget(plugin)
                self.main_window.addDockWidget(Qt.BottomDockWidgetArea, dw)
            if isinstance(plugin, QAction):
                plugin.setParent(self.main_window)
                self.add_action(plugin)

    def add_action(self, action: QAction):
        """
        Adds an action to the main window's menu bar. It supports nesting menus for actions with identifiers
        containing '/' to denote menu hierarchy.

        :param action: The action to add to the menu bar.
        :type action: QAction
        """
        parts = action.identifier.split("/")

        if len(parts) == 1:
            # If there is no '/', it's a single action, add directly to the menu bar
            self.main_window.menuBar().addAction(action)

        else:
            # Same as before, create nested menus for multiple parts
            current_menu = self.main_window.menuBar()
            for part in parts[:-1]:  # Iterate through all parts except the last one
                # Find if the menu already exists
                found_menu = None
                for menu_action in current_menu.actions():  # Iterate through existing menus
                    menu = menu_action.menu()
                    if menu and menu.title() == part:
                        found_menu = menu
                        break

                # If the menu does not exist, create it and set it as the current menu
                if found_menu is None:
                    found_menu = current_menu.addMenu(part)

                current_menu = found_menu

            # The last part is the actual action name, create and add it to the current menu
            # Create a new QAction for the last part since 'action' is the parameter
            current_menu.addAction(action)  # Add the final action to the deepest menu

    def start_plugins(self):
        """
        Calls the start method of each loaded plugin to perform any necessary initialization or setup.
        """
        for plugin in self.loaded_plugins:
            plugin.plugins = [p for p in self.loaded_plugins if p is not plugin]
            plugin.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = OPTMainWindow()
    sys.exit(app.exec())
