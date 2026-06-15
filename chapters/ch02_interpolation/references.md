# References: Data Interpolation

## Textbooks

* Richard L. Burden, J. Douglas Faires, Annette M. Burden, *Numerical Analysis*.
* Kendall Atkinson, *An Introduction to Numerical Analysis*.
* Gene H. Golub and Charles F. Van Loan, *Matrix Computations*.
* David Kincaid and Ward Cheney, *Numerical Analysis: Mathematics of Scientific Computing*.
* Alfio Quarteroni, Riccardo Sacco, and Fausto Saleri, *Numerical Mathematics*.
* Lloyd N. Trefethen, *Approximation Theory and Approximation Practice*.
* Lloyd N. Trefethen, *Spectral Methods in MATLAB*.
* Carl de Boor, *A Practical Guide to Splines*.
* M. J. D. Powell, *Approximation Theory and Methods*.

## Python and Scientific Computing

* NumPy documentation: interpolation-related array operations.
* SciPy documentation: `scipy.interpolate`.
* Matplotlib documentation: plotting numerical experiments.
* Jupyter documentation: executable notebooks and reproducible lecture notes.

## Chapter-Specific Topics

* Lagrange interpolation and polynomial interpolation error formulas.
* Newton divided differences and finite-difference interpolation.
* Runge function and endpoint oscillation on equally spaced nodes.
* Chebyshev nodes and minimization of polynomial interpolation oscillation.
* Natural cubic splines and tridiagonal linear systems.
* Cubic Hermite interpolation, PCHIP, and monotonicity-preserving piecewise methods.
* Cubic uniform B-splines and local support.
* Bilinear interpolation and triangular linear interpolation in two dimensions.

## Notes

For this chapter, SciPy should be treated as a comparison and validation tool.
The core algorithms in `src/py_sc/interpolation.py` should remain hand-written
for teaching clarity.

Chebyshev differentiation matrices are intentionally treated as an extension
pointer only. They belong more naturally to a later chapter on spectral methods.
