import time
from collections import defaultdict
from typing import Optional
from pprint import pprint

from labyrinth import Labyrinth, Field, make_labyrinth
from gen_1_bouncing_hypothesis import compute


def main() -> None:
    l0 = make_labyrinth(5,5, obstacle_fill_percent=15)

    l1 = make_labyrinth(5,5, obstacle_fill_percent=30)

    l2 = make_labyrinth(10,10, obstacle_fill_percent=20)

    l3 = make_labyrinth(20,20, obstacle_fill_percent=20)
    l3.obstacles.remove((0, 1))
    l3.obstacles.remove((11, 7))

    ls = [l0, l1, l2, l3]

    for i, l in enumerate(ls):
        print(i)
        start = time.time()
        x = solve_flood_fill(l)
        end = time.time()
        print("ff", x is not None and x <= 40, "Time elapsed:", end - start)

        start = time.time()
        x = compute(l, False)[1]
        end = time.time()
        print("genetic", x is not None and x <= 0, "Time elapsed:", end - start)


def solve_flood_fill(l: Labyrinth) -> Optional[int]:
    q = [(l.start, 0)]
    visited = set()
    t = defaultdict(None)

    while q:
        item = q.pop() 
        point, _n = item
        x, y = point
        n = _n + 1

        try:
            reachable = l[point]
        except ValueError:
            pass
        else:
            if point not in visited and reachable:
                q = [(p, n) for p in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]] + q
                t[point] = _n
        finally:    
            visited.add(point)

    return t[l.end]


if __name__ == "__main__":
    main()
