import pygame

# Bildschirmgröße, Grid-Größe
GRID_BLOCKSIZE = 30
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 720

DISPLAY_CAPTION = "Our first snake game"

# Render-FPS ("Smoothness")
FPS = 60

# Anzahl Grid-Felder Berechnung
GRID_HEIGHT = WINDOW_HEIGHT // GRID_BLOCKSIZE
GRID_WIDTH = WINDOW_WIDTH // GRID_BLOCKSIZE

# Side panel für Score-Anzeige
SIDE_PANEL_COLS = 7

# ein block oben und unten als Abstand
PLAYFIELD_MARGIN_ROWS = 1

# Spielfeld Größe
PLAYFIELD_COLS = GRID_WIDTH - 2 * SIDE_PANEL_COLS
PLAYFIELD_ROWS = GRID_HEIGHT - 2 * PLAYFIELD_MARGIN_ROWS

# Startposition Spielfeld
PLAYFIELD_OFFSET_X = SIDE_PANEL_COLS * GRID_BLOCKSIZE
PLAYFIELD_OFFSET_Y = PLAYFIELD_MARGIN_ROWS * GRID_BLOCKSIZE

# Farben (r,g,b,a)
COLOR_BG = pygame.Color(0, 0, 0, 255)

# Schriftgröße
FONT_BIG_SIZE = 64
FONT_SMALL_SIZE = 28
