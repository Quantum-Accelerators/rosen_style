"""Matplotlib styles for papers and presentations."""

from __future__ import annotations

import shutil
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Literal, cast

import matplotlib as mpl
from cycler import cycler

if TYPE_CHECKING:
    from collections.abc import Generator

StyleName = Literal["paper", "presentation"]
COLOR_CYCLE = (
    "#0072B2",
    "#D55E00",
    "#009E73",
    "#CC79A7",
    "#E69F00",
    "#56B4E9",
    "#F0E442",
)

_COMMON: dict[str, object] = {
    "axes.axisbelow": True,
    "axes.edgecolor": "#333333",
    "axes.facecolor": "white",
    "axes.grid": False,
    "axes.labelcolor": "#222222",
    "axes.prop_cycle": cycler(color=COLOR_CYCLE),
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.titlelocation": "left",
    "figure.facecolor": "white",
    "figure.constrained_layout.use": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman", "DejaVu Serif"],
    "image.cmap": "plasma",
    "legend.frameon": False,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
    "text.color": "#222222",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
}
_PAPER: dict[str, object] = {
    "axes.labelsize": 10,
    "axes.linewidth": 0.8,
    "axes.titlesize": 12,
    "figure.figsize": (6.4, 4.0),
    "font.size": 10,
    "legend.fontsize": 9,
    "lines.linewidth": 1.8,
    "lines.markersize": 5,
    "xtick.labelsize": 9,
    "xtick.minor.visible": True,
    "ytick.labelsize": 9,
    "ytick.minor.visible": True,
}
_PRESENTATION: dict[str, object] = {
    "axes.labelsize": 22,
    "axes.linewidth": 1.4,
    "axes.titlesize": 26,
    "figure.figsize": (12.0, 6.75),
    "font.size": 20,
    "legend.fontsize": 18,
    "lines.linewidth": 3.0,
    "lines.markersize": 9,
    "xtick.labelsize": 18,
    "xtick.minor.visible": False,
    "ytick.labelsize": 18,
    "ytick.minor.visible": False,
}


def latex_available() -> bool:
    """Return whether a LaTeX executable is available on ``PATH``."""
    return shutil.which("latex") is not None


def settings(name: StyleName = "paper", *, latex: bool | None = None) -> mpl.RcParams:
    """Return style rcParams without modifying global Matplotlib state."""
    if name not in ("paper", "presentation"):
        msg = f"Unknown style {name!r}; expected 'paper' or 'presentation'"
        raise ValueError(msg)
    if latex is None:
        latex = latex_available()
    values = {
        **_COMMON,
        **(_PAPER if name == "paper" else _PRESENTATION),
        "text.usetex": latex,
    }
    params = mpl.RcParams()
    # Matplotlib validates every key and value at runtime. Its private RcKeyType
    # is intentionally narrower than ``str``, so a cast is needed at this typed
    # boundary for a dynamically assembled style dictionary.
    params.update(cast("Any", values))
    return params


def use(name: StyleName = "paper", *, latex: bool | None = None) -> None:
    """Apply a style globally."""
    mpl.rcParams.update(settings(name, latex=latex))


@contextmanager
def context(
    name: StyleName = "paper", *, latex: bool | None = None
) -> Generator[None, None, None]:
    """Temporarily apply a style."""
    with mpl.rc_context(settings(name, latex=latex)):
        yield
