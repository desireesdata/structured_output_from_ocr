import numpy as np
import Levenshtein

# Données
T = ["sénat", "loi", "1931", "740", "8"]       # Vérité terrain
P = ["semat", "l0i", "1931", "74O"]            # Prédictions bruitées

print(P, "\n", T)
# Étape 1 : calcul de la matrice de distance Levenshtein
D = np.array([[Levenshtein.distance(p, t) for t in T] for p in P])
print("Matrice de distance (P x T) :\n", D)

# Étape 2 : plus proche voisin de chaque prédiction (P → T)
P_to_T = np.argmin(D, axis=1)
print("\nPlus proche T pour chaque P :", P_to_T)

# Étape 3 : plus proche voisin de chaque vérité (T → P)
T_to_P = np.argmin(D, axis=0)
print("Plus proche P pour chaque T :", T_to_P)

# Étape 4 : détection des appariements mutuels
print("\n✔ Appariements mutuels (symétriques) :")
for i, j in enumerate(P_to_T):
    if T_to_P[j] == i:
        print(f"  {P[i]} ⟷ {T[j]}")
    else:
        print(f"  ✘ {P[i]} → {T[j]}, rejeté (pas réciproque)")

# Facultatif : afficher les éléments non appariés
appariés_T = set(P_to_T[i] for i in range(len(P)) if T_to_P[P_to_T[i]] == i)
non_apparies_T = [T[i] for i in range(len(T)) if i not in appariés_T]
print("\n❌ Éléments de la vérité terrain non appariés :", non_apparies_T)
