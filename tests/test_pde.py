from __future__ import annotations

import math

import numpy as np
import pytest

from py_sc import (
    advection_cfl,
    lax_friedrichs_advection_1d,
    lax_wendroff_advection_1d,
    periodic_grid_1d,
    solve_wave_1d_dirichlet,
    upwind_advection_1d,
    upwind_advection_2d,
    wave_cfl,
    wave_discrete_energy,
)


def test_advection_cfl_uses_velocity_time_and_space_steps() -> None:
    assert advection_cfl(2.0, 0.05, 0.1) == pytest.approx(1.0)


def test_upwind_advection_1d_shifts_exactly_at_unit_cfl() -> None:
    initial = np.array([0.0, 1.0, 2.0, 3.0])

    result = upwind_advection_1d(initial, velocity=1.0, dx=0.25, dt=0.25, steps=2)

    assert result.method == "upwind"
    assert result.courant == pytest.approx(1.0)
    assert np.allclose(result.values[-1], np.roll(initial, 2))


def test_lax_wendroff_advection_1d_tracks_smooth_periodic_wave() -> None:
    points = 80
    grid = periodic_grid_1d(0.0, 1.0, points)
    initial = np.sin(2.0 * math.pi * grid)
    dx = 1.0 / points
    dt = 0.4 * dx
    steps = 20

    result = lax_wendroff_advection_1d(initial, velocity=1.0, dx=dx, dt=dt, steps=steps)
    exact = np.sin(2.0 * math.pi * ((grid - steps * dt) % 1.0))

    assert np.linalg.norm(result.values[-1] - exact, ord=np.inf) < 4e-3


def test_lax_friedrichs_advection_1d_is_mass_conservative_for_periodic_boundary() -> None:
    grid = periodic_grid_1d(0.0, 1.0, 40)
    initial = np.where((grid > 0.3) & (grid < 0.6), 1.0, 0.0)

    result = lax_friedrichs_advection_1d(initial, velocity=1.0, dx=1.0 / 40.0, dt=0.5 / 40.0, steps=8)

    assert np.sum(result.values[-1]) == pytest.approx(np.sum(initial))


def test_upwind_advection_2d_shifts_exactly_in_x_at_unit_cfl() -> None:
    initial = np.arange(12.0).reshape(3, 4)

    result = upwind_advection_2d(initial, velocity_x=1.0, velocity_y=0.0, dx=0.5, dy=0.25, dt=0.5, steps=1)

    assert result.courant_x == pytest.approx(1.0)
    assert result.courant_y == pytest.approx(0.0)
    assert np.allclose(result.values[-1], np.roll(initial, 1, axis=0))


def test_wave_cfl_uses_speed_time_and_space_steps() -> None:
    assert wave_cfl(2.0, 0.05, 0.1) == pytest.approx(1.0)


def test_solve_wave_1d_dirichlet_tracks_first_sine_mode() -> None:
    points = 101
    grid = np.linspace(0.0, 1.0, points)
    dx = grid[1] - grid[0]
    dt = 0.4 * dx
    steps = 50
    initial = np.sin(math.pi * grid)
    velocity = np.zeros_like(grid)

    result = solve_wave_1d_dirichlet(initial, velocity, speed=1.0, dx=dx, dt=dt, steps=steps)
    exact = np.cos(math.pi * result.times[-1]) * np.sin(math.pi * grid)

    assert result.courant == pytest.approx(0.4)
    assert np.linalg.norm(result.values[-1] - exact, ord=np.inf) < 5e-4


def test_wave_discrete_energy_is_positive_for_nonzero_state() -> None:
    grid = np.linspace(0.0, 1.0, 11)
    displacement = np.sin(math.pi * grid)
    velocity = np.zeros_like(grid)

    assert wave_discrete_energy(displacement, velocity, speed=1.0, dx=0.1) > 0.0


def test_pde_routines_validate_shapes() -> None:
    with pytest.raises(ValueError):
        solve_wave_1d_dirichlet([0.0, 1.0], [0.0], speed=1.0, dx=0.1, dt=0.05, steps=1)
