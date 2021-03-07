import pytest
from labyrinth import Labyrinth, make_labyrinth, Field
from main import solve_flood_fill, make_labyrinth


def test_ff():
    # in generate solve_flood_fill(make_labyrinth(x, y, 0)) == x + y - 2
    assert solve_flood_fill(make_labyrinth(10, 10, 0)) == 18


def test_labirynth():
    assert make_labyrinth(5,5) == make_labyrinth(5,5)
    assert Labyrinth(5,5)[1,1] is Field.Reachable
    assert Labyrinth(5,5)[3,3] is Field.Reachable

    with pytest.raises(ValueError):
        Labyrinth(5,5)[3,100]
    with pytest.raises(ValueError):
        Labyrinth(5,5)[100,3]
    with pytest.raises(ValueError):
        Labyrinth(5,5)[-3,0]
    with pytest.raises(ValueError):
        Labyrinth(5,5)[0,-3]

    assert Labyrinth(5, 3)

    with pytest.raises(ValueError):
        Labyrinth(-3, 5)
    with pytest.raises(ValueError):
        Labyrinth(5, -3)
