# SPDX-FileCopyrightText: © 2023 Tenstorrent USA, Inc.
# SPDX-License-Identifier: Apache-2.0

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "TT-NN"
copyright = "Tenstorrent"
author = "Tenstorrent"

_docs_version = os.environ.get("DOCS_VERSION", "latest")

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "myst_parser",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_admonition_for_notes = True

templates_path = ["_templates", "../common/_templates"]
exclude_patterns = [
    "**/CMakeLists.txt",
    "**/*.ipynb",
    "ttnn/api.rst",
    "ttnn/tutorials.rst",
    "ttnn/tutorials/**",
]

html_theme = "sphinx_rtd_theme"
html_logo = "../common/images/tt_logo.svg"
html_favicon = "../common/images/favicon.png"
html_baseurl = f"/tt-metal/{_docs_version}/ttnn"
html_static_path = ["_static", "../common/_static"]

html_context = {
    "logo_link_url": "https://firdovsimammedovk.github.io/tenstorrent-sandbox/",
    "versions": None,
}


def setup(app):
    app.add_css_file("tt_theme.css")
