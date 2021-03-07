import matplotlib.pyplot as plt
import numpy as np

data = [
    # accuracy, distribution accuracy, label
    (0.6483333333333333, 0.9853333333333334 ,"DS=1/40; BS=20; lr=1e-3; best run - 63%"),
    (0.522569082649106, 0.6867113274481658 ,"DS=1/1; BS=20; lr=1e-3 - 35%"),
    (0.32371941816363103, 0.32439731919575876 ,"DS=1/40; BS=20; lr=1e-2 - 10%"),
    (0.5122327345475763, 0.6701231558981302 ,"DS=1/40; BS=1000; lr=1e-3 - 34%"),
    (0.5693744008669195, 0.8295446538350285 ,"DS=1/40; BS=1000; lr=5e-3 - 47%"),
]


x = list(map(lambda t: t[0], data))
y = list(map(lambda t: t[1], data))

labels = list(map(lambda t: t[2], data))

plt.subplots_adjust(bottom = 0.1)
plt.scatter(x, y, marker='o', s=200)

corrections = [
    (0.3, -0.035),
    (0, 0),
    (0.3, 0.025),
    (0.3, -0.045),
    (0, 0),
]

for label, x, y, c in zip(labels, x, y, corrections):
    plt.annotate(
        label,
        xy=[sum(x) for x in zip((x, y), c)], xytext=(-20, 0),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        )

np.random.seed(1)
w = np.random.randn(6)

def f(x, y):
    return x * y - 0.48

X, Y = np.mgrid[-2:2:100j, -2:2:100j]

C = plt.contour(X, Y, f(X, Y), 6, levels=[0])
plt.clabel(C, inline=1, fontsize=10, inline_spacing=-30, fmt="benchmark", manual=[(0.823, 0.54)])
plt.xlim(0, 1)
plt.ylim(0.25, 1)

plt.ylabel('distribution accuracy')
plt.xlabel('accuracy')

plt.show()
