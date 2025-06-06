import re
import json
import requests

compteur = 0
jour = ""
mois = ""

def get_json(json_file: str):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            return json.dumps(json_data)
    except Exception as e:
        print(f"Erreur ! Petit problème avec le JSON : {e}")
        return None

def get_final_url(url):
    try:
        response = requests.get(url, allow_redirects=True)
        return response.url
    except Exception as e:
        print(f"Erreur lors de la récupération de l'URL finale : {e}")
        return None

def get_ark(url):
    match = re.search(r'/ark:\/\d+\/([^\s\/]+)', url)
    if match:
        return match.group(1)
    else:
        return None

def get_json_http(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erreur lors de la récupération du JSON : {e}")
        return None

def get_pages_from_manifest(manifest_url: str):
    entire_manifest = get_json_http(manifest_url)
    if entire_manifest is not None:
        manifest_str = json.dumps(entire_manifest)
        pages = re.findall(r'(?<=page\s)\d{1,4}', manifest_str)
        if pages:
            page_min = min(map(int, pages))
            page_max = max(map(int, pages))
            return list(range(page_min, page_max + 1))
        else:
            print("Aucune page trouvée dans les descriptions.")
            return []
    else:
        print("Rien trouvé")
        return []
    
def get_folio(id_ark: str):
    url = f'https://gallica.bnf.fr/services/Pagination?ark={id_ark}'
    print(f"URL appelée : {url}")
    response = requests.get(url)
    print(f"Statut de la réponse : {response.status_code}")
    # print('\n', response.content)

    if response.status_code == 200:
        pages = re.findall(r'(?<=<numero>)\d{1,4}(?=</numero>)', str(response.content))
        if pages:
            return pages
        else:
            print("Aucune page trouvée dans les descriptions.")
            return []
    else:
        print(f"Erreur lors de la récupération des données : {response.status_code}")
        return []

json_content = get_json("manifest_1931.json")
tab = []

if json_content:
    pattern = r'https:\/\/gallica\.bnf\.fr\/ark:\/12148\/cb34363182v\/date1931[^\s"]*'
    urls = re.findall(pattern, json_content)
    for url in urls:
        compteur += 1
        jour = url[-2:]
        mois = url[-4:-2]
        final_url = get_final_url(url)
        if final_url:
            manifest_url = final_url.replace('.item', '') + '/manifest.json'
            pages = get_folio(get_ark(final_url)) 
            print(pages)
            line = f"{compteur}\t{url}\t{jour}\t{mois}\t{final_url}\t{manifest_url}\t{pages}\n"
            tab.append(line)
            print(line, '\n')

with open("tab_extraction_via_api.txt", 'w', encoding='utf-8') as f:
    f.writelines(tab)
