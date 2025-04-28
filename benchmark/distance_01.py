from unidecode import unidecode
from Levenshtein import distance
import pandas as pd
import plotly.express as px
import re
import numpy as np

verite_terrain = pd.read_csv("truth_grnd_01.csv", delimiter='\t')
sortie_structuree_via_llm = pd.read_csv("json_converted_01.csv", delimiter='\t')
distance_for_each_lines = []

def normalisation(nom :str, fonction: str, adresse:str)-> str:
    the_concatened = (nom + " " + str(fonction) + " " + adresse).lower()
    the_concatened = unidecode(the_concatened)
    pattern = r'[^\w]' #suppression ponctuation... peut-être un peu "dur"
    result = re.sub(pattern, "·", the_concatened)
    return result

#Distance Lev Colonne FONCTION
for i in verite_terrain.index:
    distance_for_each_lines.append(distance(
        normalisation(verite_terrain['nom'][i],
                        verite_terrain['fonction'][i],
                        verite_terrain['adresse'][i]),
        normalisation(sortie_structuree_via_llm['nom'][i],
                        sortie_structuree_via_llm['fonction'][i],
                        sortie_structuree_via_llm['adresse'][i])))
    # print(distance_for_each_lines[i])

fig = px.bar(verite_terrain, x=verite_terrain.index, y=distance_for_each_lines, title=f"Distances de Levenshtein par ligne. La médiane est à {np.median(distance_for_each_lines)}")
fig.show()

print("la médiane est : ", np.median(distance_for_each_lines))

# #La somme des distances de Levenshtein entre les mots individuels d'une liste n'est pas nécessairement égale à la distance de Levenshtein entre les chaînes concaténées des deux listes. 
# #Distance Lev Colonne NOM
# distance_nom = []
# distance_fonction = []
# distance_adresse = []
# for i in verite_terrain.index:
#     print(verite_terrain['nom'][i], " | ",  sortie_structuree_via_llm['nom'][i])
#     distance_nom.append(distance(str(verite_terrain['nom'][i]), str(sortie_structuree_via_llm['nom'][i])))
#     print(distance_nom[i])

# #Distance Lev Colonne FONCTION
# for i in verite_terrain.index:
#     print(verite_terrain['fonction'][i], " | ",  sortie_structuree_via_llm['fonction'][i])
#     distance_fonction.append(distance(str(verite_terrain['fonction'][i]), str(sortie_structuree_via_llm['fonction'][i])))
#     print(distance_fonction[i])

# #Distance Lev Colonne ADRESSE
# for i in verite_terrain.index:
#     print(verite_terrain['adresse'][i], " | ",  sortie_structuree_via_llm['adresse'][i])
#     distance_adresse.append(distance(str(verite_terrain['adresse'][i]), str(sortie_structuree_via_llm['adresse'][i])))
#     print(distance_adresse[i])


