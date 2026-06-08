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

# Fall back to mocking ttnn if the C extension is not available
import subprocess as _sp, os as _os
_env = {k: v for k, v in _os.environ.items() if k != "PYTHONPATH"}
if _sp.run([sys.executable, "-c", "import ttnn._ttnn"], capture_output=True, env=_env).returncode != 0:
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


breathe_projects = {"ttmetaldoxygen": "../../doxygen_build/xml/"}
breathe_default_project = "ttmetaldoxygen"
