# Chapter 2: Data Interpolation

Interpolation estimates unknown values from known discrete data points. This
chapter introduces the mathematical motivation, basic algorithms, Python
implementations, and numerical experiments for one-dimensional interpolation.

## Main Questions

* How can a function be reconstructed from finitely many data points?
* Why can high-degree polynomial interpolation become unstable?
* What tradeoff is made by piecewise interpolation?
* How does a cubic spline impose smoothness between neighboring intervals?

## Algorithms

* Lagrange polynomial interpolation
* Newton divided differences
* Chebyshev nodes for reducing oscillation
* Piecewise linear interpolation
* Natural cubic spline interpolation

## Reading Order

1. `notebooks/01_interpolation_overview.ipynb`
2. `notebooks/02_polynomial_interpolation.ipynb`
3. `notebooks/03_piecewise_and_spline.ipynb`
4. `notebooks/04_experiments.ipynb`
5. `notes/theory.md`
6. `references.md`

## Runnable Scripts

From the repository root:

```bash
python chapters/ch02_interpolation/scripts/polynomial_interpolation.py
python chapters/ch02_interpolation/scripts/piecewise_interpolation.py
python chapters/ch02_interpolation/scripts/cubic_spline_interpolation.py
python chapters/ch02_interpolation/scripts/compare_interpolation.py
```

The scripts mirror the notebook examples and provide compact runnable versions
for quick checks.

## Implementation

Reusable teaching implementations live in:

```text
src/py_sc/interpolation.py
```

The functions are intentionally written for clarity before performance.

