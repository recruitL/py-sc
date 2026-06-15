"""Numerical computing utilities for chapter-based examples."""

from .interpolation import (
    NaturalCubicSpline,
    chebyshev_nodes,
    cubic_spline_coefficients,
    divided_difference_table,
    lagrange_interpolate,
    newton_divided_differences,
    newton_interpolate,
    piecewise_linear_interpolate,
)

__all__ = [
    "NaturalCubicSpline",
    "chebyshev_nodes",
    "cubic_spline_coefficients",
    "divided_difference_table",
    "lagrange_interpolate",
    "newton_divided_differences",
    "newton_interpolate",
    "piecewise_linear_interpolate",
]
