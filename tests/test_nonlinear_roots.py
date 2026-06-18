from __future__ import annotations

import math

import pytest

from py_sc import bisection_method, find_sign_change_brackets


def test_find_sign_change_brackets_finds_multiple_roots() -> None:
    func = lambda x: (x - 1.0) * (x + 0.5) * (x - 2.0)

    brackets = find_sign_change_brackets(func, -1.0, 2.5, subintervals=35)

    assert any(left <= -0.5 <= right for left, right in brackets)
    assert any(left <= 1.0 <= right for left, right in brackets)
    assert any(left <= 2.0 <= right for left, right in brackets)


def test_bisection_solves_cos_fixed_point_equation() -> None:
    result = bisection_method(lambda x: math.cos(x) - x, 0.0, 1.0, tolerance=1e-12)

    assert result.converged
    assert abs(result.root - 0.7390851332151607) < 1e-11
    assert result.residual < 1e-11
    assert result.history.size == result.iterations


def test_bisection_rejects_interval_without_sign_change() -> None:
    with pytest.raises(ValueError):
        bisection_method(lambda x: x**2 + 1.0, -1.0, 1.0)


def test_even_multiplicity_root_has_no_sign_change() -> None:
    brackets = find_sign_change_brackets(lambda x: (x - 1.0) ** 2, 0.0, 2.0, subintervals=19)

    assert brackets == []
