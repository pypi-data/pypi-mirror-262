

def cross_product(x: tuple[int | float, int | float],
                  y: tuple[int | float, int | float],
                  z: tuple[int | float, int | float]) -> float:
    """
    Computes the cross product of vectors (XZ) and (XY).

    :param x: Tuple representing the coordinates of point X.
    :param y: Tuple representing the coordinates of point Y.
    :param z: Tuple representing the coordinates of point Z.
    :return: The cross product of vectors (XZ) and (XY).
    """
    x1, y1 = z[0] - x[0], z[1] - x[1]
    x2, y2 = y[0] - x[0], y[1] - x[1]
    return x1 * y2 - x2 * y1


def is_point_on_segment(x: tuple[int | float, int | float],
                        y: tuple[int | float, int | float],
                        z: tuple[int | float, int | float]) -> bool:
    """
    Checks if point Z (end of the first segment) lies on the segment XY.

    :param x: Tuple representing the coordinates of point X.
    :param y: Tuple representing the coordinates of point Y.
    :param z: Tuple representing the coordinates of point Z.
    :return: True if point Z lies on the segment XY, else False.
    """
    return (
        min(x[0], y[0]) <= z[0] <= max(x[0], y[0])
        and min(x[1], y[1]) <= z[1] <= max(x[1], y[1])
    )


def do_segments_intersect(a: tuple[int | float, int | float],
                          b: tuple[int | float, int | float],
                          c: tuple[int | float, int | float],
                          d: tuple[int | float, int | float]) -> bool:
    """
    Checks if two line segments AB and CD intersect.

    :param a: Tuple representing the coordinates of point A.
    :param b: Tuple representing the coordinates of point B.
    :param c: Tuple representing the coordinates of point C.
    :param d: Tuple representing the coordinates of point D.
    :return: True if line segments AB and CD intersect, else False.
    """
    v1 = cross_product(c, d, a)
    v2 = cross_product(c, d, b)
    v3 = cross_product(a, b, c)
    v4 = cross_product(a, b, d)

    # Check if the line segments intersect for larger numbers
    if (v1 > 0 > v2 or v1 < 0 < v2) and (v3 > 0 > v4 or v3 < 0 < v4):
        return True

    return True if (v1 == 0 and is_point_on_segment(c, d, a)
                    or v2 == 0 and is_point_on_segment(c, d, b)
                    or v3 == 0 and is_point_on_segment(a, b, c)
                    or v4 == 0 and is_point_on_segment(a, b, d)) else False
