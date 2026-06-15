# Chapter 2: Data Interpolation

Interpolation estimates unknown values from known discrete data points. This
chapter introduces the mathematical motivation, basic algorithms, Python
implementations, and numerical experiments for interpolation. It should be read
as a runnable lecture chapter rather than a collection of isolated scripts.

The first-round build focuses on the main one-dimensional path:

```text
interpolation problem
  -> global polynomial interpolation
  -> interpolation error and Runge behavior
  -> Chebyshev nodes
  -> Newton divided differences
  -> piecewise linear interpolation
  -> natural cubic splines
```

Hermite interpolation, PCHIP, B-splines, and two-dimensional interpolation are
kept as extension frameworks so that later rounds can expand them without
changing the chapter layout.

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
* Extension roadmap: Hermite interpolation, PCHIP, cubic uniform B-splines,
  bilinear interpolation, and triangular linear interpolation

## Reading Order

1. `notebooks/01_interpolation_overview.ipynb`
2. `notebooks/02_polynomial_interpolation.ipynb`
3. `notebooks/03_piecewise_and_spline.ipynb`
4. `notebooks/04_experiments.ipynb`
5. `notebooks/05_extensions_framework.ipynb`
6. `notes/theory.md`
7. `references.md`

## Notebook Map

| Notebook | Role |
| --- | --- |
| `01_interpolation_overview.ipynb` | Defines interpolation, compares it with fitting, and introduces interpolation spaces. |
| `02_polynomial_interpolation.ipynb` | Covers Lagrange form, Newton divided differences, Runge behavior, and Chebyshev nodes. |
| `03_piecewise_and_spline.ipynb` | Compares local piecewise linear interpolation with natural cubic splines. |
| `04_experiments.ipynb` | Measures error trends and illustrates method limitations with reproducible experiments. |
| `05_extensions_framework.ipynb` | Stores runnable sketches for Hermite, PCHIP, B-spline, and two-dimensional interpolation topics. |

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

## Current Scope

Completed in this round:

* interpolation problem formulation;
* interpolation versus least-squares fitting;
* Lagrange interpolation and interpolation basis functions;
* interpolation error and Runge behavior;
* Chebyshev nodes and Chebyshev-node interpolation;
* Newton divided differences;
* piecewise linear interpolation;
* natural cubic spline construction and tridiagonal solve;
* experiment notebook with error comparisons.

Framework only, to be expanded later:

* Hermite interpolation;
* PCHIP and monotonicity-preserving interpolation;
* cubic uniform B-splines;
* bilinear and triangular two-dimensional interpolation;
* Chebyshev differentiation matrices for a later spectral-methods chapter.
