# Notes

Les données cleanées sont celles du fichier `data_1931.csv`

> Des données ont été ajoutées à la main, car lacunaires (celles du 2 avril): 
`33	https://gallica.bnf.fr/ark:/12148/cb34363182v/date19310402	2	4	https://gallica.bnf.fr/ark:/12148/bpt6k6220642n.item	https://gallica.bnf.fr/ark:/12148/bpt6k6220642n/manifest.json	['933', '934']`

## Récupérer tous les J.O. d'une année 

Changer la date si besoin : `https://gallica.bnf.fr/ark:/12148/cb34363182v/date1931/manifest.json` (il faut juste ajouter `/manifest.json` et le numéro après 1931)

```Regex
(?<="url":\s")https:\/\/gallica\.bnf\.fr\/ark:\/12148\/cb34363182v\/date1931.*"(?=,\n\s{1,}"etat":)
```

> Note : pour récupérer toutes les années : `https://gallica.bnf.fr/ark:/12148/cb34378481r/date.r=Journal+officiel+de+la+republique+francaise+Lois+et+decrets.langFR/manifest.json`. 

On récupère ce genre d'object JSON :

```json
        "contenu": "611 numéros",
        "description": "1931",
        "selected": false,
        "url": "https://gallica.bnf.fr/ark:/12148/cb34378481r/date1931",
        "etat": ""
```

### Récupérer pagination avec API Gallica


Une fois que l'on connaît tous les identifiants ark d'une année, on peut utiliser les API pour récupérer par exemple les éléments de pagination : 

```bash
curl "https://gallica.bnf.fr/services/Pagination?ark=bpt6k6434743d"
```

Retourne (extrait) : 

```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<livre>
<structure>
<firstDisplayedPage>1</firstDisplayedPage>
<hasToc>false</hasToc>
<TocLocation>0</TocLocation>
<hasContent>true</hasContent>
<idUPN>bpt6k6434743d</idUPN>
<nbVueImages>38</nbVueImages>
</structure>
<pages>
<page>
<numero>1797</numero>
<ordre>1</ordre>
<pagination_type>A</pagination_type>
<image_width>3550</image_width>
<image_height>5019</image_height>
</page>
<page>
<numero>1798</numero>
<ordre>2</ordre>
<pagination_type>A</pagination_type>
<image_width>3601</image_width>
<image_height>4989</image_height>
</page>
<page>
<numero>1799</numero>
<ordre>3</ordre>
<pagination_type>A</pagination_type>
<image_width>3619</image_width>
<image_height>4965</image_height>
</page>
```

Exemple : 

- URL : https://gallica.bnf.fr/ark:/12148/bpt6k6220619d
- ARK : bpt6k6220619d
- REQUETE API : `curl "https://gallica.bnf.fr/services/Pagination?ark=bpt6k6220619d"̀