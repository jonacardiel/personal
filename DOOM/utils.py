"""
utils.py

Contains general utility functions used across different game modules.
"""

import math

def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculates the Euclidean distance between two points.
    :param x1: X-coordinate of the first point.
    :param y1: Y-coordinate of the first point.
    :param x2: X-coordinate of the second point.
    :param y2: Y-coordinate of the second point.
    :return: The distance between the two points.
    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def angle_between_points(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculates the angle in degrees from point 1 to point 2.
    :param x1: X-coordinate of the first point.
    :param y1: Y-coordinate of the first point.
    :param x2: X-coordinate of the second point.
    :param y2: Y-coordinate of the second point.
    :return: Angle in degrees (0-360).
    """
    dx = x2 - x1
    dy = y2 - y1
    return math.degrees(math.atan2(dy, dx)) % 360
