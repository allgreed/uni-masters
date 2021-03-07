import numpy as np


a, b = 123, 321
print(a*b)

v1, v2 = np.array([3, 8, 9, 10, 12]), np.array([8, 7, 7, 5, 6])
print(v1 + v2, v1 * v2)

print(v1.dot(v2), np.linalg.norm(v1-v2))

m1, m2 = np.eye(3), np.identity(3)
print(m1 * m2)
print(np.matmul(m1, m2))

x = np.random.randint(1, 100, size=50)
xmax =  max(x)
xmin = min(x)
xmean = np.mean(x)
xstedv = np.std(x) 

def normalize_x(x: int) -> int:
    return (x - xmin) / (xmax - xmin)

z = np.vectorize(normalize_x)(x)

xmax_indices = np.where(x == xmax)[0].tolist()
print(xmax, xmax_indices, [z[i] for i in xmax_indices])
