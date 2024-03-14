import math


class Triangle:

    def __init__(self, a: float, b: float, c: float) -> None:
        """
        Initializes a Triangle object with given side lengths.

        :param a: Length of side a
        :param b: Length of side b
        :param c: Length of side c
        :raises ValueError: If the provided side lengths do not form a valid triangle.
        """
        if self.is_triangle_valid(a, b, c):
            self.a = a
            self.b = b
            self.c = c
        else:
            raise ValueError("Cannot create a triangle from given values")

    def __str__(self) -> str:
        return f"Triangle(A: {self.a}, B: {self.b}, C: {self.c})"

    @staticmethod
    def is_triangle_valid(a: float, b: float, c: float) -> bool:
        """
        Checks the validity of a triangle based on its side lengths.

        :param a: Length of side a
        :param b: Length of side b
        :param c: Length of side c
        :return: True if the triangle is valid, else False.
        """
        return a + b > c and a + c > b and b + c > a

    def area(self) -> float:
        """
        Calculates the area of the triangle using Heron's formula.

        :return: Area of the triangle.
        """
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def height(self) -> float:
        """
        Calculates the height of the triangle.

        :return: Height of the triangle.
        """
        return 2 * self.area() / self.a

    def perimeter(self) -> float:
        """
        Returns the perimeter of the triangle.

        :return: Perimeter of the triangle.
        """
        return self.a + self.b + self.c

    def is_right(self) -> bool:
        """
        Checks if the triangle is a right-angled triangle.

        :return: True if the triangle is right-angled, else False.
        """
        a, b, c = sorted([self.a, self.b, self.c])
        return a ** 2 + b ** 2 == c ** 2

    def check_triangle_type(self) -> str:
        """
        Determines the type of the triangle.

        :return: Type of the triangle (Equilateral, Isosceles, or Scalene).
        """
        if self.a == self.b == self.c:
            return "Equilateral"
        elif self.a == self.b or self.b == self.c or self.c == self.a:
            return "Isosceles"
        else:
            return "Scalene"
