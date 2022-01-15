from dataclasses import dataclass


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

    kd_tree = asplit(points, 0)

    print(kd_tree)
    print(query((3,1), (5,2), kd_tree))


# <

def query(a, b, t):
    ax, ay = a  
    bx, by = b
    x1, x2 = sorted([ax, bx])
    y1, y2 = sorted([ay, by])

    if not isinstance(t, Tree):
        x, y = t
        if  x1 <= x <= x2 and y1 <= y <= y2:
            return [t]
        else:
            return []
    
    if t.node[0] == "x":
        c1, c2 = x1, x2
    else:
        c1, c2 = y1, y2

    if t.node[1] < c1:
        return query(a, b, t.right)
    elif t.node[1] >= c1 and t.node[1] < c2:
        return query(a, b, t.right) + query(a, b, t.left)
    elif t.node[1] >= c2:
        return query(a, b, t.left)
    else:
        assert 0 # unreachable


def asplit(points, axis):
    if len(points) == 1:
        return points[0]

    sp = sorted(points, key=lambda p: p[axis])
    split = len(sp) // 2 - 1
    while sp[split + 1][axis] == sp[split][axis]:
        split += 1

    l = sp[:split + 1]
    r = sp[split + 1:]
    assert l[-1][axis] < r[0][axis], f"{l[-1]} < {r[0]} along {'x' if not axis else 'y'} axis"

    return Tree(node=("x" if not axis else "y", sp[split][axis]), left=asplit(l, not axis), right=asplit(r, not axis))


@dataclass
class Tree:
    node: ...
    left: ...
    right: ...

    def is_leaf(self):
        return self.left is None and self.right is None

    @staticmethod
    def _nested_repr(obj, level=1):
        if obj is None:
            return ""

        if not isinstance(obj, Tree):
            return repr(obj)

        return "{0}\n{1}left: {2}\n{1}right: {3}".format(repr(obj.node), " "  * 4 * level, Tree._nested_repr(obj.left, level + 1), Tree._nested_repr(obj.right, level + 1))
        

    def __repr__(self):
        return self._nested_repr(self)


if __name__ == "__main__":
    main()
