import json
import pandas as pd
import plotly.express as px
import Levenshtein
import numpy as np

def extract_all_values(json_obj):
    """Fonction qui extrait toutes les valeurs du fichier JSON"""
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

def shorten_texts(texts, max_len=30):
    return [text if len(text) <= max_len else text[:max_len] + "..." for text in texts]


json_obj = []
all_values = ["", ""]

# Charger le premier fichier JSON
try:
    with open('../VT_sortie_structuree/VT_01_moyen_niv_complexite.json', 'r', encoding='utf-8') as file1:
        json_obj.append(json.load(file1))
        all_values[0] = extract_all_values(json_obj[0])
except FileNotFoundError:
    print("Le fichier VT_01_moyen_niv_complexite.json n'a pas été trouvé.")
except json.JSONDecodeError:
    print("Erreur lors du chargement du fichier VT_01_moyen_niv_complexite.json.")

# Charger le second fichier JSON
try:
    with open('./GENERATED_sorties_structuree/moyen_02.json', 'r', encoding='utf-8') as file2:
        json_obj.append(json.load(file2))
        all_values[1] = extract_all_values(json_obj[1])
except FileNotFoundError:
    print("Le fichier moyen_02.json n'a pas été trouvé.")
except json.JSONDecodeError:
    print("Erreur lors du chargement du fichier moyen_02.json.")


if len(json_obj) != 2:
    print("Erreur : Les deux fichiers JSON n'ont pas été chargés correctement.")
else:
    text_values1 = all_values[0]
    text_values2 = all_values[1]

    n1 = len(text_values1)
    n2 = len(text_values2)
    similarity_matrix = np.zeros((n1, n2))

    for i in range(n1):
        for j in range(n2):
            distance = Levenshtein.distance(text_values1[i], text_values2[j])
            similarity_matrix[i][j] = distance

    cote = "A_2"
    unique_columns = make_columns_unique(text_values2)
    with open(f'matrices/{cote}_JSON_VT_vers_JSON_VT.npy', 'wb') as f:
        np.save(f, similarity_matrix)

    df = pd.DataFrame(similarity_matrix, index=text_values1, columns=unique_columns)

    fig = px.imshow(df,
                    labels=dict(x="JSON Généré", y="VT JSON", color="Levenshtein Distance"),
                    x=unique_columns,
                    y=text_values1,
                    color_continuous_scale='YlGnBu',
                    title=f"{cote}. Matrice de Similarité basée sur la Distance de Levenshtein")

    fig.update_layout(
        width=2200,
        height=3000,
        xaxis=dict(
            tickangle=-35,
            tickfont=dict(size=6)
        ),
        yaxis=dict(
            tickfont=dict(size=6)
        )
    )

    # Sauvegarder l'image
    fig.write_image("matrice_similarite.png")