from typing import Callable


def trapezoidal(f: Callable, a: float, b: float, n: int) -> float:
    """
    Calculate the area under the curve of a given function using the trapezoidal rule for numerical integration.

    :param f: The function for which the area needs to be calculated.
    :param a: The lower limit of integration.
    :param b: The upper limit of integration.
    :param n: The number of trapezoids to use for approximating the area (positive integer).

    :return: The approximate area under the curve of the given function.
    :raises ValueError: If 'n' is not a positive integer.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Trapezoid count must be a positive integer.")

    h = float(b - a) / n  # Height of each trapezoid
    s = 0.0  # Sum of trapezoid areas
    s += f(a) / 2.0  # Add the first function evaluation divided by 2 (starting point of the trapezoids)

    for i in range(1, n):
        s += f(a + i * h)  # Add the function evaluations at each trapezoid point
    s += f(b) / 2.0  # Add the last function evaluation divided by 2 (ending point of the trapezoids)

    return s * h  # Multiply the sum by the height of the trapezoids to get the approximate area
