import os
import random
from config import *

# Dateipfade zu Bildern
FOOD_DIR = "img/food"
NO_FOOD_DIR = "img/no_food"


class Food:
    def __init__(self):

        # Food-Position
        self.position_x = 0
        self.position_y = 0

        # gutes/ schlechtes Essen Bilder laden
        self.good_images = self.load_images(FOOD_DIR)
        self.bad_images = self.load_images(NO_FOOD_DIR)

        self.image = None
        self.is_bad = False

        self._choose_type_and_image()

    def load_images(self, directory):
        images = []
        # für jedes Bild im directory: bild laden, auf Blocksize anpassen, zur Liste (images) hinzufügen
        for file in os.listdir(directory):
            if file.lower().endswith(".png"):
                path = os.path.join(directory, file)
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, (GRID_BLOCKSIZE, GRID_BLOCKSIZE))
                images.append(img)

        return images

    def _choose_type_and_image(self):

        # 80% food, 20% no-food bild
        if self.bad_images and random.random() < 0.2:
            self.image = random.choice(self.bad_images)
            self.is_bad = True
        else:
            self.image = random.choice(self.good_images)
            self.is_bad = False

    # food spawnen (blocked_extra: beinhaltet alle Felder, die bereits durch Food blockiert sind)
    def spawn(self, snake1, snake2=None, blocked_extra=None):
        self._choose_type_and_image()

        if blocked_extra is None:
            blocked_extra = set()

        while True:
            x = random.randint(0, PLAYFIELD_COLS - 1)
            y = random.randint(0, PLAYFIELD_ROWS - 1)

            blocked = set(snake1.body_list)
            if snake2 is not None:
                blocked.update(snake2.body_list)
            blocked.update(blocked_extra)

            if (x, y) not in blocked:
                self.position_x = x
                self.position_y = y
                break

    # draw food: startfeld + berechnete Position
    def draw(self, surface):
        pixel_x = PLAYFIELD_OFFSET_X + self.position_x * GRID_BLOCKSIZE
        pixel_y = PLAYFIELD_OFFSET_Y + self.position_y * GRID_BLOCKSIZE
        surface.blit(self.image, (pixel_x, pixel_y))
