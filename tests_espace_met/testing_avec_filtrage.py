import numpy as np
import Levenshtein

# Données
T = ["sénat", "loi", "1931", "740", "8"]
P = ["semat", "l0i", "1931", "74O"]

# Paramètre de tolérance pour le test triangulaire
epsilon = 0.5

# Étape 1 : matrice de distance Levenshtein
D = np.array([[Levenshtein.distance(p, t) for t in T] for p in P])
print("🔢 Matrice de distance (P x T) :\n", D)

# Étape 2 : plus proche voisin
P_to_T = np.argmin(D, axis=1)
T_to_P = np.argmin(D, axis=0)

# Étape 3 : appariements mutuels
mutual_pairs = []
for i, j in enumerate(P_to_T):
    if T_to_P[j] == i:
        mutual_pairs.append((i, j))

print("\n✔ Appariements mutuels :")
for i, j in mutual_pairs:
    print(f"  {P[i]} ⟷ {T[j]}")

# Étape 4 : filtrage par cohérence métrique locale
def is_coherent(i, j):
    for k in range(len(T)):
        if k == j:
            continue
        k_p = T_to_P[k]
        if k_p == -1 or k_p >= len(P):  # sécurité
            continue
        # Triangular inequality (relâchée)
        if D[i, j] > D[i, k] + D[k_p, j] + epsilon:
            return False
    return True

filtered_pairs = []
print("\n🔍 Appariements après test de cohérence :")
for i, j in mutual_pairs:
    if is_coherent(i, j):
        print(f"  ✅ {P[i]} ⟷ {T[j]} [cohérent]")
        filtered_pairs.append((i, j))
    else:
        print(f"  ❌ {P[i]} ⟷ {T[j]} rejeté (triangulation)")

# Résumé final
print("\n📌 Appariements valides finaux :")
for i, j in filtered_pairs:
    print(f"  {P[i]} ↔ {T[j]}")
