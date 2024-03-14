from typing import Callable


def bisection(func: Callable[..., float], a: float, b: float, eps: float) -> float:
    """
    Function is used to find the approximate roots of the function by using bisection algorithm.
    :param func: Function to find the roots
    :param a: Starting point of where we look for roots
    :param b: Ending point of where we look for roots
    :param eps: Epsilon for finding roots
    :return: Root of the function func
    """
    if not callable(func):
        raise ValueError("Provided function must be callable")

    try:
        func(a)
        func(b)
    except Exception as e:
        raise ValueError("Function must be continuous on the interval [a, b]") from e

    if func(a) * func(b) >= 0:
        raise ValueError("Initial values a and b must have opposite signs")

    c = a
    while (b - a) >= eps:
        # Find middle point
        c = (a + b) / 2

        # Check if middle point is root
        if func(c) == 0.0:
            return c  # If c is exactly the root, return it immediately

        # Decide the side to repeat the steps
        if func(c) * func(a) < 0:
            b = c
        else:
            a = c

    return (a + b) / 2  # Return the approximate root
