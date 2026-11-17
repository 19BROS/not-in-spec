# Fixture for the Sphinx reader golden tests; built by ../../build.sh, never by CI.
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "fixturelib"
extensions = ["sphinx.ext.autodoc", "myst_parser"]
style = os.environ.get("FIXTURE_DOCSTRINGS", "plain")
if style == "napoleon":
    extensions.append("sphinx.ext.napoleon")
elif style == "numpydoc":
    extensions.append("numpydoc")
    numpydoc_show_class_members = False
autodoc_member_order = "bysource"
