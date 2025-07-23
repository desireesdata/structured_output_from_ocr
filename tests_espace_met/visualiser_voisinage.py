import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Levenshtein import distance as levenshtein_distance

# Données exemples
truth = ["sénat", "loi", "1931", "740", "8"]
predicted = ["semat", "l0i", "1931", "74O"]

# Matrice de distance Levenshtein
D = np.array([[levenshtein_distance(p, t) for t in truth] for p in predicted])

# Affichage de la matrice avec annotations
plt.figure(figsize=(8, 4))
sns.heatmap(D, annot=True, fmt=".0f", cmap="YlGnBu", xticklabels=truth, yticklabels=predicted)
plt.title("Matrice de distance Levenshtein (Predicted x Truth)")
plt.xlabel("Vérité terrain")
plt.ylabel("Données prédites")
plt.tight_layout()
plt.show()

# Fonction pour afficher le voisinage autour d’un appariement (i, j)
def afficher_voisinage(D, i, j, k=2):
    ligne = D[i, :]
    colonne = D[:, j]

    voisins_ligne = np.argsort(ligne)[:k+1]
    voisins_colonne = np.argsort(colonne)[:k+1]

    print(f"\n--- Voisinage pour le match ({i}, {j}) ---")
    print(f"Distance d(p_{i}, t_{j}) = {D[i, j]}")
    print("Plus proches voisins de p_{} (ligne):".format(i))
    for jj in voisins_ligne:
        print(f"  t_{jj} (distance={D[i, jj]})")
    print("Plus proches voisins de t_{} (colonne):".format(j))
    for ii in voisins_colonne:
        print(f"  p_{ii} (distance={D[ii, j]})")

# Quelques tests
afficher_voisinage(D, 0, 0)  # semat <-> sénat
afficher_voisinage(D, 1, 1)  # l0i <-> loi
afficher_voisinage(D, 3, 3)  # 74O <-> 740
