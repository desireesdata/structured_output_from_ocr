import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Levenshtein import distance as lev

# Données
T = ["sénat", "loi", "1931", "740", "8"]
P = ["semat", "l0i", "1931", "74O"]

# Paramètre
epsilon = 0.5

# Etape 1 : matrice des distances
D = np.array([[lev(p, t) for t in T] for p in P])
P_to_T = np.argmin(D, axis=1)
T_to_P = np.argmin(D, axis=0)

# Etape 2 : appariements mutuels
mutual_pairs = [(i, j) for i, j in enumerate(P_to_T) if T_to_P[j] == i]

# Etape 3 : filtrage métrique local
def is_coherent(i, j):
    for k in range(len(T)):
        if k == j:
            continue
        k_p = T_to_P[k]
        if k_p >= len(P): continue
        if D[i, j] > D[i, k] + D[k_p, j] + epsilon:
            return False
    return True

filtered_pairs = [(i, j) for (i, j) in mutual_pairs if is_coherent(i, j)]

# Visualisation
plt.figure(figsize=(8, 5))
ax = sns.heatmap(D, annot=True, fmt=".0f", cmap="coolwarm", cbar=True,
                 xticklabels=T, yticklabels=P, linewidths=0.5, linecolor='gray')

# Ajout des flèches pour les appariements retenus
for i, j in mutual_pairs:
    color = "lime" if (i, j) in filtered_pairs else "orange"
    plt.plot(j + 0.5, i + 0.5, marker="o", markersize=12, markeredgecolor=color, markerfacecolor='none', markeredgewidth=2)

plt.title("Matrice de distance Levenshtein\nCercle vert = appariement retenu / orange = rejeté")
plt.xlabel("Vérité terrain (T)")
plt.ylabel("Données prédites (P)")
plt.tight_layout()
plt.show()
