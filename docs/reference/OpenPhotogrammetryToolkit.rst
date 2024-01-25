Open Photogrammetry Toolkit API Docs
=======================================================

.. _plugin_widget_base:

Plugin Widget Base
^^^^^^^^^^^^^^^^^^

The following class is the basis for Widget-Based Plugins. (See also: :doc:`/plugins`)

.. autoclass:: OpenPhotogrammetryToolkit.OPTPluginBase.PluginWidgetBase
   :members:
   :show-inheritance:

   .. attribute:: identifier
      :type: str

      A unique identifier for the plugin.

   .. attribute:: parent
      :type: QWidget

      The main window of the plugin.


   .. attribute:: plugins
      :type: list

      Stores a list of all initialized plugins.

   .. attribute:: fplw
       :type: FilePathListWidget

       You can use the this attribute to access all the relevant data of the application`.

.. _plugin_action_base:

Plugin Action Base
^^^^^^^^^^^^^^^^^^

The following class is the basis for Action-Based Plugins. (See also: :doc:`/plugins`)

.. autoclass:: OpenPhotogrammetryToolkit.OPTPluginBase.PluginActionBase
   :members:
   :show-inheritance:

   .. attribute:: identifier
      :type: str

      A unique identifier for the plugin.

   .. attribute:: parent
      :type: QWidget

      The main window of the plugin.


   .. attribute:: plugins
      :type: list

      Stores a list of all initialized plugins.

   .. attribute:: fplw
       :type: FilePathListWidget

       You can use the this attribute to access all the relevant data of the application`.

OPT Utilities
^^^^^^^^^^^^^^^^^^

Utilities offer several helper functions required for core functionality.

.. automodule:: OpenPhotogrammetryToolkit.opt_helper_funcs
   :members:
   :show-inheritance:
