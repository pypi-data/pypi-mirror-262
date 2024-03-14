from typing import Callable


def rect_integrate(func: Callable[[float], float], lower_limit: float, upper_limit: float, num_rectangles: int) -> float:
    """
    Calculate the area under the curve of a given function using the rectangle method for numerical integration.

    :param func: The function for which the area needs to be calculated.
    :param lower_limit: The lower limit of integration.
    :param upper_limit: The upper limit of integration.
    :param num_rectangles: The number of rectangles to use for approximating the area (positive integer).

    :return: The approximate area under the curve of the given function.
    :raises TypeError: If 'func' is not a callable function, or if 'lower_limit' or 'upper_limit' are
    not integers values.
    :raises ValueError: If 'num_rectangles' is not a positive integer.
    """
    if not callable(func):
        raise TypeError("The 'func' parameter must be a callable function.")
    if not isinstance(lower_limit, (int, float)):
        raise TypeError("The 'lower_limit' parameter must be a integers value.")
    if not isinstance(upper_limit, (int, float)):
        raise TypeError("The 'upper_limit' parameter must be a integers value.")
    if not isinstance(num_rectangles, int) or num_rectangles <= 0:
        raise ValueError("The 'num_rectangles' parameter must be a positive integer.")

    cumulative_area = 0.0

    rectangle_width = (upper_limit - lower_limit) / num_rectangles

    trailing_x = lower_limit
    leading_x = lower_limit + rectangle_width

    while leading_x <= upper_limit:
        area = func((trailing_x + leading_x) / 2.0) * rectangle_width
        cumulative_area += area

        leading_x += rectangle_width
        trailing_x += rectangle_width

    return cumulative_area
