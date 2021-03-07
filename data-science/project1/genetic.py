from typing import Optional

from pyeasyga import pyeasyga

from labyrinth import Labyrinth, Field


from labyrinth import make_labyrinth


class MyGA(pyeasyga.GeneticAlgorithm):
    def __init__(self, l: Labyrinth, debug, *args, bouncing_strategy=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fitness_function = self.fitness
        self.l = l
        self.bouncing_strategy = bouncing_strategy
        self.debug = debug

    def fitness(self, individual, _):
        moves = decode_moves(individual)

        p = self.l.start
        x2, y2 = self.l.end
        distances = []
        bounces = 0

        for m in moves:
            _p = (p[0] + m[0], p[1] + m[1])

            try:
                if not self.l[_p]:
                    bounces += 1
                    continue
            except ValueError:
                bounces += 1
                continue

            p = _p

            x1, y1 = p
            d = ((((x2 - x1 ) ** 2) + ((y2 -y1) ** 2) ) **0.5)
            distances.append(d)

        sorted_distances = sorted(distances)

        self.debug["bounces"] = bounces

        if self.bouncing_strategy:
            return (sorted_distances[0], bounces, sorted_distances[1:])
        else:
            return sorted_distances


def solve_gen1(
        l: Labyrinth,
        debug=None,
        bouncing=False,  # it's likely that bouncing only improves bouncing
    ) -> Optional[int]:

    if debug is None:
        debug = {}

    # we'll trick PyEasyGA into getting 2 bits per move chromosome
    data = [None] * (40 * 2)
    ga = MyGA(l, debug, data,
        # custom toggles
        bouncing_strategy=bouncing,
        # PyEasyGA toggles
        population_size=50,
        generations=100,
        mutation_probability=0.05,
        elitism=True,
        maximise_fitness=False,
    )
    ga.run()

    debug["ga"] = ga


def decode_moves(individual, names: bool = False):
    move_groups = (zip(*(iter(individual),) * 2))

    MOVE_DECODE_T = {
        (0,0): ((1, 0), "RIGHT"),
        (0,1): ((0, 1), "DOWN"),
        (1,0): ((-1, 0), "LEFT"),
        (1,1): ((0, -1), "UP"),
    }

    return list(map(lambda m: MOVE_DECODE_T[m][names], move_groups))


def demo():
    debug_box = {}
    l = make_labyrinth(20,20, obstacle_fill_percent=20)
    l.obstacles.remove((0, 1))
    l.obstacles.remove((11, 7))
    print(l)

    solve_gen1(l, debug=debug_box)

    print(debug_box["ga"].best_individual())
    print(decode_moves(debug_box["ga"].best_individual()[1], names=True))

if __name__ == "__main__":
    demo()
