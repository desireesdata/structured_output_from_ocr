import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import Levenshtein
import numpy as np

def extract_all_values(json_obj):
    # Retourne toutes les valeurs d'un JSON de façon diachronique dans un tableau
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

json_obj = []
all_values = ["", ""]

try:
    with open('../output/f161_1_projected.json', 'r', encoding='utf-8') as file1:
        json_obj.append(json.load(file1))
    all_values[0] = extract_all_values(json_obj[0])
except FileNotFoundError:
    print("Le fichier f161_1_projected.json n'a pas été trouvé.")
except json.JSONDecodeError:
    print("Erreur lors du chargement du fichier f161_1_projected.json.")

try:
    with open('../output/f161.json', 'r', encoding='utf-8') as file2:
        json_obj.append(json.load(file2))
    all_values[1] = extract_all_values(json_obj[1])
except FileNotFoundError:
    print("Le fichier test_bruit.json n'a pas été trouvé.")
except json.JSONDecodeError:
    print("Erreur lors du chargement du fichier test_bruit.json.")

# Filtrer les chaînes vides
text_values1 = [value for value in all_values[0] if value]
text_values2 = [value for value in all_values[1] if value]

# Vérifier si les listes ne sont pas vides
if not text_values1 or not text_values2:
    print("Les fichiers JSON n'ont pas été chargés correctement ou les listes de valeurs sont vides.")
else:
    n1 = len(text_values1)
    n2 = len(text_values2)
    similarity_matrix = np.full((n1, n2), np.inf)  # Initialiser avec l'infini pour les distances non calculées

    window_size = 5

    for i in range(n1):
        for j in range(max(0, i - window_size), min(n2, i + window_size + 1)):
            distance = Levenshtein.distance(text_values1[i], text_values2[j])
            similarity_matrix[i][j] = np.log(distance)
 
    # Remplacer les valeurs infinies et négatives par NaN
    similarity_matrix[similarity_matrix == np.inf] = np.nan
    similarity_matrix[similarity_matrix < 0] = np.nan

    # Afficher la matrice de similarité
    df = pd.DataFrame(similarity_matrix, index=text_values1, columns=text_values2)
    plt.figure(figsize=(15, 12))
    sns.heatmap(df, annot=False, cmap="YlGnBu", cbar_kws={'label': 'Distance de Levenshtein'}, mask=np.isnan(similarity_matrix))
    plt.title("Matrice de Similarité basée sur la Distance de Levenshtein")
    plt.show()

    # Appliquer une transformation logarithmique
    log_similarity_matrix = np.log1p(similarity_matrix)
    log_similarity_matrix[np.isnan(similarity_matrix)] = np.nan  # Conserver les NaN après la transformation logarithmique
    df_log = pd.DataFrame(log_similarity_matrix, index=text_values1, columns=text_values2)
    plt.figure(figsize=(15, 12))
    sns.heatmap(df_log, annot=False, cmap="YlGnBu", cbar_kws={'label': 'Distance de Levenshtein (log)'}, mask=np.isnan(log_similarity_matrix))
    plt.title("Matrice de Similarité basée sur la Distance de Levenshtein (échelle logarithmique)")
    plt.show()
