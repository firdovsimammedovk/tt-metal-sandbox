# SPDX-FileCopyrightText: © 2023 Tenstorrent USA, Inc.
# SPDX-License-Identifier: Apache-2.0

import os
import sys

sys.path.insert(0, os.path.abspath(".."))
sys.path.append(os.path.abspath("./_ext"))

project = "TT-NN"
copyright = "Tenstorrent"
author = "Tenstorrent"

_docs_version = os.environ.get("DOCS_VERSION", "latest")

extensions = [
    "nbsphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "myst_parser",
]

try:
    import op_documenter
    extensions.append("op_documenter")
except ImportError:
    pass

try:
    import doc_modifier
    extensions.append("doc_modifier")
except ImportError:
    pass

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_use_admonition_for_notes = True
napoleon_use_param = True
napoleon_use_rtype = False

templates_path = ["_templates", "../common/_templates"]
exclude_patterns = [
    "**/CMakeLists.txt",
    "**/tutorials-dev.txt",
    "**/tutorials_venv.sh",
    "**/tutorials_env/**",
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

nbsphinx_execute = "never"


def setup(app):
    app.add_css_file("tt_theme.css")


breathe_projects = {"ttmetaldoxygen": "../../doxygen_build/xml/"}
breathe_default_project = "ttmetaldoxygen"
