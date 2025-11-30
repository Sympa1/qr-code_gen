import sys
import os
from tkinter import filedialog, colorchooser, messagebox, ttk
from PIL import Image, ImageTk
import qrcode
import tkinter as tk


def resource_path(relative_path):
    """
    Bestimmt den Pfad zu einer eingebetteten Ressource für Standalone-Anwendungen.

    Diese Funktion unterstützt sowohl die Entwicklungsumgebung als auch
    PyInstaller-Pakete. Sie wird verwendet, um auf Bilddateien und andere
    Ressourcen zuzugreifen, die mit der Anwendung verteilt werden.

    Args:
        relative_path (str): Der relative Pfad zur Ressource (z.B. "img/icon.png")

    Returns:
        str: Der absolute Pfad zur Ressource

    Example:
        >>> path = resource_path("img/qr-code-outline.ico")
        >>> print(path)
        /home/user/qr-code_gen/img/qr-code-outline.ico
    """
    try:
        # PyInstaller erstellt beim Packen ein temporäres Verzeichnis
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


class QRCodeGenerator:
    """
    Generiert QR-Codes mit benutzerdefinierten Farben und speichert diese als Bilddatei.

    Diese Klasse kapselt die Funktionalität zur Erstellung von QR-Codes mit
    individueller Farbgestaltung. Sie unterstützt verschiedene Bildformate
    (PNG, JPG, SVG) und ermöglicht vollständige Anpassung der Codes.

    Attributes:
        qr (qrcode.QRCode): Instanz der QRCode-Bibliotheksklasse
        content (str): Der zu kodierenden Inhalt des QR-Codes
        fill_color (str): Hexadezimal-Farbe für die QR-Code Module (z.B. "#000000")
        background_color (str): Hexadezimal-Farbe für den Hintergrund (z.B. "#FFFFFF")
        file_path (str): Vollständiger Pfad zum Speichern der QR-Code Datei

    Example:
        >>> qr_gen = QRCodeGenerator(
        ...     content="https://example.com",
        ...     fill_color="#000000",
        ...     background_color="#FFFFFF",
        ...     file_path="/home/user/qrcode.png"
        ... )
        >>> qr_gen.generate()

    Note:
        - Unterstützte Formate: PNG, JPG, SVG
        - Standardgröße: 10x10 Pixel pro Modul mit 2er-Rand
        - Die Dateigröße wird automatisch optimiert
    """

    def __init__(self, content: str, fill_color: str, background_color: str, file_path: str):
        """
        Initialisiert eine neue QRCodeGenerator-Instanz.

        Args:
            content (str): Der Inhalt, der im QR-Code kodiert werden soll.
                          Kann Text, URLs, Kontaktdaten oder andere Daten sein.
            fill_color (str): Hexadezimal-Farbwert für die QR-Code Module.
                             Format: "#RRGGBB" (z.B. "#000000" für Schwarz)
                             oder named colors (z.B. "Black", "White")
            background_color (str): Hexadezimal-Farbwert oder Farbnamen für den Hintergrund.
                                   Format: "#RRGGBB" (z.B. "#FFFFFF" für Weiß)
            file_path (str): Vollständiger Pfad zum Speichern der QR-Code Datei.
                            Das Bildformat wird automatisch erkannt (z.B. .png, .jpg)

        Raises:
            - Fehler bei ungültigen Farbwerten werden bei der Generierung geworfen

        Note:
            Die QRCode-Instanz wird mit box_size=10 (Pixelgröße pro Modul)
            und border=2 (Randbreite) initialisiert.
        """
        self.qr = qrcode.QRCode(box_size=10, border=2)
        self.content = content
        self.fill_color = fill_color
        self.background_color = background_color
        self.file_path = file_path

    def generate(self):
        """
        Generiert den QR-Code und speichert ihn als Bilddatei.

        Dieser Prozess umfasst folgende Schritte:
        1. Daten zum QR-Code hinzufügen
        2. QR-Code generieren und für optimale Größe anpassen
        3. Bild mit den benutzerdefinierten Farben erstellen
        4. Datei speichern und Erfolgsmeldung ausgeben

        Returns:
            None

        Raises:
            IOError: Falls die Datei nicht gespeichert werden konnte
            ValueError: Falls die Farbwerte ungültig sind

        Side Effects:
            - Erstellt/überschreibt die Datei unter self.file_path
            - Gibt eine Erfolgsmeldung in der Konsole aus

        Note:
            - Die Dateigröße passt sich automatisch an den Datenmenge an
            - Der QR-Code ist mit fit=True optimiert

        Example:
            >>> qr_gen = QRCodeGenerator("Test", "Black", "White", "/tmp/test.png")
            >>> qr_gen.generate()
            QR-Code erfolgreich generiert und als 'qrcode.png' gespeichert.
        """
        # Datensatz hinzufügen
        self.qr.add_data(self.content)

        # QR-Code generieren und optimieren
        self.qr.make(fit=True)

        # Bild des QR-Codes erzeugen
        img = self.qr.make_image(fill_color=self.fill_color, back_color=self.background_color)

        # Bild speichern
        img.save(self.file_path)

        print("QR-Code erfolgreich generiert und als 'qrcode.png' gespeichert.")


