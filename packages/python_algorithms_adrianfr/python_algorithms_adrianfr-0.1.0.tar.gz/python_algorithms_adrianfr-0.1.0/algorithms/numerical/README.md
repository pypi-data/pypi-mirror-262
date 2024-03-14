## Numerical


### Table of content
* [Bisection root finding](#bisection-root-finding)
* [Fast exponentiation](#fast-exponentiation)
* [Horner algorithm](#horner-algorithm)
* [Rectangular integration](#rectangular-integration)
* [Square root](#square-root)
* [Trapezoid integration](#trapezoid-integration)



### Bisection root finding
    The bisection method is used to find the roots of a polynomial equation.
    It separates the interval and subdivides the interval in which the root 
    of the equation lies. The principle behind this method is the intermediate
    theorem for continuous functions. It works by narrowing the gap between 
    the positive and negative intervals until it closes in on the correct answer. 
    This method narrows the gap by taking the average of the positive and negative 
    intervals. It is a simple method and it is relatively slow. The bisection method 
    is also known as interval halving method, root-finding method, binary search 
    method or dichotomy method.

    Let us consider a continuous function “f” which is defined on the closed interval
    [a, b], is given with f(a) and f(b) of different signs. Then by intermediate 
    theorem, there exists a point x belong to (a, b) for which f(x) = 0.

    For any continuous function f(x),

    1. Find two points, say a and b such that a < b and f(a)* f(b) < 0
    2. Find the midpoint of a and b, say “t”
    3. t is the root of the given function if f(t) = 0; else follow the next step
    4. Divide the interval [a, b] – If f(t) * f(a) <0, there exist a root between
    t and a – else if f(t) *f (b) < 0, there exist a root between t and b
    5. Repeat above three steps until f(t) = 0.

    The bisection method is an approximation method to find the roots of the given 
    equation by repeatedly dividing the interval. This method will divide the 
    interval until the resulting interval is found, which is extremely small.

### Fast exponentiation
    Fast exponentiation, also known as exponentiation by squaring, is an algorithm
    that efficiently computes the power of a number. This algorithm reduces the number
    of multiplication operations required to compute large exponentiations, making it
    particularly useful for large numbers. Standard exponentiation of expression a^n 
    needs as many as n - 1 multiplications and the algorithm for fast exponentiation
    allows to perform this step needing max 2 * log(2)n multiplications - so its very fast.

    How Fast Exponentiation Works
    1. Divide and Conquer:
    The algorithm uses a divide-and-conquer strategy to break down the exponentiation 
    problem into smaller subproblems.
    2. Recursive Calculation:
    It recursively computes the result for the smaller subproblems.
    3. Combining Results:
    The results from the subproblems are combined to obtain the final exponentiation result.
    4. Efficiency:
    The fast exponentiation algorithm significantly reduces the number of multiplication
    operations compared to naive exponentiation.

### Horner algorithm
    Horner's algorithm, also known as Horner's method or Horner's rule, is an efficient
    method for evaluating polynomials. It reduces the number of multiplication operations
    needed to compute the value of a polynomial at a specific point.

    How Horner's Algorithm Works
    1. Iterative Evaluation:
    The algorithm evaluates the polynomial by iterating through its coefficients.
    2. Accumulation of Values:
    It accumulates the result by multiplying the current accumulated value by the
    variable x and adding the next coefficient.
    3. Efficiency:
    Horner's algorithm requires fewer multiplications than the naive method of expanding 
    the polynomial, making it more efficient.

### Rectangular integration
    This algorithm performs numerical integration using the rectangular or midpoint 
    method. It approximates the integral of a function by summing the areas of 
    rectangles formed by the function's values at midpoints of subintervals.
    
    How rectangular integration method works:

    1.Subinterval Width Calculation:
    The width of each subinterval is calculated as 
    (upper_limit - lower_limit) / num_rectangles.
    2. Midpoint Evaluation:
    The function evaluates the given function func at the midpoints of each subinterval.
    3. Summation of Areas:
    The areas of rectangles are calculated using the function values at midpoints and
    summed to approximate the integral.
    4. Result:
    The result is the numerical approximation of the integral using the rectangle method.
    5. Time Complexity:
    The time complexity of the algorithm is O(n), where n is the number of rectangles.

### Square root
    The square_root function calculates the square root of a non-negative integer using 
    the Babylonian (Herons's) method. It iteratively refines the estimate until the 
    specified precision is reached.
    
    How square root function works:
    1. Initial Approximation:
    The algorithm starts with an initial approximation using a = 1.0 and b = p.
    2. Iterative Refinement:
    It iteratively refines the estimate using the Babylonian method until the 
    absolute difference between a and b is less than the specified precision eps.
    3. Rounding:
    The final result is rounded to the specified precision using the round function 
    and the negative logarithm of eps.

### Trapezoid integration
    One method of determining the area bounded by the graph of a function, the OX 
    axis and two lines parallel to the OY axis is the trapezoid method. The name 
    of this method comes from the fact that a given area is divided into many 
    rectangular trapezoids. 

    1. Subinterval Width Calculation:
    The width of each subinterval is calculated as (b - a) / n.
    2. Endpoint and Midpoint Evaluation:
    The function evaluates the given function f at the endpoints and midpoints of
    each subinterval.
    3. Summation of Trapezoid Areas:
    The areas of trapezoids are calculated using the function values at endpoints 
    and midpoints and summed to approximate the integral.
    4. Result:
    The result is the numerical approximation of the integral using the trapezoidal method.
    5. Time Complexity:
    The time complexity of the algorithm is O(n), where n is the number of trapezoids.