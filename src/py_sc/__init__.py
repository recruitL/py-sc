"""章节示例中使用的数值计算工具函数。"""

from .approximation import (
    adaptive_piecewise_linear,
    chebyshev_fit_function,
    chebyshev_series_eval,
    legendre_fit_function,
    legendre_series_eval,
    pade_eval,
    pade_from_taylor,
    polynomial_eval,
    polynomial_least_squares,
)
from .interpolation import (
    NaturalCubicSpline,
    chebyshev_nodes,
    cubic_spline_coefficients,
    divided_difference_table,
    lagrange_interpolate,
    newton_divided_differences,
    newton_interpolate,
    piecewise_cubic_hermite_interpolate,
    piecewise_linear_interpolate,
)

__all__ = [
    "NaturalCubicSpline",
    "adaptive_piecewise_linear",
    "chebyshev_fit_function",
    "chebyshev_nodes",
    "chebyshev_series_eval",
    "cubic_spline_coefficients",
    "divided_difference_table",
    "lagrange_interpolate",
    "legendre_fit_function",
    "legendre_series_eval",
    "newton_divided_differences",
    "newton_interpolate",
    "pade_eval",
    "pade_from_taylor",
    "piecewise_cubic_hermite_interpolate",
    "piecewise_linear_interpolate",
    "polynomial_eval",
    "polynomial_least_squares",
]