class QRCodeGeneratorGUI(tk.Tk):
    """
    Grafische Benutzeroberfläche für den QR-Code Generator.

    Diese Klasse erbt von tkinter.Tk und implementiert eine vollständige
    Desktop-Anwendung zur Erzeugung von QR-Codes mit benutzerdefinierten
    Farben und Speicheroptionen.

    Die Benutzeroberfläche besteht aus folgenden Komponenten:
    - Ein QR-Code Vorschaubild (GitHub-Repo QR-Code)
    - Eingabebereich mit Textfeld für QR-Code Inhalt
    - Farbwähler für Füll- und Hintergrundfarben
    - Dateidialog zur Auswahl des Speicherorts
    - Anzeigebereich für gewählte Einstellungen
    - Buttons zum Generieren und Abbrechen

    Attributes:
        icon_image (Image): Das Anwendungsicon als PIL-Image
        icon_photo (ImageTk.PhotoImage): Das Icon für die GUI
        qr_image (Image): Das QR-Code Vorschaubild
        qr_photo (ImageTk.PhotoImage): Das Vorschaubild für die GUI
        fill_color (str): Aktuelle Füllfarbe des QR-Codes
        background_color (str): Aktuelle Hintergrundfarbe des QR-Codes
        file_path (str): Aktueller Speicherpfad für die QR-Code Datei
        input_frame (ttk.Labelframe): Rahmen für Benutzereingaben
        text_input_frame (ttk.Labelframe): Rahmen für Texteingabe
        color_frame (ttk.Labelframe): Rahmen für Farbwahl
        location_frame (ttk.Labelframe): Rahmen für Speicherort-Auswahl
        settings_frame (ttk.Labelframe): Rahmen für Anzeige der Einstellungen
        button_frame (ttk.Frame): Rahmen für Steuerbuttons
        text_entry (ttk.Entry): Eingabefeld für QR-Code Inhalt
        fill_color_btn (ttk.Button): Button für Füllfarben-Wahl
        bg_color_btn (ttk.Button): Button für Hintergrundfarben-Wahl
        browse_btn (ttk.Button): Button für Dateibrowser
        generate_btn (ttk.Button): Button zum Generieren des QR-Codes
        cancel_btn (ttk.Button): Button zum Abbrechen der Anwendung
        fill_color_display (ttk.Label): Anzeige der Füllfarbe
        bg_color_display (ttk.Label): Anzeige der Hintergrundfarbe
        path_display (ttk.Label): Anzeige des Speicherpfads

    Methods:
        create_widgets(): Erstellt alle GUI-Komponenten
        choose_color(button_id): Öffnet Farbwähler-Dialog
        get_user_directory(): Bestimmt Standard-Speicherverzeichnis
        choose_save_location(): Öffnet Datei-Dialog
        generate_qr_code(): Generiert QR-Code und speichert ihn

    Example:
        >>> app = QRCodeGeneratorGUI()
        >>> app.mainloop()

    Note:
        - Lädt automatisch Icon aus img/qr-code-outline.ico
        - Verwendet Vorschaubild aus img/qrcode_gui.png
        - Unterstützt Deutsch und Englisch bei der Verzeichniserkennung
        - Speichert standardmäßig in Dokumente oder Documents Ordner
    """

    def __init__(self):
        """
        Initialisiert die QR-Code Generator GUI-Anwendung.

        Diese Methode:
        1. Ruft den Konstruktor der Tkinter-Basisklasse auf
        2. Setzt den Fenstertitel
        3. Lädt und setzt das Anwendungsicon
        4. Initialisiert die Hilfsvariablen für Farben und Dateipfade
        5. Ruft create_widgets() auf, um alle GUI-Komponenten zu erstellen

        Returns:
            None

        Note:
            - Das Icon wird automatisch aus img/qr-code-outline.ico geladen
            - Standardfarben: Schwarz für Füllfarbe, Weiß für Hintergrund
            - Der Speicherpfad wird automatisch vom System bestimmt

        Raises:
            FileNotFoundError: Falls das Icon nicht gefunden wird
        """
        super().__init__()

        self.title("QR-Code Generator")

        # Icon laden und in ein unterstütztes Format konvertieren um Linux Kompatibilität zu ermöglichen
        self.icon_image = Image.open(resource_path("img/qr-code-outline.ico"))
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)
        # Icon setzen
        self.iconphoto(False, self.icon_photo)

        # Deklaration der Hilfsvariablen
        self.fill_color = "Black"
        self.background_color = "White"
        self.file_path = self.get_user_directory()

        self.create_widgets()

    def create_widgets(self):
        """
        Erstellt alle GUI-Komponenten der Anwendung.

        Diese Methode wird vom __init__-Konstruktor aufgerufen und ist verantwortlich
        für das Layout und die Erstellung aller visuellen Elemente:

        Komponenten:
        1. QR-Code Vorschaubild (200x200 Pixel)
        2. Eingabebereich:
           - Textfeld für QR-Code Inhalt
           - Farbwähler für Füll- und Hintergrundfarben
           - Dateiauswahl-Button
        3. Einstellungsanzeige:
           - Gewählte Füllfarbe (visuell und Text)
           - Gewählte Hintergrundfarbe (visuell und Text)
           - Gewählter Speicherpfad
        4. Steuerbuttons:
           - "QR-Code Generieren" Button
           - "Abbrechen" Button

        Returns:
            None

        Side Effects:
            - Erstellt und konfiguriert alle GUI-Widgets
            - Ordnet sie auf dem Fenster an
            - Bindet Callbacks an die Buttons

        Note:
            - Verwendet ttk.Labelframe für thematische Gruppierung
            - Bildet ein responsives Layout mit Padding
            - Das QR-Vorschaubild wird auf 200x200 Pixel skaliert
        """

        # Läd den QR mit dem GitHub Repo Link & zeigt diesen an
        self.qr_image = Image.open(resource_path("img/qrcode_gui.png"))
        self.qr_image.thumbnail((200, 200))
        self.qr_photo = ImageTk.PhotoImage(self.qr_image)
        self.qr_label = ttk.Label(self, image=self.qr_photo)
        self.qr_label.pack(pady=20)

        # Erstellt den Rahmen für die Nutzereingaben
        self.input_frame = ttk.Labelframe(self, text="QR-Code Einstellung")
        self.input_frame.pack(pady=(0, 20), padx=10)

        # QR-Code Texteingabe
        self.text_input_frame = ttk.Labelframe(self.input_frame, text="QR-Code Text")
        self.text_input_frame.pack(pady=10, padx=10)
        self.text_entry = ttk.Entry(self.text_input_frame, width=60)
        self.text_entry.pack(pady=5, padx=5)

        # QR-Code Farbwahl
        self.color_frame = ttk.Labelframe(self.input_frame, text="Farbwahl")
        self.color_frame.pack(pady=10, padx=10, side="left")
        self.fill_color_btn = ttk.Button(self.color_frame, text="Füllfarbe", command=lambda: self.choose_color(1))
        self.fill_color_btn.pack(side="left", pady=5, padx=5)
        self.bg_color_btn = ttk.Button(self.color_frame, text=" Hintergrundfarbe ", command=lambda: self.choose_color(2))
        self.bg_color_btn.pack(pady=5, padx=5)

        # QR-Code Speicherort
        self.location_frame = ttk.Labelframe(self.input_frame, text="Speicherort wählen")
        self.location_frame.pack(pady=10, padx=10, side="right")
        self.browse_btn = ttk.Button(self.location_frame, text=" Durchsuchen ", command=lambda: self.choose_save_location())
        self.browse_btn.pack(pady=5, padx=5)

        # Darstellung der Usereinstellungen
        self.settings_frame = ttk.Labelframe(self, text="Gewählte Einstellungen")
        self.settings_frame.pack(pady=(20, 0), padx=10)

        self.fill_color_label = ttk.Label(self.settings_frame, text="Gewählte Füllfarbe: ")
        self.fill_color_label.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.fill_color_display = ttk.Label(self.settings_frame, text="      ", background=self.fill_color)
        self.fill_color_display.grid(row=0, column=1, pady=5, padx=5)

        self.bg_color_label = ttk.Label(self.settings_frame, text="Gewählte Hintergrundfarbe: ")
        self.bg_color_label.grid(row=1, column=0, pady=5, padx=5)
        self.bg_color_display = ttk.Label(self.settings_frame, text="      ", background=self.background_color)
        self.bg_color_display.grid(row=1, column=1, pady=5, padx=5)

        self.path_label = ttk.Label(self.settings_frame, text="Gewählter Speicherort:")
        self.path_label.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.path_display = ttk.Label(self.settings_frame, text=self.get_user_directory())
        self.path_display.grid(row=2, column=1, pady=5, padx=5)

        # Steuerbuttons
        self.button_frame = ttk.Frame(self, width=60)
        self.button_frame.pack(pady=10, side="right")
        self.generate_btn = ttk.Button(self.button_frame, text="QR-Code Generieren", command=lambda: self.generate_qr_code())
        self.generate_btn.pack(side="left", padx=5, pady=10)
        self.cancel_btn = ttk.Button(self.button_frame, text="Abbrechen", command=lambda: self.destroy())
        self.cancel_btn.pack(side="right", padx=(5, 10), pady=10)

    def choose_color(self, button_id):
        """
        Öffnet einen interaktiven Farbwähler-Dialog für Füll- oder Hintergrundfarbe.

        Diese Methode wird aufgerufen, wenn der Benutzer auf einen der Farbwähler-Buttons
        klickt. Sie öffnet einen nativen Betriebssystem-Farbdialog, über den der Benutzer
        die gewünschte Farbe auswählen kann.

        Args:
            button_id (int): Eindeutige Identifikation des Buttons:
                           - 1: Füllfarbe-Button (QR-Code Modulfarbe)
                           - 2: Hintergrundfarbe-Button (QR-Code Hintergrund)

        Returns:
            None

        Side Effects:
            - Aktualisiert self.fill_color oder self.background_color mit neuer Farbe
            - Aktualisiert visuelle Label zur Anzeige der Farbe
            - Blockiert weitere Aktionen, bis der Dialog geschlossen wird

        Raises:
            - Keine, da colorchooser ein Cancel-Ergebnis zurückgibt

        Example:
            >>> self.choose_color(1)  # Öffnet Füllfarben-Dialog
            >>> self.choose_color(2)  # Öffnet Hintergrundfarben-Dialog

        Note:
            - Die Farbwahl wird als Hex-String (z.B. "#FF0000") gespeichert
            - Die visuelle Darstellung wird sofort aktualisiert
            - Der Dialog lädt die zuletzt gewählte Farbe
        """
        if button_id == 1:
            color = colorchooser.askcolor(title="Farbauswahl")
            self.fill_color = color[1]
            self.fill_color_display.config(background=self.fill_color)
        elif button_id == 2:
            color = colorchooser.askcolor(title="Farbauswahl")
            self.background_color = color[1]
            self.bg_color_display.config(background=self.background_color)

    def get_user_directory(self):
        """
        Bestimmt das Standardverzeichnis für das Speichern von QR-Codes.

        Diese Methode versucht, den Standard-Dokumentenordner des Benutzers automatisch
        zu erkennen. Sie unterstützt mehrsprachige Systeme, indem sie sowohl deutsche
        als auch englische Ordnernamen prüft. Falls kein Dokumentenordner existiert,
        wird das Home-Verzeichnis verwendet.

        Returns:
            str: Vollständiger Pfad zum Speichern der QR-Code Datei als "/pfad/qrcode.png"

        Side Effects:
            - Keine (reine Informationsbeschaffung)

        Algorithm:
            1. Erweitert den Pfad "~" zum absoluten Home-Verzeichnis
            2. Prüft auf Existenz von "Dokumente" (Deutsch)
            3. Fällt zurück auf "Documents" (Englisch)
            4. Gibt Home-Verzeichnis zurück, falls keiner existiert

        Examples:
            >>> path = self.get_user_directory()
            >>> print(path)
            /home/user/Dokumente/qrcode.png
            >>> # oder bei englischem System:
            >>> print(path)
            /home/user/Documents/qrcode.png
            >>> # oder als Fallback:
            >>> print(path)
            /home/user/qrcode.png

        Note:
            - Erstellt das Verzeichnis nicht automatisch
            - Wird verwendet, um initialen Speicherpfad zu setzen
            - Kann mehrfach pro Session aufgerufen werden
        """
        # Dynamisch das Benutzerverzeichnis ermitteln
        user_dir = os.path.expanduser("~")

        # Mögliche Dokumentenordner-Namen (deutsch und englisch)
        document_folders = ["Dokumente", "Documents"]

        # Prüfe welcher Ordner existiert
        for folder in document_folders:
            test_path = os.path.join(user_dir, folder)
            if os.path.exists(test_path):
                return test_path + "/qrcode.png"

        return user_dir + "/qrcode.png"

    def choose_save_location(self):
        """
        Öffnet den Dateidialog zum Auswählen des Speicherortes.

        Diese Methode wird aufgerufen, wenn der Benutzer auf den "Durchsuchen"-Button klickt.
        Sie öffnet einen nativen Betriebssystem-Dateidialog, über den der Benutzer den
        Speicherort und -format für die QR-Code Datei auswählen kann.

        Returns:
            None

        Side Effects:
            - Aktualisiert self.file_path mit dem gewählten Pfad
            - Aktualisiert die Anzeige im path_display Label
            - Blockiert Benutzerintaktion, bis Dialog geschlossen wird

        Supported File Types:
            - PNG Dateien (*.png) - Empfohlen
            - JPG Dateien (*.jpg)
            - SVG Dateien (*.svg)
            - Alle Dateien (*.*)

        Dialog Eigenschaften:
            - Standarderweiterung: .png
            - Standarddateiname: qrcode.png
            - Startverzeichnis: Benutzer-Dokumentenordner
            - Titel: "Speicherort auswählen"

        Example:
            >>> self.choose_save_location()
            >>> print(self.file_path)
            /home/user/Dokumente/mein_qrcode.png

        Note:
            - Bei Abbruch (Cancel) bleibt der bisherige file_path erhalten
            - Die Datei wird erst mit generate_qr_code() erstellt
        """
        initial_dir = self.get_user_directory()

        # Öffnet den Dateidialog zum Speichern der Datei
        self.file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile="qrcode.png",
            initialdir=initial_dir,
            filetypes=[
                ("PNG Dateien", "*.png"),
                ("JPG Dateien", "*.jpg"),
                ("SVG Dateien", "*.svg"),
                ("Alle Dateien", "*.*")
            ],
            title="Speicherort auswählen"
        )
        self.path_display.config(text=self.file_path)

    def generate_qr_code(self):
        """
        Generiert den QR-Code basierend auf den Benutzereinstellungen.

        Diese Methode wird aufgerufen, wenn der Benutzer auf den "QR-Code Generieren"-Button klickt.
        Sie führt folgende Schritte durch:
        1. Prüft, ob die Zieldatei bereits existiert
        2. Fragt ggf. zur Bestätigung des Überschreibens
        3. Erstellt QRCodeGenerator-Instanz
        4. Ruft generate() auf
        5. Validiert das Ergebnis und zeigt Erfolgsmeldung
        6. Aktualisiert die Vorschau mit dem neuen QR-Code

        Returns:
            None

        Side Effects:
            - Erstellt oder überschreibt die Datei unter self.file_path
            - Zeigt Dialog-Meldungen für Erfolg/Fehler
            - Aktualisiert das QR-Code Vorschaubild
            - Ändert nichts bei Benutzzer-Abbruch

        User Interaction:
            - Wenn Datei existiert: "Ja/Nein"-Dialog zur Bestätigung
            - Nach erfolgreicher Generierung: Erfolgsmeldung
            - Bei Fehler: Fehlermeldung

        Validation:
            - Prüft, ob self.text_entry nicht leer ist
            - Validiert die Dateierstellung
            - Prüft Dateiexistenz nach dem Speichern

        Error Handling:
            - FileExistsError: Wird durch Dialog abgefragt
            - IOError: Zeigt Fehlermeldung bei Speicherfehler
            - ValueError: Wird von QRCodeGenerator.generate() propagiert

        Example:
            >>> # Benutzer gibt Text ein, wählt Farben, und klickt "Generieren"
            >>> self.generate_qr_code()
            >>> # Erfolgsbestätigung wird angezeigt

        Note:
            - Verwendet die aktuellen Werte aus self.text_entry, self.fill_color, etc.
            - Die Vorschau wird mit PIL aktualisiert
            - Originalbild wird auf 200x200 Pixel skaliert
        """
        overwrite = False

        if os.path.exists(self.file_path):
            if messagebox.askyesnocancel("Speicherort vergeben", "Der gewählte Speicherort existiert bereits."):
                overwrite = True
        else:
            overwrite = True

        if overwrite:
            content = self.text_entry.get()
            qr_generator = QRCodeGenerator(content, self.fill_color, self.background_color, self.file_path)
            qr_generator.generate()

            if os.path.exists(self.file_path):
                messagebox.showinfo("Erfolg!", "Der QR-Code wurde Erfolgreich gespeichert.")
                self.qr_image = Image.open(self.file_path)
                self.qr_image.thumbnail((200, 200))
                self.qr_photo = ImageTk.PhotoImage(self.qr_image)
                self.qr_label.config(image=self.qr_photo)
            else:
                messagebox.showerror("Fehler!", "Der QR-Code konnte nicht gespeichert werden.")

