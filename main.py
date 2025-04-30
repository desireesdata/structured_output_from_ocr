from features.config import api_key
from features.input import get_text_from_file
from features.projection import replace_caps_and_punct
from mistralai import Mistral
from pydantic import BaseModel
from unidecode import unidecode
import json


model = "ministral-8b-latest"
client = Mistral(api_key=api_key)
texte = get_text_from_file("./input/exported_text_corpusense.txt", False)

class Action(BaseModel):
    action_du_senateur:list[str]
    references_page: list[str]

class Interventions(BaseModel):
    #resume: str
    interventions : list[Action]

class Senateur(BaseModel):
    nom_du_senateur: str
    interventions_du_senateur: list[Interventions]

class Senateurs(BaseModel):
    listes_des_senateurs: list[Senateur]

def main():
    entries = client.chat.parse(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": "Extrait du texte que je vais te donner, les informations relatives à chaque personne (des sénateurs) : il y a une entrée par personne."
                "Chaque entrée est donc composé du nom et du prénom d'un sénateur, suivi d'une liste d'interventions qu'il a effectué."
                "Chaque intervention est liées à un ou plusieurs numéros de page : il faut également les indiquer, mais séparemment de leur description. "
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
    with open('./output/f161.json', 'w', encoding='utf-8') as f:
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
projection()