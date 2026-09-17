from __future__ import annotations

import itertools
import warnings

import matplotlib as mpl
import pytest
from PIL import Image

mpl.use("Agg")
import matplotlib.pyplot as plt

import rosen_style


@pytest.mark.parametrize("name", ["paper", "presentation"])
@pytest.mark.parametrize("shape", [(1, 2), (2, 2)])
def test_subpanels_fit_and_preserve_export_size(name, shape, tmp_path):
    with rosen_style.context(name, columns=2):
        figure, axes = plt.subplots(*shape, sharex=True, sharey=True, squeeze=False)
        try:
            for index, ax in enumerate(axes.flat):
                ax.plot([0, 1, 2], [0, 1, 0], label="Signal")
                ax.set(xlabel="Time (s)", ylabel="Response (a.u.)")
                ax.label_outer()
                ax.text(0.03, 0.95, f"({index + 1})", transform=ax.transAxes, va="top")
            axes[0, 0].legend(loc="upper right")
            with warnings.catch_warnings():
                warnings.simplefilter("error", UserWarning)
                figure.canvas.draw()
                output = tmp_path / "subpanels.png"
                figure.savefig(output)
                figure.savefig(tmp_path / "subpanels.pdf")

            renderer = figure.canvas.get_renderer()
            bounds = [ax.get_tightbbox(renderer) for ax in axes.flat]
            for bounds_i in bounds:
                assert bounds_i.width > 0
                assert bounds_i.height > 0
                assert bounds_i.x0 >= 0
                assert bounds_i.y0 >= 0
                assert bounds_i.x1 <= figure.bbox.width
                assert bounds_i.y1 <= figure.bbox.height
            for left, right in itertools.combinations(bounds, 2):
                assert not left.overlaps(right)
            with Image.open(output) as image:
                expected = figure.get_size_inches() * mpl.rcParams["savefig.dpi"]
                assert image.size == tuple(int(size) for size in expected)
        finally:
            plt.close(figure)
