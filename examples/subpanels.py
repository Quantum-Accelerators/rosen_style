"""Build a paper figure with four subpanels.

Run from the repository root with:
    python examples/subpanels.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import rosen_style


def build(output: Path = Path(__file__).parent) -> None:
    """Save a 7-inch-wide figure without changing its physical export size."""
    x = np.linspace(0, 2 * np.pi, 120)
    # columns sets the journal width; ncols sets the number of subplot columns.
    with rosen_style.context("paper", columns=2):
        figure, axes = plt.subplots(2, 2, sharex=True, sharey=True)
        for ax, phase, panel in zip(
            axes.flat, (0.0, 0.4, 0.8, 1.2), ("(a)", "(b)", "(c)", "(d)"), strict=True
        ):
            ax.plot(x, np.sin(x + phase), label="Control", marker="o", markevery=20)
            ax.plot(
                x,
                0.7 * np.sin(x + phase),
                label="Treatment",
                linestyle="--",
                marker="s",
                markevery=20,
            )
            ax.set(xlabel="Time (s)", ylabel="Response (a.u.)", ylim=(-1.2, 1.8))
            ax.label_outer()
            ax.text(0.03, 0.95, panel, transform=ax.transAxes, va="top", weight="bold")
        axes[0, 0].legend(loc="upper right")
        # Constrained layout is enabled by the style. Avoid bbox_inches="tight"
        # when the saved figure must retain the exact journal column width.
        figure.savefig(output / "paper_subpanels.png")
        figure.savefig(output / "paper_subpanels.pdf")
        plt.close(figure)


if __name__ == "__main__":
    build()
