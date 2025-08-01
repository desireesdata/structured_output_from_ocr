from features.config import api_key
from features.input import get_text_from_file
from features.projection import replace_caps_and_punct
from mistralai import Mistral
from pydantic import BaseModel, Field
from typing import Union
from unidecode import unidecode
import json


model = "ministral-8b-latest"
client = Mistral(api_key=api_key)
texte = get_text_from_file("./input/tests_VT/page_2_zone_manuelles_OCR.txt", False)
# texte = get_text_from_file("./input/tests_VT/corrected_page_2_OCR_VT.txt", False)

# "moyen" 
class Action(BaseModel):
    description_action: str = Field(..., description="Description de l'action effectuée par l'intervenant")
    references_pages: list[int] = Field(..., description="Liste des numéros de page où l'action est référencée")

class Interventions(BaseModel):
    action : Action

class Renvoi(BaseModel):
    nom_entree_du_renvoi: str

class ReferencesPages(BaseModel):
    references_pages: list[int]

class Intervenant(BaseModel):
    nom_de_famille: str = Field(..., description="Nom de famille de l'intervenant")
    prenom : str = Field(..., description="Prénom de l'intervenant, s'il est mentionné")
    actions_relatives_a_l_intervenant: Union[list[Action], str] = Field(default="<renvoi d'index>", description="Soit une liste des actions relatives à l'intervenant, soit juste dire qu'il s'agit d'un renvoi d'index")

class IntervenantAuSenat(BaseModel):
    listes_des_intervenants: list[Intervenant] = Field(..., description="Liste de tous les intervenants au Sénat")

def main():
    entries = client.chat.parse(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": ""
                "Extrayez du texte que je vais vous donner, des informations de chaque entrée, lesquelles sont chacunes relatives à une personne."

                "Avant tout, sachez qu'il y a une entrée par personne et que, pour le contexte, les personnes mentionnées ont participé à l'activité du Sénat."
                "Ce sont en général des sénateurs, des ministres, des sous-secrétaires, etc."
         
                "Chaque entrée se compose : du nom et parfois du prénom d'un intervenant; parfois de son rôle (ce n'est pas toujours précisé); d'une liste d'actions qu'il a effectuées ou qui le concernent."

                "Chaque action concernant un intervenant est en général lié à un ou plusieurs numéros de page. Quand il y a une référence de page, vous pouvez être certain qu'il s'agit d'une référence d'une action concernant l'intervenant. "

                "Dans le cas où une entrée n'expose pas des actions ou des faits et/ou des pages concernant un intervenant, mais une simple mention nominale, alors il s'agit d'un renvoi d'index. Dans ce cas, il faudra indiquer la référence du renvoi (str). Ces renvois sont en général des noms/prénoms d'intervenants. Ces renvois ne font donc pas référence à des pages, mais à d'autres entrées nominales."

                "VOICI DONC LES INFORMATIONS A EXTRAIRE : Je veux donc que vous me donniez les noms (et les prénoms s'il y en a); la description des actions ou interventions relatives à l'intervenant (OU, s'il n'y en a pas, juste dire qu'il s'agit d'un renvoi d'index (<renvoi d'index>)); ainsi que, pour chacune de ces interventions, leurs références de pages."

                "Note : Quant il n'y a un renvoi d'index, adopte cette syntaxe au niveau approprié :" "actions_relatives_a_l_intervenant\": \"<renvoi d'index>\""
                
                ""
                "VOICI DONC LE TEXTE dont il faut extraire les informations :  "
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
    with open('./output/vt/moyen_02_.json', 'w', encoding='utf-8') as f:
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