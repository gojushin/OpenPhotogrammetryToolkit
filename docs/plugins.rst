Plugin Development Guide
========================

In OpenPhotogrammetryToolkit, plugins extend the core functionality of the application. They are typically **.py** or **.pyc** files containing a class that inherits from specific base classes provided by the toolkit.

Plugins are placed in the `OpenPhotogrammetryToolkit/Plugins` folder.

File and Class Naming
---------------------

- **.py Files**: Each plugin should be a separate `.py` file located in the designated plugin directory. The file name should reflect the plugin's purpose or functionality.

- **Class Naming**: The class within the `.py` file must have the same name as the file (excluding the `.py` extension). This naming convention is crucial as the toolkit dynamically loads the class based on the file name.

Inheritance and Types of Plugins
--------------------------------

Depending on the plugin's intended functionality, it should inherit from one of the following base classes:

1. **GUI-Based Widgets**:

   - Inherit from :ref:`OpenPhotogrammetryToolkit.PluginWidgetBase<plugin_widget_base>`.
   - These plugins are GUI components like custom viewers, editors, or widgets integrated within the application's interface.

2. **MenuBar Entries**:

   - Inherit from :ref:`OpenPhotogrammetryToolkit.PluginActionBase<plugin_action_base>`.
   - These plugins represent actions or commands accessible from the application's menu bar rather than standalone GUI widgets.

MenuBar Naming Convention
-------------------------

For plugins that should appear under the application's menu bar, naming conventions dictate their placement:

- **Shelf Placement**: Include a "/" in the file name to specify the shelf name followed by the plugin name. The format is "ShelfName/PluginName.py".

- **Example**: Naming your plugin file "Edit/YourPlugin.py" places it under the "Edit" shelf of the menu bar, with the action labeled as "YourPlugin".

Best Practices
--------------

- Ensure the plugin `.py` file is named descriptively, and the class name inside matches the file name.
- Choose the appropriate base class to inherit from based on whether your plugin is a GUI widget or a menu bar action.
- Use the "/" in the file name to specify menu bar shelf placement for menu actions.

Examples
--------------

Widget
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from OpenPhotogrammetryToolkit import PluginWidgetBase

    PLUGIN_NAME = "PLUGIN_NAME"
    PLUGIN_DESCRIPTION = "Plugin Description. "
    PLUGIN_AUTHOR = "Your Name or Company."
    LICENSE = "MIT"
    VERSION = "0.0.1"


    class TestPlugin(PluginWidgetBase):
        def __init__(self, parent, identifier=PLUGIN_NAME):
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


Action
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from OpenPhotogrammetryToolkit import PluginActionBase

    PLUGIN_NAME = "PLUGIN_NAME"
    PLUGIN_DESCRIPTION = "Plugin Description. "
    PLUGIN_AUTHOR = "Your Name or Company."
    LICENSE = "MIT"
    VERSION = "0.0.1"

    class TestPlugin(PluginActionBase):
        def __init__(self, parent, identifier=PLUGIN_NAME):
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

        def on_triggered(self):
            # Called when the action is triggered.
            pass


