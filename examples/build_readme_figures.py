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

        # Scatter plot with redundant color and shape encodings.
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
        figure.set_figheight(figure.get_figheight() * 1.35)
        lower, upper = axes.get_ylim()
        axes.set_ylim(lower, upper + 0.5 * (upper - lower))
        axes.legend(loc="upper left")
        figure.savefig(OUTPUT / f"{name}_scatter.png")
        plt.close(figure)

        # Vertical bars with a zero baseline and readable category labels.
        figure, axes = plt.subplots()
        categories = ("Baseline", "Method A", "Method B", "Method C")
        values = (0.42, 0.68, 0.81, 0.74)
        axes.bar(categories, values)
        axes.set(ylabel="Accuracy", ylim=(0, 1))
        axes.minorticks_off()
        axes.tick_params(axis="x", pad=6, labelrotation=30)
        plt.setp(axes.get_xticklabels(), horizontalalignment="right")
        figure.savefig(OUTPUT / f"{name}_bar.png")
        plt.close(figure)

        # Heatmap using the default perceptually uniform sequential colormap.
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
        colorbar = figure.colorbar(image, ax=axes)
        colorbar.set_label("Intensity (a.u.)")
        figure.savefig(OUTPUT / f"{name}_heatmap.png")
        plt.close(figure)

        # Show observations as well as a clearly defined spread interval.
        figure, axes = plt.subplots()
        samples = rng.normal(loc=[0.4, 0.7, 0.9], scale=0.12, size=(12, 3))
        for index, values in enumerate(samples.T):
            jitter = rng.uniform(-0.12, 0.12, values.size)
            axes.scatter(
                index + jitter,
                values,
                color="0.6",
                alpha=0.7,
                label="Observations" if index == 0 else None,
            )
        axes.errorbar(
            np.arange(3),
            samples.mean(axis=0),
            yerr=samples.std(axis=0, ddof=1),
            fmt="o",
            color="black",
            capsize=3,
            label="Mean ± SD",
        )
        axes.set(
            xticks=np.arange(3),
            xticklabels=["Control", "A", "B"],
            ylabel="Response (a.u.)",
            xlim=(-0.5, 2.5),
        )
        axes.minorticks_off()
        figure.set_figheight(figure.get_figheight() * 1.35)
        lower, upper = axes.get_ylim()
        axes.set_ylim(lower, upper + 0.35 * (upper - lower))
        axes.legend(loc="upper left")
        figure.savefig(OUTPUT / f"{name}_uncertainty.png")
        plt.close(figure)

        # A shared symmetric scale gives equal weight to signed deviations.
        figure, axes = plt.subplots()
        residuals = np.array([[-2, -1, 0, 1], [1, 0, -1, 2], [-1, 2, 1, -2]])
        image = axes.imshow(
            residuals,
            cmap="BrBG",
            norm=mpl.colors.CenteredNorm(vcenter=0, halfrange=2),
            interpolation="nearest",
        )
        axes.set(
            xticks=np.arange(4), yticks=np.arange(3), xlabel="Sample", ylabel="Run"
        )
        axes.minorticks_off()
        figure.colorbar(image, ax=axes, label="Residual (a.u.)")
        figure.savefig(OUTPUT / f"{name}_diverging.png")
        plt.close(figure)


if __name__ == "__main__":
    build("paper")
    build("presentation")
