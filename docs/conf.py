# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

from django.template.defaultfilters import yesno
from sphinx.ext.autodoc import exclude_members_option

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../BlogProject2'))

project = 'Blog-Project WiWi DOKU'
copyright = '2025, WiWi'
author = 'WiWi'
release = '0.9'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo","sphinx.ext.viewcode","sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store',"django/db/models"]


language = 'de'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


