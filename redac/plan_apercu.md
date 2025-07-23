Plan mémoire : 

>  Pédagogique éléments techniques



- **Introduction**
  
  > comment mettre l'évaluation au service d'une démarche historique.

  - Exposer les "nouvelles frontières de l'historien" et les nouveaux enjeux des méthodes quantitatives. Rappeler les origines de la discipline :
    
    - Mentionner des éléments d'historiographie classique (Histoire sociale, Ladurie, Febvre, Prost, etc.)
    
    - Mentionner des éléments d'historiographie contemporaine (Kemman, Marie Puren, *Les Annales* 2015, Salmi, Claire Lemercier, etc.)
    
    - Mentionner des réponses techniques existantes à ces enjeux (eScriptorium, Aikon, etc.)
  
  - **Exposer problématiques propres à l'extraction de l'information des documents sériels**, matière "taillée" pour les approches quanti et constitutive du positionnement de Mezanno (BnF/EPITA/IGN/EHESS) : 
    
    - Mentionner "les fruits faciles" (même si pas trival) des documents sériels, 
    
    - Question de la valorisation des "fonds dormants". Le cas du J.O.
    
    - Mentionner texte d'OCR + les approches LLMs, vs les approches Bert (utilisées pour SODUCO) pour leur extraction sémantique
  
  - Conclure intro sur mon positionnement/rôle : du besoin de mettre à disposition des outils d'évaluation, avec le J.O. comme cas d'étude, pour pouvoir avoir une utilsation raisonnée / motivée des outils en SHS, comportant des biais.

  - **Parie 1 : Les sources**. 

  > Ajouter Focus la sorurce des tables ! aspect "typographique"
  > Pourquoi cette table là ?  Changement de mise en page. 

  - Le J.O. de la IIIeme République : horizon historique
    
    - Des archives ?
    
    - La République et le Journal : publier, publiciser (sur la fonction démocratique/juridique du J.O. car utile au débat public mais nécessaire sur un plan légal) 
    
    - Les mains du J.O : sténographes, imprimeurs, secrétaires. (SACIJO).
  
  - Le J.O. de la IIIe République, image des "processus métiers" du Sénat.
    
    - De l'ordre du jour à la publication dans le J.O. : vue d'ensemble des processus parlementaires côté Sénat.
    
    - Organisation des différentes parties du J.O : Tables nominatives, tables analytiques; publication quotidiennes, publications annuelles. Leur relation avec les productions du Sénat
    
    - Informations sémantiques des tables, relations entre elles.
  
  - "Lire à distance" le J.O. ?
  - RAG
    
    - Problème de l'anachronisme des catégories : biais des modèles VS cadre énonciatif du XXe siècle. (Lemercier, Foucault, Loraux)
    
    - LLMs et lecture à distance : produire d' "hallucinants" résultats ? ==> mentionner l'approche LLM pour extraire des données structurées. C'est l'approche retenue pour Mezanno (car facile à mettre en place). Mais, on ne peut pas utiliser scientifiquement des résultats produits par des LLMs, sachant ses limitations.

