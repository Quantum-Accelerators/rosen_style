"""Build the example figures embedded in the README."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import rosen_style

OUTPUT = Path(__file__).parent


def build(name: str) -> None:
    rng = np.random.default_rng(7)
    x = np.linspace(0, 2 * np.pi, 120)
    with rosen_style.context(name, latex=False):
        figure, axes = plt.subplots()
        for phase, label, marker in zip(
            (0, 0.7, 1.4),
            ("control", "method A", "method B"),
            ("o", "s", "^"),
            strict=True,
        ):
            y = np.sin(x + phase) + rng.normal(0, 0.06, x.size)
            axes.plot(x, y, label=label, marker=marker, markevery=15)
        axes.set(xlabel="Time (s)", ylabel="Response (a.u.)")
        axes.legend(ncols=3)
        figure.savefig(OUTPUT / f"{name}.png", dpi=150)
        plt.close(figure)


if __name__ == "__main__":
    build("paper")
    build("presentation")
