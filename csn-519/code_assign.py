#!/usr/bin/env python3
import numpy as np

np.set_printoptions(linewidth=500)

graph = np.zeros((13, 13))

d = {
    1: [4],
    2: [3, 4],
    3: [2, 4, 5],
    4: [1, 2, 3, 5, 7],
    5: [3, 4, 6, 8],
    6: [5, 7],
    7: [4, 6, 8],
    8: [5, 7, 9, 10],
    9: [8, 10, 11],
    10: [8, 9, 12],
    11: [9, 12, 13],
    12: [10, 11, 13],
    13: [11, 12]
}

for k in d:
    for v in d[k]:
        graph[k - 1][v - 1] = 1
        graph[v - 1][k - 1] = 1

def get_eigenpair(mat):
    """
    uses power method to find leading eigenpair
    """
    print("starting power method")
    n = len(mat)
    start = np.mat([[1] for _ in range(n)])

    print(mat)
    print(start)

    for i in range(n - 1):
        print(i + 1)
        start = mat * start
        print(start)

    m1 = np.linalg.norm(start)
    start  = mat * start
    print(n)
    print(start)
    m2 = np.linalg.norm(start)
    eigenvalue = m2 / m1
    eigenvector = start / m2 # normalize eigenvector

    print(f"{eigenvector = }")
    print(f"{eigenvalue = }")

    return eigenvector, eigenvalue

A = graph

get_eigenpair(graph)

K = np.array(graph * np.mat([[1]] * 13))
print(f"{K = }")

M = 0
for arr in K:
    M += arr[0]

print(f"{M = }")

B = np.zeros((13, 13))


for i in range(13):
    for j in range(13):
        B[i][j] = A[i][j] - (K[i][0] * K[j][0] / M)

print(f"{B = }")

eigenvector, _ = get_eigenpair(B)

s = [[0] for _ in range(13)]
for i, v in enumerate(eigenvector):
    if v > 0:
        s[i][0] = 1
    else:
        s[i][0] = -1

s = np.mat(s)
print(f"{s = }")
# print(np.transpose(s))
# print(B * np.mat(s))
print("Modularity = ", 0.5 * np.transpose(s) * B * s)

