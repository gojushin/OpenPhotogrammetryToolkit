Installation Instructions
=========================

Python Version
---------------------------

I recommend using this software with **Python 3.9** or higher for optimal performance and compatibility.
While it may still function on older versions, please note that I do not officially support or test it on anything below 3.9.

Upgrade pip
---------------

It is advisable to upgrade pip to its latest version before installing any packages.
Below are the steps to upgrade pip on different operating systems:

**Windows:**

.. code-block:: batch

   python -m pip install --upgrade pip


**macOS and Linux:**

.. code-block:: bash

    python3 -m pip install --upgrade pip


Toolkit Installation
----------------------

The installation is divided into mandatory and non-mandatory components.

Mandatory
^^^^^^^^^^
The mandatory component is PySide6, which is essential for the software to function.

**Windows:**

.. code-block:: batch

    pip install PySide6


**macOS and Linux:**

.. code-block:: bash

    pip3 install PySide6


Non-Mandatory
^^^^^^^^^^^^^^
These are used by the included plugins. They are optional but recommended for full functionality.

**Windows:**

.. code-block:: batch

    pip install opencv-python
    pip install numpy


**macOS and Linux:**

.. code-block:: bash

    pip3 install opencv-python
    pip3 install numpy


Testing Framework
^^^^^^^^^^^^^^^^^^

The testing framework is built using pytest, pytest-qt, and qtbot. *However, these are not required to run the application.*
To install these testing libraries, use the following commands:

**Windows:**

.. code-block:: batch

    pip install pytest
    pip install pytest-qt

**macOS and Linux:**

.. code-block:: bash

    pip3 install pytest
    pip3 install pytest-qt

