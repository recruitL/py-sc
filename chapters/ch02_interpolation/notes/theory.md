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

## Interpolation and Fitting

Interpolation enforces every data point exactly. Fitting, such as least-squares
approximation, usually allows residuals and asks for a simpler function that is
close to the data. Interpolation is natural when data values are trusted table
values or exact samples of a smooth function. Fitting is often safer for noisy
measurements.

The ingredients of an interpolation problem are:

* interpolation nodes \(x_i\);
* values \(y_i\), often \(y_i=f(x_i)\);
* an interpolation space \(V\), such as polynomials of degree at most \(n\);
* a basis for \(V\), used to compute or evaluate the interpolant.

For \(n+1\) distinct nodes, there is a unique polynomial \(p_n \in \mathcal P_n\)
that interpolates the data. This follows from the fact that a nonzero
polynomial of degree at most \(n\) cannot have \(n+1\) distinct roots.

## Lagrange Polynomial Interpolation

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
condition follows immediately. This form is conceptually direct because it
builds the interpolant from basis functions that each select one node value.

The interpolation error has the form

$$
f(x) - p_n(x) =
\frac{f^{(n+1)}(\xi)}{(n+1)!}
\prod_{i=0}^{n}(x-x_i),
$$

for some \(\xi\) in the interpolation interval. This formula separates two
sources of error: the smoothness and derivatives of \(f\), and the nodal product
controlled by the node locations.

## Runge Behavior and Chebyshev Nodes

Equally spaced nodes can cause severe endpoint oscillation for high-degree
interpolation. The classical example is the Runge function

$$
f(x)=\frac{1}{1+25x^2},\qquad x\in[-1,1].
$$

Increasing the degree on equally spaced nodes does not necessarily improve the
maximum error. Chebyshev nodes cluster near the interval endpoints and reduce
the maximum size of the nodal product

$$
\prod_{i=0}^{n}(x-x_i).
$$

For \(N\) nodes on \([a,b]\), this repository uses

$$
x_k=\frac{a+b}{2}+\frac{b-a}{2}
\cos\left(\frac{2k+1}{2N}\pi\right),
\qquad k=0,\dots,N-1,
$$

sorted into increasing order. Chebyshev nodes do not make polynomial
interpolation universally safe, but they make node placement an explicit part
of the numerical method.

## Newton Divided Differences

Newton interpolation writes

$$
p_n(x) = c_0 + c_1(x-x_0) + c_2(x-x_0)(x-x_1) + \cdots
+ c_n\prod_{j=0}^{n-1}(x-x_j).
$$

The coefficients are divided differences:

$$
c_k=f[x_0,x_1,\dots,x_k].
$$

This form is useful when new nodes are added because the previous coefficients
can be reused. On equally spaced nodes, the divided-difference form is closely
related to finite-difference interpolation formulas. Those formulas are useful
for tables, but the divided-difference version is more general and works on
nonuniform nodes.

## Hermite Interpolation

Hermite interpolation uses both function values and derivative values, for
example

$$
p(x_i)=y_i,\qquad p'(x_i)=m_i.
$$

It is a natural bridge from value-only interpolation to smooth piecewise
methods. In this chapter it is kept as an extension topic. Later development
should include cubic Hermite interpolation on one interval and then connect it
to monotonicity-preserving PCHIP interpolation.

## Piecewise Linear Interpolation

Piecewise linear interpolation connects neighboring data points with line
segments. On an interval \([x_i,x_{i+1}]\),

$$
p(x)=
\frac{x_{i+1}-x}{x_{i+1}-x_i}y_i
+ \frac{x-x_i}{x_{i+1}-x_i}y_{i+1}.
$$

It is local, simple, and robust. Changing one data point only affects nearby
intervals. The cost is that the derivative is discontinuous at the nodes, so it
can be too rough for derivative-sensitive problems.

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

These conditions create a tridiagonal linear system for the spline coefficients.
The implementation in `src/py_sc/interpolation.py` solves this system with the
Thomas algorithm, which is the standard direct method for tridiagonal systems.

Other boundary conditions, such as clamped endpoint derivatives, should be
added later as a contrast to the natural spline. Boundary conditions matter most
near the endpoints.

## B-Splines and Two-Dimensional Interpolation

B-splines represent splines through local basis functions with compact support.
For this chapter, the first extension target is the cubic uniform B-spline,
which can be introduced through four translated basis functions. The full
knot-vector formulation can be left for a later pass.

Two-dimensional interpolation should begin with two simple settings:

* bilinear interpolation on a rectangular grid cell;
* linear Lagrange interpolation on a triangular element using barycentric
  coordinates.

These topics connect interpolation to finite elements, image resampling, and
surface reconstruction.

## Failure Modes

* High-degree polynomial interpolation can oscillate strongly.
* Extrapolation outside the data interval is usually unreliable.
* Piecewise linear interpolation may be too rough for derivative-sensitive
  problems.
* Spline boundary conditions can influence endpoint behavior.
* Interpolation through noisy data can amplify measurement noise because it
  forces the interpolant through every point.

## Link to Later Chapters

Interpolation appears again in numerical differentiation, numerical
integration, finite differences, finite elements, spectral methods, and data
approximation. Chebyshev differentiation matrices are mentioned here only as a
future spectral-methods topic; they should not become the main line of this
chapter.
