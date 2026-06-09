# SPDX-FileCopyrightText: © 2023 Tenstorrent USA, Inc.
# SPDX-License-Identifier: Apache-2.0

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "TT-Metalium"
copyright = "Tenstorrent"
author = "Tenstorrent"

_docs_version = os.environ.get("DOCS_VERSION", "latest")

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "myst_parser",
]

try:
    import breathe
    extensions.append("breathe")
except ImportError:
    pass

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_notes = True
napoleon_use_param = True
napoleon_use_rtype = True

templates_path = ["_templates", "../common/_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_logo = "../common/images/tt_logo.svg"
html_favicon = "../common/images/favicon.png"
html_baseurl = f"/tt-metal/{_docs_version}/tt-metalium"
html_static_path = ["_static", "../common/_static"]

html_context = {
    "logo_link_url": "https://firdovsimammedovk.github.io/tenstorrent-sandbox/",
    "versions": None,
}


def setup(app):
    app.add_css_file("tt_theme.css")
    app.add_js_file("api_style.js")


breathe_projects = {"ttmetaldoxygen": "../../doxygen_build/xml/"}
breathe_default_project = "ttmetaldoxygen"
