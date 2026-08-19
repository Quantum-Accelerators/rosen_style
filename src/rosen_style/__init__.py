"""Readable, accessible Matplotlib defaults for research figures."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("rosen_style")
except PackageNotFoundError:  # Running directly from a source checkout.
    __version__ = "0.0.1"

from ._style import COLOR_CYCLE, context, latex_available, settings, use
