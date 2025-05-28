J'ai choisi trois niveaux de granularité :

- un niveau "haut" avec 1) des rôles (qui précisent si l'intervenant au Sénat n'est pas un sénateur, par exemple un ministre ou un secrétraire); 2) une liste d'actions concernant l'intervenant auxquelles sont toutes associées 3) des références de pages (int) sauf si 4) il s'agit d'un renvoi vers une autre entrée

- un niveau "moyen" qui est la même chose que le niveau haut moins les rôles

- un niveau "bas" où les références de pages ne sont pas extraites comme des entiers, mais font parties de la description.

Plus le niveau de granularité est haut, plus il y a d'erreurs; car il y a *par exemple* la difficulté pour le LLM de bien distribuer les descriptions.

Par exemple le texte brut: 
>`"Parle: discuss. d'un projet de loi portant fixation du budget général de l'exercice 1931-1932 (Instruction publique), p. 582; (Postes, télégraphes et téléphones), p. 719."` 

devient

```JSON
{
          "action": {
            "description_action": "Parle: discuss. d'un projet de loi portant fixation du budget général de l'exercice 1931-1932 (Instruction publique)",
            "references_page": [
              582
            ]
          }
        },
        {
          "action": {
            "description_action": "Parle: discuss. d'un projet de loi portant fixation du budget général de l'exercice 1931-1932 (Postes, télégraphes et téléphones)",
            "references_page": [
              719
            ]
          }
        }
```

Le LLM a ici répété ce qui permet de contextualiser une action, qui pourrait d'ailleurs être considérée comme un moment/étape d'une l'action. C'est une bonne idée que je n'avais pas envisagé au départ et que j'ai décidé de garder pour établir la VT. 

Malheureusement, cette *distribution* des éléments de contexte (ou des moments/étapes d'une action) échoue pour certains cas, à moins de réécrire le texte (ce qui impliquerait, j'imagine une température > 0, ce qui poserait probleme ?). C'est notamment le cas pour l'entrée Beaumont Jean où la "fixation de la date de la discussion" n'a pas de contexte, car ce dernier est aussi une typologie d'action différente (interpellation). Répéter cette action pour en introduire une autre d'une nature implique une contradiction (ou du moins une répétition qui n'est pas la bienvenue).

Egalement le probleme de la précision des pages où sont déposés les amendements : parfois, il est précisé à quelle page un amendement a été déposé. Malheureusement, il est difficile de trancher s'il s'agit là aussi d'une autre action et sinon, comment séparer l'information sans complexifier encore le modèle, ce qui serait porteur de nouvelles erreurs.

Il arrive aussi que parfois, (assez rarement, à voir au moment de l'évaluation) que le LLM ignore des portions de phrases.

L'hypothèse de d'une granularité plus basse, avec seulement des distictions entre les différentes actions, semble ne produire aucune erreur (en tout cas pour la correction de la VT). 

> exemple :

```JSON
 {
      "nom": "Beaumont",
      "prenom": "Jean",
      "actions_relatives_a_l_intervenant": [
        "Parle: discuss. d'un projet de loi portant fixation du budget général de l'exercice 1931-1932 (Agriculture), p. 477.",
        "Demande à interpeller sur les mesures que compte prendre le Gouvernement pour prévenir les crises agricoles, notamment celles qui sévissent sur l'élevage national que préparent les importations massives de matières alimentaires, p. 1087; parle: fixation de la date de la discuss., p. 1130; développe son interpellation, p. 1287.",
        "Parle : discuss. d'un projet de loi relatif à l'outillage national, p. 1667, 1674, 1708."
      ]
    },
    {
      "nom": "Bénard",
      "prenom": "Léonus",
      "actions_relatives_a_l_intervenant": [
        "Parle: discuss. d'un projet de loi relatif au crédit colonial, p. 146, 148.",
        "Dépose et lit son rapport sur un projet de loi désignant un nouveau lieu de déportation, p. 832."
      ]
    },
```

Certes, les numéros de pages sont solidaires au texte, mais une extraction *a posteriori* via une regex est moins incertain que de laisser le LLM à produire des distinctions/séparations qui impliquent un risque de confusion, car le forçant à trancher (cf. le cas des amendements déposés et/ou du probleme de la distribution du contexte). L'approche "moins c'est plus" pose le probleme que l'historien/utilisateur de l'outil corpusense qui voudrait exploiter le texte, n'aura pas les données "toutes prêtes" car il faudrait extraire les numéros de page avec la Regex, sauf si cette extraction fait partie du workflow... 

