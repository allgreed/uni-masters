import statistics
import matplotlib.pyplot as plt
from pyeasyga import pyeasyga


# (name, price, weight)
data = [
("zegar", 100, 7),
("obraz-pejzaż", 300, 7),
("obraz-portret", 200, 6),
("radio", 40, 2),
("laptop", 500, 5),
("lampka nocna", 70, 6),
("srebrne sztućce", 100, 1),
("porcelana", 250, 3),
("figura z brązu", 300, 10),
("skórzana torebka", 280, 3),
("odkurzacz", 300, 15),
]

WEIGHT_LIMIT = 25


class MyGA(pyeasyga.GeneticAlgorithm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.best_historical_fintess = []
        self.mean_historical_fintess = []
        self.fitness_function = self.fitness

    def fitness(self, individual, data):
        selected_items = select_items_for_indvidual(individual, data)
        total_weight = sum(map(select_key(2), selected_items))
        total_price = sum(map(select_key(1), selected_items))

        if total_weight <= WEIGHT_LIMIT:
            return (total_price, total_weight)
        else:
            return (0, 0)

    def run(self):
        self.create_first_generation()

        self._report()

        for _ in range(1, self.generations):
            self.create_next_generation()
            self._report()

    def _report(self):
        self.best_historical_fintess.append(self.best_individual()[0][0])
        self.mean_historical_fintess.append(statistics.mean(map(select_key(0), map(lambda c: c.fitness, self.current_generation))))


def select_items_for_indvidual(individual, data):
    return [data[i] for i, include in enumerate(individual) if include]


def select_key(k):
    def _wrapper(data):
        return data[k]
    return _wrapper

if __name__ == "__main__":
    ga = MyGA(data,
        population_size=25, # makes the plot a bit more interesting
        generations=100,
        mutation_probability=0.05,
        elitism=True,
    )
    ga.run()

    ble, individual = ga.best_individual()
    items = select_items_for_indvidual(individual, data)
    total_price, total_weight = ble

    print(individual)
    print(list(map(select_key(0), items)))
    print(total_price)
    print(total_weight)

    plt.plot(range(100), ga.best_historical_fintess, 'r-')
    plt.plot(range(100), ga.mean_historical_fintess, 'b-')
    plt.show()
