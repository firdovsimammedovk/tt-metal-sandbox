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

import subprocess as _sp

def _git_tags() -> list:
    try:
        out = _sp.check_output(
            ["git", "tag", "-l", "v*", "--sort=-version:refname"],
            stderr=_sp.DEVNULL,
        ).decode().strip()
        return [t for t in out.split("\n") if t]
    except Exception:
        return []

_METAL_BASE = "https://firdovsimammedovk.github.io/tt-metal-sandbox/"
_GLOBAL_CSS = "https://firdovsimammedovk.github.io/tenstorrent-sandbox/_static/tt_theme.css"
_all_versions = ["latest"] + [t for t in _git_tags() if t != "latest"]
_version_urls = [(v, f"{_METAL_BASE}tt-metalium/{v}/") for v in _all_versions]

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": True,
    "titles_only": True,
    "navigation_depth": 2,
}
html_logo = "../common/images/tt_logo.svg"
html_favicon = "../common/images/favicon.png"
html_baseurl = f"{_METAL_BASE}tt-metalium/{_docs_version}/"
html_static_path = ["_static", "../common/_static"]

# Load global theme from tenstorrent-sandbox CDN; local tt_theme.css adds API overrides
html_css_files = [_GLOBAL_CSS]

html_context = {
    "logo_link_url": "https://firdovsimammedovk.github.io/tenstorrent-sandbox/latest/",
    "versions": _version_urls,
    "current_version": _docs_version,
}
version = _docs_version


def setup(app):
    app.add_css_file("tt_theme.css")
    app.add_js_file("api_style.js")


breathe_projects = {"ttmetaldoxygen": "../../doxygen_build/xml/"}
breathe_default_project = "ttmetaldoxygen"
