import os.path
import sys

import pytest

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal
import main

from OpenPhotogrammetryToolkit import PluginActionBase, PluginWidgetBase
from Widgets import FilePathListWidget
from opt_widgets import _FilePathObject

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

WIDGET_PLUGIN = """
from OpenPhotogrammetryToolkit import PluginWidgetBase

class WIDGET_PLUGIN(PluginWidgetBase):
    def __init__(self, parent, identifier="TestWidget"):
        super().__init__(opt_main_window=parent, identifier=identifier)
        self.test_prim_succ = False
        self.test_sec_succ = False
        self.test_start = False
        self.stuff_executed = False

    def primary_selection_changed(self, selection: str):
        self.test_prim_succ = True

    def secondary_selection_changed(self, selection: str):
        self.test_sec_succ = True

    def start(self):
        self.test_start = True
        
    def exec_stuff(self):
        self.stuff_executed = True
"""


class MockCentralWidget:
    def __init__(self):
        primarySelectionChanged = Signal()
        secondarySelectionChanged = Signal()


class MockMainWindow:
    """
    Main window class for the OpenPhotogrammetryToolkit (OPT). Handles the initialization and
    dynamic loading of plugins, and sets up the primary interface and interactions.
    """
    def __init__(self):
        self.main_window = QMainWindow()

        self.fplw = FilePathListWidget()
        self.fplw.set_watched_directory(IMAGE_DIR)
        self.main_window.setCentralWidget(self.fplw)


class TestWidgetPlugin(PluginWidgetBase):
    def __init__(self, parent, identifier="TestWidget"):
        super().__init__(opt_main_window=parent, identifier=identifier)
        self.test_prim_succ = False
        self.test_sec_succ = False
        self.test_start = False

    def primary_selection_changed(self, selection: str):
        self.test_prim_succ = True

    def secondary_selection_changed(self, selection: str):
        self.test_sec_succ = True

    def start(self):
        self.test_start = True


class TestActionPlugin(PluginActionBase):
    def __init__(self, parent, identifier="TestAction"):
        super().__init__(opt_main_window=parent, identifier=identifier)
        self.test_prim_succ = False
        self.test_sec_succ = False
        self.test_start = False
        self.test_trigger = False

    def primary_selection_changed(self, selection: str):
        self.test_prim_succ = True

    def secondary_selection_changed(self, selection: str):
        self.test_sec_succ = True

    def start(self):
        self.test_start = True

    def on_triggered(self):
        self.test_trigger = True


class TestActionPluginNoTrigger(PluginActionBase):
    def __init__(self, parent, identifier="TestAction"):
        super().__init__(opt_main_window=parent, identifier=identifier)
        # Add any initialization code here. Mind that plugin-dependencies might not be available yet.

        # Signals: plugin_registered

    def primary_selection_changed(self, selection: str):
        # Called when the primary selection changes.
        pass

    def secondary_selection_changed(self, selection: str):
        # Called when the primary selection changes.
        pass

    def start(self):
        # Start is called, once all plugins are loaded and the application is constructed for the first time.
        pass


@pytest.fixture(scope="function")
def app_main(qtbot, qapp, tmp_path):
    # Overwrite the Plugin Directory
    main.PLUGIN_DIR = tmp_path

    # Construct our own mock plugin
    dummy_plugin = tmp_path / "WIDGET_PLUGIN.py"
    dummy_plugin.write_text(WIDGET_PLUGIN)

    dummy_plugin2 = tmp_path / "WIDGET_PLUGIN2.py"
    dummy_plugin2.write_text(WIDGET_PLUGIN.replace("WIDGET_PLUGIN", "WIDGET_PLUGIN2"))

    # Ensure OPT is in sys.path.
    prj_dir = os.path.dirname(os.path.dirname(__file__))
    opt_dir = os.path.join(prj_dir, "src/OpenPhotogrammetryToolkit")

    if opt_dir not in sys.path:
        sys.path.append(opt_dir)

    # Start the Application
    mainWindow = main.OPTMainWindow()

    # This signal closes the startup dialog. And properly intializes the app.
    # If we don't wait for this we get a WindowsError for improper GUI Cleanup.
    with qtbot.waitSignal(mainWindow.startup_dialog.dirSelectedSignal.dirSelected, timeout=100) as blocker:
        mainWindow.startup_dialog.dirSelectedSignal.dirSelected.emit(IMAGE_DIR)

    assert blocker.signal_triggered

    yield mainWindow


@pytest.fixture
def mock_main_window():
    m = MockMainWindow()
    return m.main_window


# PluginActionBase tests
def test_plugin_action_base_initialization(qapp, mock_main_window):
    """
    Test the initialization of a PluginActionBase instance.

    Verifies that the PluginActionBase instance is properly initialized with
    the specified identifier.
    """
    identifier = "test_action"
    action_plugin = TestActionPlugin(parent=mock_main_window, identifier=identifier)
    assert action_plugin.identifier == identifier


