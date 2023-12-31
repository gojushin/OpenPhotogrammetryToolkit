from OpenPhotogrammetryToolkit import PluginWidgetBase

PLUGIN_NAME = "Test Plugin. Poggies"
PLUGIN_DESCRIPTION = "POGGIES"
PLUGIN_AUTHOR = ""
VERSION = ""


class TestPlugin(PluginWidgetBase):
    def __init__(self, parent, identifier=PLUGIN_NAME):
        super().__init__(opt_main_window=parent, identifier=identifier)

    def primary_selection_changed(self, selection: str):
        pass

    def secondary_selection_changed(self, selection: str):
        pass

    def start(self):
        pass

