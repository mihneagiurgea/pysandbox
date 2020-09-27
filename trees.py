from collections import namedtuple
import math

Point = namedtuple("Point", ["x", "y"])


def diff(end, start):
    return (end - start) % (math.pi * 2)
# private int distance(int alpha, int beta) {
#         int phi = Math.abs(beta - alpha) % 360;       // This is either the distance or 360 - distance
#         int distance = phi > 180 ? 360 - phi : phi;
#         return distance;
#     }


def solve(origin, angle, pts):
    # Returns an angle.
    pts = [Point(pt.x - origin.x, pt.y - origin.y) for pt in pts]

    pts_with_angle = [
        (math.atan2(pt.y, pt.x), pt) for pt in pts
    ]
    pts_with_angle.sort()

    # Loop around twice.
    pts_with_angle += pts_with_angle  # ?
    end_idx = 0
    sol_num = 0
    sol = None
    for start_idx in range(0, len(pts_with_angle)):
        start_angle = pts_with_angle[start_idx][0]
        # Advance end_idx while we're still within camera angle.
        while end_idx + 1 < len(pts_with_angle):
            next_pt = pts_with_angle[end_idx + 1]
            # print next_pt, pts_with_angle[start_idx], diff(next_pt[0],
            # start_angle), angle
            if diff(next_pt[0], start_angle) < angle:
                end_idx += 1
            else:
                break
        num = end_idx - start_idx + 1
        if num > sol_num:
            sol_num = num
            sol = (
                angle, num, pts_with_angle[start_idx], pts_with_angle[end_idx])
    return sol


print diff(-math.pi + 0.1, math.pi - 0.1)
print diff(0.5880026035475675, 0.4636476090008061)

pts = [
    Point(1, 1),
    Point(1, 2),
    Point(2, 1),
    Point(2, 2),
    Point(3, 2),
    Point(2, 3),
    Point(3, 3),
    Point(-3, -3),
]
pts = [
    Point(3, 2),
    Point(3, -1),
    Point(-2, -1),
    Point(-2, 3),
    Point(-3, 1),
    Point(-4, 1),
    Point(-5, 1)
]
print solve(Point(1, 1), math.pi / 2, pts)


"""
API
"""


class Context(object):

    def __init__(self, origin, angle):
        pass

    def add_object(self, pt):
        pass

    def remove_object(self, pt):
        pass

    def query(self):
        pass
