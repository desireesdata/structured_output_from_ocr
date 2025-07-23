import numpy as np
from Levenshtein import distance as levenshtein

# Données
truth = ["sénat", "loi", "1931", "740", "8"]
preds = ["semat", "l0i", "1931", "74O"]

# Étape 1 : construire la matrice de distances (len(preds) x len(truth))
D = np.array([[levenshtein(p, t) for t in truth] for p in preds])

# Étape 2 : Appariements mutuels
mutual_matches = []
for i, row in enumerate(D):
    j = np.argmin(row)  # plus proche voisin dans truth pour pred[i]
    i_back = np.argmin(D[:, j])  # plus proche prédiction pour truth[j]
    if i == i_back:
        mutual_matches.append((i, j))

# Affichage
print("Matrice de distances (Levenshtein):")
print(D)

print("\nAppariements mutuels trouvés:")
for i, j in mutual_matches:
    print(f'P[{i}] = "{preds[i]}"  ⟷  T[{j}] = "{truth[j]}"  (Distance = {D[i,j]})')
