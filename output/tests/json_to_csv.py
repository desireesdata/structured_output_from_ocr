import json
import csv

# Chemin vers votre fichier JSON d'entrée et CSV de sortie
input_json_file = 'corrected_page_2_OCR_VT________ BLOG.json'
output_csv_file = 'output.tsv'  # Utilisez .tsv pour indiquer un fichier délimité par des tabulations

# Charger les données JSON à partir du fichier
with open(input_json_file, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Accéder à la liste des intervenants
intervenants = data['listes_des_intervenants']

# Ouvrir un fichier TSV pour écrire
with open(output_csv_file, 'w', newline='', encoding='utf-8') as tsv_file:
    # Utiliser csv.writer avec un délimiteur de tabulation
    tsv_writer = csv.writer(tsv_file, delimiter='\t')

    # Écrire l'en-tête du TSV
    tsv_writer.writerow(intervenants[0].keys())

    # Écrire les lignes de données
    for intervenant in intervenants:
        # Convertir chaque intervenant en ligne du TSV
        row = []
        for key in intervenant.keys():
            if key == 'actions_relatives_a_l_intervenant':
                # Convertir les actions en une chaîne lisible
                actions = intervenant[key]
                actions_str = "\t".join([action['action']['description_action'] for action in actions])
                row.append(actions_str)
            else:
                row.append(intervenant[key])
        tsv_writer.writerow(row)

print(f"Les données ont été converties de {input_json_file} à {output_csv_file}")
