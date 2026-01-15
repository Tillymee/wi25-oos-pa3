# Snake Game (PyGame)

Dieses Projekt ist ein Snake-Spiel, umgesetzt mit Python und PyGame.  
Es unterstützt sowohl einen Einzelspieler-Modus als auch einen Zwei-Spieler-Modus und bringt ein eigenes Menü, ein
In-Game-UI sowie einen Game-Over-Screen mit.

---

## Projektüberblick

Das Spiel ist klar in verschiedene Bereiche aufgeteilt, damit Logik, Darstellung und Benutzeroberfläche gut getrennt
bleiben:

- Zentrales Game-Loop-Handling in `main.py`
- Spiellogik wie Snakes, Food, Kollisionen und Lives in `game.py`
- Menü- und Game-Over-Screens in `screens.py`
- Zentrale Konfiguration der Spielparameter in `config.py`
- Snake-Logik in `snake.py`
- Food-Logik in `food.py`

Das Spielfeld nimmt den mittleren Bereich ein, während seitliche Panels Platz für Score, Leben und Steuerungshinweise
bieten.

---

## Features

- Einzelspieler- und Zwei-Spieler-Modus
- Menü für individuelle Einstellung (Spielmodus, Geschwindigkeit, Leben, Farben)
- Pause-Funktion
- Sidepanels mit Score, Leben und Steuerungshinweisen
- Zwei gleichzeitig aktive Food-Objekte
- Unterschied zwischen gutem und schlechtem Food
- Soundeffekte für Gameplay und UI

---

## Installation

Voraussetzungen:

- Python 3.10 oder neuer
- pip
- PyGame (wird über `requirements.txt` installiert)

Setup (virtuelle Umgebung):

    python -m venv .venv
    source .venv/bin/activate   # macOS / Linux
    # oder
    .venv\Scripts\activate      # Windows

    pip install -r requirements.txt

---

## Spiel starten

    python main.py

---

## Steuerung

### Menü:

- Maus: Menü bedienen
- TAB: Fokus wechseln
- ENTER: Spiel starten (nur wenn Spielername(n) gesetzt)
- BACKSPACE: Zeichen im Namen löschen
- Maus: Menü bedienen
- Q: Spiel beenden

### Im Spiel:

#### Player 1:

- W A S D: Bewegung

#### Player 2:

- Pfeiltasten: Bewegung

#### System

- ESC: Pause / Fortsetzen
- M: Zurück ins Menü (nur im Pause-Modus)
- R: Spiel neu starten
- Q: Spiel beenden

---

## Spielregeln

- Jeder Spieler startet mit einer im Menü einstellbaren Anzahl an Leben.
- Es sind immer zwei Food-Objekte gleichzeitig im Spielfeld aktiv.
- Gutes Food erhöht den Score und lässt die Snake wachsen.
- Schlechtes Food reduziert den Score oder zieht ein Leben ab, wenn der Score bereits 0 ist.
- Kollisionen mit Wänden, sich selbst oder dem anderen Spieler kosten ein Leben.
- Sobald ein Spieler keine Leben mehr hat, endet das Spiel.
- Der Spieler, der am Ende noch Leben hat, gewinnt.

---

## Assets

Für das Spiel werden externe Bild- und Soundressourcen verwendet.  
Alle Assets liegen lokal im Repository, die ursprünglichen Quellen sind unten aufgeführt.

### Emoji / Grafiken

- Food-Emojis (PNG):  
  https://emojiisland.com/pages/download-new-emoji-icons-in-png-ios-10

- Pfeil-Icons (Arrow Controls):  
  https://www.vecteezy.com/png/69862495-an-arrow-pointing-in-the-direction-of-the-arrow

- Snake-Grafik (Pixel-Art):  
  https://www.vecteezy.com/png/72436045-snake-in-pixel-art-style

### Soundeffekte

- Apfel-Biss (Food):  
  https://soundbible.com/1968-Apple-Bite.html

- UI Ping / Start-Sound:  
  https://pixabay.com/sound-effects/game-start-317318/

- Wand-/Kollisionssound:  
  https://pixabay.com/sound-effects/doorhit-98828/

- Game-Over-Sound:  
  https://pixabay.com/sound-effects/game-over-deep-male-voice-clip-352695/

- Falsches Essen / Fehler-Sound:  
  https://pixabay.com/sound-effects/error-126627/