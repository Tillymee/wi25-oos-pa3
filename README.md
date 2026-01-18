# Snake Game (PyGame)

Dieses Projekt ist ein Snake-Spiel, umgesetzt mit Python und PyGame.

---

## Inhaltsverzeichnis

- [Projektüberblick](#projektüberblick)
- [Features](#features)
- [Technische Umsetzung](#technische-umsetzung)
- [Installation](#installation)
- [Steuerung](#steuerung)
- [Spielregeln](#spielregeln)
- [Assets](#assets)

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

## Technische Umsetzung

### Game Loop & States

Das Spiel läuft in einer Endlosschleife (`main.py`).  
Der Ablauf wird über `GameState` gesteuert:

`MENU → COUNTDOWN → RUNNING → PAUSED → GAME_OVER`

Pro Frame werden:

1. Events gelesen
2. Eingaben verarbeitet
3. Spiellogik aktualisiert
4. Szene gerendert

---

### Zeitbasierte Bewegung (Speed)

Die Snake bewegt sich **zeitbasiert**, nicht framebasiert.

- `CLOCK.tick(FPS)` liefert `dt_ms` (vergangene Zeit seit dem letzten Frame)
- In `game.update(dt_ms)` wird diese Zeit gesammelt
- Sobald genug Zeit vergangen ist (`1000 / steps_per_second`), bewegt sich die Snake **ein Grid-Feld**

**Vorteil:**  
Die Geschwindigkeit bleibt stabil, unabhängig von FPS oder Hardware.

---

### Snake-Logik (`snake.py`)

- Die Snake besteht aus einer Liste von Grid-Positionen
- Bewegung erfolgt durch Hinzufügen eines neuen Kopfes
- Ob die Snake wächst oder schrumpft, entscheidet sich im nächsten Move
- Die Snake kennt **keine Zeitlogik**, sie bewegt sich nur, wenn das Game einen Schritt auslöst

---

### Food-Logik (`food.py`)

- Food kann **gut** oder **schlecht** sein
- Bilder werden dynamisch aus Ordnern geladen
- Beim Spawnen werden belegte Felder vermieden (Snake-Körper, anderes Food)
- Food kennt nur Typ und Position, die Spielregeln liegen in `game.py`

---

### Kollisionen & Leben

Geprüft werden:

- Wandkollisionen
- Selbstkollisionen
- Snake-zu-Snake-Kollisionen

Bei einer Kollision verliert die betroffene Snake ein Leben.  
Sobald ein Spieler keine Leben mehr hat → `GAME_OVER`.

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



### Spiel starten

    python main.py

---

## Steuerung

### Menü:

- Maus: Menü bedienen
- TAB: Fokus wechseln
- ENTER: Spiel starten (nur wenn Spielername(n) gesetzt)
- BACKSPACE: Zeichen im Namen löschen
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