import math
from dataclasses import dataclass


def is_prime(number: int) -> bool:
    """
    Check if a given number is a prime number.

    :param number: The number to check for primality (positive integer).
    :return: True if the number is prime, False otherwise.
    :raises ValueError: If the input is not a positive integer.
    """
    if not isinstance(number, int) or number <= 0:
        raise ValueError("Input must be a positive integer")

    if number < 2:
        return False
    return True


def is_perfect(number: int) -> bool:
    """
    Check if a given number is a perfect number.

    :param number: The number to be checked for perfection (positive integer).
    :return: True if the number is perfect, False otherwise.
    :raises ValueError: If the input is not a positive integer.
    """
    if not isinstance(number, int) or number <= 0:
        raise ValueError("Input must be a positive integer")

    divisor_sum, sq_root = 0, int(math.sqrt(number))

    for i in range(2, sq_root + 1):
        if number % i == 0:
            divisor_sum += i + number // i  # Use integer division for better accuracy

    if number == sq_root * sq_root:
        divisor_sum -= sq_root

    return divisor_sum == number


def number_decomposition(n: int) -> list[int]:
    """
    Perform the prime factorization of a natural number.

    :param n: The natural number to perform the decomposition on (non-negative integer).
    :return: List of prime factors of the given number.
    :raises ValueError: If n is not a non-negative integer.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer")

    factors = []
    k = 2

    while k * k <= n:
        while n % k == 0:
            factors.append(k)
            n //= k
        k += 1

    if n > 1:
        factors.append(n)

    return factors


@dataclass
class SystemConversion:
    """
    This class contains methods for converting a number from decimal system
    into a system with base specified as a class attribute
    """
    base: int

    def from_decimal_to_any_system(self, number: int) -> str:
        """
        Convert a number from decimal numerical system to the representation in any numerical system.

        :param number: The number to convert (non-negative integer).
        :return: The converted number as a string in the specified numerical system.
        :raises ValueError: If either the number is not a non-negative integer or the base is not a positive integer.
        """
        if not isinstance(number, int) or number < 0:
            raise ValueError("Number must be a non-negative integer")
        if not isinstance(self.base, int) or self.base <= 0:
            raise ValueError("System base must be a positive integer")

        if number == 0:
            return '0'

        result = ''
        while number > 0:
            remainder = number % self.base
            if remainder > 9:
                result = chr(ord('A') + remainder - 10) + result
            else:
                result = str(remainder) + result
            number //= self.base

        return result


