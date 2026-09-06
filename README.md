# rosen_style

Consistent, readable Matplotlib defaults for Rosen Research Group papers and presentations.

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
    fig.savefig("response.png")  # saved at the style default of 600 DPI
```

Paper figures default to a 3.25-inch single-column width, with height chosen using the golden ratio. Use `columns=2` for a 7-inch double-column figure:

```python
with rosen_style.context("paper", columns=2):
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 0])
    fig.savefig("double-column.png")
```

Outside the `with` block, Matplotlib's previous settings are restored. Mathematical notation such as `r"Position $x$"` is rendered by Matplotlib's built-in MathText engine and requires no external typesetting installation.

The defaults use 600 DPI for display and saved output, a color-vision-friendly categorical cycle, the perceptually uniform `plasma` image colormap, readable labels, transparent saved backgrounds, no grid lines, and minor ticks in paper mode. Figure titles are intentionally left to captions or surrounding presentation content. Pair color with markers, line styles, or direct labels when it carries meaning.

### Visual design choices

- **Typography:** both styles use bundled DejaVu Sans text and matching sans serif math for consistent typography across machines.
- **Paper:** 1.4-point lines and 4-point markers keep overlapping traces legible at single-column size. Minor ticks are shorter and lighter than major ticks.
- **Presentation:** longer, thicker major ticks and increased label spacing balance the larger type at slide scale.
- **Legends:** the examples place legends above the axes so they do not cover observations or require artificially expanded data limits. Marker shapes identify series as well as color.
- **Categories:** horizontal bars keep labels upright, with a zero baseline and one color for a single quantity.
- **Spatial data:** the heatmap uses equal aspect so equal distances on the two axes remain equal on screen. Choose `aspect="auto"` only when the axes do not represent comparable spatial units.

These are starting points: inspect figures at their final printed or projected size. Transparent exports assume a light background; use `fig.savefig("slide.png", transparent=False, facecolor="white")` when inserting a figure onto a dark slide. For crisp scalable output, save as PDF or SVG instead of PNG.

## Examples

Line plot:

![Paper line plot](examples/paper.png)

Scatter plot:

![Paper scatter plot](examples/paper_scatter.png)

Bar plot:

![Paper bar plot](examples/paper_bar.png)

Heatmap with a perceptually uniform color scale:

![Paper heatmap](examples/paper_heatmap.png)

Presentation typography and spacing:

![Presentation line plot](examples/presentation.png)

CI regenerates and commits these images when their source or the styles change.

## Structure visualization

For publication-ready atomic structures, we recommend [Pretty Lattice](https://github.com/songfeitong/pretty-lattice) for periodic materials and [xyzrender](https://github.com/aligfellow/xyzrender) for molecules.

## Design references

- [Claus O. Wilke, *Fundamentals of Data Visualization*](https://clauswilke.com/dataviz/)
- [Redundant coding: combine color with shapes or line styles](https://clauswilke.com/dataviz/redundant-coding.html)
- [Matplotlib style parameters and font configuration](https://matplotlib.org/stable/users/explain/customizing.html)

There are also many excellent Python examples on [The Python Graph Gallery](https://www.python-graph-gallery.com/) and [Python Charts](https://python-charts.com/) websites. For what not to do, check out the "[Friends Don't Let Friends Make Bad Graphs](https://github.com/cxli233/FriendsDontLetFriends)" repository.
