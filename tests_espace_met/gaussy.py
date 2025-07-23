import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.spatial.distance import cdist

def compute_distance_matrix(P, T, metric="euclidean"):
    return cdist(P, T, metric=metric)  # shape (n, m)

def mutual_nearest_neighbors(D):
    n, m = D.shape
    p_to_t = np.argmin(D, axis=1)  # indices in T
    t_to_p = np.argmin(D, axis=0)  # indices in P

    matches = []
    for i, j in enumerate(p_to_t):
        if t_to_p[j] == i:
            matches.append((i, j))
    return matches

def contrast_filter(D, matches, sigma=1.0, threshold=0.0):
    # Lissage par convolution gaussienne
    D_smooth = gaussian_filter(D, sigma=sigma)
    contrast = D - D_smooth

    # Filtrage des appariements dont le contraste est suffisant
    good_matches = [(i, j) for (i, j) in matches if contrast[i, j] < threshold]
    return good_matches, contrast

def metric_pairing(P, T, metric="euclidean", sigma=1.0, threshold=0.0):
    D = compute_distance_matrix(P, T, metric=metric)
    matches = mutual_nearest_neighbors(D)
    good_matches, contrast = contrast_filter(D, matches, sigma=sigma, threshold=threshold)
    return good_matches, D, contrast


# Exemple avec des points 2D
np.random.seed(42)
T = np.random.rand(10, 2)
P = T + 0.05 * np.random.randn(10, 2)  # version bruitée

matches, D, contrast = metric_pairing(P, T, sigma=1.0, threshold=-0.01)

for i, j in matches:
    print(f"P[{i}] <--> T[{j}]  | Distance = {D[i,j]:.3f} | Contraste = {contrast[i,j]:.3f}")
