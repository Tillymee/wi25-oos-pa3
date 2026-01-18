from config import *


# Klasse Screens für angezeigte Screens wie Menu und GameOver
class Screens:

    # Init
    def __init__(self):
        # Titelfont, große Schriftart, kleine Schriftart
        self.font_title = pygame.font.SysFont("Courier New", 64, bold=True)
        self.font_big = pygame.font.SysFont(None, 56)
        self.font_small = pygame.font.SysFont(None, 26)

        self.logo = None
        self.logo_h = 0
        self._load_and_scale_logo("img/other/logo.png")

        # benötigte Bilder laden und skalieren (Pokal, Medaille Platz 1, Medaille Platz 2)
        self.img_trophy = pygame.image.load("img/other/trophy.png").convert_alpha()
        self.img_medal_1st = pygame.image.load("img/other/1st-medal.png").convert_alpha()
        self.img_medal_2nd = pygame.image.load("img/other/2nd-medal.png").convert_alpha()
        self.img_trophy = pygame.transform.smoothscale(self.img_trophy, (64, 64))
        self.img_medal_1st = pygame.transform.smoothscale(self.img_medal_1st, (48, 48))
        self.img_medal_2nd = pygame.transform.smoothscale(self.img_medal_2nd, (48, 48))

        # active gibt an, welcher Menüpunkt ausgewählt ist (1 = Spieler 1; 2 = Spieler2; 3 = Speed; 4 = Lives;
        # 5 = Farbe Spieler 1; 6 = Farbe Spieler 2; 7 = Start)
        self.active = 0
        # Klickareas für die Maus
        self.click_areas = {}

        # Farben
        self.col_bg = pygame.Color(0, 0, 0)
        self.col_panel = pygame.Color(14, 18, 14)
        self.col_panel2 = pygame.Color(18, 24, 18)
        self.col_text = pygame.Color(235, 245, 235)

        self.col_border = pygame.Color(130, 155, 130)
        self.col_active = pygame.Color(110, 255, 140)

        # Panelbreite
        self.panel_width = 650
        # Breite einer Zeile
        self.row_width = 520
        # Höhe einer Zeile
        self.row_height = 40
        # Abstand zwischen zwei Zeilen
        self.row_gap = 12

        # Panel Paddings
        self.panel_padding_top = 15
        self.panel_padding_bottom = 15
        # Start-Button Höhe und Breite
        self.start_btn_width = 260
        self.start_btn_height = 50

        # Margins
        self.margin_bottom = 26

    # Logo auf Höhe skalieren und speichern
    def _load_and_scale_logo(self, path):
        img = pygame.image.load(path).convert_alpha()
        self.logo = pygame.transform.scale(img, (260, 220))

    # Text zeichnen und rectangle returnen
    def _text_center(self, surface, text, center, font, color):
        t = font.render(text, True, color)
        r = t.get_rect(center=center)
        surface.blit(t, r)
        return r

    # Panel zeichnen
    def _panel(self, surface, rect):
        pygame.draw.rect(surface, self.col_panel, rect, border_radius=18)
        pygame.draw.rect(surface, pygame.Color(120, 255, 140, 55), rect, 1, border_radius=18)

    # eine einzelne Zeile
    def _panel_row(self, surface, rect, highlighted=False):
        bg = self.col_panel2 if not highlighted else pygame.Color(20, 32, 20)
        border = self.col_border if not highlighted else self.col_active
        pygame.draw.rect(surface, bg, rect, border_radius=14)
        pygame.draw.rect(surface, border, rect, 2, border_radius=14)

    # Button
    def _button(self, surface, rect, text, hovered=False, enabled=True, highlighted=False):
        if enabled:
            bg = pygame.Color(22, 28, 22) if not hovered else pygame.Color(28, 38, 28)
            border = self.col_border if not highlighted else self.col_active
            txt = self.col_text if not highlighted else self.col_active
        else:
            bg = pygame.Color(14, 16, 14)
            border = pygame.Color(70, 85, 70)
            txt = pygame.Color(95, 110, 95)

        pygame.draw.rect(surface, bg, rect, border_radius=14)
        pygame.draw.rect(surface, border, rect, 2, border_radius=14)
        self._text_center(surface, text, rect.center, self.font_small, txt)

    # Fokusliste (abhängig von Ein-/Mehrspielermodus)
    def _focus_list(self, two_player: bool):
        if two_player:
            return [0, 1, 2, 3, 4, 5, 6, 7]
        return [0, 1, 3, 4, 5, 7]

    # nächstes Element der Fokusliste holen
    def _next_focus(self, two_player: bool):
        # Richtige Fokusliste holen
        focuslist = self._focus_list(two_player)
        # aktuellen Index holen, ansonsten 0 (default)
        i = focuslist.index(self.active) if self.active in focuslist else 0
        # zum nächsten Element gehen (nach dem letzten wieder zu ersten)
        self.active = focuslist[(i + 1) % len(focuslist)]

    # Prüft: Name(n) vergeben? dann Start möglich
    def _can_start(self, game):
        if not game.snake1.name:
            return False
        if game.two_player and (game.snake2 is None or not game.snake2.name):
            return False
        return True

    # modus wechseln (einzel-/Mehrspieler)
    def _toggle_mode(self, game):
        # Mode togglen und Game resetten
        game.two_player = not game.two_player
        game.reset_game(keep_names=True, start_in_countdown=False)

    # Gamespeed ändern
    def _change_speed(self, game, direction):
        game.speed_index = (game.speed_index + direction) % len(game.speed_keys)
        game.steps_per_second = game.speed_modes[game.speed_keys[game.speed_index]]
        game.move_accumulator_ms = 0.0

    # Lives ändern
    def _change_lives(self, game, direction):
        game.number_of_lives_index = (game.number_of_lives_index + direction) % len(game.number_of_lives_keys)
        game.number_of_lives = game.number_of_lives_modes[game.number_of_lives_keys[game.number_of_lives_index]]

    # Farbe Spieler 1 ändern
    def _change_color_p1(self, game, direction):
        game.color1_index = (game.color1_index + direction) % len(game.snake_colors)
        if game.snake1 is not None:
            game.snake1.color = game.snake_colors[game.color1_index][1]

    # Farbe Spieler 2 ändern
    def _change_color_p2(self, game, direction):
        game.color2_index = (game.color2_index + direction) % len(game.snake_colors)
        if game.snake2 is not None:
            game.snake2.color = game.snake_colors[game.color2_index][1]

    # Events behandeln
    def handle_menu_input(self, events, game):
        for event in events:
            # Mausklick-Events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Mausklick-Position speichern
                mx, my = event.pos
                for key, rect in self.click_areas.items():
                    if not rect.collidepoint(mx, my):
                        continue
                    # Falls Mausklick in Rectangle: active neu setzen, Sound abspielen
                    if key == "mode":
                        self.active = 0
                        self._toggle_mode(game)
                        game.sound_ping.play()
                        break

                    if key == "p1_box":
                        self.active = 1
                        game.sound_ping.play()
                        break

                    if key == "p2_box":
                        self.active = 2
                        game.sound_ping.play()
                        break

                    if key == "speed":
                        self.active = 3
                        self._change_speed(game, +1)
                        game.sound_ping.play()
                        break

                    if key == "lives":
                        self.active = 4
                        self._change_lives(game, +1)
                        game.sound_ping.play()
                        break

                    if key == "color1":
                        self.active = 5
                        self._change_color_p1(game, +1)
                        game.sound_ping.play()
                        break

                    if key == "color2":
                        self.active = 6
                        self._change_color_p2(game, +1)
                        game.sound_ping.play()
                        break

                    # Start Game
                    if key == "start_btn":
                        self.active = 7
                        if self._can_start(game):
                            game.snake1.lives = game.number_of_lives
                            if game.snake2 is not None:
                                game.snake2.lives = game.number_of_lives
                            game.start_countdown()
                        else:
                            game.sound_ping.play()
                        break

                continue

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_q:
                pygame.quit()
                return

            # mit Tab den Fokus wechseln
            if event.key == pygame.K_TAB:
                self._next_focus(game.two_player)
                game.sound_ping.play()
                continue

            # mit Enter Spiel starten
            if event.key == pygame.K_RETURN:
                if self._can_start(game):
                    game.snake1.lives = game.number_of_lives
                    if game.snake2 is not None:
                        game.snake2.lives = game.number_of_lives
                    game.start_countdown()
                else:
                    game.sound_ping.play()
                continue

            # mit backspace namen löschen
            if event.key == pygame.K_BACKSPACE:
                if self.active == 1:
                    game.snake1.name = game.snake1.name[:-1]
                elif self.active == 2 and game.two_player and game.snake2 is not None:
                    game.snake2.name = game.snake2.name[:-1]
                continue

            # Namen Eingabe
            char = event.unicode
            if char and char.isprintable():
                if self.active == 1:
                    game.snake1.name += char
                elif self.active == 2 and game.two_player and game.snake2 is not None:
                    game.snake2.name += char

    # Menü rendern
    def render_menu(self, surface, game):
        surface.fill(self.col_bg)
        self.click_areas.clear()
        mx, my = pygame.mouse.get_pos()

        # Rechteck um Logo
        r = self.logo.get_rect(center=(WINDOW_WIDTH // 2, 110))
        # Logo zeichnen
        surface.blit(self.logo, r)
        # untere Kante des Logos
        logo_bottom = r.bottom

        # Rows des Menüs: Mode, Player 1, (Player2), Speed, Lives, Color1, (Color2)
        rows = ["mode", "p1"]
        if game.two_player and game.snake2 is not None:
            rows.append("p2")
        rows += ["speed", "lives", "c1"]
        if game.two_player:
            rows.append("c2")

        # Höhe des gesamten Contents
        content_height = (
                self.panel_padding_top
                + len(rows) * self.row_height
                + (len(rows) - 1) * self.row_gap
                + 18
                + self.start_btn_height
                + self.panel_padding_bottom
        )

        # Panel Rectangle
        panel = pygame.Rect(0, 0, self.panel_width, content_height)
        panel.top = logo_bottom - 60
        panel.centerx = WINDOW_WIDTH // 2
        # Panel erstellen/ zeichnen
        self._panel(surface, panel)

        # Slider für jede Zeile zur Auswahl
        def draw_slider(y, label, value, focus_id, key):
            # neue Row anlegen
            row = pygame.Rect(0, 0, self.row_width, self.row_height)
            row.center = (WINDOW_WIDTH // 2, y)
            # highlight = true, falls Zeile aktiv ist oder gehovert wird
            highlight = (self.active == focus_id)

            # Hintergrund der Zeile zeichnen
            self._panel_row(surface, row, highlighted=highlight)

            # Text schreiben (Label= Attribut, Value= aktueller Wert)
            txt_color = self.col_active if highlight else self.col_text
            self._text_center(surface, f"{label}: {value}", row.center, self.font_small, txt_color)

            # Klickbereiche für die maus
            self.click_areas[key] = row

        # Eingabe/ Anzeige der Spielernamen
        def draw_name(y, label, value, focus_id, box_key):
            # Rechteck für Zeile
            row = pygame.Rect(0, 0, self.row_width, self.row_height)
            row.center = (WINDOW_WIDTH // 2, y)
            # true beim hovern
            hover = row.collidepoint(mx, my)
            # highlighten falls im Fokus oder hover= true
            highlight = (self.active == focus_id) or hover
            # eine neue Zeile erstellen
            self._panel_row(surface, row, highlighted=highlight)
            # Text (Name) anzeigen
            shown = value if value else "ENTER NAME"
            txt_color = self.col_active if highlight else self.col_text
            self._text_center(surface, f"{label}: {shown}", row.center, self.font_small, txt_color)

            if self.active == focus_id:
                dot = pygame.Rect(0, 0, 10, 10)
                dot.center = (row.right - 22, row.centery)
                pygame.draw.ellipse(surface, self.col_active, dot)

            self.click_areas[box_key] = row

        # y-Wert der ersten Zeile im Menü
        y = panel.top + self.panel_padding_top + self.row_height // 2
        # Slider für Mode (Single, Two Players)
        mode_value = "SOLO" if not game.two_player else "TWO PLAYERS"
        draw_slider(y, "MODE", mode_value, 0, "mode")

        # y-Wert für nächste Zeile erhöhen und nächste Zeile zeichnen (Player 1)
        y += self.row_height + self.row_gap
        draw_name(y, "PLAYER 1", game.snake1.name, 1, "p1_box")

        # Player 2
        y += self.row_height + self.row_gap
        if game.two_player and game.snake2 is not None:
            draw_name(y, "PLAYER 2", game.snake2.name, 2, "p2_box")

            y += self.row_height + self.row_gap
        # Speed Slider
        draw_slider(y, "SPEED", game.speed_keys[game.speed_index], 3, "speed")

        # Lives Slider
        y += self.row_height + self.row_gap
        draw_slider(y, "LIVES", game.number_of_lives_keys[game.number_of_lives_index], 4, "lives")

        # Color Player 1 Slider
        y += self.row_height + self.row_gap
        c1_name, c1_col = game.snake_colors[game.color1_index]
        draw_slider(y, "COLOR P1", c1_name, 5, "color1")
        y += self.row_height + self.row_gap

        # Color Player 2 Slider
        if game.two_player:
            c2_name, c2_col = game.snake_colors[game.color2_index]
            draw_slider(y, "COLOR P2", c2_name, 6, "color2")
            y += self.row_height + self.row_gap

        # Startbutton
        btn = pygame.Rect(0, 0, self.start_btn_width, self.start_btn_height)
        btn.center = (
            WINDOW_WIDTH // 2,
            panel.bottom - (self.panel_padding_bottom + self.start_btn_height // 2) - 4
        )
        self.click_areas["start_btn"] = btn

        hover_btn = btn.collidepoint(mx, my)
        highlight_btn = (self.active == 7) or hover_btn
        # nur enabled, falls _can_start = true
        self._button(surface, btn, "START", hovered=hover_btn, enabled=self._can_start(game), highlighted=highlight_btn)

    # Game Over Screen Events abfangen
    def handle_game_over_input(self, events, game):
        for event in events:
            # falls linke Maustaste gedrückt:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for key, rect in self.click_areas.items():
                    if rect.collidepoint(mx, my):
                        # neustarten
                        if key == "go_restart":
                            game.reset_game(keep_names=True, start_in_countdown=True)
                            return
                        # zurück zum Menü
                        if key == "go_menu":
                            game.reset_game(keep_names=True, start_in_countdown=False)
                            return
                        # Spiel beenden
                        if key == "go_quit":
                            pygame.quit()
                            return

            if event.type != pygame.KEYDOWN:
                continue

            # Shortcuts:
            # Quit = Q
            if event.key == pygame.K_q:
                pygame.quit()
                return
            # Restart = R
            if event.key == pygame.K_r:
                game.reset_game(keep_names=True, start_in_countdown=True)
                return
            # Menu = M
            if event.key == pygame.K_m:
                game.reset_game(keep_names=True, start_in_countdown=False)
                return

    # Game Over Screen rendern
    def render_game_over(self, surface, game):
        surface.fill(self.col_bg)
        self.click_areas.clear()
        # neues Panel
        panel = pygame.Rect(0, 0, 650, 460)
        panel.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10)
        self._panel(surface, panel)

        # gameover solo oder duo
        if game.snake2 is None:
            self._render_game_over_solo(surface, game, panel)
        else:
            self._render_game_over_duo(surface, game, panel)

    # für einen Spieler rendern
    def _render_game_over_solo(self, surface, game, panel):
        # titeltext
        self._text_center(surface, "GAME OVER", (WINDOW_WIDTH // 2, panel.top + 60), self.font_big, self.col_text)

        # pokal
        trophy_rect = self.img_trophy.get_rect(center=(WINDOW_WIDTH // 2, panel.top + 130))
        surface.blit(self.img_trophy, trophy_rect)

        # Glückwunschtext
        self._text_center(
            surface,
            f"Congratulations, {game.snake1.name}!",
            (WINDOW_WIDTH // 2, panel.top + 190),
            self.font_small,
            self.col_text,
        )

        # Zeile mit Score
        row = pygame.Rect(0, 0, 520, 56)
        row.center = (WINDOW_WIDTH // 2, panel.top + 265)
        self._panel_row(surface, row, highlighted=True)

        # Icon (Medaille)
        x_icon = row.left + 24
        y_mid = row.centery
        surface.blit(self.img_medal_1st, self.img_medal_1st.get_rect(center=(x_icon, y_mid)))
        # Scoretext
        score_txt = self.font_small.render(f"{game.snake1.name}: {game.snake1.score}", True, self.col_text)
        surface.blit(score_txt, (x_icon + 40, y_mid - score_txt.get_height() // 2))

        # Buttons für Meu, Neustart, Beenden
        btn_w, btn_h = 180, 54
        gap = 18

        btn_restart = pygame.Rect(0, 0, btn_w, btn_h)
        btn_menu = pygame.Rect(0, 0, btn_w, btn_h)
        btn_quit = pygame.Rect(0, 0, btn_w, btn_h)

        y_btn = panel.bottom - 70
        btn_restart.center = (WINDOW_WIDTH // 2 - (btn_w + gap), y_btn)
        btn_menu.center = (WINDOW_WIDTH // 2, y_btn)
        btn_quit.center = (WINDOW_WIDTH // 2 + (btn_w + gap), y_btn)

        # Buttons erstellen
        mx, my = pygame.mouse.get_pos()
        self._button(surface, btn_restart, "RESTART", hovered=btn_restart.collidepoint(mx, my), enabled=True)
        self._button(surface, btn_menu, "MENU", hovered=btn_menu.collidepoint(mx, my), enabled=True)
        self._button(surface, btn_quit, "QUIT", hovered=btn_quit.collidepoint(mx, my), enabled=True)

        # Clickareas
        self.click_areas["go_restart"] = btn_restart
        self.click_areas["go_menu"] = btn_menu
        self.click_areas["go_quit"] = btn_quit

    # Game Over Rendern für zwei Personen
    def _render_game_over_duo(self, surface, game, panel):
        # Gewinner und Verlierer bestimmen
        if game.snake1.lives == 0:
            winner = game.snake2
            loser = game.snake1
        else:
            winner = game.snake1
            loser = game.snake2

        # titeltext
        self._text_center(surface, "GAME OVER", (WINDOW_WIDTH // 2, panel.top + 55), self.font_big, self.col_text)
        # pokal
        trophy_rect = self.img_trophy.get_rect(center=(WINDOW_WIDTH // 2, panel.top + 120))
        surface.blit(self.img_trophy, trophy_rect)

        # Zeile Gewinner
        self._text_center(surface, f"Winner: {winner.name}", (WINDOW_WIDTH // 2, panel.top + 175), self.font_small,
                          self.col_active)

        # Score beide Spieler
        row1 = pygame.Rect(0, 0, 520, 56)
        row2 = pygame.Rect(0, 0, 520, 56)
        row1.center = (WINDOW_WIDTH // 2, panel.top + 245)
        row2.center = (WINDOW_WIDTH // 2, panel.top + 315)

        self._panel_row(surface, row1, highlighted=True)
        self._panel_row(surface, row2, highlighted=False)

        # Zeile GEwinner
        x_icon = row1.left + 24
        surface.blit(self.img_medal_1st, self.img_medal_1st.get_rect(center=(x_icon, row1.centery)))
        t1 = self.font_small.render(f"{winner.name}: {winner.score}", True, self.col_text)
        surface.blit(t1, (x_icon + 40, row1.centery - t1.get_height() // 2))

        # Zeile Verlierer
        x_icon2 = row2.left + 24
        surface.blit(self.img_medal_2nd, self.img_medal_2nd.get_rect(center=(x_icon2, row2.centery)))
        t2 = self.font_small.render(f"{loser.name}: {loser.score}", True, self.col_text)
        surface.blit(t2, (x_icon2 + 40, row2.centery - t2.get_height() // 2))

        # Buttons zum neustart, beenden, menü
        btn_w, btn_h = 180, 54
        gap = 18

        btn_restart = pygame.Rect(0, 0, btn_w, btn_h)
        btn_menu = pygame.Rect(0, 0, btn_w, btn_h)
        btn_quit = pygame.Rect(0, 0, btn_w, btn_h)

        y_btn = panel.bottom - 70
        btn_restart.center = (WINDOW_WIDTH // 2 - (btn_w + gap), y_btn)
        btn_menu.center = (WINDOW_WIDTH // 2, y_btn)
        btn_quit.center = (WINDOW_WIDTH // 2 + (btn_w + gap), y_btn)

        mx, my = pygame.mouse.get_pos()
        self._button(surface, btn_restart, "RESTART", hovered=btn_restart.collidepoint(mx, my), enabled=True)
        self._button(surface, btn_menu, "MENU", hovered=btn_menu.collidepoint(mx, my), enabled=True)
        self._button(surface, btn_quit, "QUIT", hovered=btn_quit.collidepoint(mx, my), enabled=True)

        # clickareas
        self.click_areas["go_restart"] = btn_restart
        self.click_areas["go_menu"] = btn_menu
        self.click_areas["go_quit"] = btn_quit
