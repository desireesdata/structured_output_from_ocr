import json
import pandas as pd
import plotly.express as px
import Levenshtein
import numpy as np


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
    with open('./VT_sortie_structuree/VT_01_just_pages_and_names.json', 'r', encoding='utf-8') as file1:
        json_obj.append(json.load(file1))
    all_values[0] = extract_all_values(json_obj[0])
except FileNotFoundError:
    print("Le fichier f161_1_projected.json n'a pas été trouvé.")
except json.JSONDecodeError:
    print("Erreur lors du chargement du fichier f161_1_projected.json.")

# Généré
try:
    with open('./GENERATED_sorties_structuree/04_corpusense_sortie_structuree_depuis_OCR_brut.json', 'r', encoding='utf-8') as file2:
        json_obj.append(json.load(file2))
    all_values[1] = extract_all_values(json_obj[1])
except FileNotFoundError:
    print("Le fichier test_bruit.json n'a pas été trouvé.")
except json.JSONDecodeError:
    print("Erreur lors du chargement du fichier test_bruit.json.")

text_values1 = all_values[0]
text_values2 = all_values[1]

# print("Valeurs extraites du premier JSON :")
# print(text_values1)
# print("\nValeurs extraites du second JSON :")
# print(text_values2)

n1 = len(text_values1)
n2 = len(text_values2)
similarity_matrix = np.zeros((n1, n2))

for i in range(n1):
    for j in range(n2):
        distance = Levenshtein.distance(text_values1[i], text_values2[j])
        similarity_matrix[i][j] = distance

cote = "A_4"
unique_columns = make_columns_unique(text_values2)
with open(f'{cote}_OCR_corrige.npy', 'wb') as f:
    np.save(f, similarity_matrix)

df = pd.DataFrame(similarity_matrix, index=text_values1, columns=unique_columns)

fig = px.imshow(df,
                labels=dict(x="JSON Généré", y="VT JSON", color="Levenshtein Distance"),
                x=unique_columns,
                y=text_values1,
                color_continuous_scale='YlGnBu',
                title=f"{cote}. Matrice de Similarité basée sur la Distance de Levenshtein")
fig.show()

# Pour une échelle logarithmique
# log_similarity_matrix = np.log1p(similarity_matrix)
# df_log = pd.DataFrame(log_similarity_matrix, index=text_values1, columns=unique_columns)

# fig_log = px.imshow(df_log,
#                     labels=dict(x="Text Values 2", y="Text Values 1", color="Log(Levenshtein Distance)"),
#                     x=unique_columns,
#                     y=text_values1,
#                     color_continuous_scale='YlGnBu',
#                     title="Matrice de Similarité basée sur la Distance de Levenshtein (échelle logarithmique)")
# fig_log.show()
