import functools
from collections import defaultdict

import networkx as nx
import matplotlib.pyplot as plt
from networkx import Graph


def main():
    g = nx.generators.trees.random_tree(15, seed=1)

    print(solve(g))
    # pos = nx.spring_layout(g, seed=225)
    # nx.draw(g, pos)
    # plt.show()


def solve(g):
    root = next(iter(g.nodes)) # arbitrary picking one
    ct = build_children_table(root, g)
    return max_independent_set(root, ct)


def max_independent_set(v, ct):
    _children = lambda v: ct[v]

    @functools.lru_cache(maxsize=None)
    def _max_i_subset(v):
        return max(sum(map(_max_i_subset, _children(v))), 1 + sum(map(_max_i_subset, sum(map(_children, _children(v)), []))))

    return _max_i_subset(v)


def build_children_table(root, g):
    result = defaultdict(set)

    def f(v, g, table):
        chld = table[v].union(set(g[v].keys()).difference(set(table.keys())))
        table[v] = list(chld)
        for v in chld:
            f(v,g,table)

    f(root, g, result)
    
    return result

if __name__ == "__main__":
    main()
