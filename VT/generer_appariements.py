import numpy as np
from scipy.optimize import linear_sum_assignment
import json

version = "A_4"
file_path = f'./matrices/{version}_OCR_corrige.npy'
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

# VT
try:
    with open('./VT_sortie_structuree/VT_01_just_pages_and_names.json', 'r', encoding='utf-8') as file1:
        json_obj.append(json.load(file1))
    all_values[0] = extract_all_values(json_obj[0])
except Exception as e:
    print(f"Error loading file1: {e}")

# SORTIE STRUCTUREE GENEREE à partir de telle ou tel source TXT (avec DLD via Corpusense, sans, etc)
try:
    with open('./GENERATED_sorties_structuree/04_corpusense_sortie_structuree_depuis_OCR_brut.json', 'r', encoding='utf-8') as file2:
        json_obj.append(json.load(file2))
    all_values[1] = extract_all_values(json_obj[1])
except Exception as e:
    print(f"Error loading file2: {e}")

text_values1 = all_values[0]
text_values2 = all_values[1]

# Utiliser linear_sum_assignment pour trouver les appariements optimaux
row_ind, col_ind = linear_sum_assignment(similarity_matrix)
matched_in_text_values1 = set(row_ind)

# dico pour les appariements pour un accès rapide
match_dict = {i: j for i, j in zip(row_ind, col_ind)}

# Afficher les résultats dans l'ordre ordinal de text_values1
for i, value in enumerate(text_values1):
    if i in matched_in_text_values1:
        # Si l'élément est apparié, afficher l'appariement
        j = match_dict[i]
        print(f'"{value}" -----(score : {similarity_matrix[i, j]:.2f})-----> "{text_values2[j]}"')
    else:
        # Si l'élément n'est pas apparié, afficher sans correspondance
        print(f'"{value}" -----(score : X)-----> <aucun match>')

# Afficher les éléments de text_values2 qui n'ont pas de correspondance
matched_in_text_values2 = set(col_ind)
for j, value in enumerate(text_values2):
    if j not in matched_in_text_values2:
        print(f'"aucun match" <-----(score : X)----- "{value}"')

# # Afficher les paires de valeurs avec leur distance 
# for i, j in zip(row_ind, col_ind):
#     print(f'"{text_values1[i]}" -----(score : {similarity_matrix[i, j]:.2f})-----> "{text_values2[j]}"')


# # Element non-matchés
# unmatched_in_text_values1 = set(range(len(text_values1))) - set(row_ind)
# unmatched_in_text_values2 = set(range(len(text_values2))) - set(col_ind)

# print("pas de match vt : ")
# for index in unmatched_in_text_values1:
#     print(f"Index: {index}, Value: {text_values1[index]}")

# print("pas de match données evaluéees: ")
# for index in unmatched_in_text_values2:
#     print(f"Index: {index}, Value: {text_values2[index]}")
