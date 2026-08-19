# rosen_style

Consistent, readable Matplotlib defaults for Rosen research-group papers and presentations.

## Install

```bash
pip install git+https://github.com/Quantum-Accelerators/rosen_style.git
```

## Use

```python
import matplotlib.pyplot as plt
import rosen_style

rosen_style.use("paper")  # or "presentation"
fig, ax = plt.subplots()
ax.plot([0, 1, 2], [0, 1, 0])
ax.set(xlabel="Time (s)", ylabel="Response (a.u.)")
```

Use a context manager to apply a style temporarily:

```python
import matplotlib.pyplot as plt
import rosen_style

with rosen_style.context("paper"):
    fig, ax = plt.subplots()
    ax.scatter([1, 2, 3], [2.1, 3.8, 6.2])
    ax.set(xlabel="Concentration (mol/L)", ylabel="Response (a.u.)")
    fig.savefig("response.pdf")
```

Outside the `with` block, Matplotlib's previous settings are restored. LaTeX is selected automatically when a `latex` executable is available; pass `latex=False` to use Matplotlib's built-in renderer.

### Installing LaTeX

LaTeX is optional. If it is not already installed, use a TeX distribution appropriate for your operating system:

- **Windows:** Download and run the [Basic MiKTeX Installer](https://miktex.org/howto/install-miktex). Allow MiKTeX to install missing packages automatically.
- **macOS:** Download and install [MacTeX](https://www.tug.org/mactex/).
- **Ubuntu or Debian:** Install TeX Live and the rendering tools Matplotlib needs:

  ```bash
  sudo apt update
  sudo apt install texlive-latex-extra dvipng cm-super
  ```

  For other Linux distributions, install [TeX Live](https://tug.org/texlive/quickinstall.html) using the distribution's package manager or the official installer.

After installation, open a new terminal and verify that LaTeX is available:

```bash
latex --version
```

If LaTeX is unavailable or causes a rendering problem, use `rosen_style.use("paper", latex=False)` or `rosen_style.context("paper", latex=False)`.

The defaults use a color-vision-friendly categorical cycle, the perceptually uniform `plasma` image colormap, readable labels, no grid lines, and minor ticks in paper mode. Figure titles are intentionally left to captions or surrounding presentation content. Pair color with markers, line styles, or direct labels when it carries meaning.

## Examples

Line plot:

![Paper line plot](examples/paper.png)

Scatter plot:

![Paper scatter plot](examples/paper_scatter.png)

Bar plot:

![Paper bar plot](examples/paper_bar.png)

Heatmap with a perceptually uniform color scale:

![Paper heatmap](examples/paper_heatmap.png)

CI regenerates and commits these images when their source or the styles change.

## Structure visualization

For publication-ready atomic structures, we recommend [Pretty Lattice](https://github.com/songfeitong/pretty-lattice) for periodic materials and [xyzrender](https://github.com/aligfellow/xyzrender) for molecules.

## Development

```bash
pip install -e .[dev]
pytest
python examples/build_readme_figures.py
ruff check .
```

Tests disable LaTeX rendering, so CI does not require a TeX installation.

## Design references

- [Claus O. Wilke, *Fundamentals of Data Visualization*](https://clauswilke.com/dataviz/)

There are also many excellent Python examples on [The Python Graph Gallery](https://www.python-graph-gallery.com/) and [Python Charts](https://python-charts.com/) websites. For what not to do, check out the "[Friends Don't Let Friends Make Bad Graphs](https://github.com/cxli233/FriendsDontLetFriends)" repository.
