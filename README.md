# QR-Code Generator

Eine einfache Desktop-Anwendung zum Generieren von anpassbaren QR-Codes.

## Überblick

Dieser QR-Code Generator ermöglicht das einfache Erstellen von QR-Codes mit vollständiger Anpassungsfähigkeit - von Inhalt bis Farbe.

## Funktionen

- Benutzerdefinierter Textinhalt für QR-Codes
- Freie Farbwahl für Füllung und Hintergrund
- Individueller Speicherort
- Vorschau nach Erstellung des QR-Codes
- Plattformübergreifend (Windows, Linux)

## Voraussetzungen

- Python 3.12+
- pip
- tkinter (Teil der Python-Standardbibliothek)
- virtualenv (empfohlen)

## Verzeichnisstruktur

```
.
├── img/
│   ├── qr-code-outline.ico
│   ├── qr-code-outline.svg
│   └── qrcode_gui.png
├── gui_mockup.dio
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
└── starter.sh
```

## Installation

1. Klone dieses Repository:
   ```shell
   git clone https://github.com/Sympa1/QR-CodeGen
   ```

2. Navigiere in das Verzeichnis:
   ```shell
   cd QR-CodeGen
   ```

3. Virtuelles Environment einrichten
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Abhängigkeiten installieren
   ```bash
   pip install -r requirements.txt
   ```

## Ausführung

Die Anwendung kann auf folgende Wege gestartet werden:

### Methode 1: Direkt mit Python
```bash
python main.py
```

### Methode 2: Mit dem Start-Skript (Linux/macOS)
```bash
chmod +x starter.sh
./starter.sh
```

### Methode 3: Mit dem Start-Skript (Windows)
```bash
starter.sh
```

## Verwendung

1. **Text/URL eingeben** – Geben Sie den Inhalt des QR-Codes ein
2. **Farben anpassen** (optional) – Klicken Sie auf die Farbwähler-Buttons
3. **Speicherort wählen** – Klicken Sie "Durchsuchen" um den Speicherort zu bestimmen
4. **Dateityp wählen** – Wählen Sie zwischen PNG, JPG oder SVG
5. **Generieren** – Klicken Sie "QR-Code Generieren" zum Erstellen

## Abhängigkeiten

- Pillow 11.1.0
- qrcode 8.0.0
- colorama==0.4.6

## Lizenz

Dieses Projekt ist unter der GPL-3.0 license lizenziert - siehe die [LICENSE](LICENSE)-Datei für Details.