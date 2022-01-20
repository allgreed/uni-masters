#!/usr/bin/env python
import itertools
import operator

K = 7
M = 4
PRINT = True

LABELS = [False for i in range(K)] + [True for i in range(M)]

def main():
    print("M", M, "K", K)

    b = generate_necklaces(LABELS)

    result = filter(is_any_man_next_to_man, b)

    c = iter_count_exhaust(result)
    print(c)


def is_any_man_next_to_man(seq) -> bool:
    if seq[0] and seq[-1]:
        return False

    for i in range(len(seq) - 1):
        if seq[i] and seq[i + 1]:
            return False

    return True


def is_man(label):
    return label[0] == "m"

# =====


def is_good_man(label):
    # TODO: what makes a good man?
    return ...


def generate_necklaces(labels):
    # the /n aspect really shows here
    # naive implementation would be *much* worse
    ble = labels[0]
    result = itertools.permutations(LABELS[1:], len(LABELS) - 1)
    return map(lambda seq: [ble] + list(seq), result)


def iter_count_exhaust(it):
    c = 0
    for _ in it:
        c += 1

    return c


if __name__ == "__main__":
    main()
