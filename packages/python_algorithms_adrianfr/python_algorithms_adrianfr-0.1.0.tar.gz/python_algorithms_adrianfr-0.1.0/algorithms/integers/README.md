## Algorithms on integers

### Table of content
* [Euclidean algorithm](#euclidean-algorithm)
* [Fibonacci sequence](#fibonacci)
* [Checking if number is prime](#checking-if-number-is-prime)
* [Checking if number is perfect](#checking-if-number-is-perfect)
* [Numeral systems conversion](#numeral-systems-conversion)
* [Number decomposition](#number-decomposition)

### Euclidean algorithm
    The Euclidean algorithm is a way to find the greatest common divisor
    of two positive integers, a and b. GCD of two numbers is the largest
    number that divides both of them. A simple way to find GCD is to 
    factorize both numbers and multiply common prime factors.
    The solution method is as follows. We choose the larger of the two
    numbers and replace it with the difference of the larger and the 
    smaller. We repeat this action until we get two values that are the same.
    Let's follow the example for the numbers 12 and 18. 
    It is known that GCD(12, 18) = 6
                12 | 18
                12 | 18 - 12 = 6
        12 - 6 = 6 | 6 
    
    For numbers 28 and 14:
                28 | 24
       28 - 24 = 4 | 24
                 4 | 24 - 4 = 20
                 4 | 20 - 4 = 16
                 4 | 16 - 4 = 12
                 4 | 12 - 4 = 8
                 4 | 8 - 4 = 4
    
    It is worth noting that this algorithm is very inefficient. When we choose
    the numbers appropriately, the number of operations will increase significantly.

    For the optimal solution of the GCD, we proceed as follows:
    Suppose we are determining the GCD of two natural numbers a and b.
    In each pass of the loop, we perform two operations:
    a = b
    b = a mod b
    These steps are repeated until the variable b reaches zero. 
    The variable a will then store the greatest common divisor of the 
    numbers given in the input.

    In Python you can use gcd algorithm from Math module instead of implementing your own.

### Fibonacci
    We define the Fibonacci sequence as follows:
    The first and second elements of the string are equal to 1. Each subsequent 
    element is obtained by adding the previous two together.
    The first few elements of this sequence according to the first definition 
    are as follows: 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
    
    There are two possible approaches for implementing this algorithm in Python:
    iterative and recursive. The iterative method is efficient and will determine 
    all the elements of the sequence without any problems, however the recursive 
    solution is very inefficient and is only suitable for determining a small number
    of elements of a Fibonacci sequence


### Checking if number is prime
    Let's start with the definition of a prime number. 
    A prime number is a natural number greater than 1 
    whose only natural divisors are the number 1 and itself. 
    Here are some of the prime numbers: 2, 3, 5, 7, 11 ...
    It is worth noting that there are infinitely many such 
    numbers. In order to determine whether a number is prime one 
    should examine its divisors. For a given number n, we check
    consecutive natural numbers belonging to the interval: [2...√n]
    If any of these numbers is a divisor, it means that our number
    is not prime. Why is it enough to check only numbers from 2 to
    the root of n ? Let's go through some examples and write out 
    the divisors for the following numbers: 24, 25 i 31.

### Checking if number is perfect
    A perfect number is defined as a positive integer that can be expressed 
    as the sum of its proper factors. Such a number is for example 6,
    because D6 = {1, 2, 3} and 6 = 1 + 2 + 3

    Algorithm:

    The algorithm iterates through all possible divisors of the number up to 
    the square root of the number. For each divisor i, it checks if 
    number % i == 0. If true, i and number // i are proper divisors.
    It calculates the sum of these proper divisors.

    Perfect Number Check:
    After calculating the sum of proper divisors, it checks if the sum equals 
    the original number. If the sum is equal to the number, the function 
    returns True, indicating that the number is perfect. Otherwise, it 
    returns False.

### Numeral systems conversion
    Problem of converting a decimal number to its representation in any
    numerical system  of base "b" will be covered here, where
    b ∈ {2, 3,..., 15, 16}
    The solution to the problem is analogous to the conversion from 
    the decimal to the binary system. We abbreviate a number in the decimal
    system by dividing by the base b until the value 0. On the right side we
    write down the remainder of dividing by b. The solution is the values on 
    the left side in reverse order.
    
    Let's go through some cases:
    Let's convert the number 100 into the system with base 3:
               100 | 100 mod 3 = 1
    100 div 3 = 33 | 33 mod 3 = 0
     33 div 3 = 11 | 11 mod 3 = 2
     11 div 3 = 3  |  3 mod 3 = 0
      3 div 3 = 1  |  1 mod 3 = 1
      1 div 3 = 0  |

    Then we write down the result in reverse order and get:
    100 = 10201

    Another example:
    Let's convert number 1201 into hexadecimal system:
                1201 | 1201 mod 16 = 1
    1201 div 16 = 75 |   75 mod 16 = 11(B)
       75 div 16 = 4 |    4 mod 16 =  4
        4 div 16 = 0 | 
    
    Result will be:
    1201 = 4B1
    
    One approach to solving the problem is the recursive solution

### Number decomposition
    Prime factorization involves finding the prime numbers that 
    multiply together to give the original number.

    1. Algorithm:
     - It starts with the smallest prime number, 2.
     - It iterates through all numbers from 2 up to the square root of n.
     - For each number k, it divides n by k as long as n is divisible by k.
     - If k divides n, it means k is a prime factor of n. So, k is appended
     to the list of factors, and n is divided by k.
     - The process continues until k * k > n.
    2. Remaining Number Check:
        After the loop, if the remaining value of n is greater than 1, it means n
        itself is a prime factor. So, n is appended to the list of factors.
    3. Result:
        The result is a list of prime factors of the given number.