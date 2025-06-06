import requests
import re
import json

def get_json_http(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        return response.json()  # Parse le contenu JSON
    except Exception as e:
        print(f"Erreur lors de la récupération du JSON : {e}")
        return None

def get_pages_from_manifest(manifest_url: str):
    entire_manifest = get_json_http(manifest_url)
    if entire_manifest is not None:
        manifest_str = json.dumps(entire_manifest)
        pages = re.findall(r'(?<=page\s)\d{1,4}', manifest_str)
        page_min = min(pages)
        page_max = max(pages)
        pages = []
        for i in range(int(page_min), int(page_max)+1):
            pages.append(i)
        return pages
    else:
        print("Rien trouvé")
        return []

# text = get_json_http("https://gallica.bnf.fr/ark:/12148/bpt6k6220610p/manifest.json")
# if text:
#     with open("test.txt", 'w') as f:
#         f.write(json.dumps(text))

print(get_pages_from_manifest("https://gallica.bnf.fr/ark:/12148/bpt6k6220610p/manifest.json"))
