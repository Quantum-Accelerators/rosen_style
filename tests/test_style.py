from __future__ import annotations

from unittest.mock import patch

import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

import rosen_style


def test_paper_has_readable_type_and_minor_ticks():
    style = rosen_style.settings("paper", latex=False)
    assert style["font.size"] >= 10
    assert style["axes.grid"] is False
    assert style["xtick.minor.visible"] is True
    assert style["ytick.minor.visible"] is True
    assert style["image.cmap"] == "plasma"


def test_presentation_is_larger_than_paper():
    paper = rosen_style.settings("paper", latex=False)
    presentation = rosen_style.settings("presentation", latex=False)
    assert presentation["font.size"] > paper["font.size"]
    assert presentation["axes.labelsize"] > paper["axes.labelsize"]
    assert presentation["figure.figsize"][0] > paper["figure.figsize"][0]


def test_latex_is_selected_when_available():
    with patch("rosen_style._style.latex_available", return_value=True):
        assert rosen_style.settings()["text.usetex"] is True


def test_explicit_latex_override_avoids_external_dependency():
    assert rosen_style.settings(latex=False)["text.usetex"] is False


def test_context_restores_matplotlib_settings():
    original_size = mpl.rcParams["font.size"]
    with rosen_style.context("presentation", latex=False):
        assert mpl.rcParams["font.size"] == 20
    assert mpl.rcParams["font.size"] == original_size


def test_styles_render_without_latex(tmp_path):
    for name in ("paper", "presentation"):
        with rosen_style.context(name, latex=False):
            figure, axes = plt.subplots()
            axes.plot([0, 1, 2], [0, 1, 0], label="signal")
            axes.set(xlabel="Time (s)", ylabel="Value (a.u.)")
            axes.legend()
            figure.savefig(tmp_path / f"{name}.png")
            plt.close(figure)
        assert (tmp_path / f"{name}.png").stat().st_size > 0


def test_unknown_style_is_rejected():
    with pytest.raises(ValueError, match="Unknown style"):
        rosen_style.settings("poster")
