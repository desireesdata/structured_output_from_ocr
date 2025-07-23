import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import Levenshtein  # pip install python-Levenshtein
import json

json_obj = []
all_values = ["", ""]

def extract_all_values(json_obj):
    all_values = []

    def recurse(obj):
        if isinstance(obj, dict):
            for value in obj.values():
                recurse(value)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)
        else:
            all_values.append(str(obj))

    recurse(json_obj)
    return all_values

# VT
try:
    with open('VT/VT_sortie_structuree/VT_01_bas_niv_complexite_VT.json', 'r', encoding='utf-8') as file1:
        json_obj.append(json.load(file1))
        all_values[0] = extract_all_values(json_obj[0])
except FileNotFoundError:
    print("Le fichier VT_01_moyen_niv_complexite.json n'a pas été trouvé.")
except json.JSONDecodeError:
    print("Erreur lors du chargement du fichier VT_01_moyen_niv_complexite.json.")

# Charger le second fichier JSON
try:
    with open('VT/niveau_moyen/GENERATED_sorties_structuree/moyen_02.json', 'r', encoding='utf-8') as file2:
        json_obj.append(json.load(file2))
        all_values[1] = extract_all_values(json_obj[1])
except FileNotFoundError:
    print("Le fichier moyen_02.json n'a pas été trouvé.")
except json.JSONDecodeError:
    print("Erreur lors du chargement du fichier moyen_02.json.")

T = all_values[0]
P = all_values[1]

print(T)
# --- Étape 0 : Données
# P = ["semat", "l0i", "1931", "74O"]
# T = ["sénat", "loi", "1931", "740", "8"]

# --- Étape 1 : Calcul de la matrice de distances D[p_i, t_j]
D = np.zeros((len(P), len(T)))
for i, p in enumerate(P):
    for j, t in enumerate(T):
        D[i, j] = Levenshtein.distance(p, t)

# --- Étape 2 : Appariement mutuel (symétrique)
mutual_matches = []
for i, row in enumerate(D):
    j_star = np.argmin(row)  # t_j* plus proche de p_i
    i_star = np.argmin(D[:, j_star])  # p_i* plus proche de t_j*
    if i == i_star:
        mutual_matches.append((i, j_star))

# --- Étape 3 : Filtrage par inégalité triangulaire relâchée
# Pour un appariement (p_i, t_j), on vérifie s’il existe t_k tel que :
# D[i,j] > D[i,k] + D[i_k,j] + ε → incohérence (à écarter)
epsilon = 0.5  # marge tolérée pour le relâchement
consistent_matches = []

for (i, j) in mutual_matches:
    is_consistent = True
    for k in range(len(T)):
        if k == j:
            continue
        i_k = np.argmin(D[:, k])  # meilleur match pour t_k
        lhs = D[i, j]
        rhs = D[i, k] + D[i_k, j]
        if lhs > rhs + epsilon:
            is_consistent = False
            break
    if is_consistent:
        consistent_matches.append((i, j))

# --- Résultat
def show_matches(matches, label):
    print(f"\n {label}")
    for i, j in matches:
        print(f"  - {P[i]} ⟷ {T[j]}  (distance = {D[i,j]})")

show_matches(mutual_matches, "Appariements mutuels")
show_matches(consistent_matches, "Appariements validés (triangulaire relâchée)")

# --- Visualisation
# plt.figure(figsize=(8, 5))
# sns.heatmap(D, annot=True, cmap="mako", xticklabels=T, yticklabels=P)
# plt.title("Matrice de distance Levenshtein (P vs T)")
# plt.xlabel("Vérité terrain (T)")
# plt.ylabel("Données prédites (P)")
# plt.tight_layout()
# plt.show()
