"""Readable, accessible Matplotlib defaults for research figures."""

from __future__ import annotations

from importlib.metadata import version

__version__ = version("rosen_style")

from rosen_style._style import COLOR_CYCLE, context, paper_size, settings, use
