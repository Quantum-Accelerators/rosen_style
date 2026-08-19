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
    with rosen_style.context(name):
        # Line plot with redundant color, marker, and label encodings.
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

        # Scatter plot with uncertainty encoded by point size.
        figure, axes = plt.subplots()
        for offset, label, marker in zip(
            (0.0, 0.7, 1.4),
            ("control", "method A", "method B"),
            ("o", "s", "^"),
            strict=True,
        ):
            values = rng.normal(offset, 0.45, 35)
            response = 0.65 * values + rng.normal(0, 0.35, values.size)
            axes.scatter(values, response, label=label, marker=marker, alpha=0.8)
        axes.set(xlabel="Predictor (a.u.)", ylabel="Response (a.u.)")
        axes.legend()
        figure.savefig(OUTPUT / f"{name}_scatter.png", dpi=150)
        plt.close(figure)

        # Bar plot using a restrained subset of the categorical palette.
        figure, axes = plt.subplots()
        categories = ("Baseline", "Method A", "Method B", "Method C")
        values = (0.42, 0.68, 0.81, 0.74)
        axes.bar(categories, values)
        axes.set(ylabel="Accuracy")
        axes.set_ylim(0, 1)
        axes.minorticks_off()
        figure.savefig(OUTPUT / f"{name}_bar.png", dpi=150)
        plt.close(figure)

        # Heatmap using the default perceptually uniform sequential colormap.
        figure, axes = plt.subplots()
        xx, yy = np.meshgrid(np.linspace(-2, 2, 100), np.linspace(-2, 2, 80))
        field = np.exp(-(xx**2 + yy**2)) + 0.5 * np.exp(
            -((xx - 1.1) ** 2 + (yy + 0.8) ** 2) / 0.25
        )
        image = axes.imshow(field, extent=(-2, 2, -2, 2), origin="lower", aspect="auto")
        axes.set(xlabel=r"Position $x$", ylabel=r"Position $y$")
        colorbar = figure.colorbar(image, ax=axes)
        colorbar.set_label("Intensity (a.u.)")
        figure.savefig(OUTPUT / f"{name}_heatmap.png", dpi=150)
        plt.close(figure)


if __name__ == "__main__":
    build("paper")
    build("presentation")
