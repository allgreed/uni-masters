import pytest
from main import asplit, query


HARDCODED_CASES = [
    (
        [
            [4,4],
            [3,3],
            [2,2],
            [1,1],
            [0,0]
        ],
        [
            [1, 1],
            [3, 3],
        ],
        {
            (2,2),
            (1,1),
            (3,3),
        },
    ),
    (
        [
            [4,4],
            [3,3],
            [2,2],
            [1,1],
            [0,0]
        ],
        [
            [0, 0],
            [4, 4],
        ],
        {
            (4,4),
            (3,3),
            (2,2),
            (1,1),
            (0,0)
        },
    ),
    (
        [
            [4,4],
            [3,3],
            [2,2],
            [1,1],
            [0,0]
        ],
        [
            [3, 0],
            [4, 2],
        ],
        set()
    ),
]


@pytest.mark.parametrize("case", HARDCODED_CASES)
def test_main(case):
    _points, area, expected = case
    points = list(map(tuple, _points))

    kdt = asplit(points, 0)
    assert set(query(*area, kdt)) == expected
