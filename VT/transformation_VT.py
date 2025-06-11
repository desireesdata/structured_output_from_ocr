import json


with open('VT_01_haut_niv_complexite_VT.json', 'r', encoding='utf-8') as fichier:
    data = json.load(fichier)

intervenants_transformes = []

for intervenant in data['listes_des_intervenants']:
    intervenant_transforme = {
        'nom': f"{intervenant['nom_de_famille']} {intervenant.get('prenom', '')}".strip()
    }
    if 'actions_relatives_a_l_intervenant' in intervenant:
        references_page = []
        for action in intervenant['actions_relatives_a_l_intervenant']:
            if 'references_page' in action['action']:
                references_page.extend(action['action']['references_page'])
        if references_page:
            intervenant_transforme['references_page'] = references_page
    if 'nom_entree_du_renvoi' in intervenant:
        intervenant_transforme['nom_entree_du_renvoi'] = intervenant['nom_entree_du_renvoi']
    intervenants_transformes.append(intervenant_transforme)

data['listes_des_intervenants'] = intervenants_transformes

with open('VT_01_just_pages_and_names.json', 'w', encoding='utf-8') as fichier:
    json.dump(data, fichier, ensure_ascii=False, indent=4)

print("Transformation terminée et sauvegardée dans fichier_transforme.json")
