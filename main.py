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
    action_du_senateur:list[str]
    references_page: list[str]

class Interventions(BaseModel):
    interventions : list[Action]

class RenvoiAutreEntree(BaseModel):
    nom_entree_du_renvoi: str

class Senateur(BaseModel):
    nom_du_senateur: str
    interventions_du_senateur: list[Interventions] | None
    renvoi_d_index : RenvoiAutreEntree | None

class Senateurs(BaseModel):
    listes_des_senateurs: list[Senateur]

def main():
    entries = client.chat.parse(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": "Extrayez du texte que je vais vous donner, les informations relatives à chaque personne, à savoir des sénateurs. Il y a une entrée par personne."
                "Chaque entrée est composée du nom et du prénom d'un sénateur, suivi d'une liste d'actions qu'il a effectuées ou qui le concernent. "
                "Chaque intervention ou action qui concerne un sénateur est lié à un ou plusieurs numéros de page : il faut également les indiquer, mais séparemment de leur description. "
                "Dans le cas où une entrée n'expose pas des actions ou des faits concernant un sénateur, alors il s'agit d'un renvoi d'index. Dans ce cas, ne mentionne pas d'interventions (None) mais la référence du renvoi."
                ""
                "Un exemple : "
                "{"
  "\"listes_des_senateurs\": ["
   " {"
      "\"nom_du_senateur\": \"Larcher Gérard\","
     " \"interventions_du_senateur\": ["
        "{"
          "\"interventions\": ["
            "{"
              "\"action_du_senateur\": ["
               " \"Est proclamé secrétaire du Sénat\""
              "],"
              "\"references_page\": ["
                "\"p. 8\""
              "]"
            "},"
            "{"
              "\"action_du_senateur\": ["
                "\"Parle: discuss. d'un projet de loi portant fixation du budget général de l'exercice 1931-1932 (Instruction publique)\""
              "],"
              "\"references_page\": ["
               " \"p. 582\""
             " ],  \"renvoi_d_index\": null"
          "  },"
                ""
                "Voici le texte a étudier :  "
            },
            {
                "role": "user", 
                "content": texte
            },
        ],
        response_format=Senateurs,
        max_tokens=len(texte)*2,
        temperature=0
    )
    entries_dict = json.loads(entries.choices[0].message.content)
    entry_list = Senateurs(**entries_dict)
    with open('./output/vt/corrected_page_2_OCR_VT_.json', 'w', encoding='utf-8') as f:
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