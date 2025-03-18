# Prompts utilisés pour ce projet

## ChatGPT o3-mini
## Prompt fait à ChatGPT pour générer un meilleur prompt à Claude

Avec l'image que je viens de te donner, créer le meilleur prompt à donner à une IA générative pour créer le projet porté dans le cahier des charges que je te donne

PS : "L'image" est une capture d'écran d'un tweet de Greg Brokman donnant des astuces pour faire de meilleurs prompts. Le sujet du TP a également été donné (cahier des charges)


## Claude 3.7 Sonnet Thinking
## Prompt Principal pour la création du jeu Tetris Humain vs IA

Mets toi dans la peau d'un Software Engineer. Je t'ai donné en pièce jointe mon repository Github vide ainsi que le cahiers des charges. Réalise le projet en respectants les instructions suivantes :

Goal
Créer un jeu Tetris à deux joueurs (un humain et une IA) en Python avec Tkinter, conformément au cahier des charges suivant :
* Deux grilles : une pour le joueur humain, une pour l’IA, affichées côte à côte.
* Contrôles :
   * Joueur humain : utiliser les flèches du clavier (gauche/droite pour se déplacer, bas pour accélérer la descente, haut pour faire pivoter la pièce).
   * IA : l’IA doit placer les pièces de façon automatique, selon une logique simple (pas besoin d’un algorithme complexe).
* Tableau des scores : afficher en direct les points de chaque joueur.
   * 50 points par ligne complétée.
   * Bonus : +100 pour 2 lignes d’un coup, +200 pour 3 lignes, +300 pour 4 lignes (Tetris).
* Règles fun :
   1. Cadeau surprise : si un joueur complète 2 lignes d’un coup, l’adversaire reçoit une pièce « facile » (carré ou ligne) pour l’aider.
   2. Pause douceur : tous les 1 000 points, la vitesse de chute des pièces est réduite de 20 % pendant 10 secondes pour les deux joueurs.
   3. Pièce rigolote : tous les 3 000 points, une pièce spéciale (cœur, étoile, etc.) apparaît et rapporte 100 points bonus si elle est bien placée.
   4. Arc-en-ciel : toutes les 2 minutes, les pièces changent de couleur pendant 20 secondes (effet purement visuel).
* Livrables :
   * Un dépôt GitHub public contenant :
      * Tout le code source.
      * Un fichier PROMPTS.md documentant la liste des prompts utilisés pour réaliser le projet.
      * Un fichier README.md détaillant la procédure pour lancer le projet.
Le but est donc de générer l’intégralité du code Python (avec Tkinter) pour ce Tetris deux joueurs (Humain vs IA) et de respecter les règles et fonctionnalités décrites.

Return Format
1. Code source complet sous forme de script(s) Python.
2. Organisation du code avec des fonctions/classes clairement identifiées.
3. Commentaires expliquant les parties importantes du code (logique IA, gestion des bonus, etc.).
4. Fichier README (ou contenu à intégrer dans le README.md) :
   * Dépendances nécessaires.
   * Instructions pas à pas pour lancer le jeu.
   * Brève description de chaque fonctionnalité.
5. Fichier PROMPTS (ou contenu pour PROMPTS.md) :
   * Récapituler ce prompt et éventuellement d’autres prompts utilisés.
La sortie attendue doit donc être un « package » de code et de documentation prêt à être déployé sur un dépôt GitHub.

Warnings
* Vérifier que la logique de l’IA ne bloque pas le jeu ou ne le rend pas trop lent.
* S’assurer que le scoring fonctionne correctement, en particulier pour les bonus (2 lignes, 3 lignes, 4 lignes).
* Respecter les règles fun (cadeau surprise, pause douceur, pièce rigolote, arc-en-ciel) et vérifier qu’elles se déclenchent correctement.
* Faire attention aux coordonnées et aux collisions des pièces dans chaque grille.
* Éviter les dépendances inutiles : Tkinter est inclus de base avec Python, mais préciser toute autre librairie externe si utilisée.
* Assurer une bonne gestion d’erreurs (pas de crash majeur) et une interface jouable.

Context Dump
Nous devons rendre ce projet Tetris pour un cours/une évaluation où la qualité des prompts et la documentation (fichier PROMPTS.md) sont aussi importantes que le code lui-même. L’IA doit être simple mais jouable, et l’humain peut s’amuser en mode local, chacun ayant sa propre grille.
De plus, nous voulons un effet « wow » via les règles fun : la pause douceur, la pièce rigolote et l’arc-en-ciel sont là pour surprendre et rendre le jeu plus dynamique.
Le projet sera évalué sur :
* Qualité des prompts (10 points)
* Fonctionnalités du jeu (7 points)
* Documentation et utilisabilité (3 points)
* Utilise ce prompt complet pour générer la meilleure version possible du projet Tetris à deux joueurs.
* Respecte le style « o1 » :
   * Objectif clairement défini (Goal).
   * Format de sortie précis (Return Format).
   * Mises en garde (Warnings).
   * Contexte détaillé (Context Dump).
* Fournis ensuite le code Python, le contenu du README.md et un exemple de PROMPTS.md.

## GitHub Copilot (Claude 3.7 Sonnet Thinking)
## Prompts pour peaufiner le projet

1. Optimisation de l'IA

- Mon IA pour le jeu Tetris est fonctionnelle mais je souhaite l'optimiser. Voici l'implémentation actuelle :

   (voir lignes de code surlignés)

   Comment puis-je améliorer l'algorithme pour que l'IA prenne de meilleures décisions tout en conservant une complexité raisonnable ?


2. Améliorations visuelles

   Comment puis-je améliorer l'interface utilisateur de mon jeu Tetris ? Je voudrais notamment :

   - Améliorer l'apparence visuelle des grilles 
   - Rendre l'affichage du score plus attrayant 
   - Ajouter des animations pour les lignes complétées 
   - Avoir la possibilité de voir la pièce suivante de l'IA 
   - Améliorer la visibilité des pièces suivantes Augmenter la taille de la fenetre (certaines informations ne rentrent pas entier, elles sont coupés de par la taille du canva)