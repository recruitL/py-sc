"""Numerical computing utilities for chapter-based examples."""

from .interpolation import (
    NaturalCubicSpline,
    lagrange_interpolate,
    piecewise_linear_interpolate,
)

__all__ = [
    "NaturalCubicSpline",
    "lagrange_interpolate",
    "piecewise_linear_interpolate",
]

