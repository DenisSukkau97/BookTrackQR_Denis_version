from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from CentralWidget import CentralWidget
from Schuelerverwaltung import SchuelerverwaltungWidget # <-- Hier ist der Name angepasst!

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("BooktrackQR")
        self.setMinimumSize(900, 700)
        self.setStyleSheet("QWidget { background-color: white; }")

        # 1. Den "Kartenstapel" erstellen
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # 2. Deine erstellten Bildschirme laden
        self.main_menu_widget = CentralWidget()
        self.schueler_widget = SchuelerverwaltungWidget()

        # 3. Bildschirme zum Stapel hinzufügen
        self.stacked_widget.addWidget(self.main_menu_widget)
        self.stacked_widget.addWidget(self.schueler_widget)

        # 4. Den Button aus dem Hauptmenü mit der Wechsel-Funktion verbinden
        self.main_menu_widget.btn_schueler.clicked.connect(self.zeige_schuelerverwaltung)

    def zeige_schuelerverwaltung(self):
        """Wechselt zur Schülerverwaltung (Index 1)"""
        self.stacked_widget.setCurrentIndex(1)

    def zeige_hauptmenue(self):
        """Wechselt zurück zum Hauptmenü (Index 0)"""
        self.stacked_widget.setCurrentIndex(0)