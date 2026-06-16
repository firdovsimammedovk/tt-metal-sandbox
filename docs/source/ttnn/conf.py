# SPDX-FileCopyrightText: © 2023 Tenstorrent USA, Inc.
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import collections
from pathlib import Path

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../common"))
sys.path.append(os.path.abspath("./_ext"))

from docs_versions import get_published_versions

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

# sphinx crashes when trying to introspect real ttnn (C extension issues in main process).
# Mock ttnn so pages are accessible, even with empty stubs.
# TODO: build ttnn from source in separate environment to get real docs.
autodoc_mock_imports = ["ttnn"]

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
_version_urls = [(v, f"{_METAL_BASE}ttnn/{v}/") for v in _all_versions]

html_theme = "sphinx_rtd_theme"
html_logo = "../common/images/tt_logo.svg"
html_favicon = "../common/images/favicon.png"
html_baseurl = f"{_METAL_BASE}ttnn/{_docs_version}/"
html_static_path = ["_static", "../common/_static"]

_docs_site_base = os.environ.get("DOC_SITE_BASE_URL", "https://firdovsimammedovk.github.io/tt-metal-sandbox").rstrip("/")

# Load global theme from tenstorrent-sandbox CDN; local tt_theme.css adds API overrides
html_css_files = [_GLOBAL_CSS]

html_context = {
    "logo_link_url": "https://firdovsimammedovk.github.io/tenstorrent-sandbox/latest/",
    "versions": _version_urls,
    "current_version": _docs_version,
    "docs_site_base": _docs_site_base,
    "docs_project_subpath": "ttnn",
}
version = _docs_version

nbsphinx_execute = "never"


def setup(app):
    app.add_css_file("tt_theme.css")
    app.add_js_file("api_style.js")


breathe_projects = {"ttmetaldoxygen": "../../doxygen_build/xml/"}
breathe_default_project = "ttmetaldoxygen"
