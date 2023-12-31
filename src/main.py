from Widgets import *
from OpenPhotogrammetryToolkit.opt_helper_funcs import find_files_by_type, get_class_name, import_module
import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

PLUGIN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "OpenPhotogrammetryToolkit/Plugins")

if PLUGIN_DIR not in sys.path:
    sys.path.append(PLUGIN_DIR)


class OPTMainWindow:
    def __init__(self):
        self.startup_dialog = StartupDialog()
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("OPT")
        self.plugins = []
        self.loaded_plugins = []

        self.fplw = FilePathListWidget()
        self.main_window.setCentralWidget(self.fplw)

        self.startup_dialog.dirSelectedSignal.dirSelected.connect(self.start)
        self.startup_dialog.show()

    def start(self, dir_path):
        self.fplw.set_watched_directory(dir_path)
        self.startup_dialog.close()
        self.startup_dialog.deleteLater()

        self.load_plugins()
        self.instantiate_plugins()

        self.main_window.show()

    def load_plugins(self):
        # Use the find_files_by_type function to get all Python files in the PLUGIN_DIR
        plugin_files = find_files_by_type(PLUGIN_DIR, "py")

        for plugin_file in plugin_files:
            module = import_module(plugin_file)

            if module:
                self.plugins.append(module)

    def instantiate_plugins(self):
        for plugin in self.plugins:
            class_name = get_class_name(plugin)
            try:
                PluginClass = getattr(plugin, class_name)

                self.loaded_plugins.append(PluginClass(parent=self.main_window))
            except Exception as e:
                print("Failed to call {}\n{}".format(class_name, e))  # TODO Log Error later

                continue

            print("Loaded Plugin: {}!".format(class_name))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = OPTMainWindow()
    sys.exit(app.exec())
