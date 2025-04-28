from config import api_key
from input import get_text_from_file
from mistralai import Mistral
from pydantic import BaseModel
import json

texte = get_text_from_file("cinoche.txt", False)

class Entry(BaseModel):
    nom: str
    fonction: str
    adresse : str

class EntryList(BaseModel):
    entry: list[Entry]

model = "ministral-8b-latest"
client = Mistral(api_key=api_key)

entries = client.chat.parse(
    model=model,
    messages=[
        {
            "role": "system", 
            "content": "Extrait les informations relatives à chaque entrée. Chaque entrée est composé d'un nom (un nom propre, le nom d'une marque, etc.); d'une fonction (activité, métier, etc.); et enfin l'adresse. Fais attention, il peut y avoir du bruit. "
            "Voici mon texte :  "
        },
        {
            "role": "user", 
            "content": texte
        },
    ],
    response_format=EntryList,
    max_tokens=len(texte)*2,
    temperature=0
)

entries_dict = json.loads(entries.choices[0].message.content)
entry_list = EntryList(**entries_dict)
with open('entries.json', 'w', encoding='utf-8') as f:
    json.dump(entry_list.model_dump(), f, ensure_ascii=False, indent=2)

print(entries.choices[0].message.content)