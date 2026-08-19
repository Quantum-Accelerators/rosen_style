from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

import rosen_style


def test_paper_has_readable_type_and_minor_ticks():
    style = rosen_style.settings("paper")
    assert style["font.size"] >= 10
    assert style["axes.grid"] is False
    assert style["xtick.minor.visible"] is True
    assert style["ytick.minor.visible"] is True
    assert style["image.cmap"] == "plasma"


def test_presentation_is_larger_than_paper():
    paper = rosen_style.settings("paper")
    presentation = rosen_style.settings("presentation")
    assert presentation["font.size"] > paper["font.size"]
    assert presentation["axes.labelsize"] > paper["axes.labelsize"]
    assert presentation["figure.figsize"][0] > paper["figure.figsize"][0]


def test_paper_column_widths_and_aspect_ratio():
    single = rosen_style.settings("paper")
    double = rosen_style.settings("paper", columns=2)
    assert single["figure.figsize"][0] == 3.25
    assert double["figure.figsize"][0] == 7.0
    assert single["figure.figsize"][1] == pytest.approx(3.25 / ((1 + 5**0.5) / 2))
    assert double["figure.figsize"][1] == pytest.approx(7.0 / ((1 + 5**0.5) / 2))


def test_context_restores_matplotlib_settings():
    original_size = mpl.rcParams["font.size"]
    with rosen_style.context("presentation"):
        assert mpl.rcParams["font.size"] == 20
    assert mpl.rcParams["font.size"] == original_size


def test_styles_render(tmp_path):
    for name in ("paper", "presentation"):
        with rosen_style.context(name):
            figure, axes = plt.subplots()
            axes.plot([0, 1, 2], [0, 1, 0], label="signal")
            axes.set(xlabel="Time (s)", ylabel="Value (a.u.)")
            axes.legend()
            figure.savefig(tmp_path / f"{name}.png")
            plt.close(figure)
        assert (tmp_path / f"{name}.png").stat().st_size > 0


def test_unknown_style_is_rejected():
    with pytest.raises(ValueError, match="Unknown style"):
        rosen_style.settings("cow")


def test_unknown_paper_column_count_is_rejected():
    with pytest.raises(ValueError, match="column count"):
        rosen_style.settings("paper", columns=3)
