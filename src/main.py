from Widgets import *
import sys
from PySide6.QtWidgets import QApplication, QMainWindow


class OPTMainWindow:
    def __init__(self):
        self.startup_dialog = StartupDialog()
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("OPT")

        self.startup_dialog.dirSelectedSignal.dirSelected.connect(self.start)
        self.startup_dialog.show()

        self.fplw = FilePathListWidget()
        self.main_window.setCentralWidget(self.fplw)

    def start(self, dir_path):
        self.fplw.set_watched_directory(dir_path)
        self.startup_dialog.close()
        self.startup_dialog.deleteLater()
        self.main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = OPTMainWindow()
    sys.exit(app.exec())
