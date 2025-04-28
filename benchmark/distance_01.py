from unidecode import unidecode
from Levenshtein import distance
import pandas as pd
import plotly.express as px

verite_terrain = pd.read_csv("truth_grnd_01.csv", delimiter='\t')
sortie_structuree_via_llm = pd.read_csv("json_converted_01.csv", delimiter='\t')
distance_for_each_lines = []

def normalisation(nom :str, fonction: str, adresse:str)-> str:
    the_concated = (nom + " " + str(fonction) + " " + adresse).lower()
    the_concated = unidecode(the_concated)
    return the_concated

#Distance Lev Colonne FONCTION
for i in verite_terrain.index:
    distance_for_each_lines.append(distance(
        normalisation(verite_terrain['nom'][i],
                        verite_terrain['fonction'][i],
                        verite_terrain['adresse'][i]),
        normalisation(sortie_structuree_via_llm['nom'][i],
                        sortie_structuree_via_llm['fonction'][i],
                        sortie_structuree_via_llm['adresse'][i])))
    print(distance_for_each_lines[i])

fig = px.bar(verite_terrain, x=verite_terrain.index, y=distance_for_each_lines, title="Distances de Levenshtein par ligne")
fig.show()

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


