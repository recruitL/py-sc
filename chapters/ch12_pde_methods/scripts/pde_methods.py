"""第十二章偏微分方程数值方法示例脚本。"""

from __future__ import annotations

import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from py_sc import (  # noqa: E402
    lax_friedrichs_advection_1d,
    lax_wendroff_advection_1d,
    periodic_grid_1d,
    solve_heat_1d_crank_nicolson,
    solve_heat_1d_ftcs,
    solve_heat_1d_implicit_euler,
    solve_laplace_2d_sor,
    solve_poisson_2d_sor,
    solve_wave_1d_dirichlet,
    upwind_advection_1d,
    upwind_advection_2d,
)


def main() -> None:
    points = 80
    grid = periodic_grid_1d(0.0, 1.0, points)
    dx = 1.0 / points
    dt = 0.4 * dx
    steps = 20
    initial = np.sin(2.0 * math.pi * grid)
    exact = np.sin(2.0 * math.pi * ((grid - steps * dt) % 1.0))

    print("1D advection on a smooth sine wave:")
    for solver in [upwind_advection_1d, lax_friedrichs_advection_1d, lax_wendroff_advection_1d]:
        result = solver(initial, velocity=1.0, dx=dx, dt=dt, steps=steps)
        error = np.linalg.norm(result.values[-1] - exact, ord=np.inf)
        print(f"  {result.method:15s} CFL={result.courant:.3f} max_error={error:.3e}")

    square = np.zeros((20, 20))
    square[6:12, 8:14] = 1.0
    adv2 = upwind_advection_2d(square, velocity_x=1.0, velocity_y=0.0, dx=0.05, dy=0.05, dt=0.05, steps=3)
    print("\n2D upwind advection:")
    print(
        f"  shape={adv2.values.shape}",
        f"CFL_x={adv2.courant_x:.3f}",
        f"CFL_y={adv2.courant_y:.3f}",
        f"mass={np.sum(adv2.values[-1]):.6f}",
    )

    wave_points = 101
    wave_grid = np.linspace(0.0, 1.0, wave_points)
    wave_dx = wave_grid[1] - wave_grid[0]
    wave_dt = 0.4 * wave_dx
    wave_steps = 50
    displacement = np.sin(math.pi * wave_grid)
    velocity = np.zeros_like(wave_grid)
    wave = solve_wave_1d_dirichlet(displacement, velocity, speed=1.0, dx=wave_dx, dt=wave_dt, steps=wave_steps)
    wave_exact = np.cos(math.pi * wave.times[-1]) * np.sin(math.pi * wave_grid)
    print("\n1D wave equation:")
    print(
        f"  CFL={wave.courant:.3f}",
        f"max_error={np.linalg.norm(wave.values[-1] - wave_exact, ord=np.inf):.3e}",
        f"energy_change={wave.energy_history[-1] - wave.energy_history[0]:.3e}",
    )

    heat_points = 51
    heat_grid = np.linspace(0.0, 1.0, heat_points)
    heat_dx = heat_grid[1] - heat_grid[0]
    heat_initial = np.sin(math.pi * heat_grid)
    print("\n1D heat equation:")
    heat_cases = [
        ("FTCS", solve_heat_1d_ftcs, 0.4 * heat_dx * heat_dx, 40),
        ("Implicit Euler", solve_heat_1d_implicit_euler, 2.0 * heat_dx * heat_dx, 10),
        ("Crank-Nicolson", solve_heat_1d_crank_nicolson, 0.8 * heat_dx, 5),
    ]
    for name, solver, heat_dt, heat_steps in heat_cases:
        heat = solver(heat_initial, diffusivity=1.0, dx=heat_dx, dt=heat_dt, steps=heat_steps)
        heat_exact = np.exp(-math.pi * math.pi * heat.times[-1]) * np.sin(math.pi * heat_grid)
        error = np.linalg.norm(heat.values[-1] - heat_exact, ord=np.inf)
        print(f"  {name:15s} r={heat.diffusion_number:.3f} max_error={error:.3e}")

    nx = ny = 18
    x = np.linspace(0.0, 1.0, nx + 2)
    y = np.linspace(0.0, 1.0, ny + 2)
    xx, yy = np.meshgrid(x, y, indexing="ij")
    poisson_exact = np.sin(math.pi * xx) * np.sin(math.pi * yy)
    source = 2.0 * math.pi * math.pi * poisson_exact
    boundary = np.zeros_like(poisson_exact)
    poisson = solve_poisson_2d_sor(source, boundary, hx=x[1] - x[0], hy=y[1] - y[0], omega=1.6, tolerance=1e-9)
    print("\n2D Poisson equation by SOR:")
    print(
        f"  iterations={poisson.iterations}",
        f"residual={poisson.residual_norm:.3e}",
        f"max_error={np.max(np.abs(poisson.solution - poisson_exact)):.3e}",
    )

    laplace_boundary = np.ones((8, 8))
    laplace = solve_laplace_2d_sor(laplace_boundary, hx=1.0 / 7.0, hy=1.0 / 7.0, omega=1.4, tolerance=1e-10)
    print("\n2D Laplace equation by SOR:")
    print(
        f"  iterations={laplace.iterations}",
        f"residual={laplace.residual_norm:.3e}",
        f"center={laplace.solution[4, 4]:.6f}",
    )


if __name__ == "__main__":
    main()