- **Partie 2 : le Projet Mezanno. Aspects institutionnels et techniques**
  
  - Contexte institutionnel : projet Soduco, AGODA. Liens BnF/EHESS/IGN/Epita. ANR.
  
  - Problématique de départ sur l'annotation des sources (consortium IIIF).
    
    - Journée d'études janvier 2025.
    
    - Différentes approches : eScriptorium, AIkon, etc.
  
  - Outil Corpusense (en développement)
    
    - "les instruments sont de la théorie réifiée" : exposer le workflow, de l'image OCRisée à la donnée structurée pour l'historien.ne
    
    - Différences avec les autres solutions : la génération structurée et la spécialisation de documents sériels.

  - Génération structurée, sortie structurée ? \(iaetbibliotheque)\
    
    - Parler de ces deux approches
    
    - API Mistral (Expliquer ce qu'est une API !)
    
    - Exemple avec la Table. Parler du JSON

- **Partie 3 : Mise en application (Cas d'étude : le table de 1931.). Evaluation de l'approche de la sortie structurée**

> Focus technique, évaluation.
Comment faire le lien "historien" / "ingénieur".
  
  - Fiabilité de la sortie structurée (exposition de la méthode d'évaluation)
    
    - Exposer risques / problème (hallucinations, ici avec une température à zéro, concernent les mauvaises attributions du LLM. Biais OCR se répercutent ? Question du prompting, de ses limitations. Mentionner des différences avec approche BERT.
    
    - Exposer la méthode d'évaluation des erreurs d'attributions : matrice de coût + le problème d'assignement (appariement) ; scoring avec fonction de densité. Partir des vérités terrain
      
      - Vérités terrain : une vérité pas si évidente que ça : quel modèle pour quels usages ?
    
    - Résultats et commentaire des tests
  
  -  Exploitation des résultats ?


  > Résultats : écueils / challenge. Livrables données : Vérité terrain. Codes + prompts + data. Intégration corpusense ?
  > Développements futurs : qu'apporte le projet corpusense ? aux institutions patrimoniales. Techniques de prompting pour chercheur utilisateur.

  Bien lister les contributions du travail : 
  - Refaire état des lieux corpus ()
  - la formalisation d'une démarced de création de données structurée
  - eval extrinsqe
  - prodction données de ref
  - co-implémetntation technique d'évaluation

  Perspective directe : 

- Venir tester de façon systématiques les prompts (benchamark à plusieurs dimensions)
- quelles sont les strcutres qu'on peut espérer extraitre
- quels prompts ?

Utiliser un réseau génératif pour créer des prompts.
- Ouv
  
> Commencer 2/3. Ne pas oubier dissection de la source : impact structuration de la donnée !
Structurer autour des contribuations

> Compresser les parties 1/2? pour ajouter une "4" eme partie aspect "interprétation / exploitation des données"


> JSON, expliciter pourquoi 

produire / vérifier / interpérater

> 2 : Aspects donénées ne sont jamais parfaites : 
> Donner les outils pour une évaluation systématique

"Approche exploratoire"

"Approche LLM".

Pierre Carles LLM éthique.

====

PArtie 2 + 3
+ introduction et conclusion

"penser archiviste" : être pédagogue !!!
ëtre didactique.

+ annexe github

lien vers repo ==> développer README cadre TNAH; structure repo (dossiers / file); Badges langages utilisés; CCBY per la licence

> short paper CHR : position paper (donner opinion sur le sujet)
Comment donner confiance / obstacles à la confiance ?
Contexte humanités numériques (faut il employer les méthodes de benchmark côté informatique)

Réutiliser les données des autres, utiliser leur brosse à dent

Données tellement taillées pour une question de recherche.


Comment donner confiance dans les données (dans les corpus massif ou semi massifs en histoire).

On respecte une chaine de traitement :
tendance à ne pas utiliser les données des autres (interprétation modélisante) Données par réutilisées

Idées : quand on produit des données de manière automatique moins bien que données produites manuellement


La question des métriques 
comparaison VT / P
Donner exemple (avec Sénat) 
Le rag Aurelien, question avec LLM ==> méfiance, surtout côté des "ingénus".

Papier à écrire pour le 18 ! (semaine du 14 juillet rempli, gaffe)

1) données pour rpz chaine de traitement (surtout sur la question de l'évaluation)
2) 

Données pas neutres <=== impliquées par question de recherche
LLM <== cristallisent des biais (parti pris, parce que situé)

Documenter la non-neutralité, les admettre  

Etage des données : comment savoir si on est aligné par rapport à nos questions

Illustration.

Pourquoi LLM ; technique.
Adaptable ;
Pas beaucoup de codes ?
LLMs 

Spécificité des données : question de design.
Rectification.

Parallèle.



			*	*	*
	
PROBLEMATIQUE, SOURCES DE DONNES STRCTUREES, COMMENT FAIRE POUR LES RENDRE ACCESSIBLES AUX HISTORIENS? EN RETIRER LE PLUS DE MATIERE POSSIBLES? QUELS DEFIS, QUELS CHALLENGE?
ARCHIVES INSTITUTIONNELLES ==> annuaires biographies, tables, lois et décrets. "VALORISER" DES SOURCES : pas de goût de l'archive? "archives sans goût". Traces pas émouvantes mais importante. Rapport émotionnel ? Sources inexploités ou difficies à transcrire. (Dépouillement sans qualité)

Histoire et mesure (dernier numéro) (cumulativité). pour mesure divers choses.

écrire protocole DANS LE CADRE DE l'HISTOIRE (ARCHIVES INSTITUTIONNELLES). Beaucoup de données structurées, mais regorgent d'information, être capable de les extraire pour les lier avec d'autres sources. (Pour savoir combien de fois un tel à fait ça, etc). La bibliographie de la France; Annuaires; tous ces fonds utiles mais "pas agréables à lire). Domaine des données structurées. Comment en tirer le plus de données pour des histoiriens (notamment) : je ne suis pas conduit par une question fermée, mais comment on fait pour mettre en place un protocole expérimental pour en extrait la moelle.
	
1- Pourquoi LLM (détailler la source diplo). Choix pas neutre. Pourquoi pas REGEX (pas généralisables tableau comparatif)? ça gagne du temps, données plus propre au final. Taillé pour plusieurs tâches... Vérifier les limites du LLM

Quoi de plus quoi de moins 
Problèmematique data sctructurée (approche exploratoire)
- que peut on faire pour producteur de données pour permettre d'utiliser ces données pour répondre à une question de recherche

Le choix de la mise en place de la chaine de traitement, quel impact sur la sortie ? (parti pris A JUSTIFIER !!!) Début de réponse ==> Super adaptable, code léger. Quels risques (hallucinations, sensibilisation, oublis)...

Comment ça informe le résultat ?

2) Question Evaluation. D

OCR ==>
Stats, le transport optimal est-il optimal?
Pourquoi cette méthode pas une autre ? Pourquoi ces quatres données à comparer, et comment ?
4 données comparées : comment ça donne confiance ?
Expliciter protocole

3