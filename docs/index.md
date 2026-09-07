# rosen_style

Readable Matplotlib defaults for Rosen Research Group papers and presentations.

```python
import matplotlib.pyplot as plt
import rosen_style

with rosen_style.context("paper"):
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 0], marker="o")
    ax.set(xlabel="Time (s)", ylabel="Response (a.u.)")
    fig.savefig("response.pdf")
```

Install with `pip install git+https://github.com/Quantum-Accelerators/rosen_style.git`.
Use `"presentation"` for slides or `columns=2` for a double-column paper figure.
The context manager restores your previous Matplotlib settings on exit.

