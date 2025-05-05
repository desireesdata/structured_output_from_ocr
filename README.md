# Structured output from text (ocr) via Mistral API 

> Sources : https://docs.mistral.ai/capabilities/structured-output/custom_structured_output/

Create virtual environment, enable it and :

```
pip install -r requirements.txt
```

Then run `python3 main.py` or `python main.py`

## Evaluation:

(à faire)
- Vérité terrain
    - A partir de CSV plutôt que JSON pour faire des tests aussi avec SQL et recherche floue?
- Normaliser les strings (ponctuation + bas de casse etc.)
- Calcul des distances 

- Pour le traitement API-->JSON, utiliser **async**

> Sources :
> - truth ground 01 : https://gallica.bnf.fr/ark:/12148/bd6t543024772/f28.item

### Idées

- démo géocodage des adresses via folium

### Notes

Regex pour nettoyer sur la vérité terrain les espaces en général contenues dans les parenthèses

> Voir fonctions de normalisation du benchmark

```Regex
(?<=\(\d)\ 
(?<=\d)\ (?=\w)
\d(\ )\w*
\ (?=\))
((?<=\d)\ (?=\w.*\ \)))
```

Comme `diff` pour aperçu :

```shell
diff -h -b --color json_converted.csv truth_grnd_01.csv 
```

> La somme des distances de Levenshtein entre les mots individuels d'une liste n'est pas nécessairement égale à la distance de Levenshtein entre les chaînes concaténées des deux listes. 

Aberrations à cause de l'OCR : se mêlent les margent et le labeur, d'où le pic.

![alt text](benchmark/img/stats.png "Title")
![alt text](benchmark/img/abberations_marges.png "Title")

Comment déterminer le seuil minimal de distance de LEv ? Voir si ce qui est couvert par la recherche floue

---
Faire chemin global de la chaine de traitement

1) Prompt pour générer données
2) Evaluation quantitative avec vérité terrain ===> Projection (simplification des chaines de caractères) ==> matrice d'appariment en fonction des distances de lev (demadner à vérifier méthodo) sorte d'étude des bijections ===> scoring; et (avec?) fonction de densité de Prédiction /Expected 1, P1/E3, p1 étant prédiction == scoring
3) Valoriser avec données des Tables
4) évalutation quali presque une détection d'hallucinations (visualisation des présence et absences)
5) Débats / ciné : tester la méthode sur l'un et l'autre corpus (**facultatif ?**)
6) Tester avec d'autres modèles (LLama + outlines, Chat GPT, etc.)


échantillonage et vérité terrain : prendre zone représentative: 5 groupes de pages.

---
Après avoir testé vite fait avec la Cinémathèque, retour au JO. Objectif, tester / évaluer avec les vrais documents avec une situation "favorable" (scénario d'extraction colonne par colonne)

1) Extraction via corpusense
    - source choisie : https://gallica.bnf.fr/ark:/12148/bpt6k65430703/f161.item
2) Projection : 
    - il y a des symboles égals (présents dans la source)
    - remplacement de tous les symboles de ponctuation par des points
    - remplacement des majuscules par des basses casses
3) Le calcul des distances : pas si évident de faire un choix sur la méthode car il faut considérer à la fois la structure (TED) et les différences entre les noeuds de chaque arbre ! Les "objets" sont des abres, pas des labels : on ne peut pas faire une matrice "à plat".
    - Je pars du principe que la structure est un a priori nécessaire : tout calcul doit repose sur une TED strictement égale à zéro.
    - Si 0 --> calcul distance de Levshtein entre chaque noeud cousin

___

Ce qu'on veut : évaluer la qualité du JSON prédit en le comparant avec une vérité terrain. Pour ce faire, il faut vérifier si chaque valeur prédite est en bijection avec la vérité terrain. Mais dans le cas d'une application de l'ensemble de valeur de P vers la vérité terrain est une surjection, il faudra choisir le cable le plus pertinent avec la distance de Levenstein. Le cas injectif (oublis), il faudra réfléchir à une application qui va cette fois de l'autre sens ?