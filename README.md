# py-sc

Python numerical computing notes and code organized like a book.

This repository collects small, readable implementations for scientific
computing topics. Each chapter has explanatory notes, runnable examples, and
reusable code in `src/py_sc`.

## Structure

```text
py-sc/
  chapters/
    ch02_interpolation/      # Chapter 2: interpolation examples
  src/
    py_sc/                   # Reusable implementations
  tests/                     # Lightweight regression tests
```

## Current Chapters

### Chapter 2: Data Interpolation

Implemented topics:

* Polynomial interpolation
* Piecewise linear interpolation
* Natural cubic spline interpolation

Run the comparison example:

```bash
python chapters/ch02_interpolation/compare_interpolation.py
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

