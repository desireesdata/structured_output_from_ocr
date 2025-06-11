import numpy as np
from scipy.optimize import linear_sum_assignment
import json

# Charger la matrice depuis le fichier .npy
file_path = './matrices/A_0_JSON_VT_vers_JSON_VT.npy'
similarity_matrix = np.load(file_path)

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

# Charger les fichiers JSON
try:
    with open('./VT_sortie_structuree/VT_01_just_pages_and_names.json', 'r', encoding='utf-8') as file1:
        json_obj.append(json.load(file1))
    all_values[0] = extract_all_values(json_obj[0])
except Exception as e:
    print(f"Error loading file1: {e}")

try:
    with open('./VT_sortie_structuree/VT_01_just_pages_and_names.json', 'r', encoding='utf-8') as file2:
        json_obj.append(json.load(file2))
    all_values[1] = extract_all_values(json_obj[1])
except Exception as e:
    print(f"Error loading file2: {e}")

text_values1 = all_values[0]
text_values2 = all_values[1]

# Utiliser linear_sum_assignment pour trouver les appariements optimaux
row_ind, col_ind = linear_sum_assignment(similarity_matrix)

# Afficher les paires de valeurs avec leur score de similarité
for i, j in zip(row_ind, col_ind):
    print(f'"{text_values1[i]}" -----(score : {similarity_matrix[i, j]:.2f})-----> "{text_values2[j]}"')
