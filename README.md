# py-sc

Python numerical computing notes and runnable lecture materials.

`py-sc` is a long-term course-style and book-style repository for numerical
computing, scientific computing, and physics-oriented computation. It is meant
to be read in order like an electronic lecture note: theory motivates the
algorithm, the algorithm is implemented in Python, and notebooks provide
experiments and figures.

## Structure

```text
py-sc/
  AGENTS.md                 # Maintenance and writing rules
  chapters/
    ch02_interpolation/     # Chapter 2: interpolation
      notebooks/            # Main teaching notebooks
      notes/                # Theory and reference notes
      scripts/              # Runnable script versions of examples
      references.md         # Chapter references
  docs/                     # Course-level notes and roadmap
  references/               # Shared bibliography notes
  src/
    py_sc/                  # Reusable teaching implementations
  tests/                    # Lightweight regression tests
```

## Current Chapters

| Chapter | Topic | Status |
| --- | --- | --- |
| Chapter 2 | Data Interpolation | First-round lecture build: overview, polynomial interpolation, Runge behavior, Chebyshev nodes, Newton form, piecewise linear interpolation, and natural cubic splines |

## Reading Order

Start with the chapter README, then read notebooks in numerical order:

1. `chapters/ch02_interpolation/README.md`
2. `chapters/ch02_interpolation/notebooks/01_interpolation_overview.ipynb`
3. `chapters/ch02_interpolation/notebooks/02_polynomial_interpolation.ipynb`
4. `chapters/ch02_interpolation/notebooks/03_piecewise_and_spline.ipynb`
5. `chapters/ch02_interpolation/notebooks/04_experiments.ipynb`
6. `chapters/ch02_interpolation/notebooks/05_extensions_framework.ipynb`

Run the script comparison example:

```bash
python chapters/ch02_interpolation/scripts/compare_interpolation.py
```

Run tests:

```bash
python -m pytest
```

## Setup

Create an environment and install the project in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```
