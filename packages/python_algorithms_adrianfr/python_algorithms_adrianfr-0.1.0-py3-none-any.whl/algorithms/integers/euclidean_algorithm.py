

def gcd(a: int, b: int) -> int:
    """
    Compute the greatest common divisor (GCD) of two integers using the Euclidean algorithm.

    :param a: The first integer.
    :param b: The second integer.
    :return: The greatest common divisor of integers a and b.
    :raises ValueError: If either a or b is not an integer.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Both values a and b must be integers")

    while b:
        a, b = b, a % b

    return abs(a)


def gcd_recursive(a: int, b: int) -> int:
    """
    Compute the greatest common divisor (GCD) of two integers in a recursive way using the Euclidean algorithm.

    :param a: The first integer.
    :param b: The second integer.
    :return: The greatest common divisor of integers a and b.
    :raises ValueError: If either a or b is not an integer.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Both values a and b must be integers")

    return a if b == 0 else gcd_recursive(b, a % b)
