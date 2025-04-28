# Structured output from text (ocr)

Create virtual environment, enable it and :

```
pip install -r requirements.txt
```

Then run `python3 main.py` or `python main.py`

## Evaluation:

(à faire)
- Vérité terrain
    - A partir de CSV plutôt que JSON 
- Normaliser les strings (ponctuation + bas de casse etc.)
- Calcul des distances 

- Pour le traitement API-->JSON, utiliser **async**

> Sources :
> - truth ground 01 : https://gallica.bnf.fr/ark:/12148/bd6t543024772/f28.item

### Idées

- démo géocodage des adresses via folium

###

```Regex
(?<=\(\d)\ 
(?<=\d)\ (?=\w)
\d(\ )\w*
\ (?=\))
```

Comme `diff` pour aperçu :

```shell
diff -h -b --color json_converted.csv truth_grnd_01.csv 
```