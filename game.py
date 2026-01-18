from config import *
from food import Food
from snake import Snake


class GameState:
    MENU = 0
    COUNTDOWN = 1
    RUNNING = 2
    PAUSED = 3
    GAME_OVER = 4


class Game:
    def __init__(self):
        # Fonts (für Sidepanels + Countdown)
        self.font_big = pygame.font.SysFont(None, FONT_BIG_SIZE)
        self.font_small = pygame.font.SysFont(None, FONT_SMALL_SIZE)

        # farben (Panels, Text, abgedunkelter text, Border, aktive Elemente)
        self.ui_panel = pygame.Color(14, 18, 14)

        self.ui_text = pygame.Color(235, 245, 235)
        self.ui_dim = pygame.Color(150, 170, 150)

        self.ui_border = pygame.Color(130, 155, 130)
        self.ui_active = pygame.Color(110, 255, 140)

        # Herzen für Leben
        self.heart_full_base = pygame.image.load("img/other/heart-filled.png").convert_alpha()
        self.heart_empty_base = pygame.image.load("img/other/heart-empty.png").convert_alpha()

        # unskalierte und skalierte bilder Pfeile
        self.arrow_icons_base = {}

        # Pfeil-Icons laden
        for name in ("up", "left", "down", "right"):
            path = f"img/arrows/{name}.png"
            try:
                self.arrow_icons_base[name] = pygame.image.load(path).convert_alpha()
            except Exception:
                self.arrow_icons_base[name] = None

        # Sounds
        self.sound_food = pygame.mixer.Sound("wav/eat_food.wav")
        self.sound_collision = pygame.mixer.Sound("wav/collision.wav")
        self.sound_gameover = pygame.mixer.Sound("wav/game_over.wav")
        self.sound_no_food = pygame.mixer.Sound("wav/no_food.wav")
        self.sound_ping = pygame.mixer.Sound("wav/ping.wav")

        for s in [self.sound_food, self.sound_collision, self.sound_gameover, self.sound_no_food, self.sound_ping]:
            s.set_volume(0.25)

        # gamestate
        self.state = GameState.MENU
        self.two_player = False

        # Geschwindigkeit: Schritte pro Sekunde (zeitbasiert)
        self.speed_modes = {
            "SLOW": 4.0,
            "MID": 8.0,
            "FAST": 12.0
        }
        self.speed_keys = list(self.speed_modes.keys())
        self.speed_index = 1
        self.steps_per_second = self.speed_modes[self.speed_keys[self.speed_index]]

        # sammelt Zeit, bis ein "Step" ausgeführt wird
        self.move_accumulator_ms = 0.0

        # lives
        self.number_of_lives_modes = {"THREE": 3, "FIVE": 5, "SEVEN": 7, "TEN": 10}
        self.number_of_lives_keys = list(self.number_of_lives_modes.keys())
        self.number_of_lives_index = 1
        self.number_of_lives = self.number_of_lives_modes[self.number_of_lives_keys[self.number_of_lives_index]]

        # Colors für snakes
        self.snake_colors = [
            ("BLUE", pygame.Color(0, 120, 255)),
            ("GREEN", pygame.Color(0, 220, 120)),
            ("RED", pygame.Color(255, 70, 70)),
            ("PURPLE", pygame.Color(170, 90, 255)),
            ("ORANGE", pygame.Color(255, 170, 0)),
            ("PINK", pygame.Color(255, 105, 180)),
            ("WHITE", pygame.Color(230, 230, 230)),
            ("CYAN", pygame.Color(0, 220, 220)),
        ]
        self.color1_index = 0
        self.color2_index = 1

        # Snakes und Food
        self.snake1 = None
        self.snake2 = None
        self.food1 = None
        self.food2 = None

        # zählt Food, wann aktualisiert werden soll
        self.refresh_after_total_eats = 2
        self.total_eats_counter = 0

        # Countdown
        self.countdown_duration_ms = 3000
        self.countdown_start_ms = 0

        self.reset_game(keep_names=False, start_in_countdown=False)

    def reset_game(self, keep_names=False, start_in_countdown=False):
        # falls restarted wird
        old_name_1 = self.snake1.name if (keep_names and self.snake1 is not None) else ""
        old_name_2 = self.snake2.name if (keep_names and self.snake2 is not None) else ""

        # snake colors
        color1 = self.snake_colors[self.color1_index][1]
        color2 = self.snake_colors[self.color2_index][1]

        # Startposition snake 1
        startpos1 = (2, PLAYFIELD_ROWS // 2)
        # snake1 initialisieren
        self.snake1 = Snake(startpos1, color1, name=old_name_1)
        self.snake1.score = 0
        self.snake1.lives = self.number_of_lives
        self.snake1.direction = (0, 1)

        if self.two_player:
            # Startpostion snake2
            startpos2 = (PLAYFIELD_COLS - 3, PLAYFIELD_ROWS // 2)
            # snake 2 initialisieren
            self.snake2 = Snake(startpos2, color2, name=old_name_2)
            self.snake2.score = 0
            self.snake2.lives = self.number_of_lives
            self.snake2.direction = (0, 1)
        else:
            self.snake2 = None

        self.total_eats_counter = 0
        self._refresh_both_foods()
        self.move_accumulator_ms = 0.0

        if start_in_countdown:
            self.start_countdown()
        else:
            self.state = GameState.MENU

    # Countdown
    def start_countdown(self):
        self.state = GameState.COUNTDOWN
        self.countdown_start_ms = pygame.time.get_ticks()
        self.sound_ping.play()

    # Restart game
    def restart_instant(self):
        self.reset_game(keep_names=True, start_in_countdown=True)

    # Seitenpanel zeichnen methode
    def _draw_panel(self, surface, rect):
        pygame.draw.rect(surface, self.ui_panel, rect, border_radius=18)
        pygame.draw.rect(surface, pygame.Color(120, 255, 140, 55), rect, 1, border_radius=18)

    # heart images
    def _get_heart_images(self, size_px: int):
        size_px = int(size_px)
        full_img = pygame.transform.smoothscale(self.heart_full_base, (size_px, size_px))
        empty_img = pygame.transform.smoothscale(self.heart_empty_base, (size_px, size_px))
        return full_img, empty_img

    # Pfeil-Icon
    def _get_arrow_icon(self, name: str, size_px: int):
        base = self.arrow_icons_base.get(name)
        if base is None:
            return None
        return pygame.transform.smoothscale(base, (int(size_px), int(size_px)))

    # beide Foods neu spawnen
    def _refresh_both_foods(self):
        self.food1 = Food()
        self.food2 = Food()

        self.food1.spawn(self.snake1, self.snake2)
        self.food2.spawn(
            self.snake1,
            self.snake2,
            blocked_extra={(self.food1.position_x, self.food1.position_y)},
        )

    # nur ein Food spawnen
    def _respawn_food_keep_current(self, food_obj, other_food_obj):
        food_obj.spawn(
            self.snake1,
            self.snake2,
            blocked_extra={(other_food_obj.position_x, other_food_obj.position_y)},
        )

    def handle_input(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            # quit
            if event.key == pygame.K_q:
                pygame.quit()
                return
            # restart
            if event.key == pygame.K_r:
                self.restart_instant()
                return

            # Stoppen/ pausieren
            if event.key == pygame.K_ESCAPE:
                if self.state == GameState.RUNNING:
                    self.state = GameState.PAUSED
                    return
                elif self.state == GameState.PAUSED:
                    self.state = GameState.RUNNING
                    return

            # zurück zu menü (nur wenn pausiert)
            if event.key == pygame.K_m and self.state == GameState.PAUSED:
                self.reset_game(keep_names=True, start_in_countdown=False)
                return

            # Richtung nur während Countdown oder running änderbar
            if self.state not in (GameState.COUNTDOWN, GameState.RUNNING):
                continue

            # Spieler 1 (WASD Steuerung)
            if event.key == pygame.K_w:
                self.snake1.change_direction((0, -1))
            elif event.key == pygame.K_s:
                self.snake1.change_direction((0, 1))
            elif event.key == pygame.K_a:
                self.snake1.change_direction((-1, 0))
            elif event.key == pygame.K_d:
                self.snake1.change_direction((1, 0))

            # Spieler 2 (Pfeiltasten-Steuerung)
            if self.snake2 is not None:
                if event.key == pygame.K_UP:
                    self.snake2.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake2.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake2.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake2.change_direction((1, 0))

    # Update Methode
    def update(self, dt_ms):
        if self.state in (GameState.MENU, GameState.GAME_OVER, GameState.PAUSED):
            return

        if self.state == GameState.COUNTDOWN:
            if pygame.time.get_ticks() - self.countdown_start_ms >= self.countdown_duration_ms:
                self.state = GameState.RUNNING
            return

        # Zeit sammeln
        self.move_accumulator_ms += dt_ms

        # wie viele ms pro Step? (z.B. 5 steps/s -> 200ms pro Step -> alle 200ms darf Snake 1 Feld weitergehen)
        step_ms = 1000.0 / self.steps_per_second

        # solange genug Zeit "angespart" ist: einen oder mehrere Steps ausführen
        while self.move_accumulator_ms >= step_ms:
            self.move_accumulator_ms -= step_ms # hier wird ein move aus dem Zeit-Konto "bezahlt"

            # Snakes bewegen
            self.snake1.move()
            if self.snake2 is not None:
                self.snake2.move()

            self.check_food_collision(self.snake1)
            if self.snake2 is not None:
                self.check_food_collision(self.snake2)

            self.resolve_all_collisions()

            # falls game over o.Ä. passiert ist: abbrechen
            if self.state != GameState.RUNNING:
                break

    # rendern
    def render(self, surface):
        if self.state not in (GameState.RUNNING, GameState.COUNTDOWN, GameState.PAUSED):
            return
        # Hintergrundfarbe, Seitenpanels, Spielfeldrand
        surface.fill(COLOR_BG)
        self.draw_side_panels(surface)
        self.draw_playfield_border(surface)
        # Food
        self.food1.draw(surface)
        self.food2.draw(surface)
        # snake 1 (und snake2)
        self.snake1.draw(surface)
        if self.snake2 is not None:
            self.snake2.draw(surface)

        # ggf. Countdown Fläche zeichnen
        if self.state == GameState.COUNTDOWN:
            self.draw_countdown_overlay(surface)
        # ggf. Pausen Fläche zeichnen
        if self.state == GameState.PAUSED:
            self.draw_pause_overlay(surface)

    # Seitenpanel zeichnen
    def draw_side_panels(self, surface):
        UI_MARGIN = 12
        # Panel-Breite und Höhe berechen
        panel_width = PLAYFIELD_OFFSET_X - UI_MARGIN * 2
        panel_height = WINDOW_HEIGHT - UI_MARGIN * 2
        # linkes Panel
        left_rect = pygame.Rect(
            UI_MARGIN,
            UI_MARGIN,
            panel_width,
            panel_height
        )
        # x-Startwert für rechtes Panel
        right_x = PLAYFIELD_OFFSET_X + PLAYFIELD_COLS * GRID_BLOCKSIZE + UI_MARGIN
        # rechtes Panel
        right_rect = pygame.Rect(
            right_x,
            UI_MARGIN,
            panel_width,
            panel_height
        )
        # linkes und rechtes Panel zeichnen
        self._draw_panel(surface, left_rect)
        self._draw_panel(surface, right_rect)

        # Panel für Spieler 1 zeichnen
        self._draw_player_panel(surface, self.snake1, left_rect, is_left=True)

        # falls zweiter Spieler, dann rechts Panel für Spieler zwei zeichnen
        if self.snake2 is not None:
            self._draw_player_panel(surface, self.snake2, right_rect, is_left=False)

        # ansonsten rechtes Panel für Infos zu Shortcuts nutzen
        else:
            y = right_rect.y + 18
            y = self._draw_section_title(surface, right_rect, "Solo", y)

            shortcuts = [("ESC", "", "Pause"), ("M", "", "Menu"), ("R", "", "Restart"), ("Q", "", "Quit")]
            # rechtes Panel mit Controls zeichnen
            self._draw_controls_block(surface, right_rect, "System", shortcuts, y + 6)

    # Zeichnen der Panels; Attribute: rect (rectangel mit Start-x-Wert, Start-y-Wert, Breits, Höhe), is_left (je nach
    # Panelseite)
    def _draw_player_panel(self, surface, snake, rect, is_left=True):
        # name
        name = snake.name

        y = rect.y + 18
        # Titel mit Namen
        y = self._draw_section_title(surface, rect, name, y)

        # Score
        y = self._draw_score(surface, rect, "Score", snake.score, y)
        y += 6
        # lives titel
        y = self._draw_section_title(surface, rect, "Lives", y)

        # Leben (Herz-Icons)
        margin_x = 14
        # Startpunkt zum Zeichnen
        x_start = rect.x + margin_x
        y_start = y + 4
        available_width = rect.w - 2 * margin_x

        # Abstand Herzen zueinander und Herzengröße
        gap = 8
        size_px = 24

        # holt Herz-Icons
        heart_full, heart_empty = self._get_heart_images(size_px)
        # Berechnet Herz-Icons pro Reihe
        per_row = max(1, (available_width + gap) // (size_px + gap))

        # Herz-Icons anzeigen
        for i in range(self.number_of_lives):
            row = i // per_row
            col = i % per_row
            x = x_start + col * (size_px + gap)
            yy = y_start + row * (size_px + gap)

            img = heart_full if i < snake.lives else heart_empty
            surface.blit(img, (x, yy))

        # Anzahl der genutzten Rows zur Berechnung der Position des nächsten Blocks
        rows_used = (self.number_of_lives + per_row - 1) // per_row
        y_controls = y_start + rows_used * (size_px + gap) + 18

        if is_left:
            # Spieler 1 linke Seite
            keys = [
                ("W", "", "Up"),
                ("A", "", "Left"),
                ("S", "", "Down"),
                ("D", "", "Right"),
            ]
            # Controls-Block zeichnen für Spieler 1
            self._draw_controls_block(surface, rect, "Controls", keys, y_controls)
        else:
            # Spieler 2 rechte Seite
            keys = [
                ("ICON:up", "", "Up"),
                ("ICON:left", "", "Left"),
                ("ICON:down", "", "Down"),
                ("ICON:right", "", "Right"),
            ]
            # Control-Block für Spieler 2 zeichnen
            self._draw_controls_block(surface, rect, "Controls", keys, y_controls)

    # Zwischenüberschriften zeichnen (Überschrift + Linie)
    def _draw_section_title(self, surface, rect, text, y):
        title = self.font_small.render(text, True, self.ui_active)
        surface.blit(title, (rect.x + 14, y))

        line_y = y + title.get_height() + 6
        pygame.draw.line(surface, pygame.Color(120, 255, 140, 55),
                         (rect.x + 14, line_y), (rect.right - 14, line_y), 1)
        return line_y + 10

    # Score zeichnen
    def _draw_score(self, surface, rect, key, value, y):
        # key-value row: "Score:" ... "12"
        score_name = self.font_small.render(key, True, self.ui_dim)
        score_value = self.font_small.render(str(value), True, self.ui_text)

        surface.blit(score_name, (rect.x + 14, y))
        surface.blit(score_value, (rect.right - 14 - score_value.get_width(), y))
        return y + 28

    # Controls Blöcke mit Infos zeichnen
    def _draw_controls_block(self, surface, rect, title, keys_rows, y):
        # Titel zeichnen
        y = self._draw_section_title(surface, rect, title, y)

        icon_size = 26
        gap = 10
        text_gap = 14

        for k1, k2, label in keys_rows:
            x = rect.x + 14
            row_y = y

            # k1 zeichnen
            if isinstance(k1, str) and k1.startswith("ICON:"):
                name = k1.split(":", 1)[1]
                icon = self._get_arrow_icon(name, icon_size)
                if icon:
                    surface.blit(icon, (x, row_y))
                    x += icon_size + gap
            else:
                t1 = self.font_small.render(str(k1), True, self.ui_text)
                surface.blit(t1, (x, row_y + (icon_size - t1.get_height()) // 2))
                x += t1.get_width() + gap

            # k2 zeichnen
            if k2:
                if isinstance(k2, str) and k2.startswith("ICON:"):
                    name2 = k2.split(":", 1)[1]
                    icon2 = self._get_arrow_icon(name2, icon_size)
                    if icon2:
                        surface.blit(icon2, (x, row_y))
                        x += icon_size + gap
                else:
                    t2 = self.font_small.render(str(k2), True, self.ui_text)
                    surface.blit(t2, (x, row_y + (icon_size - t2.get_height()) // 2))
                    x += t2.get_width() + gap

            # Label zeichnen
            lbl = self.font_small.render(label, True, self.ui_dim)
            surface.blit(lbl, (x + text_gap, row_y + (icon_size - lbl.get_height()) // 2))

            # nächste Zeile
            y += icon_size + 14

        return y

    # Spielfeldumrandung zeichnen
    def draw_playfield_border(self, surface):
        play_rect = pygame.Rect(
            PLAYFIELD_OFFSET_X,
            PLAYFIELD_OFFSET_Y,
            PLAYFIELD_COLS * GRID_BLOCKSIZE,
            PLAYFIELD_ROWS * GRID_BLOCKSIZE,
        )
        pygame.draw.rect(surface, self.ui_border, play_rect, 2, border_radius=10)

    # Countdown Fläche
    def draw_countdown_overlay(self, surface):
        elapsed = pygame.time.get_ticks() - self.countdown_start_ms
        remaining_ms = max(0, self.countdown_duration_ms - elapsed)

        if remaining_ms > 2000:
            text = "3"
        elif remaining_ms > 1000:
            text = "2"
        elif remaining_ms > 0:
            text = "1"
        else:
            text = "GO!"

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))

        txt = self.font_big.render(text, True, pygame.Color("white"))
        rect = txt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        surface.blit(txt, rect)

    # Overlay beim Pausieren des Spiels
    def draw_pause_overlay(self, surface):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        play_rect = pygame.Rect(
            PLAYFIELD_OFFSET_X,
            PLAYFIELD_OFFSET_Y,
            PLAYFIELD_COLS * GRID_BLOCKSIZE,
            PLAYFIELD_ROWS * GRID_BLOCKSIZE,
        )
        cx, cy = play_rect.center

        txt = self.font_big.render("PAUSED", True, pygame.Color("white"))
        rect = txt.get_rect(center=(cx, cy - 20))
        surface.blit(txt, rect)

        hint = self.font_small.render("ESC = resume    M = menu", True, pygame.Color("white"))
        rect2 = hint.get_rect(center=(cx, cy + 35))
        surface.blit(hint, rect2)

    # Wenn food gegessen wurde, beide Foods refreshen
    def _on_any_food_eaten(self):
        self.total_eats_counter += 1
        if self.total_eats_counter >= self.refresh_after_total_eats:
            self.total_eats_counter = 0
            self._refresh_both_foods()

    # wenn Food gegessen wurde
    def _eat_food(self, snake, food_obj, other_food_obj):
        # falls no-food: Sound abspielen, Snake verliert Leben falls nur noch Länge 1, ansonsten wird sie kürzer um 1,
        # score verringert sich um 1
        if food_obj.is_bad:
            self.sound_no_food.play()

            if snake.score <= 0:
                self.loose_life(snake)
            else:
                snake.shrink(1)
                snake.score = max(0, snake.score - 1)
        # falls food: Sound abspielen, snake wächst um 1, score erhöht sich um 1
        else:
            self.sound_food.play()
            snake.grow()
            snake.score += 1
        # Food neu spawnen und zweites Food-Objekt aber behalten
        self._respawn_food_keep_current(food_obj, other_food_obj)
        self._on_any_food_eaten()

    # Prüft Food-Kollisionen
    def check_food_collision(self, snake):
        head = snake.body_list[0]
        # Falls head mit Food1-Position oder Food2-Position übereinstimmt: snake isst Food
        if (self.food1.position_x, self.food1.position_y) == head:
            self._eat_food(snake, self.food1, self.food2)
            return

        if (self.food2.position_x, self.food2.position_y) == head:
            self._eat_food(snake, self.food2, self.food1)
            return

    # Alle Kollisionen checken
    def resolve_all_collisions(self):
        # Snake1 (bzw. beide Snakes)
        snakes = [self.snake1]
        if self.snake2 is not None:
            snakes.append(self.snake2)

        to_lose = set()

        for s in snakes:
            x, y = s.body_list[0]
            # prüft Wandkollision
            if x < 0 or y < 0 or x >= PLAYFIELD_COLS or y >= PLAYFIELD_ROWS:
                to_lose.add(s)
            # Prüft Selbstkollision
            if s.collides_with_self():
                to_lose.add(s)

        # Prüft Snakekollision
        if self.snake2 is not None:
            head1 = self.snake1.body_list[0]
            head2 = self.snake2.body_list[0]

            # "head-on-head": beide verlieren Leben
            if head1 == head2:
                to_lose.add(self.snake1)
                to_lose.add(self.snake2)
            else:
                # head-in body: nur eine verliert ein Leben
                if head1 in self.snake2.body_list[1:]:
                    to_lose.add(self.snake1)
                if head2 in self.snake1.body_list[1:]:
                    to_lose.add(self.snake2)

        # falls to_lose nicht leer: Sound spielen, Snake verliert Leben
        if to_lose:
            self.sound_collision.play()

            for s in to_lose:
                s.lives -= 1
            # falls Snake keine Leben mehr hat: Game Over
            if any(s.lives <= 0 for s in to_lose):
                self.game_over()
                return
            # Snakes werden resettet (Länge=0)
            for s in to_lose:
                self.reset_snake(s)

    # Leben verlieren:
    def loose_life(self, snake):
        self.sound_collision.play()
        snake.lives -= 1

        if snake.lives <= 0:
            self.game_over()
        else:
            self.reset_snake(snake)

    # wenn Snake Leben verliert, wird sie resettet (Startpunkt Spielfeld, Körperlänge = 1)
    def reset_snake(self, snake):
        if snake is self.snake1:
            start = (2, PLAYFIELD_ROWS // 2)
            snake.direction = (0, 1)
        else:
            start = (PLAYFIELD_COLS - 3, PLAYFIELD_ROWS // 2)
            snake.direction = (0, 1)

        snake.body_list.clear()
        snake.body_list.append(start)
        snake.growing = False

    def game_over(self):
        self.state = GameState.GAME_OVER
        self.sound_gameover.play()