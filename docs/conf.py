# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

PRJ_DIR = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(PRJ_DIR, "src")
OPT_DIR = os.path.join(SRC_DIR, "OpenPhotogrammetryToolkit.rst")
WGT_DIR = os.path.join(SRC_DIR, "Widgets")

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

    print("src dir=" + SRC_DIR)


project = 'Open Photogrammetry Toolkit'
copyright = '2023, Nico Breycha'
author = 'Nico Breycha'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo", "sphinx.ext.autodoc"]
source_suffix = ".rst"
master_doc = "index"
html_logo = '_static/OPT_LOGO_small.png'
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

autosummary_generate = True

html_theme = 'furo'

