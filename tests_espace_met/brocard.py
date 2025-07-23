import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import Levenshtein

# Données
P = ["senat", "loi", "1931"]
T = ["semat", "l0i", "1931", "740"]

# Matrice de distances Levenshtein
def compute_distance_matrix(P, T):
    return np.array([[Levenshtein.distance(p, t) for t in T] for p in P])

D = compute_distance_matrix(P, T)

# Test Brocard-métrique (triangles équilibrés)
def brocard_metric_score(D, epsilon=1.0):
    n, m = D.shape
    triplets = []

    for i in range(n):
        for j, k in combinations(range(m), 2):
            d_ij = D[i, j]
            d_ik = D[i, k]
            d_jk = Levenshtein.distance(T[j], T[k])

            delta = abs(d_ij - (d_ik + d_jk))
            if delta < epsilon:
                triplets.append((P[i], T[j], T[k], delta))

    return triplets

triplets = brocard_metric_score(D, epsilon=1.5)

# Affichage
print("Triplets Brocard-métriques détectés :")
for (p, t1, t2, delta) in triplets:
    print(f"  {p} -- {t1} -- {t2} | Δ: {delta:.2f}")
