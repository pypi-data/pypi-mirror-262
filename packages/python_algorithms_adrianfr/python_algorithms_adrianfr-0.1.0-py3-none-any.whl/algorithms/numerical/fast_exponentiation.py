
def fast_exp(b: int, exp: int) -> int:
    """
    Efficiently calculates the power of an integer using fast exponentiation.

    :param b: Base integer
    :param exp: Exponent
    :return: Result of a raised to the power of n
    """

    if exp == 0:
        return 1

    if exp % 2 == 0:
        w = fast_exp(b, exp // 2)
        return w * w

    return b * fast_exp(b, exp - 1)
