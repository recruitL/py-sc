# Theory Notes: Data Interpolation

Given data points

$$
(x_0, y_0), (x_1, y_1), \dots, (x_n, y_n),
$$

interpolation constructs a function \(p(x)\) such that

$$
p(x_i) = y_i,\quad i = 0, 1, \dots, n.
$$

The central numerical question is not only whether such a function exists, but
whether it is stable, accurate, and useful between the data points.

## Polynomial Interpolation

The Lagrange form writes the interpolation polynomial as

$$
p_n(x) = \sum_{j=0}^{n} y_j L_j(x),
$$

where

$$
L_j(x) = \prod_{\substack{m=0 \\ m \ne j}}^n
\frac{x - x_m}{x_j - x_m}.
$$

Each basis polynomial satisfies \(L_j(x_i)=\delta_{ij}\), so the interpolation
condition follows immediately.

The error has the form

$$
f(x) - p_n(x) =
\frac{f^{(n+1)}(\xi)}{(n+1)!}
\prod_{i=0}^{n}(x-x_i),
$$

for some \(\xi\) in the interpolation interval. This formula shows that both
the smoothness of \(f\) and the node placement affect accuracy.

## Newton Divided Differences

Newton interpolation writes

$$
p_n(x) = c_0 + c_1(x-x_0) + c_2(x-x_0)(x-x_1) + \cdots.
$$

The coefficients \(c_k\) are divided differences. This form is useful when new
nodes are added because the previous coefficients can be reused.

## Chebyshev Nodes

Equally spaced nodes can cause severe endpoint oscillation for high-degree
interpolation. Chebyshev nodes cluster near the interval endpoints and reduce
the maximum size of the nodal product

$$
\prod_{i=0}^{n}(x-x_i).
$$

This does not make polynomial interpolation universally safe, but it explains
why node selection is part of the algorithm.

## Piecewise Linear Interpolation

Piecewise linear interpolation connects neighboring data points with line
segments. It is local, simple, and robust, but its derivative is discontinuous
at the nodes.

## Natural Cubic Spline

A cubic spline uses a cubic polynomial on each interval:

$$
S_i(x)=a_i+b_i(x-x_i)+c_i(x-x_i)^2+d_i(x-x_i)^3.
$$

The pieces are joined so that the function, first derivative, and second
derivative are continuous at interior nodes. The natural spline adds

$$
S''(x_0)=0,\qquad S''(x_n)=0.
$$

This creates a tridiagonal linear system for the spline coefficients.

## Failure Modes

* High-degree polynomial interpolation can oscillate strongly.
* Extrapolation outside the data interval is usually unreliable.
* Piecewise linear interpolation may be too rough for derivative-sensitive
  problems.
* Spline boundary conditions can influence endpoint behavior.

## Link to Later Chapters

Interpolation appears again in numerical integration, finite differences,
spectral methods, and data approximation. It is one of the basic tools for
turning discrete data into computable functions.

