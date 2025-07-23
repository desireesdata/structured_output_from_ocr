import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import textdistance
from scipy.optimize import linear_sum_assignment
import pandas as pd

# Ensembles
T = ["chat", "chien", "oiseau", "souris"]
P = ["chien", "chat", "oiseau", "sourie", "voiture"]

# Distance de Levenshtein
D = np.array([[textdistance.levenshtein(p, t) for t in T] for p in P])

# Appariement mutuel
def mutual_match(D):
    matches = []
    for i in range(D.shape[0]):
        j_star = np.argmin(D[i])
        i_rev = np.argmin(D[:, j_star])
        if i_rev == i:
            matches.append((i, j_star, D[i, j_star]))
    return matches

# Transport optimal
def optimal_transport(D):
    row_ind, col_ind = linear_sum_assignment(D)
    return list(zip(row_ind, col_ind, D[row_ind, col_ind]))

# DTW distance
def dtw_distance_matrix(P, T):
    n, m = len(P), len(T)
    dtw = np.full((n+1, m+1), np.inf)
    dtw[0, 0] = 0
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = textdistance.levenshtein(P[i-1], T[j-1])
            dtw[i, j] = cost + min(dtw[i-1, j], dtw[i, j-1], dtw[i-1, j-1])
    return dtw[n, m]

# Exécutions
mutual = mutual_match(D)
optimal = optimal_transport(D)
dtw_dist = dtw_distance_matrix(P, T)

# Résultats
results = pd.DataFrame({
    "Méthode": ["Mutuelle", "Transport optimal", "DTW (global)"],
    "Appariements valides": [
        sum(1 for i, j, _ in mutual if T[j] in T),
        sum(1 for i, j, _ in optimal if T[j] in T),
        "-"
    ],
    "Faux positifs": [
        sum(1 for i, j, _ in mutual if T[j] not in T),
        sum(1 for i, j, _ in optimal if T[j] not in T),
        "-"
    ],
    "Distance totale": [
        sum(d for _, _, d in mutual),
        sum(d for _, _, d in optimal),
        dtw_dist
    ]
})

# Affichage graphique
plt.figure(figsize=(8, 5))
sns.heatmap(D, annot=True, xticklabels=T, yticklabels=P, cmap="Blues", cbar_kws={'label': 'Levenshtein'})
for i, j, _ in mutual:
    plt.text(j + 0.5, i + 0.5, "✔", ha='center', va='center', color='red', fontsize=16)
plt.title("Matrice de distance Levenshtein\n(Appariements mutuels en rouge)")
plt.xlabel("Vérité terrain (T)")
plt.ylabel("Prédictions (P)")
plt.tight_layout()
plt.show()

# Résumé
print(results)
