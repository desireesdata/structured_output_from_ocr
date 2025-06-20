# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from scipy.stats import dirichlet

# # Générer des échantillons dans le simplexe 2x2
# n_samples = 500
# samples = dirichlet.rvs([1, 1, 1, 1], size=n_samples)

# # Chaque gamma = [gamma11, gamma12, gamma21, gamma22]
# gamma11 = samples[:, 0]
# gamma12 = samples[:, 1]
# gamma21 = samples[:, 2]
# gamma22 = samples[:, 3]

# # Visualisation 3D d'une projection du simplexe
# fig = plt.figure(figsize=(10, 7))
# ax = fig.add_subplot(111, projection='3d')

# ax.scatter(gamma11, gamma12, gamma21, c='dodgerblue', alpha=0.6, s=20)

# ax.set_xlabel(r'$\gamma_{11}$')
# ax.set_ylabel(r'$\gamma_{12}$')
# ax.set_zlabel(r'$\gamma_{21}$')
# ax.set_title("Projection du simplexe des plans de transport 2×2 (somme = 1)")

# plt.tight_layout()
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

# Ensembles de mots
ensemble1 = ["sénat", "loi", "1931"]
ensemble2 = ["sémat", "l0i", "1931"]

# Calculer la matrice de distance de Levenshtein entre les deux ensembles
matrice_distance_ensembles = np.zeros((len(ensemble1), len(ensemble2)), dtype=int)
for i, mot1 in enumerate(ensemble1):
    for j, mot2 in enumerate(ensemble2):
        matrice_distance_ensembles[i, j] = levenshtein_distance(mot1, mot2)
    

# Créer une heatmap pour visualiser la matrice de distance de Levenshtein
plt.figure(figsize=(6, 4))
sns.heatmap(matrice_distance_ensembles, annot=True, xticklabels=ensemble2, yticklabels=ensemble1, cmap='viridis_r')
print(matrice_distance_ensembles)
plt.title("Matrice de distance de Levenshtein entre deux ensembles")
plt.show()
