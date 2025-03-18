# Tetris Humain vs IA

Un jeu Tetris à deux joueurs, où vous affrontez une IA sur des grilles parallèles. Ce projet est développé en Python avec Tkinter.

## Fonctionnalités

- **Deux grilles de jeu** : Une pour l'humain, une pour l'IA
- **Contrôles intuitifs** : Utilisez les flèches du clavier pour déplacer et faire pivoter vos pièces
- **Système de score** : Gagnez des points en complétant des lignes
- **Intelligence artificielle** : L'IA évalue les meilleurs coups possibles pour placer ses pièces
- **Règles spéciales** :
  - **Cadeau surprise** : Quand un joueur complète 2 lignes d'un coup, l'adversaire reçoit une pièce facile
  - **Pause douceur** : Tous les 1000 points, la vitesse de chute est réduite pendant 10 secondes
  - **Pièce rigolote** : Des pièces spéciales (cœur, étoile) apparaissent périodiquement
  - **Arc-en-ciel** : Toutes les 2 minutes, les pièces changent de couleur pendant 20 secondes

## Prérequis

- Python 3.6 ou version ultérieure
- Tkinter (généralement inclus avec Python)

## Installation et lancement

1. Clonez ce dépôt :
```bash
git clone https://github.com/PlasmaMWK/TetrisIA.git 
```

2. Lancez le jeu :
```bash
python .\main.py
```


## Comment jouer

### Contrôles du joueur humain
- **Flèche gauche** : Déplacer la pièce vers la gauche
- **Flèche droite** : Déplacer la pièce vers la droite
- **Flèche bas** : Accélérer la descente de la pièce
- **Flèche haut** : Faire pivoter la pièce
- **Bouton Pause** : Mettre le jeu en pause ou reprendre la partie

### Système de score
- 50 points par ligne complétée
- Bonus : +100 points pour 2 lignes, +200 pour 3 lignes, +300 pour un Tetris (4 lignes)
- 100 points bonus pour chaque pièce spéciale correctement placée

## Fonctionnement de l'IA

L'IA utilise une approche heuristique pour déterminer le meilleur placement pour chaque pièce. Elle évalue différentes positions et rotations possibles en fonction de plusieurs critères :

1. Nombre de lignes complétées
2. Hauteur résultante de la pile
3. Nombre de "trous" créés (cases vides inaccessibles)
4. Transitions entre cases pleines et vides

## Développement

Ce projet a été réalisé avec l'aide de GitHub Copilot, ChatGPT o-3mini, Claude 3.7 Sonnet Thinking pour générer les prompts et le code, documenté dans le fichier PROMPTS.md.

