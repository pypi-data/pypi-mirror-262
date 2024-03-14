## Geometric properties


### Table of content
* [Triangle properties](#triangle-properties)
* [Point position](#point-position)
* [Point on segment](#point-on-segment)


### Triangle properties

    The properties of the triangle are:

        - The sum of all the angles of a triangle (of all types) is equal to 180°.
        - The sum of the length of the two sides of a triangle is greater than the 
            length of the third side.
        - In the same way, the difference between the two sides of a triangle is 
            less than the length of the third side.
        - The side opposite the greater angle is the longest side of all the three
            sides of a triangle.
        - The exterior angle of a triangle is always equal to the sum of the interior
            opposite angles. This property of a triangle is called an exterior 
            angle property.
        - Two triangles are said to be similar if their corresponding angles of both
            triangles are congruent and the lengths of their sides are proportional.
        - Area of a triangle = ½ × Base × Height
        - The perimeter of a triangle = sum of all its three sides

    Triangle Formula
    Area of a triangle is the region occupied by a triangle in a two-dimensional plane. 
    The dimension of the area is square units. The formula for area is given by;
           Area = 1/2 x Base x Height

    The perimeter of a triangle is the length of the outer boundary of a triangle. 
    To find the perimeter of a triangle we need to add the length of the sides of the triangle.
          P = a + b + c

    Semi-perimeter of a triangle is half of the perimeter of the triangle. It is represented by s.
          s = (a + b + c)/2
          where a, b and c are the sides of the triangle.

    By Heron’s formula, the area of the triangle is given by:
          A = √[s(s – a)(s – b)(s – c)]

          where ‘s’ is the semi-perimeter of the triangle.

    By the Pythagorean theorem, the hypotenuse of a right-angled triangle can be calculated by the formula:
          Hypotenuse^2 = Base^2 + Perpendicular^2

    The triangle is equilateral if all of the traingle sides have equal length.
    The triangle is isosceles if two of the sides have equal length.
    The triangle is scalene if all of the sides have different length.

### Point position
    Given a straight line defined by the equation:
    y = ax+b
    Where a and b are real numbers
    To check if the point P(xp, yp) lies on the straight line, substitute its coordinates into
    the equation of the straight line accordingly and see if it will be satisfied.

### Point on segment
    Let's start with one of the simpler algorithms - checking whether a point
    belongs to a straight line. Note that a straight line lying in the plane 
    is a set of points satisfying some equation. We can distinguish several 
    equations of straight lines. One of them is the directional equation, the
    formula of which we can write as:
    y = ax + b

    where:
    a - directional coefficient
    b - is the intercept

    In order to check whether a given point lies on a straight line, it is 
    necessary to check whether, after substituting its coordinates into the 
    equation of the straight line, the equation will be satisfied.

    If the straight line is parallel to the axis, we use the formula:
    x = b, where b is a certain constant.

    The straight line is described by the equation y = x. Also given are the 
    points A(1,3) and C(2,2)

    Let's check that the points lie on the straight line.
    
    We substitute the coordinates of the point A to the equation of the 
    straight line and we get:
    3 = 1
    The equation is contradictory. Therefore, the point does not lie on the segment.

    Now let's check how the situation is in the case of a point C.
    We substitute the coordinates into the formula of the function:
    2 = 2
    The equation holds, so the point lies on a segment.


