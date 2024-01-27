.. Open Photogrammetry Toolkit documentation master file, created by
   sphinx-quickstart on Fri Dec 22 20:23:42 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Open Photogrammetry Toolkit's documentation!
=======================================================

Welcome to the API documentation for OpenPhotogrammetryToolkit (OPT). OPT is a Python-based framework that is designed to facilitate the process of capturing and evaluating source material for photogrammetry and Structure from Motion (SFM) tasks.

OPT's philosophy is based on simplicity, extensibility, and a strong commitment to being free and open-source software (FOSS). This guide seeks to help you navigate and effectively utilize the extensive capabilities of OPT.


Key Features
------------

- Qt 6 Based (PySide6): The PySide6 Python bindings are utilized by OPT which is built on the sturdy Qt 6 framework, providing a user-friendly and powerful graphical interface.
- Flexibility and Extensibility: The versatility of OPT is mainly due to its plugin-based functionality. This means that users have the ability to modify or extend the capabilities of the toolkit to suit their individual requirements, as well as integrate additional tools and features as needed. In production environment licensing issues are often a hindrance when it comes to embedding software. OPTs plugin based support enabled developers to narrow the use of copyleft-based software to small plugin snippets.
- FOSS Philosophy:OPT is designed in accordance with the principles of free and open-source software, which means it can be freely modified and distributed. This philosophy guides every design decision, with the goal of nurturing a community of users and developers that is both collaborative and innovative.
- Apache 2.0 License: We are pleased to inform you that OPT operates under the `Apache 2.0 License`_, which not only ensures legal security and transparency for both users and contributors, but also encourages broad acceptance and participation. Although we are firm advocates of open-source software, we acknowledge that the copyleft approach may present certain obstacles in some cases. Hence, we grant you the freedom to apply your preferred licensing terms to any plugins you create, including the option to compile them into bytecode (.pyc files).
- Designed for Photogrammetry & SFM: The primary aim of OPT is to serve as a robust framework for source material acquisition and evaluation specific to the needs of photogrammetry and Structure from Motion (SFM) processes.


Before using OPT, it is important to have a compatible environment with Python (3.9) and PySide6 set up. This will help ensure that you can get started with the tool without any issues.

.. warning::
    In order to ensure all the requirenments are met, please follow our :doc:`/installation`:

Once you have set up the OpenPhotogrammetryToolkit, you can explore its various plugins and customize it for your project requirements.

We welcome you to join our community, contribute to the project, and help shape the future of open-source photogrammetry tools.
Regardless of whether you are an experienced developer or an enthusiast, your journey with OPT begins here!


.. toctree::
   :maxdepth: 2

   installation.rst
   plugins.rst
   reference/OpenPhotogrammetryToolkit.rst
   reference/Widgets.rst


Indices and tables
==================

* :ref:`modindex`

.. _Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0
