
def horner_iter(poly: list, n: int, x: int) -> int:
    """
    Calculate the value of a polynomial using the Horner method.

    The Horner method efficiently evaluates a polynomial of the form:
    poly[0] * x^(n-1) + poly[1] * x^(n-2) + ... + poly[n-1]

    :param poly: List of coefficients in the polynomial.
    :param n: Degree of the polynomial (non-negative integer).
    :param x: The value at which to evaluate the polynomial.
    :return: Value of the polynomial function at the given x.
    :raises ValueError: If n is not a non-negative integer.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Degree of the polynomial must be a non-negative integer")

    result = poly[0]
    for i in range(1, n):
        result = result * x + poly[i]

    return result


def horner_recursive(poly: list, n: int, x: int) -> int:
    """
    Calculate the value of a polynomial using the Horner method (recursive version).

    The Horner method efficiently evaluates a polynomial of the form:
    poly[0] * x^(n-1) + poly[1] * x^(n-2) + ... + poly[n-1]

    :param poly: List of coefficients in the polynomial.
    :param n: Degree of the polynomial (non-negative integer).
    :param x: The value at which to evaluate the polynomial.
    :return: Value of the polynomial function at the given x.
    :raises ValueError: If n is not a non-negative integer.
    """

    if not isinstance(n, int) or n < 0:
        raise ValueError("Degree of the polynomial must be a non-negative integer")
    if n == 0:
        return poly[0]

    return x * horner_recursive(poly, n - 1, x) + poly[n]
