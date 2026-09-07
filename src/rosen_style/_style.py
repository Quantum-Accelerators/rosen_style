"""Matplotlib styles for papers and presentations."""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Literal, cast

import matplotlib as mpl
from cycler import cycler

if TYPE_CHECKING:
    from collections.abc import Generator

StyleName = Literal["paper", "presentation"]
PaperColumns = Literal[1, 2]
_GOLDEN_RATIO = (1 + 5**0.5) / 2
COLOR_CYCLE = ("#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9")

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
    "figure.autolayout": False,
    "figure.dpi": 600,
    "figure.facecolor": "white",
    "figure.constrained_layout.use": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "image.cmap": "plasma",
    "legend.frameon": False,
    "mathtext.fontset": "dejavusans",
    # Keep publication text editable and embed TrueType fonts in PDF/PS.
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "savefig.bbox": None,
    "savefig.dpi": 600,
    # Preserve contrast when figures are placed on a different background.
    "savefig.facecolor": "white",
    "savefig.edgecolor": "white",
    "savefig.transparent": False,
    "text.color": "#222222",
    "text.usetex": False,
    "xtick.color": "#333333",
    "xtick.direction": "out",
    "ytick.color": "#333333",
    "ytick.direction": "out",
}
_PAPER: dict[str, object] = {
    "axes.labelpad": 4,
    "axes.labelsize": 10,
    "axes.linewidth": 0.8,
    "axes.titlesize": 12,
    "figure.figsize": (3.25, 3.25 / _GOLDEN_RATIO),
    "font.size": 10,
    "legend.fontsize": 9,
    "lines.linewidth": 1.4,
    "lines.markersize": 4,
    "xtick.labelsize": 9,
    "xtick.major.pad": 3.5,
    "xtick.major.size": 3.5,
    "xtick.major.width": 0.8,
    "xtick.minor.size": 2,
    "xtick.minor.width": 0.5,
    "xtick.minor.visible": True,
    "ytick.labelsize": 9,
    "ytick.major.pad": 3.5,
    "ytick.major.size": 3.5,
    "ytick.major.width": 0.8,
    "ytick.minor.size": 2,
    "ytick.minor.width": 0.5,
    "ytick.minor.visible": True,
}
_PRESENTATION: dict[str, object] = {
    "axes.labelpad": 8,
    "axes.labelsize": 22,
    "axes.linewidth": 1.4,
    "axes.titlesize": 26,
    "figure.figsize": (12.0, 6.75),
    "font.size": 20,
    "legend.fontsize": 18,
    "lines.linewidth": 3.0,
    "lines.markersize": 9,
    "xtick.labelsize": 18,
    "xtick.major.pad": 6,
    "xtick.major.size": 7,
    "xtick.major.width": 1.4,
    "xtick.minor.visible": False,
    "ytick.labelsize": 18,
    "ytick.major.pad": 6,
    "ytick.major.size": 7,
    "ytick.major.width": 1.4,
    "ytick.minor.visible": False,
}


def paper_size(
    columns: PaperColumns = 1, *, square: bool = False
) -> tuple[float, float]:
    """Return a journal figure size for one or two columns."""
    if columns not in (1, 2):
        msg = f"Unknown paper column count {columns!r}; expected 1 or 2"
        raise ValueError(msg)
    width = 3.25 if columns == 1 else 7.0
    return width, width if square else width / _GOLDEN_RATIO


def settings(
    name: StyleName = "paper", *, columns: PaperColumns = 1, square: bool = False
) -> mpl.RcParams:
    """Return style rcParams without modifying global Matplotlib state."""
    if name not in ("paper", "presentation"):
        msg = f"Unknown style {name!r}; expected 'paper' or 'presentation'"
        raise ValueError(msg)
    values = {**_COMMON, **(_PAPER if name == "paper" else _PRESENTATION)}
    if name == "paper":
        values["figure.figsize"] = paper_size(columns, square=square)
    elif square:
        width = cast("tuple[float, float]", values["figure.figsize"])[0]
        values["figure.figsize"] = (width, width)
    params = mpl.RcParams()
    # Matplotlib validates every key and value at runtime. Its private RcKeyType
    # is intentionally narrower than ``str``, so a cast is needed at this typed
    # boundary for a dynamically assembled style dictionary.
    params.update(cast("Any", values))
    return params


def use(
    name: StyleName = "paper", *, columns: PaperColumns = 1, square: bool = False
) -> None:
    """Apply a style globally."""
    mpl.rcParams.update(settings(name, columns=columns, square=square))


@contextmanager
def context(
    name: StyleName = "paper", *, columns: PaperColumns = 1, square: bool = False
) -> Generator[None, None, None]:
    """Temporarily apply a style."""
    with mpl.rc_context(settings(name, columns=columns, square=square)):
        yield

