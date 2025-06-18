Plan mémoire : 

- **Introduction**
  
  - Exposer les "nouvelles frontières de l'historien" et les nouveaux enjeux des méthodes quantitatives. Rappeler les origines de la discipline :
    
    - Mentionner des éléments d'historiographie classique (Histoire sociale, Ladurie, Febvre, Prost, etc.)
    
    - Mentionner des éléments d'historiographie contemporaine (Kemman, Marie Puren, *Les Annales* 2015, Salmi, Claire Lemercier, etc.)
    
    - Mentionner des réponses techniques existantes à ces enjeux (eScriptorium, Aikon, etc.)
  
  - Exposer problématiques propres à l'extraction de l'information des documents sériels, matière "taillée" pour les approches quanti et constitutive du positionnement de Mezanno (BnF/EPITA/IGN/EHESS) : 
    
    - Mentionner "les fruits faciles" (même si pas trival) des documents sériels, 
    
    - Question de la valorisation des "fonds dormants". Le cas du J.O.
    
    - Mentionner texte d'OCR + les approches LLMs, vs les approches Bert (utilisées pour SODUCO) pour leur extraction sémantique
  
  - Conclure intro sur mon positionnement/rôle : du besoin de mettre à disposition des outils d'évaluation, avec le J.O. comme cas d'étude, pour pouvoir avoir une utilsation raisonnée / motivée des outils en SHS, comportant des biais.

  - **Parie 1 : Les sources**. 
  
  - Le J.O. de la IIIeme République : horizon historique
    
    - Des archives ?
    
    - La République et le Journal : publier, publiciser (sur la fonction démocratique/juridique du J.O. car utile au débat public mais nécessaire sur un plan légal) 
    
    - Les mains du J.O : sténographes, imprimeurs, secrétaires. (SACIJO).
  
  - Le J.O. de la IIIe République, image des "processus métiers" du Sénat.
    
    - De l'ordre du jour à la publication dans le J.O. : vue d'ensemble des processus parlementaires côté Sénat.
    
    - Organisation des différentes parties du J.O : Tables nominatives, tables analytiques; publication quotidiennes, publications annuelles. Leur relation avec les productions du Sénat
    
    - Informations sémantiques des tables, relations entre elles.
  
  - "Lire à distance" le J.O. ?
    
    - hypothèses sur les productions **possibles** à partir des données extraites du  J.O. Mentionner les exemples de liage de données, Zeitgeist, topic modeling.
    
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


- **Partie 3 : Mise en application (Cas d'étude : le table de 1931.). Evaluation de l'approche de la sortie structurée**
  
  - Génération structurée, sortie structurée ? (iaetbibliotheque)
    
    - Parler de ces deux approches
    
    - API Mistral (Expliquer ce qu'est une API !)
    
    - Exemple avec la Table. Parler du JSON
  
  - Fiabilité de la sortie structurée (exposition de la méthode d'évaluation)
    
    - Exposer risques / problème (hallucinations, ici avec une température à zéro, concernent les mauvaises attributions du LLM. Biais OCR se répercutent ? Question du prompting, de ses limitations. Mentionner des différences avec approche BERT.
    
    - Exposer la méthode d'évaluation des erreurs d'attributions : matrice de coût + le problème d'assignement (appariement) ; scoring avec fonction de densité. Partir des vérités terrain
      
      - Vérités terrain : une vérité pas si évidente que ça : quel modèle pour quels usages ?
    
    - Résultats et commentaire des tests
  
  -  Exploitation des résultats ?
