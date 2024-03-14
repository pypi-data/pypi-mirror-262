

def fib_iter(n: int) -> int:
    """
    Calculate the nth number in the Fibonacci sequence iteratively.

    :param n: The position of the desired number in the Fibonacci sequence (non-negative integer).
    :return: The nth number in the Fibonacci sequence.
    :raises ValueError: If n is not a non-negative integer.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Value of n must be a non-negative integer")

    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b


def fib_recursive(n: int) -> int:
    """
    Calculate the nth number in the Fibonacci sequence recursively.

    :param n: The position of the desired number in the Fibonacci sequence (non-negative integer).
    :return: The nth number in the Fibonacci sequence.
    :raises ValueError: If n is not a non-negative integer.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Value of n must be a non-negative integer")

    if n <= 2:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)
