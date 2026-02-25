# ------------------------------------------------------------------------------
# Projekt: BooktrackQR
# Modul: BuchverwaltungWidget (GUI Design & Logik)
# Autoren:
# - Harun: Dialoge (DeleteConfirmDialog, BookDialog) + Validierung
# - Batuhan: BuchverwaltungWidget (Layout, Tabelle, Filter, Bestand +/- , Aktionen)
# ------------------------------------------------------------------------------

import os
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QDialog, QFormLayout, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap


# ==============================================================================
# Harun: DeleteConfirmDialog
# Zweck: Bestätigungsdialog, damit man Bücher nicht aus Versehen löscht.
# ==============================================================================

class DeleteConfirmDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Fenster-Einstellungen
        self.setWindowTitle("Löschen bestätigen")
        self.setFixedSize(350, 180)
        self.setStyleSheet("background-color: #FFFFFF;")

        # Grundlayout im Dialog
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Hinweistext / Warnung
        self.label = QLabel("⚠️ Möchten Sie dieses Buch wirklich\nunwiderruflich löschen?")
        self.label.setFont(QFont("Open Sans", 11, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #333333; margin-bottom: 10px;")
        layout.addWidget(self.label)

        # Buttons: Abbrechen / Löschen
        btn_layout = QHBoxLayout()
        self.btn_no = QPushButton("Abbrechen")
        self.btn_yes = QPushButton("Löschen")

        # Styling der Buttons (Rot = gefährlich / Grau = neutral)
        style_yes = """
            QPushButton { background-color: #D32F2F; color: white; padding: 8px; border: 3px solid #D32F2F; border-radius: 6px; font-weight: bold; }
            QPushButton:hover { border: 3px solid #333333; }
            QPushButton:pressed { background-color: #444444; border: 3px solid #444444; }
        """
        style_no = """
            QPushButton { background-color: #E0E0E0; color: #333333; padding: 8px; border: 3px solid #E0E0E0; border-radius: 6px; font-weight: bold; }
            QPushButton:hover { border: 3px solid #333333; }
            QPushButton:pressed { background-color: #444444; border: 3px solid #444444; color: white; }
        """
        self.btn_yes.setStyleSheet(style_yes)
        self.btn_no.setStyleSheet(style_no)

        # Dialog-Ergebnis: accept() = OK / reject() = Abbrechen
        self.btn_yes.clicked.connect(self.accept)
        self.btn_no.clicked.connect(self.reject)

        btn_layout.addWidget(self.btn_no)
        btn_layout.addWidget(self.btn_yes)
        layout.addLayout(btn_layout)


# ==============================================================================
# Harun: BookDialog
# Zweck: Dialog zum "Buch hinzufügen" und "Buch bearbeiten"
# - Bei Bearbeiten ist ISBN read-only (damit Schlüssel nicht geändert wird).
# - validate_and_save() prüft Pflichtfelder + Bestand muss Zahl sein.
# ==============================================================================

class BookDialog(QDialog):
    def __init__(self, parent=None, book_data=None):
        super().__init__(parent)

        self.setWindowTitle("Neues Buch" if not book_data else "Buch bearbeiten")
        self.setFixedSize(420, 340)

        # Grund-Stylesheet für Dialog + Eingabefelder
        self.setStyleSheet("""
            QDialog { background-color: #FFFFFF; }
            QLabel { color: #333333; font-weight: bold; }
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px;
                color: #333333;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #5CB1D6; }
        """)

        layout = QVBoxLayout(self)

        # FormLayout -> Label links, Eingabefeld rechts
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Eingabefelder
        self.input_isbn = QLineEdit()
        self.input_isbn.setPlaceholderText("ISBN eingeben")

        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("Titel eingeben")

        self.input_publisher = QLineEdit()
        self.input_publisher.setPlaceholderText("Verlag eingeben")

        self.input_edition = QLineEdit()
        self.input_edition.setPlaceholderText("Auflage eingeben")

        self.input_stock = QLineEdit()
        self.input_stock.setPlaceholderText("Bestand (Zahl)")

        # Fehlermeldung (standardmäßig versteckt)
        self.error_label = QLabel("Bitte alle markierten Pflichtfelder (*) ausfüllen.")
        self.error_label.setStyleSheet("color: #D32F2F; font-size: 12px; font-style: italic; font-weight: normal;")
        self.error_label.hide()

        # Bearbeitungsmodus: bestehende Daten in Felder laden
        if book_data:
            # book_data: (isbn, titel, verlag, auflage, bestand)
            self.input_isbn.setText(book_data[0])
            self.input_isbn.setReadOnly(True)  # ISBN bleibt fix
            self.input_isbn.setStyleSheet("background:#F3F3F3;")
            self.input_title.setText(book_data[1])
            self.input_publisher.setText(book_data[2])
            self.input_edition.setText(book_data[3])
            self.input_stock.setText(str(book_data[4]))

        # Pflichtfelder mit * markiert
        form_layout.addRow(QLabel("ISBN*:"), self.input_isbn)
        form_layout.addRow(QLabel("Titel*:"), self.input_title)
        form_layout.addRow(QLabel("Verlag*:"), self.input_publisher)
        form_layout.addRow(QLabel("Auflage*:"), self.input_edition)
        form_layout.addRow(QLabel("Bestand*:"), self.input_stock)

        layout.addLayout(form_layout)
        layout.addWidget(self.error_label)
        layout.addStretch()

        # Aktionsbuttons: Abbrechen / Speichern
        btn_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Abbrechen")
        self.btn_save = QPushButton("Speichern")

        # Button-Styles (Grau / Blau)
        self.btn_cancel.setStyleSheet("""
            QPushButton { background-color: #E0E0E0; color: #333333; padding: 7px 17px; border: 3px solid #E0E0E0; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { border: 3px solid #333333; }
            QPushButton:pressed { background-color: #444444; border: 3px solid #444444; color: white; }
        """)
        self.btn_save.setStyleSheet("""
            QPushButton { background-color: #5CB1D6; color: white; padding: 7px 17px; border: 3px solid #5CB1D6; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { border: 3px solid #333333; }
            QPushButton:pressed { background-color: #444444; border: 3px solid #444444; }
        """)

        # Dialog-Steuerung
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.validate_and_save)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

    def validate_and_save(self):
        """
        Validierung:
        - ISBN, Titel, Verlag, Auflage dürfen nicht leer sein
        - Bestand muss eine Zahl sein
        - Bei Fehler: rote Rahmen + Fehlermeldung anzeigen
        """
        isbn = self.input_isbn.text().strip()
        t = self.input_title.text().strip()
        p = self.input_publisher.text().strip()
        e = self.input_edition.text().strip()
        s = self.input_stock.text().strip()

        # Reset Rahmen (falls vorher Fehler)
        self.input_isbn.setStyleSheet("")
        self.input_title.setStyleSheet("")
        self.input_publisher.setStyleSheet("")
        self.input_edition.setStyleSheet("")
        self.input_stock.setStyleSheet("")

        ok = True

        if not isbn:
            self.input_isbn.setStyleSheet("border: 2px solid #D32F2F;")
            ok = False
        if not t:
            self.input_title.setStyleSheet("border: 2px solid #D32F2F;")
            ok = False
        if not p:
            self.input_publisher.setStyleSheet("border: 2px solid #D32F2F;")
            ok = False
        if not e:
            self.input_edition.setStyleSheet("border: 2px solid #D32F2F;")
            ok = False
        if not s or not s.isdigit():
            self.input_stock.setStyleSheet("border: 2px solid #D32F2F;")
            ok = False

        if not ok:
            self.error_label.show()
            return

        self.accept()


# ==============================================================================
# Batuhan: BuchverwaltungWidget
# Zweck: Hauptseite der Buchverwaltung
# - Header (Titel + Logo), Breadcrumbs, Titel
# - Actionbar: Suche + Filter-Dropdown + Button "Buch hinzufügen"
# - Tabelle mit Bestand (+/-) und Aktionen (Bearbeiten/Löschen)
# - Filterlogik (Suche + Verlag-Filter)
# ==============================================================================

class BuchverwaltungWidget(QWidget):
    def __init__(self, parent=None):
        super(BuchverwaltungWidget, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #FFFFFF;")

        # ---------------------------
        # Layout-Grundstruktur
        # ---------------------------
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 50)
        main_layout.setSpacing(15)

        # ================= HEADER =================
        header_layout = QHBoxLayout()

        dummy_left = QWidget()
        dummy_left.setFixedWidth(200)  # sorgt dafür, dass Titel mittig bleibt
        header_layout.addWidget(dummy_left)

        title_label = QLabel("BooktrackQR")
        title_label.setFont(QFont("Open Sans", 50, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #333333; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)

        # Logo oben rechts
        logo_label = QLabel()
        logo_path = self.get_image_path("technikerschule_logo.png")
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            logo_label.setPixmap(
                pixmap.scaled(200, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            )
        logo_label.setFixedWidth(200)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        header_layout.addWidget(logo_label)

        main_layout.addLayout(header_layout)

        # ================= BREADCRUMBS =================
        self.back_label = QLabel("Startseite > Hauptmenü > Buchverwaltung")
        self.back_label.setStyleSheet("color: #666666; font-style: italic; margin-left: 10px;")
        main_layout.addWidget(self.back_label)

        # ================= TITEL =================
        page_title = QLabel("Bücherverwaltung")
        page_title.setFont(QFont("Open Sans", 24, QFont.Weight.Bold))
        page_title.setStyleSheet("color: #5CB1D6; margin-left: 10px;")
        main_layout.addWidget(page_title)

        # ================= ACTION BAR =================
        # Hier: Suche + Filter-Dropdown + Button "Buch hinzufügen"
        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(10, 10, 10, 5)
        action_layout.setSpacing(15)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Suche...")
        self.search_input.setFixedWidth(400)
        self.search_input.setStyleSheet(
            "padding: 10px; border: 1px solid #CCCCCC; border-radius: 6px; background-color: #FFFFFF; color: #333333; font-size: 14px;"
        )
        action_layout.addWidget(self.search_input)

        # Filter-Dropdown (Verlag)
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Filter: Alle Verlage"])  # dynamisch ergänzt
        self.filter_combo.setFixedWidth(200)
        self.filter_combo.setStyleSheet(
            "padding: 10px; border: 1px solid #CCCCCC; border-radius: 6px; background-color: #FFFFFF; color: #333333; font-size: 14px;"
        )
        action_layout.addWidget(self.filter_combo)

        action_layout.addStretch()

        btn_add = QPushButton("➕ Buch hinzufügen")
        btn_add.setStyleSheet("""
            QPushButton { background-color: #5CB1D6; color: white; padding: 10px 25px; border: 3px solid #5CB1D6; border-radius: 6px; font-weight: bold; font-size: 14px; }
            QPushButton:hover { border: 3px solid #333333; }
            QPushButton:pressed { background-color: #444444; border: 3px solid #444444; }
        """)
        btn_add.clicked.connect(self.open_book_dialog)
        action_layout.addWidget(btn_add)

        main_layout.addLayout(action_layout)

        # ================= TABLE =================
        # Spalten: ISBN, Titel, Verlag, Auflage, Bestand(+/-), Aktionen(Edit/Delete)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ISBN", "Titel", "Verlag", "Auflage", "Bestand", "Aktionen"])
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)

        self.table.setStyleSheet("""
            QTableWidget { 
                background-color: #FFFFFF; alternate-background-color: #F9F9F9; border: 1px solid #E0E0E0; 
                border-radius: 8px; gridline-color: #EDEDED; font-size: 15px; color: #333333; 
            }
            QHeaderView::section { 
                background-color: #F0F0F0; color: #000000; font-weight: bold; 
                border: none; border-bottom: 3px solid #5CB1D6; padding: 12px; 
            }
        """)
        self.table.verticalHeader().setVisible(False)

        # Spaltenbreiten wie in Schülerverwaltung: gemischt Fixed/Stretch
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)   # ISBN
        self.table.setColumnWidth(0, 160)

        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Titel
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Verlag

        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)   # Auflage
        self.table.setColumnWidth(3, 120)

        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)   # Bestand
        self.table.setColumnWidth(4, 180)

        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)   # Aktionen
        self.table.setColumnWidth(5, 150)

        main_layout.addWidget(self.table)

        # ================= DUMMY DATEN =================
        # Datenformat: (ISBN, Titel, Verlag, Auflage, Bestand)
        self.dummy_books = [
            ("9783123456789", "Mathe 5", "Cornelsen", "2023", 150),
            ("9783120000001", "Deutsch 6", "Klett", "2022", 85),
        ]
        for i in range(3, 30):
            self.dummy_books.append((
                f"97831200000{i:02d}",
                f"Testbuch{i}",
                "Cornelsen" if i % 2 == 0 else "Klett",
                "2021",
                10 + i
            ))

        # Filterwerte (Verlage) aus Daten generieren
        self._refresh_filter_values()

        # Tabelle initial befüllen
        self.load_table_data(self.dummy_books)

        # Signale: bei Änderungen sofort filtern
        self.search_input.textChanged.connect(self.filter_table)
        self.filter_combo.currentTextChanged.connect(self.filter_table)

        # ================= FOOTER =================
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()

        # Wichtig: btn_back wird vom CentralWidget (StackedLayout) verbunden
        self.btn_back = QPushButton("⬅ Zurück zum Hauptmenü")
        self.btn_back.setStyleSheet("""
            QPushButton { background-color: #5CB1D6; color: white; padding: 12px 25px; border: 3px solid #5CB1D6; border-radius: 6px; font-weight: bold; font-size: 13px; }
            QPushButton:hover { border: 3px solid #333333; }
            QPushButton:pressed { background-color: #444444; border: 3px solid #444444; }
        """)
        footer_layout.addWidget(self.btn_back)
        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)

    # --------------------------------------------------------------------------
    # Batuhan: Helper
    # Zweck: Image-Pfad wie im restlichen Projekt
    # --------------------------------------------------------------------------
    def get_image_path(self, filename):
        return os.path.join(os.path.dirname(__file__), "..", "pic", filename)

    # --------------------------------------------------------------------------
    # Batuhan: Filter-Dropdown dynamisch befüllen
    # Zweck: Dropdown zeigt alle vorhandenen Verlage an
    # --------------------------------------------------------------------------
    def _refresh_filter_values(self):
        publishers = sorted({b[2] for b in self.dummy_books})

        current = self.filter_combo.currentText()
        self.filter_combo.blockSignals(True)
        self.filter_combo.clear()
        self.filter_combo.addItem("Filter: Alle Verlage")
        for p in publishers:
            self.filter_combo.addItem(p)

        if current in publishers:
            self.filter_combo.setCurrentText(current)
        else:
            self.filter_combo.setCurrentIndex(0)
        self.filter_combo.blockSignals(False)

    # --------------------------------------------------------------------------
    # Batuhan: Tabelle befüllen
    # - 0..3 sind normale Zellen (ISBN, Titel, Verlag, Auflage)
    # - 4 ist ein Widget (Bestand: – Zahl +)
    # - 5 ist ein Widget (Aktionen: ✏️ / 🗑️)
    # --------------------------------------------------------------------------
    def load_table_data(self, data_list):
        self.table.setRowCount(len(data_list))

        for row, book in enumerate(data_list):
            # book: (isbn, titel, verlag, auflage, bestand)
            for col in range(4):
                item = QTableWidgetItem(str(book[col]))
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)  # nicht editierbar
                if col in [0, 3]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

            # Bestand-Widget in Spalte 4
            self._set_stock_widget(row, book[0], int(book[4]))

            # Aktionen-Widget in Spalte 5
            self._set_actions_widget(row, book[0])

    # --------------------------------------------------------------------------
    # Batuhan: Bestand-Widget (– Zahl +)
    # - Klick auf minus: Bestand -1 (nicht unter 0)
    # - Klick auf plus: Bestand +1
    # --------------------------------------------------------------------------
    def _set_stock_widget(self, row, isbn, stock):
        bg_color = "#F9F9F9" if row % 2 != 0 else "#FFFFFF"

        stock_widget = QWidget()
        stock_widget.setStyleSheet(f"background-color: {bg_color};")

        layout = QHBoxLayout(stock_widget)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_minus = QPushButton("–")
        btn_minus.setFixedSize(35, 35)
        btn_minus.setStyleSheet("""
            QPushButton { background: #E0E0E0; border: none; font-size: 18px; font-weight: bold; border-radius: 6px; }
            QPushButton:hover { border: 2px solid #333333; }
            QPushButton:pressed { background: #444444; color: white; }
        """)

        lbl_stock = QLabel(str(stock))
        lbl_stock.setFixedWidth(50)
        lbl_stock.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_stock.setStyleSheet("font-size: 15px; font-weight: bold; color: #333333; background: transparent;")

        btn_plus = QPushButton("+")
        btn_plus.setFixedSize(35, 35)
        btn_plus.setStyleSheet("""
            QPushButton { background: #E0E0E0; border: none; font-size: 18px; font-weight: bold; border-radius: 6px; }
            QPushButton:hover { border: 2px solid #333333; }
            QPushButton:pressed { background: #444444; color: white; }
        """)

        # Signal -> ruft change_stock() auf
        btn_minus.clicked.connect(lambda ch, x=isbn: self.change_stock(x, -1))
        btn_plus.clicked.connect(lambda ch, x=isbn: self.change_stock(x, +1))

        layout.addWidget(btn_minus)
        layout.addWidget(lbl_stock)
        layout.addWidget(btn_plus)

        self.table.setCellWidget(row, 4, stock_widget)

    # --------------------------------------------------------------------------
    # Batuhan: Aktionen-Widget (Bearbeiten/Löschen)
    # - ✏️ öffnet Bearbeiten-Dialog
    # - 🗑️ öffnet DeleteConfirmDialog
    # --------------------------------------------------------------------------
    def _set_actions_widget(self, row, isbn):
        bg_color = "#F9F9F9" if row % 2 != 0 else "#FFFFFF"

        action_widget = QWidget()
        action_widget.setStyleSheet(f"background-color: {bg_color};")

        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(5, 0, 5, 0)
        action_layout.setSpacing(15)
        action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_edit = QPushButton("✏️")
        btn_edit.setFixedSize(45, 45)
        btn_edit.setStyleSheet(
            "QPushButton { background: transparent; border: none; font-size: 20px; }"
            "QPushButton:hover { background-color: #E0E0E0; border-radius: 8px; }"
        )
        btn_edit.clicked.connect(lambda ch, x=isbn: self.edit_book(x))

        btn_delete = QPushButton("🗑️")
        btn_delete.setFixedSize(45, 45)
        btn_delete.setStyleSheet(
            "QPushButton { background: transparent; border: none; font-size: 20px; }"
            "QPushButton:hover { background-color: #FFCDD2; border-radius: 8px; }"
        )
        btn_delete.clicked.connect(lambda ch, x=isbn: self.delete_book(x))

        action_layout.addWidget(btn_edit)
        action_layout.addWidget(btn_delete)

        self.table.setCellWidget(row, 5, action_widget)

    # --------------------------------------------------------------------------
    # Batuhan: "Buch hinzufügen" -> Dialog öffnen -> Daten hinzufügen
    # --------------------------------------------------------------------------
    def open_book_dialog(self):
        d = BookDialog(self)
        if d.exec() == QDialog.DialogCode.Accepted:
            isbn = d.input_isbn.text().strip()

            # ISBN muss eindeutig sein
            if any(b[0] == isbn for b in self.dummy_books):
                # quick & dirty: doppelte ISBN ignorieren
                return

            self.dummy_books.append((
                isbn,
                d.input_title.text().strip(),
                d.input_publisher.text().strip(),
                d.input_edition.text().strip(),
                int(d.input_stock.text().strip())
            ))

            # Filter aktualisieren + Tabelle neu laden
            self._refresh_filter_values()
            self.filter_table()

    # --------------------------------------------------------------------------
    # Batuhan: Bearbeiten -> Dialog öffnen -> Datensatz überschreiben
    # --------------------------------------------------------------------------
    def edit_book(self, isbn):
        for i, b in enumerate(self.dummy_books):
            if b[0] == isbn:
                d = BookDialog(self, book_data=b)
                if d.exec() == QDialog.DialogCode.Accepted:
                    self.dummy_books[i] = (
                        isbn,
                        d.input_title.text().strip(),
                        d.input_publisher.text().strip(),
                        d.input_edition.text().strip(),
                        int(d.input_stock.text().strip())
                    )
                    self._refresh_filter_values()
                    self.filter_table()
                break

    # --------------------------------------------------------------------------
    # Batuhan: Löschen -> Bestätigungsdialog -> aus Liste entfernen
    # --------------------------------------------------------------------------
    def delete_book(self, isbn):
        confirm = DeleteConfirmDialog(self)
        if confirm.exec() == QDialog.DialogCode.Accepted:
            self.dummy_books = [b for b in self.dummy_books if b[0] != isbn]
            self._refresh_filter_values()
            self.filter_table()

    # --------------------------------------------------------------------------
    # Batuhan: Bestand ändern (plus/minus)
    # - passt Wert im Datensatz an
    # - läd danach gefilterte Tabelle neu
    # --------------------------------------------------------------------------
    def change_stock(self, isbn, delta):
        for i, b in enumerate(self.dummy_books):
            if b[0] == isbn:
                new_stock = max(0, int(b[4]) + delta)
                self.dummy_books[i] = (b[0], b[1], b[2], b[3], new_stock)
                break
        self.filter_table()

    # --------------------------------------------------------------------------
    # Batuhan: Filterlogik
    # - txt: Suchtext (sucht in ISBN, Titel, Verlag, Auflage)
    # - f: Verlag-Filter aus Dropdown
    # - Ergebnis -> load_table_data()
    # --------------------------------------------------------------------------
    def filter_table(self):
        txt = self.search_input.text().lower().strip()
        f = self.filter_combo.currentText()

        filtered = []
        for b in self.dummy_books:
            match_text = (
                txt in b[0].lower()
                or txt in b[1].lower()
                or txt in b[2].lower()
                or txt in b[3].lower()
            )
            match_filter = (f == "Filter: Alle Verlage" or f == b[2])

            if match_text and match_filter:
                filtered.append(b)

        self.load_table_data(filtered)