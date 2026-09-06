# Scientific figure guide

`rosen_style` supplies a starting point; the data, audience, and destination still
determine the figure. The recommendations below connect the defaults to their
sources and explain choices that cannot be made by an rcParams style.

## Defaults and deliberate choices

| Concern | Package choice | Rationale |
| --- | --- | --- |
| Categorical color | Six colors from Okabe–Ito; existing order retained | Distinguish a few groups, with shapes or line styles as additional cues. [Wilke, chapters 19–20](https://clauswilke.com/dataviz/color-pitfalls.html) |
| Continuous color | `plasma` | A sequential scale for ordered magnitudes. Choose a diverging scale explicitly when there is a meaningful midpoint. [Wilke, chapter 4](https://clauswilke.com/dataviz/color-basics.html) |
| Typography | DejaVu Sans and matching MathText; paper labels 9–10 pt | Preview at the intended size and keep symbols in proportion to text. [Wilke, chapter 24](https://clauswilke.com/dataviz/small-axis-labels.html) |
| Context | Visible left/bottom axes, no default grid | Retain orientation while limiting clutter; a light major grid can help comparisons. [Wilke, chapter 23](https://clauswilke.com/dataviz/balance-data-context.html) |
| Export | White background; TrueType PDF/PS fonts; SVG text | Maintain contrast and allow text editing. [Nature figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/) |

White saved backgrounds replace the previous transparent default. For deliberate
compositing, use `fig.savefig("figure.png", transparent=True)` and inspect contrast
on the destination background. PDF/PS now use font type 42, SVG uses live text,
and the style explicitly selects MathText (`text.usetex=False`).

The existing 600 DPI display and export settings, figure widths, palette, and
font sizes are retained. These are group defaults, not universal journal rules.

## Size and typography

Build at the final physical size. `paper_size()` provides 3.25-inch and 7-inch
widths, not a guarantee of compliance with any particular journal. Adjust height
for the content; a golden-ratio rectangle is only a starting point. Reducing a
7-inch figure to 3.5 inches also halves its text and marker sizes. Inspect the
export at its final placement size, including tick labels, legends, and colorbars.
[Wilke, chapter 24](https://clauswilke.com/dataviz/small-axis-labels.html)

Publication requirements differ. Nature requests Arial or Helvetica and has its
own lettering sizes; DejaVu Sans is retained here because Matplotlib bundles it.
If required, install the journal's font and override it inside the style context.
Check mathematical glyphs separately. Label axes with quantities and units, and
keep text clear of data. [Nature figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)

```python
import matplotlib as mpl
import matplotlib.pyplot as plt
import rosen_style

with rosen_style.context("paper"):
    # Example custom width, in millimeters. Use your journal's actual dimensions.
    fig, ax = plt.subplots(figsize=(90 / 25.4, 65 / 25.4))
    ax.plot([0, 1, 2], [0, 1, 0], marker="o")
    ax.set(xlabel="Time (s)", ylabel="Response (a.u.)")
    fig.savefig("response.pdf")
```

## Color and redundant encoding

Keep category-to-color assignments consistent across panels. The cycle repeats
after six series; use direct labels or small multiples for larger collections.
Check grayscale and color-vision-deficiency simulations of the finished figure:
a palette alone does not guarantee distinguishability, especially for thin lines.
[Wilke, chapter 19](https://clauswilke.com/dataviz/color-pitfalls.html)

Pair color with marker shapes, dash patterns, or nearby labels. The examples set
these explicitly so a global marker cycle does not inadvertently imply discrete
sampling for every line. [Wilke, chapter 20](https://clauswilke.com/dataviz/redundant-coding.html)

For signed residuals, use a diverging colormap and a meaningful center. Equal
positive and negative magnitudes should receive comparable visual weight; use
common limits when comparing panels. [Wilke, chapter 4](https://clauswilke.com/dataviz/color-basics.html)

```python
with rosen_style.context("paper"):
    fig, ax = plt.subplots()
    residuals = [[-2, -1, 0], [0, 1, 2]]
    image = ax.imshow(
        residuals,
        cmap="BrBG",
        norm=mpl.colors.CenteredNorm(vcenter=0, halfrange=2),
        interpolation="nearest",
    )
    ax.set(xticks=[0, 1, 2], yticks=[0, 1], xlabel="Sample", ylabel="Run")
    ax.minorticks_off()
    fig.colorbar(image, ax=ax, label="Residual (a.u.)")
    fig.savefig("residuals.pdf")
```

## Honest scales and uncertainty

Start linear bars at zero. Use positions (dots) when a nonzero range is necessary.
If marker size represents a value, scale its area rather than its radius. Label
transformations and axis breaks explicitly. [Wilke, chapter 17](https://clauswilke.com/dataviz/proportional-ink.html)

Show observations or distributions when variation matters. For error bars or
bands, state whether they show SD, SE, a confidence interval, or something else;
give sample size and the calculation method in the caption. Do not infer
significance simply from overlapping error bars. The example generator includes
synthetic observations with mean ± one sample SD, explicitly distinguished from
uncertainty in the mean. [Wilke, chapter 16](https://clauswilke.com/dataviz/visualizing-uncertainty.html)

## Export and review

Prefer PDF for publication and PNG for raster previews. For dense plots, set
`rasterized=True` on the dense artist so axes and text remain vector graphics.
DPI affects raster content; it does not sharpen vector lines.
[Wilke, chapter 27](https://clauswilke.com/dataviz/image-file-formats.html)

SVG text remains editable but requires the font on the viewing computer. PDF
embeds a font subset and is the more portable choice. To prioritize SVG appearance
over editable text, set `mpl.rcParams["svg.fonttype"] = "path"` before export.
[Matplotlib font documentation](https://matplotlib.org/stable/users/explain/text/fonts.html)

Before sharing, check clipping, overlaps, units, legend meaning, and comparable
panel scales. Review the exported file, not only the plotting window. Provide a
caption that explains the result and uncertainty, plus a text description for
readers who cannot see the figure. Keep the source data and script alongside the
figure so revisions remain reproducible. Adapt detail to the audience and medium.
[Rougier, Droettboom & Bourne, *Ten Simple Rules for Better Figures*](https://doi.org/10.1371/journal.pcbi.1003833)
