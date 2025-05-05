import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import Levenshtein
import numpy as np

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
        # print(f"Distance entre '{text_values1[i]}' et '{text_values2[j]}': {distance}")

# print(similarity_matrix)

# df = pd.DataFrame(similarity_matrix, index=text_values1, columns=text_values2)
# plt.figure(figsize=(15, 12))
# sns.heatmap(df, annot=False, cmap="YlGnBu", cbar_kws={'label': 'Distance de Levenshtein'})
# plt.title("Matrice de Similarité basée sur la Distance de Levenshtein")
# plt.show()

log_similarity_matrix = np.log1p(similarity_matrix)
df = pd.DataFrame(log_similarity_matrix, index=text_values1, columns=text_values2)
plt.figure(figsize=(15, 12))
sns.heatmap(df, annot=False, cmap="YlGnBu", cbar_kws={'label': 'Distance de Levenshtein (log)'})
plt.title("Matrice de Similarité basée sur la Distance de Levenshtein (échelle logarithmique)")
plt.show()