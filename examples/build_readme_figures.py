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
        figure.set_figheight(figure.get_figheight() * 1.35)
        lower, upper = axes.get_ylim()
        axes.set_ylim(lower, upper + 0.5 * (upper - lower))
        axes.legend(loc="upper left")
        figure.savefig(OUTPUT / f"{name}.png")
        plt.close(figure)

        # Parity plot with identical limits and scale on both axes.
        with rosen_style.context(name, square=True):
            figure, axes = plt.subplots()
            for bias, noise, label, marker in zip(
                (0.0, 0.12, -0.12),
                (0.12, 0.18, 0.22),
                ("control", "method A", "method B"),
                ("o", "s", "^"),
                strict=True,
            ):
                actual = rng.uniform(0, 2.5, 35)
                predicted = actual + bias + rng.normal(0, noise, actual.size)
                axes.scatter(actual, predicted, label=label, marker=marker, alpha=0.8)
            limits = (-0.25, 2.75)
            axes.plot(limits, limits, color="#555555", linestyle="--", label="parity")
            axes.set(
                xlabel="Actual (a.u.)",
                ylabel="Predicted (a.u.)",
                xlim=limits,
                ylim=limits,
                aspect="equal",
            )
            axes.legend(loc="upper left")
            figure.savefig(OUTPUT / f"{name}_scatter.png")
            plt.close(figure)

        # Square heatmap using the default perceptually uniform sequential colormap.
        with rosen_style.context(name, square=True):
            figure, axes = plt.subplots()
            xx, yy = np.meshgrid(np.linspace(-2, 2, 100), np.linspace(-2, 2, 80))
            field = np.exp(-(xx**2 + yy**2)) + 0.5 * np.exp(
                -((xx - 1.1) ** 2 + (yy + 0.8) ** 2) / 0.25
            )
            # Equal spatial units must have equal visual lengths.
            image = axes.imshow(
                field, extent=(-2, 2, -2, 2), origin="lower", aspect="equal"
            )
            axes.set(xlabel=r"Position $x$", ylabel=r"Position $y$")
            colorbar = figure.colorbar(image, ax=axes, shrink=0.6, aspect=30)
            colorbar.set_label("Intensity (a.u.)")
            figure.savefig(OUTPUT / f"{name}_heatmap.png")
            plt.close(figure)


if __name__ == "__main__":
    build("paper")
    build("presentation")
