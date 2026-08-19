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

Use `with rosen_style.context("paper"):` for temporary styling. LaTeX is selected automatically when a `latex` executable is available; pass `latex=False` to use Matplotlib's built-in renderer.

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

For publication-ready atomic structures, we recommend [Pretty Lattice](https://pypi.org/project/pretty-lattice/) for periodic materials and [xyzrender](https://github.com/aligfellow/xyzrender) for molecules.

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