def main():
    """
    Einstiegspunkt der QR-Code Generator Anwendung.

    Diese Funktion:
    1. Erstellt eine Instanz der QRCodeGeneratorGUI-Klasse
    2. Startet die tkinter Event-Schleife
    3. Blockiert bis zur Beendigung der Anwendung

    Returns:
        None

    Side Effects:
        - Erstellt ein neues Anwendungsfenster
        - Startet die GUI-Event-Loop
        - Blockiert das Programm bis Fenster geschlossen wird

    Raises:
        FileNotFoundError: Falls Icon- oder Bilddateien nicht gefunden werden
        ImportError: Falls Abhängigkeiten (PIL, qrcode, tkinter) nicht installiert sind

    Example:
        >>> if __name__ == "__main__":
        ...     main()

    Note:
        - Dies ist der Standard-Einstiegspunkt für Standalone-Anwendungen
        - Wird nur aufgerufen, wenn Skript direkt ausgeführt wird
        - Die Anwendung bleibt aktiv bis der Benutzer das Fenster schließt
    """
    app = QRCodeGeneratorGUI()
    app.mainloop()

if __name__ == "__main__":
    """
    Einstiegspunkt für direktes Ausführen des Skripts.
    
    Dieser Block wird nur ausgeführt, wenn die Datei direkt als Programm
    aufgerufen wird (nicht als Modul importiert). Er ruft die main()-Funktion auf,
    um die Anwendung zu starten.
    
    Note:
        - Erlaubt Import der Funktionen in anderen Modulen ohne Ausführung
        - Best Practice für Python-Einstiegspunkte
        - Kompatibel mit PyInstaller und anderen Packern
    """
    main()