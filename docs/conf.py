# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import tegen
sys.path.insert(0, os.path.abspath('../tegen'))


# -- Project information -----------------------------------------------------

project = 'tegen'
copyright = '2021, 7d'
author = '7d'

# The full version, including alpha/beta/rc tags
release = 'v'+tegen.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = 'sphinx_material'

branch = os.getcwd().split("/")[-1]

html_theme_options = {

    # Set the name of the project to appear in the navigation.
    'nav_title': 'tegen '+release,

    # Set the repo location to get a badge with stats
    'repo_url': 'https://github.com/iiiii7d/tegen/',
    'repo_name': 'tegen',

    # Visible levels of the global TOC; -1 means unlimited
    'globaltoc_depth': -1,
    # If False, expand all TOC entries
    'globaltoc_collapse': False,
    # If True, show hidden TOC entries
    'globaltoc_includehidden': False,

    'base_url': 'https://tegen.readthedocs.io/en/{}/'.format(branch)
}
html_sidebars = {
    "**": ["globaltoc.html"]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']