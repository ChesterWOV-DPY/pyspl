# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import pathlib
import sys
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PySPL'
copyright = '2023, ChesterWOV'
author = 'ChesterWOV'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.autodoc',
    'sphinx_design',
    'sphinx_tabs.tabs',
    'sphinx_copybutton',
]

sphinx_tabs_disable_tab_closing = True

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_js_files = ['custom.js']
html_theme_options = {
    'show_toc_level': 4,
    'home_page_in_toc': True,
    'toc_title': 'On this page'
}
