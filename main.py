# IDEA PRINZIP
# 1. Import and Initialize
import sys

import pygame

from config import *
from game import Game, GameState
from screens import Screens

# preinitialisieren des Sounds für schnellere Reaktionsgeschwindigkeit
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=128)

pygame.init()
pygame.mixer.init()
# mehrere Sounds gleichzeitig abspielen
pygame.mixer.set_num_channels(16)

# 2. Display Configuration
DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(DISPLAY_CAPTION)
CLOCK = pygame.time.Clock()

# 3. Entities
game = Game()
screens = Screens()


# 4. Action (ALTER)
# Assign key variables (Laufvar., boolsche Werte)
# loop (Spielschleife)
# Timing (FPS-->Spielgeschwindigkeit)
# Event (Reagieren auf Events)
# Redisplay (Update, Render)
def main():
    # A, L
    while True:
    # T
        dt_ms = CLOCK.tick(FPS) # vergangene Zeit seit letztem Frame (Millisekunden)
        events = pygame.event.get()
    # E
        for event in events:
            # Quit-Event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # game-state
        if game.state == GameState.MENU:
            screens.handle_menu_input(events, game)
            screens.render_menu(DISPLAY, game)

        elif game.state in (GameState.COUNTDOWN, GameState.RUNNING, GameState.PAUSED):
            game.handle_input(events)
            game.update(dt_ms)
            game.render(DISPLAY)

        elif game.state == GameState.GAME_OVER:
            screens.handle_game_over_input(events, game)
            screens.render_game_over(DISPLAY, game)
    # R
        pygame.display.update()


if __name__ == "__main__":
    main()