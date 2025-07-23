import numpy as np
from Levenshtein import distance as lev
from scipy.ndimage import gaussian_filter

# Données
T = ["sénat", "loi", "1931", "740", "8"]
P = ["semat", "l0i", "1931", "74O"]

# Paramètres
sigma = 1.0  # écart-type pour le flou gaussien
epsilon = 0.1  # tolérance sur le min local

# Étape 1 : calcul de la matrice de distance
D = np.array([[lev(p, t) for t in T] for p in P])
print("🔢 Matrice de distance D (P x T):\n", D)

# Étape 2 : convolution gaussienne
D_smooth = gaussian_filter(D, sigma=sigma)
print("\n🌫️ Matrice lissée D_smooth :\n", np.round(D_smooth, 2))

# Étape 3 : appariement mutuel brut
P_to_T = np.argmin(D, axis=1)
T_to_P = np.argmin(D, axis=0)
mutual_pairs = [(i, j) for i, j in enumerate(P_to_T) if T_to_P[j] == i]

# Étape 4 : filtre par minima locaux dans D_smooth
def is_local_min(i, j):
    neighborhood = D_smooth[max(0, i-1):i+2, max(0, j-1):j+2]
    return D_smooth[i, j] <= np.min(neighborhood) + epsilon

filtered_pairs = []
print("\n🔍 Appariements filtrés par convolution :")
for i, j in mutual_pairs:
    if is_local_min(i, j):
        print(f"  ✅ {P[i]} ⟷ {T[j]} [min local]")
        filtered_pairs.append((i, j))
    else:
        print(f"  ❌ {P[i]} ⟷ {T[j]} rejeté (pas un minimum local)")

# Résultat final
print("\n📌 Appariements valides finaux :")
for i, j in filtered_pairs:
    print(f"  {P[i]} ↔ {T[j]}")
