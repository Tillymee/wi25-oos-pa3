from config import *


class Snake:
    # Snake initialisieren (Farbe, Körper, Spielrichtung, wächst, Punkte, Leben, NAme)
    def __init__(self, position, color, name=""):
        self.color = color
        self.body_list = [position]
        self.direction = (0, 1)
        self.growing = False
        self.score = 0
        self.lives = 3
        self.name = name

    # bewegt sich: neuer head
    def move(self):
        head = self.body_list[0]
        new_x = head[0] + self.direction[0]
        new_y = head[1] + self.direction[1]
        self.body_list.insert(0, (new_x, new_y))
        # falls nicht länger werden soll: letztes Element entfernen
        if not self.growing:
            self.body_list.pop()
        else:
            self.growing = False

    # Richtung ändern (falls nicht die entgegengesetzte)
    def change_direction(self, new_direction):
        if new_direction != (-self.direction[0], -self.direction[1]):
            self.direction = new_direction

    # growing = true
    def grow(self):
        self.growing = True

    # schrumpfen
    def shrink(self, amount=1):
        for _ in range(amount):
            if len(self.body_list) > 1:
                self.body_list.pop()

    # snake zeichnen
    def draw(self, surface):
        for (x, y) in self.body_list:
            pixel_x = PLAYFIELD_OFFSET_X + x * GRID_BLOCKSIZE
            pixel_y = PLAYFIELD_OFFSET_Y + y * GRID_BLOCKSIZE
            pygame.draw.rect(
                surface,
                self.color,
                (pixel_x, pixel_y, GRID_BLOCKSIZE, GRID_BLOCKSIZE),
            )

    # falls es mit sich selbst kollidiert, dann gibt true zurück
    def collides_with_self(self):
        return self.body_list[0] in self.body_list[1:]