def test_plugin_action_base_trigger(qapp, mock_main_window):
    """
    Test the triggering mechanism of a PluginActionBase instance.

    Ensures that the on_triggered method raises a NotImplementedError,
    verifying that it's not implemented by default and should be overridden.
    """
    identifier = "test_action"
    action = TestActionPluginNoTrigger(mock_main_window, identifier)
    with pytest.raises(NotImplementedError):
        action.on_triggered()  # Assuming the default on_triggered isn't implemented


def test_plugin_action_base_primary_selection_changes(qapp, qtbot, mock_main_window):
    """
    Test the primary selection change handling in PluginActionBase.

    Ensures that the primary_selection_changed method is correctly called and
    alters the state of the plugin to reflect the primary selection success.
    """
    action = TestActionPlugin(mock_main_window, "test_action")
    action.fplw.set_primary_selection(os.path.join(IMAGE_DIR, "test_img1.jpg"))
    assert action.test_prim_succ
    assert not action.test_sec_succ
    assert not action.test_start
    assert not action.test_trigger


def test_plugin_action_base_secondary_selection_changes(qapp, qtbot, mock_main_window):
    """
    Test the secondary selection change handling in PluginActionBase.

    Ensures that the secondary_selection_changed method is correctly called and
    alters the state of the plugin to reflect the secondary selection success.
    """
    action = TestActionPlugin(mock_main_window, "test_action")
    action.fplw.set_secondary_selection(os.path.join(IMAGE_DIR, "test_img1.jpg"))
    assert not action.test_prim_succ
    assert action.test_sec_succ
    assert not action.test_start
    assert not action.test_trigger


def test_plugin_action_base_start(qapp, qtbot, mock_main_window):
    """
    Test the start method of PluginActionBase.

    Verifies that the start method correctly alters the state of the plugin to reflect that
    it has started.
    """
    action = TestActionPlugin(mock_main_window, "test_action")
    action.start()

    assert not action.test_prim_succ
    assert not action.test_sec_succ
    assert action.test_start
    assert not action.test_trigger


def test_plugin_action_base_triggered(qapp, qtbot, mock_main_window):
    """
    Test the triggered state of PluginActionBase.

    Ensures that triggering the plugin correctly alters its state to reflect
    that it has been triggered.
    """
    action = TestActionPlugin(mock_main_window, "test_action")
    action.trigger()

    assert not action.test_prim_succ
    assert not action.test_sec_succ
    assert not action.test_start
    assert action.test_trigger


def test_plugin_widget_base_initialization(qapp, mock_main_window):
    """
    Test the initialization of a PluginWidgetBase instance.

    Verifies that the PluginWidgetBase instance is properly initialized with
    the specified identifier.
    """
    identifier = "test_widget"
    widget = PluginWidgetBase(mock_main_window, identifier)
    assert widget.identifier == identifier


def test_selections(qapp, mock_main_window):
    """
    Test primary and secondary selections for both PluginWidgetBase and PluginActionBase.

    This test ensures that the primary and secondary selections are initially None and then correctly
    updated to reflect changes in the selections. It verifies this behavior for both widget and action
    plugin types.
    """
    identifier = "test_widget"
    identifier2 = "test_widget2"
    guiwidget = PluginWidgetBase(mock_main_window, identifier)
    actionwidget = PluginActionBase(mock_main_window, identifier2)

    assert guiwidget.primarySelection is None
    assert actionwidget.primarySelection is None
    assert guiwidget.secondarySelection is None
    assert actionwidget.secondarySelection is None

    fpo1 = _FilePathObject(os.path.join(IMAGE_DIR, "test_img1.jpg"), mock_main_window.centralWidget())
    fpo2 = _FilePathObject(os.path.join(IMAGE_DIR, "test_img2.jpg"), mock_main_window.centralWidget())

    mock_main_window.centralWidget()._primary_sel = fpo1
    mock_main_window.centralWidget()._secondary_sel = fpo2

    assert guiwidget.primarySelection is fpo1
    assert actionwidget.primarySelection is fpo1
    assert guiwidget.secondarySelection is fpo2
    assert actionwidget.secondarySelection is fpo2


