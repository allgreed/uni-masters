import pytest
from main import solve, brute_force, distance

HARDCODED_CASES = [
  (
      ((1, 1),
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
  ), {(10, 2.5), (10, 3.5)})
]

CASES = [
(
  (1, 1),
  (1, 2),
  (1, 3),
  (1, 4),
  (1, 5),
  (1, 6),
  (1, 7),
  (1, 8),
  (1, 9),
  (1, 10),
),
(
  (1, 1),
  (2, 1),
  (3, 1),
  (4, 1),
  (5, 1),
  (6, 1),
  (7, 1),
  (8, 1),
  (9, 1),
  (10, 1),
),
# (
  # (1, 1),
  # (1, 1),
  # (1, 1),
  # (1, 1),
  # (1, 1),
  # (1, 1),
  # (1, 1),
  # (1, 1),
  # (1, 1),
  # (1, 1),
# ),
(
  (0, 0),
  (1, 0),
  (2, 0),
  (3, 0),
  (4, 2),
  (5, 2),
  (6, 2),
  (7, 2),
  (8, 3),
  (9, 3),
  (10, 3),
  (11, 3),
),
]

def test_brute():
    case = HARDCODED_CASES[0]

    data_in, expected_output = case
    assert brute_force(data_in) == expected_output


@pytest.mark.parametrize("case", CASES)
def test_solve(case):
    points = case
    test_solution = solve(points)
    refference_solution = brute_force(points)
    print(test_solution, refference_solution)
    assert distance(*test_solution) == distance(*refference_solution)
