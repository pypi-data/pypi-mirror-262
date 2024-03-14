

def point_position(line_point1: tuple[int | float, int | float],
                   line_point2: tuple[int | float, int | float],
                   test_point: tuple[int | float, int | float]) -> int:
    """
    Determines the position of a point relative to a line.

    :param line_point1: First point defining the line.
    :param line_point2: Second point defining the line.
    :param test_point: Point to test.
    :return: 1 if the point is to the left of the line, -1 if to the right, and 0 if on the line.
    """
    x1, y1 = line_point1
    x2, y2 = line_point2
    x, y = test_point

    # Calculate the position using the cross product of vectors
    # (line_point1 -> line_point2) and (line_point1 -> test_point)
    position = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)

    # Return the sign of the result
    return (position > 0) - (position < 0)
