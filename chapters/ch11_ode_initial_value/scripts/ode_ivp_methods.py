"""第十一章常微分方程初值问题示例脚本。"""

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
    estimate_convergence_order,
    euler_step,
    global_error,
    heun_euler_embedded_step,
    heun_step,
    midpoint_step,
    rk4_step,
    solve_ivp_adaptive_heun,
    solve_ivp_fixed_step,
)


def exponential_rhs(_time: float, state: np.ndarray) -> np.ndarray:
    return state


def main() -> None:
    step_size = 0.1
    exact_one_step = math.exp(step_size)
    print("one-step comparison for y'=y, y(0)=1:")
    for name, stepper in [
        ("Euler", euler_step),
        ("Heun", heun_step),
        ("Midpoint", midpoint_step),
        ("RK4", rk4_step),
    ]:
        value = stepper(exponential_rhs, 0.0, 1.0, step_size)[0]
        print(f"  {name:8s} value={value:.12f} error={abs(value - exact_one_step):.3e}")

    print("\nfixed-step solve on [0, 1]:")
    for method in ["euler", "heun", "midpoint", "rk4"]:
        result = solve_ivp_fixed_step(exponential_rhs, (0.0, 1.0), 1.0, step_size, method=method)
        errors = global_error(result.times, result.values, lambda time: math.exp(time))
        print(f"  {method:8s} y(1)={result.values[-1, 0]:.12f} error={errors[-1]:.3e}")

    step_sizes = np.array([0.2, 0.1, 0.05])
    euler_errors = []
    rk4_errors = []
    for h in step_sizes:
        euler = solve_ivp_fixed_step(exponential_rhs, (0.0, 1.0), 1.0, h, method="euler")
        rk4 = solve_ivp_fixed_step(exponential_rhs, (0.0, 1.0), 1.0, h, method="rk4")
        euler_errors.append(abs(euler.values[-1, 0] - math.e))
        rk4_errors.append(abs(rk4.values[-1, 0] - math.e))
    print("\nobserved order:")
    print(f"  Euler: {estimate_convergence_order(step_sizes, euler_errors):.3f}")
    print(f"  RK4:   {estimate_convergence_order(step_sizes, rk4_errors):.3f}")

    high, low, error = heun_euler_embedded_step(exponential_rhs, 0.0, 1.0, step_size)
    print("\nHeun-Euler embedded step:")
    print(
        f"  high={high[0]:.12f}",
        f"low={low[0]:.12f}",
        f"estimate={abs(error[0]):.3e}",
    )

    adaptive = solve_ivp_adaptive_heun(
        exponential_rhs,
        (0.0, 1.0),
        1.0,
        initial_step=0.25,
        absolute_tolerance=1e-7,
        relative_tolerance=1e-5,
    )
    print("\nadaptive Heun:")
    print(
        f"  y(1)={adaptive.values[-1, 0]:.12f}",
        f"accepted={adaptive.accepted_steps}",
        f"rejected={adaptive.rejected_steps}",
        f"max_error_norm={np.max(adaptive.error_estimates):.3e}",
    )

    def oscillator(_time: float, state: np.ndarray) -> np.ndarray:
        return np.array([state[1], -state[0]])

    oscillator_result = solve_ivp_fixed_step(
        oscillator,
        (0.0, math.pi / 2.0),
        [1.0, 0.0],
        math.pi / 200.0,
        method="rk4",
    )
    print("\noscillator at pi/2:", np.array2string(oscillator_result.values[-1], precision=12))


if __name__ == "__main__":
    main()
