Source : 

![https://gallica.bnf.fr/ark:/12148/bpt6k65430703/f161.item](https://gallica.bnf.fr/ark:/12148/bpt6k65430703/f161.highres "JO, f161, tables du Sénat") .

### Notes 

Pour les VT, j'ai choisi quatre niveaux de granularité :

- un niveau "haut" avec 1) des rôles (qui précisent si l'intervenant au Sénat n'est pas un sénateur, par exemple un ministre ou un secrétraire); 2) une liste d'actions concernant l'intervenant auxquelles sont toutes associées 3) des références de pages (int) sauf si 4) il s'agit d'un renvoi vers une autre entrée

- un niveau "moyen" qui est la même chose que le niveau haut moins les rôles

- un niveau "bas" où les références de pages ne sont pas extraites comme des entiers, mais font parties de la description.

- une niveau "épuré" ou seuls les noms des sénateurs et les pages où ils apparaissent sont mentionnés (utile pour faire un "Zeitgeist-like" de Google par exemple)

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

Si c'est un format très intéressant (on a la référence de page pour chaque action de façon indépendante), malheuresement ça implique le LLMs à faire des choix :

En effet, le LLM a ici répété ce qui permet de contextualiser une action, qui pourrait d'ailleurs être considérée comme un moment/étape d'une l'action. C'est une bonne idée que je n'avais pas envisagé au départ et que j'ai décidé de garder pour établir la VT. 

Malheureusement, cette *distribution* des éléments de contexte (ou des moments/étapes d'une action) échoue pour certains cas, à moins de réécrire le texte (ce qui impliquerait, j'imagine une température > 0, ce qui poserait probleme ?). C'est notamment le cas pour l'entrée Beaumont Jean où la "fixation de la date de la discussion" n'a pas de contexte, car ce dernier est aussi une typologie d'action différente (interpellation). Répéter cette action pour en introduire une autre d'une nature implique une contradiction (ou du moins une répétition qui n'est pas la bienvenue).

Egalement le probleme de la précision des pages où sont déposés les amendements : parfois, il est précisé à quelle page un amendement a été déposé. Malheureusement, il est difficile de trancher s'il s'agit là aussi d'une autre action et sinon, comment séparer l'information sans complexifier encore le modèle, ce qui serait porteur de nouvelles erreurs.

Il arrive aussi parfois, (assez rarement, à voir au moment de l'évaluation) que le LLM ignore des portions de phrases.

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

Certes, les numéros de pages sont solidaires au texte, mais une extraction *a posteriori* via une regex est moins incertain que de laisser le LLM à produire des distinctions/séparations qui impliquent un risque de confusion, car le forçant à trancher (cf. le cas des amendements déposés et/ou du probleme de la distribution du contexte). L'approche "moins c'est plus" pose le probleme que l'historien/utilisateur de l'outil corpusense qui voudrait exploiter le texte, n'aura pas les données "toutes prêtes" car il faudrait extraire les numéros de page avec la Regex, sauf si cette extraction fait partie du workflow... Tout dépend aussi de quel historien.ne fait le traitement; ou encore de quel contexte de recherche il s'agit. (Difficile de séparer l'outil technique de son contexte social de production comme dirait Simondon !... ou encore Karl Marx haha)

Une autre solution intermédiaire (à voir si c'est intéressant) est de garder et tout le texte de la description (pages incluses) et les numéros de pages comme des entiers dans une liste à part. Exemple :

```JSON

  "listes_des_intervenants": [
    {
      "nom": "Babin-Chevaye",
      "prenom": "",
      "actions_relatives_a_l_intervenant": [
        "Est proclamé secrétaire du Sénat, p. 8.",
        "Parle: discuss. d'un projet de loi portant fixation du budget général de l'exercice 1931-1932 (Instruction publique), p. 582; (Postes, télégraphes et téléphones), p. 719."
      ],
      "references_pages": [
        8,
        582,
        719
      ]
    },
    {
      "nom": "Bachelet",
      "prenom": "Alexandre",
      "nom_entree_du_renvoi": "V. Alexandre Bachelet"
    },
    {
      "nom": "Barthou",
      "prenom": "Louis",
      "actions_relatives_a_l_intervenant": [
        "Son allocution à l'occasion du décès du maréchal Joffre, p. 2.",
        "Parle: discuss. d'un projet de loi relatif à l'exploitation des lignes de l'aéropostale, p. 394, 396, 397, 399.",
        "Son amendement déposé au cours de la discuss. d'un projet de loi portant ouverture et annulation de crédits sur l'exercice 1930-1931 au titre du budget général et des budgets annexes, p. 1211.",
        "Parle : rectification au procès-verbal, p. 1237."
      ],
      "references_pages": [
        2,
        394,
        396,
        397,
        399,
        1211,
        1237
      ]
    }
  ]
```

Ou bien de demander au LLMS de ne pas séparer les différents moments d'une action. On le voit, il y a beaucoup de possibilités et qui dépendent ici du prompting. Malheureusement, la complexité de la formulation pourrait rendre difficile le passage du particulier au général, sur d'autres pages du J.O. réputées inconnues...

On voit que le probleme de constituer une vérité terrain semble simple de prime abord. Mais la structuration des données, même dans un scénario optimal de machines avec 100% de succès qu'est censé représenter la VT, implique quand même de trancher et d'abandonner certaines spécifictés documentaires, à l'instar celles des Tables et ce malgré la rigueur de la composition. On pourrait bien sur établir un niveau de granularité extrêmement fin qui rendent compte des spécificités sur une ou deux pages.... mais impossible de le savoir *a priori* pour des dizaines, des centaines voire des milliers de page. Faire un modèle de représentation des données implique nécessairement de "gommer" le grain atomique de la matière documentaire -- et le commentaire le plus exhaustif de quelque chose c'est la chose elle-même comme a du dire Todorov (je crois) dans "Poétique".

#### NB : autre proposition

Pour effectuer un Zeitgeist-like (façon Google), une autre proposition, sans les actions des sénateurs :

```JSON
{
            "nom": "Boivin-Champeaux",
            "references_page": [
                1,
                344,
                376,
                379,
                406,
                784,
                1590
            ]
        },
        {
            "nom": "Bompard Maurice",
            "references_page": [
                754
            ]
        },
        {
            "nom": "Bon",
            "references_page": [
                1417
            ]
        },
```