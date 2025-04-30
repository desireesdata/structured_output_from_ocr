import requests
from bs4 import BeautifulSoup
from features.config import api_key
from mistralai import Mistral
from pydantic import BaseModel
import json
import time

def scraping(url_:str)-> str:
    url = url_
    response = requests.get(url)
    text = ""
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        li_elements = soup.find_all('li')
        for li in li_elements:
            a_element = li.find('a')
            if a_element:
                # print(a_element.get_text(strip=True))
                text = text + a_element.get_text(strip=True)
                text = text + " | \n"
                text = text + "\n"
                # print(a_element['href'])
        print(text)
        return text
    else:
        print(f"Oops : {response.status_code}")

source_autorites = scraping("https://www.senat.fr/senateurs-3eme-republique/senatl.html")
exit()

class Senateur(BaseModel):
    nom : str
    prenom : str

class ListeSenateurs(BaseModel):
    senateurs : list[Senateur]

model = "ministral-8b-latest"
client = Mistral(api_key=api_key)

entries = client.chat.parse(
    model=model,
    messages=[
        {
            "role": "system", 
            "content": "Extrayez les informations du texte fourni. Je veux la liste des noms et prénoms de toutes les personnes mentionnées (des sénateurs)."
            "Attention au bruit : tout ce qu'il y a dans le texte n'est pas forcément un sénateur. "
            "Voici mon texte :  "
        },
        {
            "role": "user", 
            "content": source_autorites
        },
    ],
    response_format=ListeSenateurs,
    max_tokens=len(source_autorites)*2,
    temperature=0
)

entries_dict = json.loads(entries.choices[0].message.content)
entry_list = ListeSenateurs(**entries_dict)
with open('./output/autorites.json', 'w', encoding='utf-8') as f:
    json.dump(entry_list.model_dump(), f, ensure_ascii=False, indent=2)

print(entries.choices[0].message.content)