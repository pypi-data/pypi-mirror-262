import math


def square_root(p: int, eps: float) -> float:
    """
    Calculate the square root of a number using the Babylonian (Herons's) method.

    :param p: Integer to calculate the square root of (non-negative integer).
    :param eps: Precision of the rounding (positive float).
    :return: Square root with specified precision.
    :raises ValueError: If p is not a non-negative integer or eps is not a positive float.
    """
    if not isinstance(p, int) or p < 0:
        raise ValueError("p must be a non-negative integer.")
    if not isinstance(eps, (float, int)) or eps <= 0:
        raise ValueError("accuracy value eps must be a positive float.")

    a, b = 1.0, p

    while abs(a - b) >= eps:
        a, b = (a + b) / 2.0, p / a

    result = (a + b) / 2.0
    return round(result, int(-math.log10(eps)))
