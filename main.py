import tkinter as tk
import random
import time
import copy
from enum import Enum
from typing import List, Tuple, Dict, Optional, Set

class PlayerType(Enum):
    HUMAN = 0
    AI = 1

# Dimensions de la grille
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30

# Couleurs des pièces
COLORS = {
    'I': '#00FFFF',  # Cyan
    'O': '#FFFF00',  # Jaune
    'T': '#800080',  # Violet
    'S': '#00FF00',  # Vert
    'Z': '#FF0000',  # Rouge
    'J': '#0000FF',  # Bleu
    'L': '#FF7F00',  # Orange
    'HEART': '#FF69B4',  # Rose pour la pièce en forme de cœur
    'STAR': '#FFD700',  # Or pour la pièce en forme d'étoile
}

# Définition des pièces standard
SHAPES = {
    'I': [[(0, 0), (0, 1), (0, 2), (0, 3)],
          [(0, 0), (1, 0), (2, 0), (3, 0)]],
    'O': [[(0, 0), (0, 1), (1, 0), (1, 1)]],
    'T': [[(0, 0), (0, 1), (0, 2), (1, 1)],
          [(0, 1), (1, 0), (1, 1), (2, 1)],
          [(1, 0), (0, 1), (1, 1), (1, 2)],
          [(0, 0), (1, 0), (2, 0), (1, 1)]],
    'S': [[(0, 1), (0, 2), (1, 0), (1, 1)],
          [(0, 0), (1, 0), (1, 1), (2, 1)]],
    'Z': [[(0, 0), (0, 1), (1, 1), (1, 2)],
          [(0, 1), (1, 0), (1, 1), (2, 0)]],
    'J': [[(0, 0), (1, 0), (1, 1), (1, 2)],
          [(0, 0), (0, 1), (1, 0), (2, 0)],
          [(0, 0), (0, 1), (0, 2), (1, 2)],
          [(0, 1), (1, 1), (2, 0), (2, 1)]],
    'L': [[(0, 0), (0, 1), (0, 2), (1, 0)],
          [(0, 0), (1, 0), (2, 0), (2, 1)],
          [(0, 2), (1, 0), (1, 1), (1, 2)],
          [(0, 0), (0, 1), (1, 1), (2, 1)]],
    # Pièces spéciales
    'HEART': [[(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]],
    'STAR': [[(0, 2), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 2)]]
}

# Pièces standards (non spéciales)
STANDARD_SHAPES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
# Pièces faciles à placer
EASY_SHAPES = ['I', 'O']
# Pièces spéciales
SPECIAL_SHAPES = ['HEART', 'STAR']

class TetrisGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Tetris Humain vs IA")
        
        # Augmenter la taille de la fenêtre
        window_width = CELL_SIZE * GRID_WIDTH * 2 + 400  # Augmenté de 300 à 400
        window_height = CELL_SIZE * GRID_HEIGHT + 150    # Augmenté de 100 à 150
        
        self.master.geometry(f"{window_width}x{window_height}")
        self.master.minsize(window_width, window_height)  # Définir une taille minimale
        self.master.resizable(True, True)  # Permettre le redimensionnement
        self.master.configure(bg="#2C3E50")  # Couleur de fond
        
        # Centrer la fenêtre sur l'écran
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.master.geometry(f"+{x_position}+{y_position}")
        
        # Le reste de votre code...

        # Création du conteneur principal
        self.container = tk.Frame(self.master, bg="#2C3E50")
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Initialisation des données du jeu
        self.initialize_game_data()

        # Créer les composants du jeu
        self.create_game_components()

        # Démarrer le jeu
        self.start_game()
        
        # Bind des événements clavier
        self.master.bind("<Left>", self.human_move_left)
        self.master.bind("<Right>", self.human_move_right)
        self.master.bind("<Down>", self.human_move_down)
        self.master.bind("<Up>", self.human_rotate)

    def initialize_game_data(self):
        """Initialise les données du jeu pour les deux joueurs"""
        # Initialisation des grilles (0 = vide, 1+ = bloc avec couleur)
        self.human_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.ai_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Pièces actuelles et suivantes
        self.human_current_piece = None
        self.human_next_piece = None
        self.ai_current_piece = None
        self.ai_next_piece = None
        
        # Position des pièces actuelles
        self.human_piece_position = (0, 0)
        self.ai_piece_position = (0, 0)
        
        # Orientation des pièces
        self.human_piece_rotation = 0
        self.ai_piece_rotation = 0
        
        # Scores
        self.human_score = 0
        self.ai_score = 0
        
        # Niveaux et vitesses
        self.human_level = 1
        self.ai_level = 1
        self.human_speed = 1000  # ms
        self.ai_speed = 500  # ms, IA légèrement plus rapide
        
        # Flags des règles spéciales
        self.slow_mode_active = False
        self.slow_mode_start_time = 0
        self.rainbow_mode_active = False
        self.rainbow_mode_start_time = 0
        self.rainbow_colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#8B00FF']
        
        # Timers
        self.last_rainbow_time = time.time()
        
        # Indicateurs de jeu
        self.game_over = False
        self.paused = False

    def create_game_components(self):
        """Crée les composants visuels du jeu"""
        # Frame pour les grilles
        self.grids_frame = tk.Frame(self.container, bg="#2C3E50")
        self.grids_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Frame pour les informations (score, niveau, etc.)
        self.info_frame = tk.Frame(self.container, bg="#2C3E50", width=300)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Création des canvas pour les grilles avec une bordure plus distincte
        self.human_canvas = tk.Canvas(
            self.grids_frame, 
            width=GRID_WIDTH * CELL_SIZE, 
            height=GRID_HEIGHT * CELL_SIZE, 
            bg="#34495E",
            highlightthickness=4,  # Bordure plus épaisse
            highlightbackground="#3498DB"  # Couleur plus vive
        )
        self.human_canvas.pack(side=tk.LEFT, padx=10)  # Plus d'espace
        
        self.ai_canvas = tk.Canvas(
            self.grids_frame, 
            width=GRID_WIDTH * CELL_SIZE, 
            height=GRID_HEIGHT * CELL_SIZE, 
            bg="#34495E",
            highlightthickness=4,  # Bordure plus épaisse
            highlightbackground="#E74C3C"  # Couleur plus vive
        )
        self.ai_canvas.pack(side=tk.LEFT, padx=10)  # Plus d'espace
        
        # Création des composants d'affichage pour les informations
        self.create_info_display()
        
        # Création des canvas pour les pièces suivantes
        self.create_next_piece_displays()

    def create_info_display(self):
        """Crée les affichages d'informations (scores, niveau, etc.)"""
        # Titre avec ombre
        title_frame = tk.Frame(self.info_frame, bg="#2C3E50")
        title_frame.pack(pady=(0, 20))
        
        # Effet d'ombre pour le titre
        shadow_label = tk.Label(
            title_frame, 
            text="TETRIS HUMAIN VS IA", 
            font=("Arial", 16, "bold"), 
            bg="#2C3E50", 
            fg="#2C3E50"
        )
        shadow_label.pack()
        shadow_label.place(x=2, y=2)
        
        tk.Label(
            title_frame, 
            text="TETRIS HUMAIN VS IA", 
            font=("Arial", 16, "bold"), 
            bg="#2C3E50", 
            fg="#ECF0F1"
        ).pack()
        
        # Score de l'humain avec effet 3D
        human_score_frame = tk.Frame(self.info_frame, bg="#2C3E50", relief=tk.RAISED, bd=3)
        human_score_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            human_score_frame, 
            text="JOUEUR", 
            font=("Arial", 14, "bold"), 
            bg="#3498DB", 
            fg="#ECF0F1",
            padx=10,
            pady=5
        ).pack(fill=tk.X)
        
        self.human_score_label = tk.Label(
            human_score_frame, 
            text="Score: 0", 
            font=("Arial", 18, "bold"), 
            bg="#3498DB", 
            fg="#ECF0F1",
            pady=8
        )
        self.human_score_label.pack(fill=tk.X)
        
        # Score de l'IA avec effet 3D
        ai_score_frame = tk.Frame(self.info_frame, bg="#2C3E50", relief=tk.RAISED, bd=3)
        ai_score_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            ai_score_frame, 
            text="INTELLIGENCE ARTIFICIELLE", 
            font=("Arial", 14, "bold"), 
            bg="#E74C3C", 
            fg="#ECF0F1",
            padx=10,
            pady=5
        ).pack(fill=tk.X)
        
        self.ai_score_label = tk.Label(
            ai_score_frame, 
            text="Score: 0", 
            font=("Arial", 18, "bold"), 
            bg="#E74C3C", 
            fg="#ECF0F1",
            pady=8
        )
        self.ai_score_label.pack(fill=tk.X)
        
        # Label pour les règles spéciales
        self.special_rules_label = tk.Label(
            self.info_frame,
            text="Aucune règle active",
            font=("Arial", 12),
            bg="#2C3E50",
            fg="#ECF0F1",
            pady=10
        )
        self.special_rules_label.pack(fill=tk.X, pady=10)
        
        # Frame pour les boutons
        buttons_frame = tk.Frame(self.info_frame, bg="#2C3E50")
        buttons_frame.pack(pady=20, fill=tk.X)
        
        # Bouton Pause
        self.pause_button = tk.Button(
            buttons_frame,
            text="PAUSE",
            command=self.toggle_pause,
            bg="#3498DB",
            fg="#ECF0F1",
            font=("Arial", 12, "bold"),
            width=10,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        self.pause_button.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        
        # Bouton Quitter
        self.quit_button = tk.Button(
            buttons_frame,
            text="QUITTER",
            command=self.master.destroy,
            bg="#E74C3C",
            fg="#ECF0F1",
            font=("Arial", 12, "bold"),
            width=10,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        self.quit_button.pack(side=tk.RIGHT, padx=10, expand=True, fill=tk.X)

    def create_next_piece_displays(self):
        """Crée les affichages pour les pièces suivantes"""
        # Frame pour les pièces suivantes
        next_pieces_frame = tk.Frame(self.info_frame, bg="#2C3E50", relief=tk.RIDGE, bd=2)
        next_pieces_frame.pack(fill=tk.X, pady=15)
        
        # Titre
        tk.Label(
            next_pieces_frame, 
            text="PIÈCES SUIVANTES", 
            font=("Arial", 14, "bold"), 
            bg="#2C3E50", 
            fg="#ECF0F1"
        ).pack(pady=5)
        
        # Conteneur pour les deux affichages
        displays_frame = tk.Frame(next_pieces_frame, bg="#2C3E50")
        displays_frame.pack(pady=10)
        
        # Affichage de la pièce suivante de l'humain
        human_next_frame = tk.Frame(displays_frame, bg="#3498DB", padx=5, pady=5, relief=tk.SUNKEN, bd=2)
        human_next_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            human_next_frame, 
            text="JOUEUR", 
            font=("Arial", 12, "bold"), 
            bg="#3498DB", 
            fg="#ECF0F1"
        ).pack()
        
        self.human_next_canvas = tk.Canvas(
            human_next_frame, 
            width=120,  # Augmenter la taille
            height=120, 
            bg="#34495E",
            highlightthickness=1,
            highlightbackground="#3498DB"
        )
        self.human_next_canvas.pack(padx=5, pady=5)
        
        # Affichage de la pièce suivante de l'IA
        ai_next_frame = tk.Frame(displays_frame, bg="#E74C3C", padx=5, pady=5, relief=tk.SUNKEN, bd=2)
        ai_next_frame.pack(side=tk.RIGHT, padx=10)
        
        tk.Label(
            ai_next_frame, 
            text="IA", 
            font=("Arial", 12, "bold"), 
            bg="#E74C3C", 
            fg="#ECF0F1"
        ).pack()
        
        self.ai_next_canvas = tk.Canvas(
            ai_next_frame, 
            width=120,  # Augmenter la taille
            height=120, 
            bg="#34495E",
            highlightthickness=1,
            highlightbackground="#E74C3C"
        )
        self.ai_next_canvas.pack(padx=5, pady=5)

    def start_game(self):
        """Démarre le jeu pour les deux joueurs"""
        # Générer les premières pièces
        self.human_next_piece = self.generate_piece()
        self.ai_next_piece = self.generate_piece()
        
        # Démarrer la boucle de jeu
        self.spawn_human_piece()
        self.spawn_ai_piece()
        
        # Démarrer la gestion des événements spéciaux
        self.check_special_events()

    def generate_piece(self, type_override=None):
        """Génère une nouvelle pièce de jeu"""
        # Vérifier si on doit forcer un type spécifique
        if type_override:
            piece_type = type_override
        else:
            # Déterminer si on génère une pièce spéciale
            if (self.human_score >= 3000 and self.human_score % 3000 < 100) or \
               (self.ai_score >= 3000 and self.ai_score % 3000 < 100):
                piece_type = random.choice(SPECIAL_SHAPES)
            else:
                piece_type = random.choice(STANDARD_SHAPES)
        
        # Générer la pièce
        piece = {
            'type': piece_type,
            'color': COLORS[piece_type],
            'rotation': 0
        }
        
        return piece

    def spawn_human_piece(self):
        """Fait apparaître une nouvelle pièce pour le joueur humain"""
        if self.game_over:
            return
            
        # La pièce suivante devient la pièce actuelle
        self.human_current_piece = self.human_next_piece
        self.human_next_piece = self.generate_piece()
        
        # Définir la position de départ
        self.human_piece_position = (0, GRID_WIDTH // 2 - 1)
        self.human_piece_rotation = 0
        
        # Mettre à jour l'affichage
        self.update_next_piece_display(PlayerType.HUMAN)
        
        # Vérifier si la pièce peut être placée, sinon game over
        if not self.is_valid_position(self.human_current_piece, self.human_piece_position, 
                                     self.human_piece_rotation, PlayerType.HUMAN):
            self.game_over = True
            self.show_game_over("L'IA a gagné !")
            return
        
        # Programmer le mouvement de la pièce
        self.human_move_timer = self.master.after(self.human_speed, self.human_move_piece_down)

    def spawn_ai_piece(self):
        """Fait apparaître une nouvelle pièce pour l'IA"""
        if self.game_over:
            return
            
        # La pièce suivante devient la pièce actuelle
        self.ai_current_piece = self.ai_next_piece
        self.ai_next_piece = self.generate_piece()
        
        # Définir la position de départ
        self.ai_piece_position = (0, GRID_WIDTH // 2 - 1)
        self.ai_piece_rotation = 0
        
        # Mettre à jour l'affichage
        self.update_next_piece_display(PlayerType.AI)
        
        # Vérifier si la pièce peut être placée, sinon game over
        if not self.is_valid_position(self.ai_current_piece, self.ai_piece_position, 
                                     self.ai_piece_rotation, PlayerType.AI):
            self.game_over = True
            self.show_game_over("Le joueur humain a gagné !")
            return
        
        # Laisser l'IA jouer son coup
        self.ai_move_timer = self.master.after(100, self.ai_play_move)

    def update_next_piece_display(self, player_type):
        """Met à jour l'affichage de la pièce suivante"""
        if player_type == PlayerType.HUMAN:
            piece = self.human_next_piece
            canvas = self.human_next_canvas
        else:
            piece = self.ai_next_piece
            canvas = self.ai_next_canvas
        
        # Effacer le canvas
        canvas.delete("all")
        
        # Déterminer la forme à afficher
        shape = SHAPES[piece['type']][0]
        
        # Trouver les dimensions de la forme
        min_x = min(coord[0] for coord in shape)
        max_x = max(coord[0] for coord in shape)
        min_y = min(coord[1] for coord in shape)
        max_y = max(coord[1] for coord in shape)
        
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        
        # Calculer la taille de la cellule et les décalages pour centrer
        cell_size = min(80 / max(width, height), 20)
        offset_x = (100 - width * cell_size) / 2
        offset_y = (100 - height * cell_size) / 2
        
        # Dessiner les blocs de la pièce
        for x, y in shape:
            x1 = offset_x + (x - min_x) * cell_size
            y1 = offset_y + (y - min_y) * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            
            canvas.create_rectangle(x1, y1, x2, y2, fill=piece['color'], outline="#ECF0F1")

    def human_move_piece_down(self):
        """Déplace la pièce du joueur humain vers le bas"""
        if self.paused or self.game_over:
            return
        
        # Calculer la nouvelle position
        new_position = (self.human_piece_position[0] + 1, self.human_piece_position[1])
        
        # Vérifier si la nouvelle position est valide
        if self.is_valid_position(self.human_current_piece, new_position, 
                                 self.human_piece_rotation, PlayerType.HUMAN):
            self.human_piece_position = new_position
            self.draw_grid(PlayerType.HUMAN)
            
            # Programmer le prochain mouvement
            self.human_move_timer = self.master.after(self.human_speed, self.human_move_piece_down)
        else:
            # La pièce ne peut pas descendre davantage, la fixer dans la grille
            self.lock_piece(PlayerType.HUMAN)
            
            # Vérifier et effacer les lignes complètes
            lines_cleared = self.clear_lines(PlayerType.HUMAN)
            
            # Appliquer les effets des règles spéciales en fonction des lignes effacées
            self.apply_special_rules(lines_cleared, PlayerType.HUMAN)
            
            # Générer une nouvelle pièce
            self.spawn_human_piece()

    def ai_play_move(self):
        """L'IA joue son coup"""
        if self.paused or self.game_over:
            return
        
        try:
            # Algorithme de l'IA pour décider où placer la pièce
            best_move = self.ai_find_best_move()
            
            # Vérifier que best_move est correctement défini
            if not best_move or 'rotation' not in best_move or 'column' not in best_move:
                # Valeurs par défaut sûres
                best_move = {'rotation': 0, 'column': GRID_WIDTH // 2 - 1}
                print("Utilisation de valeurs par défaut pour l'IA")
            
            # S'assurer que les valeurs sont des nombres
            rotation = best_move.get('rotation', 0)
            target_column = best_move.get('column', GRID_WIDTH // 2 - 1)
            
            # Appliquer le mouvement
            self.ai_piece_rotation = rotation
            
            # Déplacer la pièce horizontalement
            current_column = self.ai_piece_position[1]
            
            # Déplacer vers la gauche si nécessaire
            while current_column > target_column:
                if self.is_valid_position(self.ai_current_piece, 
                                        (self.ai_piece_position[0], self.ai_piece_position[1] - 1), 
                                        self.ai_piece_rotation, PlayerType.AI):
                    self.ai_piece_position = (self.ai_piece_position[0], self.ai_piece_position[1] - 1)
                    self.draw_grid(PlayerType.AI)  # Mise à jour visuelle
                    self.master.update()  # Forcer la mise à jour de l'interface
                    self.master.after(10)  # Court délai pour animation fluide
                    current_column = self.ai_piece_position[1]
                else:
                    break
            
            # Déplacer vers la droite si nécessaire
            while current_column < target_column:
                if self.is_valid_position(self.ai_current_piece, 
                                        (self.ai_piece_position[0], self.ai_piece_position[1] + 1), 
                                        self.ai_piece_rotation, PlayerType.AI):
                    self.ai_piece_position = (self.ai_piece_position[0], self.ai_piece_position[1] + 1)
                    self.draw_grid(PlayerType.AI)  # Mise à jour visuelle
                    self.master.update()  # Forcer la mise à jour de l'interface
                    self.master.after(10)  # Court délai pour animation fluide
                    current_column = self.ai_piece_position[1]
                else:
                    break
            
            # Faire descendre la pièce
            self.ai_move_timer = self.master.after(self.ai_speed, self.ai_move_piece_down)
        
        except Exception as e:
            print(f"Erreur dans ai_play_move: {e}")
            # En cas d'erreur, continuer le jeu
            self.ai_move_timer = self.master.after(self.ai_speed, self.ai_move_piece_down)

    def ai_move_piece_down(self):
        """Déplace la pièce de l'IA vers le bas"""
        if self.paused or self.game_over:
            return
        
        # Calculer la nouvelle position
        new_position = (self.ai_piece_position[0] + 1, self.ai_piece_position[1])
        
        # Vérifier si la nouvelle position est valide
        if self.is_valid_position(self.ai_current_piece, new_position, 
                                 self.ai_piece_rotation, PlayerType.AI):
            self.ai_piece_position = new_position
            self.draw_grid(PlayerType.AI)
            
            # Programmer le prochain mouvement
            self.ai_move_timer = self.master.after(self.ai_speed, self.ai_move_piece_down)
        else:
            # La pièce ne peut pas descendre davantage, la fixer dans la grille
            self.lock_piece(PlayerType.AI)
            
            # Vérifier et effacer les lignes complètes
            lines_cleared = self.clear_lines(PlayerType.AI)
            
            # Appliquer les effets des règles spéciales en fonction des lignes effacées
            self.apply_special_rules(lines_cleared, PlayerType.AI)
            
            # Générer une nouvelle pièce
            self.spawn_ai_piece()

    def ai_find_best_move(self):
        """Trouve le meilleur coup pour l'IA avec anticipation"""
        best_score = float('-inf')
        best_move = {'rotation': 0, 'column': 0}
        
        # Obtenir la forme actuelle
        current_piece_type = self.ai_current_piece['type']
        next_piece_type = self.ai_next_piece['type']
        
        # Essayer toutes les rotations possibles
        for rotation in range(len(SHAPES[current_piece_type])):
            shape = SHAPES[current_piece_type][rotation]
            width = max(coord[1] for coord in shape) - min(coord[1] for coord in shape) + 1
            
            # Essayer toutes les positions horizontales possibles
            for column in range(GRID_WIDTH - width + 1):
                # Évaluer ce coup pour la pièce actuelle
                current_score = self.evaluate_ai_move(rotation, column)
                
                if current_score == float('-inf'):
                    continue
                
                # Créer une copie de la grille pour la simulation de la pièce suivante
                temp_grid = [row[:] for row in self.ai_grid]
                
                # Simuler le placement de la pièce actuelle
                shape = SHAPES[current_piece_type][rotation]
                drop_height = 0
                while self.is_valid_position_on_grid(shape, (drop_height, column), temp_grid):
                    drop_height += 1
                drop_height -= 1
                
                # Placer la pièce dans la grille temporaire
                for x, y in shape:
                    grid_x = drop_height + x
                    grid_y = column + y
                    if 0 <= grid_x < GRID_HEIGHT and 0 <= grid_y < GRID_WIDTH:
                        temp_grid[grid_x][grid_y] = 1
                
                # Supprimer les lignes complétées dans la simulation
                for row in range(GRID_HEIGHT):
                    if all(temp_grid[row]):
                        del temp_grid[row]
                        temp_grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                
                # Calculer le meilleur score possible pour la pièce suivante
                next_score = float('-inf')
                
                # Limiter le lookahead à moins de positions pour réduire la complexité
                for next_rot in range(len(SHAPES[next_piece_type])):
                    next_shape = SHAPES[next_piece_type][next_rot]
                    next_width = max(coord[1] for coord in next_shape) - min(coord[1] for coord in next_shape) + 1
                    
                    # Essayer moins de positions pour la pièce suivante
                    step = 2  # Vérifier une colonne sur deux pour réduire la complexité
                    for next_col in range(0, GRID_WIDTH - next_width + 1, step):
                        score = self.evaluate_move_on_grid(next_rot, next_col, next_piece_type, temp_grid)
                        next_score = max(next_score, score)
                
                # Combiner le score actuel et le score anticipé
                combined_score = current_score + next_score * 0.5  # La pièce suivante a 50% de l'importance
                
                if combined_score > best_score:
                    best_score = combined_score
                    best_move = {'rotation': rotation, 'column': column}
        
        return best_move

    def evaluate_ai_move(self, rotation, column):
        """Évalue un coup possible pour l'IA avec critères améliorés"""
        # Créer une copie de la grille pour la simulation
        temp_grid = [row[:] for row in self.ai_grid]
        
        # Obtenir la forme avec cette rotation
        shape = SHAPES[self.ai_current_piece['type']][rotation]
        
        # Trouver la hauteur à laquelle la pièce s'arrêtera
        drop_height = 0
        while self.is_valid_position_on_grid(shape, (drop_height, column), temp_grid):
            drop_height += 1
        
        # Revenir à la dernière position valide
        drop_height -= 1
        
        # Si la pièce ne peut pas être placée, c'est un très mauvais coup
        if drop_height < 0:
            return float('-inf')
        
        # Placer la pièce dans la grille temporaire
        for x, y in shape:
            grid_x = drop_height + x
            grid_y = column + y
            if 0 <= grid_x < GRID_HEIGHT and 0 <= grid_y < GRID_WIDTH:
                temp_grid[grid_x][grid_y] = 1
        
        # Calculer le score du coup basé sur plusieurs facteurs
        score = 0
        
        # Critère 1: Nombre de lignes complétées
        lines_cleared = 0
        for row in range(GRID_HEIGHT):
            if all(temp_grid[row]):
                lines_cleared += 1
        
        score += lines_cleared * 150  # Augmenter cette valeur (était 100)
        
        # Critère 2: Hauteur de la pile
        height_sum = 0
        for col in range(GRID_WIDTH):
            for row in range(GRID_HEIGHT):
                if temp_grid[row][col] == 1:
                    height_sum += GRID_HEIGHT - row
                    break
        
        score -= height_sum * 0.6  # Légèrement plus pénalisant (était 0.5)
        
        # Critère 3: Nombre de trous (cellules vides avec des blocs au-dessus)
        holes = 0
        for col in range(GRID_WIDTH):
            block_found = False
            for row in range(GRID_HEIGHT):
                if temp_grid[row][col] == 1:
                    block_found = True
                elif block_found and temp_grid[row][col] == 0:
                    holes += 1
        
        score -= holes * 15  # Plus pénalisant (était 10)
        
        # Critère 4: Nombre de transitions (changements bloc/vide)
        transitions = 0
        for col in range(GRID_WIDTH):
            for row in range(1, GRID_HEIGHT):
                if temp_grid[row][col] != temp_grid[row-1][col]:
                    transitions += 1
        
        score -= transitions * 0.3  # Moins pénalisant (était 0.5)
        
        # Nouveau critère 5: Rugosité (différences de hauteur entre colonnes adjacentes)
        heights = []
        for col in range(GRID_WIDTH):
            col_height = 0
            for row in range(GRID_HEIGHT):
                if temp_grid[row][col] == 1:
                    col_height = GRID_HEIGHT - row
                    break
            heights.append(col_height)  # Ajouter à l'intérieur de la boucle for col
    
        bumpiness = 0
        for i in range(GRID_WIDTH - 1):
            bumpiness += abs(heights[i] - heights[i+1])
    
        score -= bumpiness * 1.0
    
        # Nouveau critère 6: Pénaliser les placements en hauteur
        max_height = max(heights) if heights else 0
        score -= (max_height * 2.0)
    
        # Nouveau critère 7: Récompenser les emplacements qui créent un puits pour Tetris
        well_suitability = 0
        if max_height > 4 and self.ai_current_piece['type'] != 'I':
            # Vérifier s'il y a un puits profond idéal pour une pièce I
            for col in range(1, GRID_WIDTH - 1):
                if heights[col] < heights[col-1] - 3 and heights[col] < heights[col+1] - 3:
                    well_suitability += 10
    
        score += well_suitability
    
        return score

    def evaluate_move_on_grid(self, rotation, column, piece_type, grid):
        """Évalue un coup possible sur une grille temporaire"""
        # Créer une copie de la grille fournie
        temp_grid = [row[:] for row in grid]
        
        # Obtenir la forme avec cette rotation
        shape = SHAPES[piece_type][rotation]
        
        # Trouver la hauteur à laquelle la pièce s'arrêtera
        drop_height = 0
        while self.is_valid_position_on_grid(shape, (drop_height, column), temp_grid):
            drop_height += 1
        
        # Revenir à la dernière position valide
        drop_height -= 1
        
        # Si la pièce ne peut pas être placée, c'est un très mauvais coup
        if drop_height < 0:
            return float('-inf')
        
        # Placer la pièce dans la grille temporaire
        for x, y in shape:
            grid_x = drop_height + x
            grid_y = column + y
            if 0 <= grid_x < GRID_HEIGHT and 0 <= grid_y < GRID_WIDTH:
                temp_grid[grid_x][grid_y] = 1
        
        # Réutiliser la logique d'évaluation existante
        score = 0
        
        # Critère 1: Nombre de lignes complétées
        lines_cleared = 0
        for row in range(GRID_HEIGHT):
            if all(temp_grid[row]):
                lines_cleared += 1
        
        score += lines_cleared * 150
        
        # Critère 2: Hauteur de la pile
        heights = []
        for col in range(GRID_WIDTH):
            col_height = 0
            for row in range(GRID_HEIGHT):
                if temp_grid[row][col] == 1:
                    col_height = GRID_HEIGHT - row
                    break
            heights.append(col_height)
        
        height_sum = sum(heights)
        score -= height_sum * 0.6
        
        # Autres critères comme dans evaluate_ai_move
        # (version simplifiée pour l'exemple)
        
        return score

    def is_valid_position_on_grid(self, shape, position, grid):
        """Vérifie si une position est valide sur une grille donnée"""
        for x, y in shape:
            grid_x = position[0] + x
            grid_y = position[1] + y
            
            # Vérifier si la position est dans la grille
            if grid_x < 0 or grid_x >= GRID_HEIGHT or grid_y < 0 or grid_y >= GRID_WIDTH:
                return False
            
            # Vérifier si la position est déjà occupée
            if grid[grid_x][grid_y] != 0:
                return False
        
        return True

    def is_valid_position(self, piece, position, rotation, player_type):
        """Vérifie si une position est valide pour une pièce"""
        if not piece:
            return False
            
        # Obtenir la forme avec la rotation donnée
        shape = SHAPES[piece['type']][rotation % len(SHAPES[piece['type']])]
        
        # Vérifier que chaque bloc de la pièce est dans une position valide
        for x, y in shape:
            grid_x = position[0] + x
            grid_y = position[1] + y
            
            # Vérifier si la position est dans la grille
            if grid_x < 0 or grid_x >= GRID_HEIGHT or grid_y < 0 or grid_y >= GRID_WIDTH:
                return False
            
            # Vérifier si la position est déjà occupée
            grid = self.human_grid if player_type == PlayerType.HUMAN else self.ai_grid
            if grid[grid_x][grid_y] != 0:
                return False
                
        # Si toutes les vérifications sont passées, la position est valide
        return True

    def human_move_left(self, event=None):
        """Déplace la pièce du joueur humain vers la gauche"""
        if self.paused or self.game_over:
            return
        
        # Calculer la nouvelle position
        new_position = (self.human_piece_position[0], self.human_piece_position[1] - 1)
        
        # Vérifier si la nouvelle position est valide
        if self.is_valid_position(self.human_current_piece, new_position, 
                                 self.human_piece_rotation, PlayerType.HUMAN):
            self.human_piece_position = new_position
            self.draw_grid(PlayerType.HUMAN)

    def human_move_right(self, event=None):
        """Déplace la pièce du joueur humain vers la droite"""
        if self.paused or self.game_over:
            return
        
        # Calculer la nouvelle position
        new_position = (self.human_piece_position[0], self.human_piece_position[1] + 1)
        
        # Vérifier si la nouvelle position est valide
        if self.is_valid_position(self.human_current_piece, new_position, 
                                 self.human_piece_rotation, PlayerType.HUMAN):
            self.human_piece_position = new_position
            self.draw_grid(PlayerType.HUMAN)

    def human_move_down(self, event=None):
        """Accélère la descente de la pièce du joueur humain"""
        if self.paused or self.game_over:
            return
        
        # Annuler le timer actuel
        self.master.after_cancel(self.human_move_timer)
        
        # Déplacer immédiatement la pièce vers le bas
        self.human_move_piece_down()

    def human_rotate(self, event=None):
        """Fait pivoter la pièce du joueur humain"""
        if self.paused or self.game_over or not self.human_current_piece:
            return
        
        # Calculer la nouvelle rotation
        new_rotation = (self.human_piece_rotation + 1) % len(SHAPES[self.human_current_piece['type']])
        
        # Vérifier si la nouvelle rotation est valide
        if self.is_valid_position(self.human_current_piece, self.human_piece_position, 
                                 new_rotation, PlayerType.HUMAN):
            self.human_piece_rotation = new_rotation
            self.draw_grid(PlayerType.HUMAN)

    def lock_piece(self, player_type):
        """Fixe une pièce dans la grille"""
        if player_type == PlayerType.HUMAN:
            piece = self.human_current_piece
            position = self.human_piece_position
            rotation = self.human_piece_rotation
            grid = self.human_grid
        else:
            piece = self.ai_current_piece
            position = self.ai_piece_position
            rotation = self.ai_piece_rotation
            grid = self.ai_grid
        
        # Obtenir la forme avec la rotation donnée
        shape = SHAPES[piece['type']][rotation % len(SHAPES[piece['type']])]
        
        # Ajouter la pièce à la grille
        for x, y in shape:
            grid_x = position[0] + x
            grid_y = position[1] + y
            
            if 0 <= grid_x < GRID_HEIGHT and 0 <= grid_y < GRID_WIDTH:
                # Pour les pièces spéciales, utiliser un identifiant spécial
                grid[grid_x][grid_y] = piece['type'] if piece['type'] in SPECIAL_SHAPES else 1
        
        # Dessiner la grille mise à jour
        self.draw_grid(player_type)

    def clear_lines(self, player_type):
        """Efface les lignes complètes et met à jour le score avec animation"""
        if player_type == PlayerType.HUMAN:
            grid = self.human_grid
            canvas = self.human_canvas
            score_label = self.human_score_label
        else:
            grid = self.ai_grid
            canvas = self.ai_canvas
            score_label = self.ai_score_label
        
        # Trouver les lignes complètes
        lines_to_clear = []
        for row in range(GRID_HEIGHT):
            if all(cell != 0 for cell in grid[row]):
                lines_to_clear.append(row)
        
        # Si aucune ligne à effacer, retourner
        if not lines_to_clear:
            return 0
        
        # Animation pour les lignes à effacer (faire clignoter)
        self.animate_line_clearing(player_type, lines_to_clear)
        
        # Supprimer les lignes complètes et ajouter des lignes vides au-dessus
        lines_to_clear.sort()  # Trier pour commencer par le bas
        for row in lines_to_clear:
            del grid[row]
            grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        # Mettre à jour le score
        lines_count = len(lines_to_clear)
        
        # Points par ligne: 100, 300, 500, 800 pour 1, 2, 3, 4 lignes
        points = {1: 100, 2: 300, 3: 500, 4: 800}
        score_to_add = points.get(lines_count, lines_count * 200)  # Valeur par défaut pour 5+ lignes
        
        if player_type == PlayerType.HUMAN:
            self.human_score += score_to_add
            self.human_score_label.config(text=f"Score: {self.human_score}")
        else:
            self.ai_score += score_to_add
            self.ai_score_label.config(text=f"Score: {self.ai_score}")
        
        # Dessiner la grille mise à jour
        self.draw_grid(player_type)
        
        return lines_count

    def animate_line_clearing(self, player_type, lines):
        """Anime la suppression des lignes avec un effet de clignotement"""
        if player_type == PlayerType.HUMAN:
            canvas = self.human_canvas
        else:
            canvas = self.ai_canvas
        
        # Nombre de fois que les lignes vont clignoter
        blink_count = 3
        
        def blink(count):
            if count <= 0:
                return
            
            # Créer flash pour chaque ligne
            flash_ids = []
            for row in lines:
                x1 = 0
                y1 = row * CELL_SIZE
                x2 = GRID_WIDTH * CELL_SIZE
                y2 = y1 + CELL_SIZE
                
                # Couleur alternée: blanc pour flasher, puis transparent pour revenir
                color = "#FFFFFF" if count % 2 == 0 else "#FFA500"  # Blanc puis orange
                
                flash_id = canvas.create_rectangle(x1, y1, x2, y2, 
                                                 fill=color, 
                                                 stipple="gray50" if count % 2 == 1 else "",
                                                 outline="")
                flash_ids.append(flash_id)
            
            # Mettre à jour l'affichage
            self.master.update()
            
            # Attendre un court instant
            self.master.after(150)
            
            # Supprimer le flash
            for f_id in flash_ids:
                canvas.delete(f_id)
            
            # Continuer l'animation
            self.master.after(50, lambda: blink(count - 1))
        
        # Démarrer l'animation
        blink(blink_count * 2)  # *2 car chaque blink compte pour 2 étapes (allumé/éteint)
        
        # Attendre que l'animation se termine avant de continuer
        self.master.after((blink_count * 2) * 200 + 100)

    def apply_special_rules(self, lines_cleared, player_type):
        """Applique les règles spéciales en fonction des lignes effacées"""
        # Règle 1: Cadeau surprise - si un joueur complète 2 lignes d'un coup, l'adversaire reçoit une pièce facile
        if lines_cleared == 2:
            if player_type == PlayerType.HUMAN:
                # L'IA reçoit une pièce facile pour le prochain tour
                self.ai_next_piece = self.generate_piece(type_override=random.choice(EASY_SHAPES))
                self.update_next_piece_display(PlayerType.AI)
            else:
                # Le joueur humain reçoit une pièce facile pour le prochain tour
                self.human_next_piece = self.generate_piece(type_override=random.choice(EASY_SHAPES))
                self.update_next_piece_display(PlayerType.HUMAN)
        
        # Règle 2: Pause douceur - tous les 1000 points, la vitesse de chute est réduite de 20% pendant 10 secondes
        current_score = self.human_score if player_type == PlayerType.HUMAN else self.ai_score
        if current_score % 1000 < 50 and current_score > 0 and not self.slow_mode_active:
            self.slow_mode_active = True
            self.slow_mode_start_time = time.time()
            
            # Réduire la vitesse de chute
            self.human_speed = int(self.human_speed * 1.2)
            self.ai_speed = int(self.ai_speed * 1.2)
            
            # Mettre à jour le statut des règles spéciales
            self.special_rules_label.config(text="Mode Ralenti actif!")

    def check_special_events(self):
        """Vérifie et gère les événements spéciaux récurrents"""
        current_time = time.time()
        
        # Fin du mode ralenti
        if self.slow_mode_active and current_time - self.slow_mode_start_time > 10:
            self.slow_mode_active = False
            self.human_speed = int(self.human_speed / 1.2)
            self.ai_speed = int(self.ai_speed / 1.2)
            self.special_rules_label.config(text="Aucune règle active")
        
        # Règle 4: Arc-en-ciel - toutes les 2 minutes (120 secondes), les pièces changent de couleur
        minutes_elapsed = int(current_time / 120)
        if minutes_elapsed > 0 and not self.rainbow_mode_active and current_time % 120 < 20:
            self.rainbow_mode_active = True
            self.rainbow_mode_start_time = current_time
            self.special_rules_label.config(text="Mode Arc-en-ciel actif!")
        
        # Fin du mode arc-en-ciel
        if self.rainbow_mode_active and current_time - self.rainbow_mode_start_time > 20:
            self.rainbow_mode_active = False
            if not self.slow_mode_active:
                self.special_rules_label.config(text="Aucune règle active")
        
        # Mettre à jour les couleurs en mode arc-en-ciel
        if self.rainbow_mode_active and current_time - self.last_rainbow_time > 0.5:
            self.last_rainbow_time = current_time
            self.draw_grid(PlayerType.HUMAN)
            self.draw_grid(PlayerType.AI)
        
        # Continuer à vérifier les événements spéciaux
        self.master.after(100, self.check_special_events)

    def draw_grid(self, player_type):
        """Dessine la grille et la pièce actuelle avec des améliorations visuelles"""
        if player_type == PlayerType.HUMAN:
            grid = self.human_grid
            canvas = self.human_canvas
            piece = self.human_current_piece
            position = self.human_piece_position
            rotation = self.human_piece_rotation
        else:
            grid = self.ai_grid
            canvas = self.ai_canvas
            piece = self.ai_current_piece
            position = self.ai_piece_position
            rotation = self.ai_piece_rotation
        
        # Effacer le canvas
        canvas.delete("all")
        
        # Dessiner les lignes de la grille (lignes légères pour visualiser les cellules)
        for i in range(GRID_WIDTH + 1):
            x = i * CELL_SIZE
            canvas.create_line(x, 0, x, GRID_HEIGHT * CELL_SIZE, fill="#2C3E50", width=1)
        
        for i in range(GRID_HEIGHT + 1):
            y = i * CELL_SIZE
            canvas.create_line(0, y, GRID_WIDTH * CELL_SIZE, y, fill="#2C3E50", width=1)
        
        # Dessiner la grille avec effet 3D pour les blocs
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                
                if grid[row][col] != 0:
                    # Déterminer la couleur
                    if isinstance(grid[row][col], str) and grid[row][col] in COLORS:
                        base_color = COLORS[grid[row][col]]
                    else:
                        # En mode arc-en-ciel, utiliser des couleurs alternées
                        if self.rainbow_mode_active:
                            color_index = (row + col + int(time.time() * 5)) % len(self.rainbow_colors)
                            base_color = self.rainbow_colors[color_index]
                        else:
                            # Couleur par défaut pour les blocs placés
                            base_color = "#7F8C8D"  # Gris
                    
                    # Effet 3D: côtés plus foncés
                    darker_color = self.darken_color(base_color, 0.7)
                    
                    # Dessiner le bloc principal
                    canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, fill=base_color, outline="")
                    
                    # Dessiner les bords pour l'effet 3D (haut et gauche plus clairs)
                    canvas.create_line(x1+2, y1+2, x2-2, y1+2, fill=self.lighten_color(base_color, 0.3), width=2)
                    canvas.create_line(x1+2, y1+2, x1+2, y2-2, fill=self.lighten_color(base_color, 0.3), width=2)
                    
                    # Dessiner les bords pour l'effet 3D (bas et droite plus foncés)
                    canvas.create_line(x1+2, y2-2, x2-2, y2-2, fill=darker_color, width=2)
                    canvas.create_line(x2-2, y1+2, x2-2, y2-2, fill=darker_color, width=2)
                else:
                    # Case vide avec effet de profondeur
                    canvas.create_rectangle(x1, y1, x2, y2, fill="#34495E", outline="#2C3E50")
                    canvas.create_rectangle(x1+3, y1+3, x2-3, y2-3, fill="#2C3E50", outline="")
        
        # Dessiner la pièce actuelle avec effet de brillance
        if piece:
            shape = SHAPES[piece['type']][rotation % len(SHAPES[piece['type']])]
            
            for x, y in shape:
                grid_x = position[0] + x
                grid_y = position[1] + y
                
                if 0 <= grid_x < GRID_HEIGHT and 0 <= grid_y < GRID_WIDTH:
                    x1 = grid_y * CELL_SIZE
                    y1 = grid_x * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    
                    # Déterminer la couleur
                    if self.rainbow_mode_active:
                        color_index = (int(time.time() * 10)) % len(self.rainbow_colors)
                        base_color = self.rainbow_colors[color_index]
                    else:
                        base_color = piece['color']
                    
                    # Effet 3D: côtés plus foncés
                    darker_color = self.darken_color(base_color, 0.7)
                    
                    # Dessiner le bloc principal
                    canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, fill=base_color, outline="")
                    
                    # Dessiner les bords pour l'effet 3D (haut et gauche plus clairs)
                    canvas.create_line(x1+2, y1+2, x2-2, y1+2, fill=self.lighten_color(base_color, 0.3), width=2)
                    canvas.create_line(x1+2, y1+2, x1+2, y2-2, fill=self.lighten_color(base_color, 0.3), width=2)
                    
                    # Dessiner les bords pour l'effet 3D (bas et droite plus foncés)
                    canvas.create_line(x1+2, y2-2, x2-2, y2-2, fill=darker_color, width=2)
                    canvas.create_line(x2-2, y1+2, x2-2, y2-2, fill=darker_color, width=2)

    def lighten_color(self, hex_color, factor=0.3):
        """Éclaircit une couleur hexadécimale"""
        # Convertir la couleur hex en RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        # Éclaircir chaque composante
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        # Reconvertir en hex
        return f'#{r:02x}{g:02x}{b:02x}'

    def darken_color(self, hex_color, factor=0.7):
        """Assombrit une couleur hexadécimale"""
        # Convertir la couleur hex en RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        # Assombrir chaque composante
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        
        # Reconvertir en hex
        return f'#{r:02x}{g:02x}{b:02x}'

    def show_game_over(self, message):
        """Affiche l'écran de fin de jeu"""
        # Créer une nouvelle fenêtre pour le message de fin
        game_over_window = tk.Toplevel(self.master)
        game_over_window.title("Fin de la partie")
        game_over_window.geometry("300x200")
        game_over_window.resizable(False, False)
        game_over_window.configure(bg="#2C3E50")
        
        # Centrer la fenêtre
        x = self.master.winfo_x() + (self.master.winfo_width() - 300) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - 200) // 2
        game_over_window.geometry(f"+{x}+{y}")
        
        # Ajouter un message
        tk.Label(
            game_over_window, 
            text="PARTIE TERMINÉE", 
            font=("Arial", 16, "bold"), 
            bg="#2C3E50", 
            fg="#ECF0F1"
        ).pack(pady=(20, 10))
        
        tk.Label(
            game_over_window, 
            text=message, 
            font=("Arial", 12), 
            bg="#2C3E50", 
            fg="#ECF0F1"
        ).pack(pady=10)
        
        # Afficher les scores finaux
        tk.Label(
            game_over_window, 
            text=f"Score Humain: {self.human_score}", 
            font=("Arial", 12), 
            bg="#2C3E50", 
            fg="#3498DB"
        ).pack()
        
        tk.Label(
            game_over_window, 
            text=f"Score IA: {self.ai_score}", 
            font=("Arial", 12), 
            bg="#2C3E50", 
            fg="#E74C3C"
        ).pack()
        
        # Bouton pour fermer le jeu
        tk.Button(
            game_over_window, 
            text="Fermer", 
            command=self.master.destroy, 
            bg="#E74C3C", 
            fg="#ECF0F1", 
            font=("Arial", 10, "bold"),
        ).pack(pady=20)
        
        # Empêcher d'interagir avec la fenêtre principale
        game_over_window.grab_set()

    def toggle_pause(self):
        """Met le jeu en pause ou le reprend"""
        self.paused = not self.paused
        
        if self.paused:
            # Mettre à jour l'affichage
            self.special_rules_label.config(text="JEU EN PAUSE")
        else:
            # Reprendre le jeu
            self.special_rules_label.config(text="Aucune règle active" if not (self.slow_mode_active or self.rainbow_mode_active) else 
                                            "Mode Arc-en-ciel actif!" if self.rainbow_mode_active else 
                                            "Mode Ralenti actif!")
            
            # Relancer les déplacements des pièces
            self.human_move_timer = self.master.after(self.human_speed, self.human_move_piece_down)
            self.ai_move_timer = self.master.after(self.ai_speed, self.ai_move_piece_down)

# Point d'entrée principal
if __name__ == "__main__":
    root = tk.Tk()
    game = TetrisGame(root)
    root.mainloop()