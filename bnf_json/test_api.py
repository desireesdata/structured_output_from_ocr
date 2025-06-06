import requests
import re

lien = "https://gallica.bnf.fr/ark:/12148/bpt6k6220619d.item"

def get_ark(url):
    match = re.search(r'/ark:\/\d+\/([^\s\/]+)', url)
    if match:
        return match.group(1)
    else:
        return None

def get_folio(id_ark:str):
    response = requests.get(f'https://gallica.bnf.fr/services/Pagination?ark={id_ark}')
    if response.status_code == 200:
        # print(response.content)
        pages = re.findall(r'(?<=<numero>)\d{1,4}(?=</numero>)', str(response.content))
        if pages:
            # page_min = min(map(int, pages))
            # page_max = max(map(int, pages))
            # return list(range(page_min, page_max + 1))
            return pages
        else:
            print("Aucune page trouvée dans les descriptions.")
            return []
    else:
        print(f"Erreur !...: {response.status_code}")

test = get_folio(get_ark(lien))
print(test)