import numpy as np
from Levenshtein import distance as levenshtein
from scipy.ndimage import gaussian_filter

# --- Étape 1 : données ---
truth = ["sénat", "loi", "1931", "740", "8"]
preds = ["semat", "l0i", "1931", "74O"]

# --- Étape 2 : distance Levenshtein ---
D = np.array([[levenshtein(p, t) for t in truth] for p in preds])

# --- Étape 3 : appariements mutuels (symétriques) ---
mutual_matches = []
for i, row in enumerate(D):
    j = np.argmin(row)  # T[j] est le plus proche voisin de P[i]
    i_back = np.argmin(D[:, j])  # P[i_back] est le plus proche voisin de T[j]
    if i == i_back:
        mutual_matches.append((i, j))

# --- Étape 4 : lissage local (gaussien) ---
sigma = 1.0  # échelle de détection locale
D_smooth = gaussian_filter(D, sigma=sigma)
contrast = D - D_smooth

# --- Étape 5 : filtrage adaptatif basé sur le contraste ---
# Plus contrasté = plus fiable → on garde ceux avec un contraste suffisant
threshold = -0.01  # peut être adapté
filtered_matches = [(i, j) for (i, j) in mutual_matches if contrast[i, j] < threshold]

# --- Résultats ---
print("Matrice de distance D :")
print(D)

print("\nMatrice de contraste :")
print(np.round(contrast, 2))

print("\nAppariements mutuels fiables :")
for i, j in filtered_matches:
    print(f'P[{i}] = "{preds[i]}"  ⟷  T[{j}] = "{truth[j]}"  (Distance = {D[i,j]}, Contraste = {contrast[i,j]:.3f})')
