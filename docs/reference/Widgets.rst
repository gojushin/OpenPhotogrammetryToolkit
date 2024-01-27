Open Photogrammetry Toolkit API (Widget) Docs
=======================================================

The module includes a JSON file, "widget_texts.json," which contains all the text used in the application's widgets.
This makes the app's text easily customizable and adaptable to different languages or preferences.

FilePathObject Class
--------------------

.. autoclass:: Widgets.opt_widgets._FilePathObject
   :members:
   :show-inheritance:

    .. attribute:: Widgets.opt_widgets._FilePathObject.file_path
       Returns the File Path of the FPO.

.. _fplw:

FilePathListWidget Class
------------------------

The FilePathListWidget (**fplw**) is a crucial component in the module and serves as the core of the file path interaction system.
It's designed as a starting point and reference for all plugins and extensions within the application,
mainly due to its central role in managing file paths and emitting a variety of signals that reflect user interaction and system changes.
It is set as the `CentralWidget`_ in the applications `MainWindow`_.

This widget is accessible from every Plugin with the `fplw` attribute and contains references to all available files and the current selection.

.. autoclass:: Widgets.opt_widgets.FilePathListWidget
   :members:
   :show-inheritance:

StartupDialog Class
-------------------

Lets the user pick the watched directory.

.. warning::
    Currently only the usage of a single folder is supported. In future version there will be the option to create a "new working directory" where the user can accumlate symlinks to several folders & files.

.. autoclass:: Widgets.opt_widgets.StartupDialog
   :members:
   :show-inheritance:


.. _CentralWidget: https://doc.qt.io/qt-6/qmainwindow.html#qt-main-window-framework#
.. _MainWindow: https://doc.qt.io/qt-6/qmainwindow.html