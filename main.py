from features.config import api_key
from features.input import get_text_from_file
from features.projection import replace_caps_and_punct
from mistralai import Mistral
from pydantic import BaseModel
from typing import Union
from unidecode import unidecode
import json


model = "ministral-8b-latest"
client = Mistral(api_key=api_key)
texte = get_text_from_file("./VT/sources/01_VT_OCR.txt", False)
# texte = get_text_from_file("./input/tests_VT/corrected_page_2_OCR_VT.txt", False)

class Action(BaseModel):
    description_action:str
    references_page: list[int]

class Interventions(BaseModel):
    action : Action

class Renvoi(BaseModel):
    nom_entree_du_renvoi: str

class ReferencesPages(BaseModel):
    references_pages: list[int]

class Intervenant(BaseModel):
    nom: str
    references_pages: Union[list[int], str]
    
class IntervenantAuSenat(BaseModel):
    listes_des_intervenants: list[Intervenant]

def main():
    entries = client.chat.parse(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": ""
                "Extrayez du texte que je vais vous donner, des informations de chaque entrée, lesquelles sont chacunes relatives à une personne."

                "Avant tout, sachez qu'il y a une entrée par personne et que, juste pour le contexte, les personnes mentionnées ont participé à l'activité du Sénat."
                "Ce sont en général ses sénateurs, des ministres, des sous-secrétaires, etc."
         
                "Chaque entrée se compose : du nom et parfois du prénom d'un intervenant; parfois de son rôle (ce n'est pas toujours précisé); d'une liste d'actions qu'il a effectuées ou qui le concernent."

                "Chaque action concernant un intervenant est en général lié à un ou plusieurs numéros de page. Quand il y a une référence de page, vous pouvez être certain qu'il s'agit d'une référence d'une action concernant l'intervenant. "

                "Dans le cas où une entrée n'expose pas des actions ou des faits et/ou des pages concernant un intervenant, mais une simple mention nominale, alors il s'agit d'un renvoi d'index. Dans ce cas, il faudra indiquer la référence du renvoi (str). Ces renvois sont en général des noms/prénoms d'intervenants. Ces renvois ne font donc pas référence à des pages, mais à d'autres entrées nominales."

                "VOICI DONC LES INFORMATIONS A EXTRAIRE : Je veux donc que vous me donniez les noms (et les prénoms s'il y en a); ainsi que les numéros de pages OU, s'il n'y en a pas, la référence du renvoi."
        
                
                ""
                "Voici un exemple du format attendu : "
                "{    'listes_des_intervenants': [        {            'nom': 'Larcher',            'references_page': [                18,                20,                109            ]        },        {            'nom': 'Loureaux',            'references_pages': 'V. Michel Loureaux'        },        {            'nom': 'Montel',            'references_page': [                3            ]        },"
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
    with open('./output/vt/01_VT_OCR.json', 'w', encoding='utf-8') as f:
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