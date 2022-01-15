import pytest
from main import solve

import networkx as nx


EDGELIST = [
    (
        (
            (1,2),
            (1,3),
            (2,4),
            (2,5),
            (3,6),
            (3,7),
        )
        ,
        5
    ),
    (
        (
            (1,2),
            (1,3),
            (2,4),
            (4,8),
            (8,13),
            (3,5),
            (3,6),
            (3,7),
            (7,9),
            (7,10),
            (7,11),
            (7,12),
        )
        ,
        9
    ),
]


@pytest.mark.parametrize("edges,expected", EDGELIST)
def test_main(edges, expected):
    g = nx.Graph()
    for e in edges:
        g.add_edge(*e)

    assert solve(g) == expected
