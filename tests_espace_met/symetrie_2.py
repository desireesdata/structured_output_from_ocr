import numpy as np

# Redéfinir tout après réinitialisation de l'environnement

def dummy_distance(a, b):
    """Distance simplifiée : nombre de positions différentes (comme Hamming, pour même taille)."""
    return sum(c1 != c2 for c1, c2 in zip(a, b))

def build_distance_matrix(P, T, distance_fn):
    """Construit une matrice de distances entre les prédictions P et la vérité terrain T."""
    n, m = len(P), len(T)
    D = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            D[i, j] = distance_fn(P[i], T[j])
    return D

def mutual_nearest_neighbors(D):
    """Retourne les paires (i, j) qui sont mutuellement les plus proches dans D."""
    min_pred_to_truth = D.argmin(axis=1)
    min_truth_to_pred = D.argmin(axis=0)

    matches = []
    for i, j in enumerate(min_pred_to_truth):
        if min_truth_to_pred[j] == i:
            matches.append((i, j))
    return matches

def is_triangle_valid(D, i, j):
    """Vérifie que la distance D[i, j] respecte l'inégalité triangulaire avec tous les autres k."""
    for k in range(D.shape[1]):
        if k == j:
            continue
        if D[i, j] > D[i, k] + D[k, j]:
            return False
    return True

def match_with_metric_filtering(P, T, distance_fn):
    D = build_distance_matrix(P, T, distance_fn)
    matches = mutual_nearest_neighbors(D)

    reliable_matches = []
    for i, j in matches:
        if is_triangle_valid(D, i, j):
            reliable_matches.append((i, j))
    return reliable_matches, D

# Exemple de chaînes pour test
P = ['abc', 'xyz', 'abd']
T = ['abc', 'xyy', 'abe']

reliable_matches, D = match_with_metric_filtering(P, T, dummy_distance)
reliable_matches, D.round(1)
