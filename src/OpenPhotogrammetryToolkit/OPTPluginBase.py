"""
This module defines base classes for plugin actions and widgets,
facilitating the dynamic interaction and functionality extension through plugins.
It primarily consists of PluginActionBase and PluginWidgetBase classes which can be inherited to create
specific actions and widgets for plugins, and a signal class for plugin registration events.

Classes:
    _PluginRegisteredSignal: An internal signal class for notifying when a plugin is registered.
    PluginActionBase: A base class for creating actions as plugins.
    PluginWidgetBase: A base class for creating widgets as plugins.
"""


from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget


class _PluginRegisteredSignal(QObject):
    """
    An internal signal class used by plugin base classes to emit registration signals.
    This is particularly used to notify the system when a plugin is registered successfully.
    """
    registered = Signal()


class PluginActionBase(QAction):
    """
    A base class for creating plugin actions within the application. It initializes with basic
    setup and connects to the necessary signals for primary and secondary selection changes.

    :param opt_main_window: The main window or parent widget for the plugin.
    :param identifier: A unique identifier for the plugin, used in action text and other identifications.
    """
    def __init__(self, opt_main_window, identifier):
        super().__init__(parent=opt_main_window)

        if "/" not in identifier:
            self.setText(identifier)
        else:
            name = identifier.split("/")[-1]
            self.setText(name)

        self.identifier = identifier
        self.parent = opt_main_window
        self.fplw = opt_main_window.centralWidget()
        self.plugin_registered = _PluginRegisteredSignal()
        self.triggered.connect(self.on_triggered)

        self._register_plugin()

        self.primarySelectionChanged = None
        self.secondarySelectionChanged = None

    def _register_plugin(self):
        """
        Registers the plugin by connecting the primary and secondary selection change signals
        and setting up the action specifics.
        """
        self.fplw.primarySelectionChanged.primarySelectionChanged.connect(self.primary_selection_changed)
        self.fplw.secondarySelectionChanged.secondarySelectionChanged.connect(self.secondary_selection_changed)

        self.plugin_registered.registered.emit()

    @Slot(str)
    def primary_selection_changed(self, selected_file: str):
        """
        Slot for handling changes in the primary selection.

        :param selected_file: The file path of the newly selected primary file.
        :type selected_file: str
        """
        pass

    @Slot(str)
    def secondary_selection_changed(self, selected_file: str):
        """
        Slot for handling changes in the secondary selection.

        :param selected_file: The file path of the newly selected secondary file.
        :type selected_file: str
        """
        pass

    def start(self):
        """
        Called once all plugins are initialized. This is intended to be overridden in subclasses.
        """
        pass

    @Slot()
    def on_triggered(self):
        """
        Slot to be called when the action is triggered. This is intended to be overridden in subclasses
        to provide specific action functionality.
        """
        raise NotImplementedError


class PluginWidgetBase(QWidget):
    """
    A base class for creating plugin widgets within the application. It initializes with basic setup
    and connects to the necessary signals for primary and secondary selection changes.

    :param opt_main_window: The main window or parent widget for the plugin.
    :param identifier: A unique identifier for the plugin, used in various identifications and UI elements.
    """
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
        """
        Registers the plugin by connecting the primary and secondary selection change signals
        and setting up the widget specifics.
        """
        self.fplw.primarySelectionChanged.primarySelectionChanged.connect(self.primary_selection_changed)
        self.fplw.secondarySelectionChanged.secondarySelectionChanged.connect(self.secondary_selection_changed)

        self.plugin_registered.registered.emit()

    @Slot(str)
    def primary_selection_changed(self, selected_file: str):
        """
        Slot for handling changes in the primary selection.

        :param selected_file: The file path of the newly selected primary file.
        :type selected_file: str
        """
        pass

    @Slot(str)
    def secondary_selection_changed(self, selected_file: str):
        """
        Slot for handling changes in the secondary selection.

        :param selected_file: The file path of the newly selected secondary file.
        :type selected_file: str
        """
        pass

    def start(self):
        """
        Called once all plugins are initialized. This is intended to be overridden in subclasses.
        """
        raise NotImplementedError
