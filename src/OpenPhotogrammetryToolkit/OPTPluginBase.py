from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Signal


class _PluginRegisteredSignal(QObject):
    """Signal for when a single file has changed."""
    registered = Signal()


class PluginActionBase(QAction):
    def __init__(self, opt_main_window, identifier):
        super().__init__(parent=opt_main_window)
        self.identifier = identifier
        self.parent = opt_main_window
        self.fplw = opt_main_window.centralWidget()
        self.plugin_registered = _PluginRegisteredSignal()

        self._register_plugin()

        self.primarySelectionChanged = None
        self.secondarySelectionChanged = None

    def _register_plugin(self):
        self.fplw.primarySelectionChanged.primarySelectionChanged.connect(self.primary_selection_changed)
        self.fplw.secondarySelectionChanged.secondarySelectionChanged.connect(self.secondary_selection_changed)

        self._setup_action()

        self.plugin_registered.registered.emit()
        self.start()

    def _setup_action(self):
        pass

    def primary_selection_changed(self, selected_file: str):
        pass

    def secondary_selection_changed(self, selected_file: str):
        pass

    def start(self):
        pass


class PluginWidgetBase(QWidget):
    def __init__(self, opt_main_window, identifier):
        super().__init__(parent=opt_main_window)
        self.identifier = identifier
        self.parent = opt_main_window
        self.fplw = opt_main_window.centralWidget()
        self.plugin_registered = _PluginRegisteredSignal()

        self._register_plugin()

        self.primarySelectionChanged = None
        self.secondarySelectionChanged = None

    def _register_plugin(self):
        self.fplw.primarySelectionChanged.primarySelectionChanged.connect(self.primary_selection_changed)
        self.fplw.secondarySelectionChanged.secondarySelectionChanged.connect(self.secondary_selection_changed)

        self._setup_widget()

        self.plugin_registered.registered.emit()
        self.start()

    def _setup_widget(self):
        pass

    def primary_selection_changed(self, selected_file: str):
        pass

    def secondary_selection_changed(self, selected_file: str):
        pass

    def start(self):
        pass

