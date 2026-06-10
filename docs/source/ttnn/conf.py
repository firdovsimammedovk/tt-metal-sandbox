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

try:
    import op_documenter
    extensions.append("op_documenter")
except Exception:
    pass

try:
    import doc_modifier
    extensions.append("doc_modifier")
except Exception:
    pass

# Mock ttnn if ttnn.experimental (referenced in api.rst) is not importable.
# autosummary raises a fatal ExtensionError if it can't import any listed module.
import subprocess as _sp, os as _os
_env = {k: v for k, v in _os.environ.items() if k != "PYTHONPATH"}
_check = _sp.run(
    [sys.executable, "-c", "import ttnn.experimental; print('ok')"],
    capture_output=True, text=True, env=_env,
)
if _check.returncode != 0 or "ok" not in _check.stdout:
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

html_theme = "sphinx_rtd_theme"
html_logo = "../common/images/tt_logo.svg"
html_favicon = "../common/images/favicon.png"
html_baseurl = f"/tt-metal-sandbox/{_docs_version}/ttnn"
html_static_path = ["_static", "../common/_static"]

_docs_site_base = os.environ.get("DOC_SITE_BASE_URL", "https://firdovsimammedovk.github.io/tt-metal-sandbox").rstrip("/")

html_context = {
    "logo_link_url": "https://firdovsimammedovk.github.io/tenstorrent-sandbox/",
    "versions": get_published_versions(Path(__file__)),
    "current_version": _docs_version,
    "docs_site_base": _docs_site_base,
    "docs_project_subpath": "ttnn",
}

nbsphinx_execute = "never"


def setup(app):
    app.add_css_file("tt_theme.css")
    app.add_js_file("api_style.js")


breathe_projects = {"ttmetaldoxygen": "../../doxygen_build/xml/"}
breathe_default_project = "ttmetaldoxygen"
