import numpy as np
from scipy.special import softmax
from scipy.stats import entropy
import jellyfish
import json

# 1. Données
# truth = ["sénat", "loi", "1931", "740", "8", "9", "10", "p. 8", "p.9"]
# predicted = ["semat", "l0i", "1931", "74O", "B", "p.9"]

def extract_all_values(json_obj):
    """Fonction qui extrait toutes les valeurs du fichier JSON

    Args:
        json_obj (_type_): fichier JSON

    Returns:
        _type_: String
    """
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

def make_columns_unique(columns):
    counts = {}
    new_columns = []
    for col in columns:
        if col in counts:
            counts[col] += 1
            new_columns.append(f"{col}_{counts[col]}")
        else:
            counts[col] = 1
            new_columns.append(col)
    return new_columns

json_obj = []
all_values = ["", ""]

# VT
try:
    with open('VT/VT_sortie_structuree/VT_01_just_pages_and_names.json', 'r', encoding='utf-8') as file1:
        json_obj.append(json.load(file1))
    all_values[0] = extract_all_values(json_obj[0])
except Exception as e:
    print(f"Error loading file1: {e}")

# SORTIE STRUCTUREE GENEREE à partir de telle ou tel source TXT (avec DLD via Corpusense, sans, etc)
try:
    with open('VT/names_and_pages/GENERATED_sorties_structuree/02_corpusense_zones_manuelles.json', 'r', encoding='utf-8') as file2:
        json_obj.append(json.load(file2))
    all_values[1] = extract_all_values(json_obj[1])
except Exception as e:
    print(f"Error loading file2: {e}")

truth= all_values[0]
predicted = all_values[1]

# 2. Matrice de distance Levenshtein
def levenshtein_matrix(A, B):
    return np.array([[jellyfish.levenshtein_distance(a, b) for b in B] for a in A])

D = levenshtein_matrix(truth, predicted)
n, m = D.shape

# 3. Entropie locale (pour quantifier le bruit)
def local_entropy(row, alpha=1.0):
    probs = softmax(-row)
    return alpha * entropy(probs)

local_epsilons = np.array([local_entropy(D[i, :]) for i in range(n)])

# 4. Appariements mutuels
matches = []
for i in range(n):
    j = np.argmin(D[i])
    i_back = np.argmin(D[:, j])
    if i == i_back:
        matches.append((i, j))

# 5. Relaxation de l’inégalité triangulaire
filtered_matches = []
for i, j in matches:
    epsilon = local_epsilons[i]
    is_consistent = True
    for k in range(m):
        if k != j:
            if D[i, j] > D[i, k] + D[np.argmin(D[:, j]), j] + epsilon:
                is_consistent = False
                break
    if is_consistent:
        filtered_matches.append((i, j))

# 6. Résultats
print("Appariements mutuels et cohérents (relaxation triangulaire adaptative) :\n")
for i, j in filtered_matches:
    print(f"  {truth[i]}  ⟷  {predicted[j]}  (d = {D[i, j]}, ε = {local_epsilons[i]:.2f})")
