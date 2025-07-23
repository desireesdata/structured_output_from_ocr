# Appariement robuste entre deux ensembles discrets avec symétrie et cohérence locale

import numpy as np
from Levenshtein import distance as lev_distance

# -------------------------------
# 1. Matrice de distance Levenshtein
# -------------------------------
def compute_distance_matrix(P, T):
    """
    Calcule une matrice des distances Levenshtein entre deux listes de chaînes P et T.
    Chaque case D[i, j] contient la distance entre P[i] et T[j].
    """
    return np.array([[lev_distance(p, t) for t in T] for p in P])

# -------------------------------
# 2. Appariements mutuels
# -------------------------------
def mutual_nearest_neighbors(D):
    """
    Identifie les paires (i, j) telles que P[i] est le plus proche voisin de T[j]
    et T[j] est le plus proche voisin de P[i].
    """
    P_to_T = np.argmin(D, axis=1)  # indice j pour chaque i
    T_to_P = np.argmin(D, axis=0)  # indice i pour chaque j
    pairs = []
    for i, j in enumerate(P_to_T):
        if T_to_P[j] == i:
            pairs.append((i, j))
    return pairs

# -------------------------------
# 3. Score de convergence Cauchy locale
# -------------------------------
def cauchy_convergence_score(D, k=3):
    """
    Pour chaque ligne (i.e. chaque élément de P), mesure la régularité locale
    des distances vers ses k plus proches voisins dans T. Plus le score est petit,
    plus l'environnement local est "cohérent" (style séquence).
    """
    scores = []
    for i in range(D.shape[0]):
        nearest_distances = np.sort(D[i])[:k]
        pairwise_diffs = [abs(a - b) for i1, a in enumerate(nearest_distances)
                                        for b in nearest_distances[i1+1:]]
        score = max(pairwise_diffs) if pairwise_diffs else 0.0
        scores.append(score)
    return np.array(scores)

# -------------------------------
# 4. Test de cohérence triangulaire relâchée
# -------------------------------
def relaxed_triangle_consistency(D, i, j, epsilon=1.0):
    """
    Vérifie si l'inégalité triangulaire (relâchée) est globalement respectée
    pour l'appariement (i, j). Si une autre cible k est trop proche, on rejette.
    """
    for k in range(D.shape[1]):
        if k == j:
            continue
        if D[i, j] > D[i, k] + abs(D[i, j] - D[i, k]) + epsilon:
            return False
    return True

# -------------------------------
# 5. Pipeline complet
# -------------------------------
def robust_pairing(P, T, k=3, cauchy_thresh=2.0, epsilon=1.0):
    D = compute_distance_matrix(P, T)
    mutual_pairs = mutual_nearest_neighbors(D)
    cauchy_scores = cauchy_convergence_score(D, k)

    final_pairs = []
    for i, j in mutual_pairs:
        if cauchy_scores[i] <= cauchy_thresh and relaxed_triangle_consistency(D, i, j, epsilon):
            final_pairs.append((P[i], T[j], D[i, j], cauchy_scores[i]))

    return final_pairs

# -------------------------------
# 6. Exemple d'utilisation
# -------------------------------
P = ["semat", "l0i", "1931", "74O"]
T = ["sénat", "loi", "1931", "740", "8"]

results = robust_pairing(P, T, k=3, cauchy_thresh=2.0, epsilon=1.0)

print("Appariements robustes détectés :\n")
for p, t, dist, score in results:
    print(f"{p:6s} ⟷ {t:6s} | distance = {dist}, score Cauchy = {score:.2f}")
