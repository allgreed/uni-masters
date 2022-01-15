import math
from typing import Set
from contextlib import suppress
import itertools
import bisect


def main():
    points = [
      (1, 1),
      (2, 2),
      (4, 1),
      (10, 2.5),
      (10, 3.5),
      (5, 5),
      (4, 4),
      (2, 10),
      (0, 6),
      (2, 5),
      (0, 0),
      ]
    print(the_solve(points))


def solve(points):
    if len(points) < 2:
        raise ValueError("Too few points to select a pair")

    if len(points) <= 3:
        return brute_force(points)

    x_sorted_points = sorted(points, key=lambda x: x[0])
    return divide_and_conquer(x_sorted_points)


def brute_force(points) -> Set["Point"]:
    pair = {points[0], points[1]}
    min_distance = distance(points[0], points[1])
    for p1, p2 in itertools.combinations(points, 2):
        d = distance(p1, p2)
        if d < min_distance:
            min_distance = d
            pair = {p1, p2}

    return pair


def divide_and_conquer(points):
    split_idx = len(points) // 2

    left_points, right_points = points[:split_idx], points[split_idx:]
    left_result, right_result = solve(left_points), solve(right_points)

    best_of_sections = min(map(distanced_point_tuple, [left_result, right_result]))

    split_x = points[split_idx][0] + points[split_idx - 1][0] / 2
    lm = split_x - points[split_idx][0] 
    rm = points[split_idx + 1][0] - split_x
    d = best_of_sections[0]

    # since Python 3.9 doesn't have to be materialized
    xes = list(map(lambda p: p[0], points))
    l = bisect.bisect(xes, split_x - (d - rm))
    h = bisect.bisect_left(xes, split_x + (d - lm)) + 1 or len(points)
    intersection_points = points[l:h]
    # otherwise we'd be stuck forever
    if len(intersection_points) == len(points):
        return brute_force(points)

    if len(intersection_points) >= 2:
        result = min(best_of_sections, distanced_point_tuple(solve(intersection_points)))
    else:
        result = best_of_sections

    r_d, r_p1, r_p2 = result
    return {r_p1, r_p2}


def distanced_point_tuple(pointset):
    pointset = iter(pointset)
    p1 = next(pointset)
    p2 = next(pointset)
    return (distance(p1, p2), p1, p2)


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

if __name__ == "__main__":
    main()