def test_get_all(qapp, mock_main_window):
    """
    Test the get_all_files method for both PluginWidgetBase and PluginActionBase.

    This test checks whether the get_all_files method correctly returns all file paths in the main window's
    central widget. It also verifies the functionality of excluding specific files from the returned list.
    """
    guiwidget = PluginWidgetBase(mock_main_window, "test_widget")
    actionwidget = PluginActionBase(mock_main_window, "test_widget2")

    fpo1 = _FilePathObject(os.path.join(IMAGE_DIR, "test_img1.jpg"), mock_main_window.centralWidget())
    fpo2 = _FilePathObject(os.path.join(IMAGE_DIR, "test_img2.jpg"), mock_main_window.centralWidget())
    fpo3 = _FilePathObject(os.path.join(IMAGE_DIR, "test_img3.jpg"), mock_main_window.centralWidget())
    fpo4 = _FilePathObject(os.path.join(IMAGE_DIR, "test_img4.jpg"), mock_main_window.centralWidget())

    mock_file_paths = {
        fpo1.label: fpo1,
        fpo2.label: fpo2,
        fpo3.label: fpo3,
        fpo4.label: fpo4
    }

    mock_main_window.centralWidget().curr_file_paths = mock_file_paths

    assert guiwidget.get_all_files() == list(mock_file_paths.values())
    assert actionwidget.get_all_files() == list(mock_file_paths.values())

    mock_file_paths.pop(fpo3.label)

    assert guiwidget.get_all_files([fpo3]) == list(mock_file_paths.values())
    assert actionwidget.get_all_files([fpo3]) == list(mock_file_paths.values())


def test_plugin_widget_primary_selection_changes(qapp, mock_main_window):
    """
    Test primary selection changes in PluginWidgetBase.

    Ensures that changing the primary selection updates the state of the widget
    to reflect the change.
    """
    widget = TestWidgetPlugin(mock_main_window, "test_widget")
    widget.fplw.set_primary_selection(os.path.join(IMAGE_DIR, "test_img1.jpg"))

    assert widget.test_prim_succ
    assert not widget.test_sec_succ
    assert not widget.test_start


def test_plugin_widget_secondary_selection_changes(qapp, mock_main_window):
    """
    Test secondary selection changes in PluginWidgetBase.

    Ensures that changing the secondary selection updates the state of the widget
    to reflect the change.
    """
    widget = TestWidgetPlugin(mock_main_window, "test_widget")
    widget.fplw.set_secondary_selection(os.path.join(IMAGE_DIR, "test_img2.jpg"))

    assert not widget.test_prim_succ
    assert widget.test_sec_succ
    assert not widget.test_start


def test_plugin_widget_start(qapp, mock_main_window):
    """
    Test the start method of PluginWidgetBase.

    Verifies that the start method correctly alters the state of the widget to reflect that
    it has started.
    """
    widget = TestWidgetPlugin(mock_main_window, "test_widget")
    widget.start()

    assert not widget.test_prim_succ
    assert not widget.test_sec_succ
    assert widget.test_start


def test_plugin_widget_start_and_primary_selection_changes(qapp, mock_main_window):
    """
    Test the start and primary selection changes in PluginWidgetBase together.

    Ensures that starting the widget and changing the primary selection updates the state
    of the widget to reflect both actions.
    """
    widget = TestWidgetPlugin(mock_main_window, "test_widget")
    widget.fplw.set_primary_selection(os.path.join(IMAGE_DIR, "test_img1.jpg"))
    widget.start()

    assert widget.test_prim_succ
    assert not widget.test_sec_succ
    assert widget.test_start


def test_main_loads_and_start_plugin(app_main):
    """
    Test the loading and starting of plugins in the main application.

    Verifies that exactly one plugin (the mock plugin) is loaded and its start
    function is called.
    """
    # EXACTLY One Plugin (Our Mock Plugin) should be loaded
    loaded_one_plugin = len(app_main.loaded_plugins) == 2

    # The Plugins "start()" function should have been called
    plugin_was_started = app_main.loaded_plugins[0].test_start

    # We need to clean up all loaded widgets and the main window so that pytest-qt can properly shut down
    for plug in app_main.loaded_plugins:
        plug.close()

    app_main.main_window.close()

    assert loaded_one_plugin
    assert plugin_was_started


def test_plugin_class_var(app_main):
    """
    Test the visibility of plugins within each other in the main application.

    This test checks that each plugin within the main application does not have visibility of itself
    but can see other loaded plugins. It ensures proper isolation and interaction among loaded plugins.
    """
    plug1 = app_main.loaded_plugins[0]
    plug2 = app_main.loaded_plugins[1]

    # Every Plugin should not be able to see itself.
    assert plug1 not in plug1.plugins
    assert plug2 not in plug2.plugins

    # Every Plugin should instead only see the other one (since we only have two).
    assert plug1.plugins[0] == plug2
    assert plug2.plugins[0] == plug1

    app_main.main_window.close()


def test_plugin_interop(app_main):
    """
    Test the interoperability between loaded plugins in the main application.

    This test ensures that an action performed by one plugin (here, executing 'exec_stuff' method)
    has the expected effect on another plugin (here, setting 'stuff_executed' to True). It verifies
    the ability of plugins to interact with each other correctly within the main application environment.
    """
    plug1 = app_main.loaded_plugins[0]
    plug2 = app_main.loaded_plugins[1]

    plug1.plugins[0].exec_stuff()
    assert plug2.stuff_executed

    app_main.main_window.close()
