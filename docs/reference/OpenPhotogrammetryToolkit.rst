Open Photogrammetry Toolkit API Docs
=======================================================

.. _plugin_widget_base:

Plugin Widget Base
^^^^^^^^^^^^^^^^^^

The following class is the basis for Widget-Based Plugins. (See also: :doc:`/plugins`)

.. autoclass:: OpenPhotogrammetryToolkit.OPTPluginBase.PluginWidgetBase
   :members:
   :show-inheritance:

You can access the :ref:`FilePathListWidget <fplw>` from your Plugin at any time to get the current selection:

.. attribute:: OpenPhotogrammetryToolkit.OPTPluginBase.PluginActionWidget.fplw

.. _plugin_action_base:

Plugin Action Base
^^^^^^^^^^^^^^^^^^

The following class is the basis for Action-Based Plugins. (See also: :doc:`/plugins`)

.. autoclass:: OpenPhotogrammetryToolkit.OPTPluginBase.PluginActionBase
   :members:
   :show-inheritance:

You can access the :ref:`FilePathListWidget <fplw>` from your Plugin at any time to get the current selection:

.. attribute:: OpenPhotogrammetryToolkit.OPTPluginBase.PluginActionBase.fplw

OPT Utilities
^^^^^^^^^^^^^^^^^^

Utilities offer several helper functions required for core functionality.

.. automodule:: OpenPhotogrammetryToolkit.opt_helper_funcs
   :members:
   :show-inheritance:
