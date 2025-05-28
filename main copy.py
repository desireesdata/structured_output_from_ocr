from features.config import api_key
from features.input import get_text_from_file
from features.projection import replace_caps_and_punct
from mistralai import Mistral
from pydantic import BaseModel
from unidecode import unidecode
import json


model = "ministral-8b-latest"
client = Mistral(api_key=api_key)
texte = get_text_from_file("./input/tests_VT/corrected_page_2_OCR_VT.txt", False)

class Action(BaseModel):
    description_action:str
    references_page: list[int]

class Interventions(BaseModel):
    action : Action

class RenvoiAutreEntree(BaseModel):
    nom_entree_du_renvoi: str

class Intervenant(BaseModel):
    nom_de_famille: str
    prenom : str
    role : str
    actions_relatives_a_l_intervenant: list[Action] | list[RenvoiAutreEntree] # choisir entre l'une et l'autre classe !

class IntervenantAuSenat(BaseModel):
    listes_des_intervenants: list[Intervenant]

def main():
    entries = client.chat.parse(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": ""
                "Extrayez du texte que je vais vous donner, les informations de chaque entrée, lesquelles sont chacunes relatives à une personne. Ces personnes ont participé à l'activité du Sénat. Ce sont en général ses sénateurs, des ministres, des sous-secrétaires, etc."

                "Il y a une entrée par personne."

                "Chaque entrée se compose : du nom et du prénom d'un intervenant; parfois de son rôle (ce n'est pas toujours précisé : quand il n'y a pas d'indications, c'est qu'il s'agit d'un sénateur); d'une liste d'actions qu'il a effectuées ou qui le concernent. Ce sont des informations à relever."

                "Chaque action (pouvant comprendre différents moments, ils sont en général séparés par un point-virgule) concernant un intervenant est lié à un ou plusieurs numéros de page : il faut également les indiquer. Quand il y a une référence de page, vous pouvez être certain qu'il s'agit d'une action concernant l'intervenant. Je veux donc que vous me donniez toutes ces informations quand vous le pouvez."
                
                "Dans le cas où une entrée n'expose pas des actions ou des faits concernant un intervenant, alors il s'agit d'un renvoi d'index. Dans ce cas, au lieu de mentionner des interventions, indiquez la référence du renvoi. Ces renvois sont en général des noms/prénoms d'intervenants. Ces renvois ne font donc pas référence à des pages, mais à d'autres entrées nominales. Quand il y a un renvoi d'index, alors il n'est pas question d'interventions."
                ""
                ""
                "Voici le texte a étudier :  "
            },
            {
                "role": "user", 
                "content": texte
            },
        ],
        response_format=IntervenantAuSenat,
        max_tokens=len(texte)*2,
        temperature=0
    )
    entries_dict = json.loads(entries.choices[0].message.content)
    entry_list = IntervenantAuSenat(**entries_dict)
    with open('./output/vt/corrected_page_2_OCR_VT__________.json', 'w', encoding='utf-8') as f:
        json.dump(entry_list.model_dump(), f, ensure_ascii=False, indent=2)
    print(entries.choices[0].message.content)  
    return "Success ! \n \n \n"  

def projection():
    with open("./output/f161.json") as f:
        data = json.load(f)
    projected_data = replace_caps_and_punct(data)
    with open('./output/f161_1_projected.json', 'w', encoding='utf-8') as f:
        json.dump(projected_data, f, ensure_ascii=False, indent=2)
    print(projected_data)

main()
# projection()