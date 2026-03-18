# Phase 4 – macOS Test-Build Dokumentation (BooktrackQR)

## 1. Ausgangslage vor Phase 4
- Analyse und Vorarbeiten aus Phase 1–3 waren abgeschlossen.
- Ressourcenpfade und Schreibpfade waren bundling-fähig vorbereitet.
- QR-Logik war bereits überarbeitet (Payload/Image/Workflow getrennt).
- Druckfunktion war bewusst nur Stub.
- `.env` sollte extern liegen und nicht im Repository oder Bundle sein.

## 2. Ziel von Phase 4
- Erster echter Test-Build als macOS `.app`
- Noch keine `.dmg`
- Kein Signing
- Keine Notarization

## 3. Vorbereitung des Build-Tests
- Wechsel in den Projektordner.
- Python-Version geprüft.
- `pyinstaller` war zunächst nicht installiert.
- Problem mit „externally managed environment“.
- Deshalb lokale `.venv` erstellt und aktiviert.
- PyInstaller in `.venv` installiert.
- Verwendete Versionen:
  - Python 3.14.3
  - PyInstaller 6.19.0

## 4. Verwendeter Build-Befehl
```bash
pyinstaller \
  --windowed \
  --name BooktrackQR \
  --paths src \
  --add-data "pic:pic" \
  src/main.py
```

Begründung:
- `src/main.py` ist der zentrale Einstiegspunkt der App.
- `pic/` enthält UI-Bilder/Icons und muss gebundelt werden.
- `.env` wurde bewusst **nicht** gebundelt (Sicherheitskonzept: extern).

## 5. Ergebnis des ersten Build-Laufs
- Build lief erfolgreich durch.
- `BooktrackQR.app` wurde erstellt.
- Speicherort: `dist/BooktrackQR.app`
- Keine fatalen Build-Fehler.
- Erster echter Erfolgsnachweis für den `.app`-Build.

## 6. Erster App-Start
- App wurde gestartet.
- Es erschien eine Fehlermeldung wegen fehlender `.env`.
- Das war erwartbar und korrekt.
- Dadurch wurde bestätigt, dass die externe `.env`-Strategie funktioniert.

## 7. Erstellung der externen `.env`
- Ordner wurde manuell angelegt:
  - `~/Library/Application Support/BooktrackQR`
- `.env` wurde dort erstellt.
- Format wurde korrigiert: keine Leerzeichen um `=`.

Beispielinhalt:
```
DB_HOST=192.168.10.195
DB_PORT=3306
DB_NAME=booksdb
DB_USER=booksuser
DB_PASSWORD=Fswi-2!
DB_CONNECT_TIMEOUT=20
```

Warum dieses Format wichtig ist:
- Die ENV-Loader erwarten exakte `KEY=VALUE` Paare ohne Leerzeichen.
- Verhindert Fehlinterpretationen beim Laden.

Warum `.env` extern gehalten wird:
- Keine Zugangsdaten im Repository.
- Keine Zugangsdaten im Bundle.
- Bewusste Sicherheitsentscheidung.

## 8. Erfolgreicher Start nach `.env`
- App startete danach erfolgreich.
- GUI funktionierte.
- Test-Build war funktional erfolgreich.

## 9. Realitätsnaher Test
- `.app` wurde auf den Desktop verschoben.
- Start vom Desktop funktionierte.
- Dadurch wurde bestätigt, dass die App auch außerhalb des Projektordners läuft.
- `open dist/BooktrackQR.app` schlug danach nur wegen des geänderten Speicherorts fehl.
- `open ~/Desktop/BooktrackQR.app` funktionierte.

## 10. Rückverschiebung und Alias
- `.app` wurde zurück nach `dist/` verschoben.
- Auf dem Desktop wurde stattdessen ein Alias/Symlink verwendet.

## 11. ZIP-Erstellung
- Die `.app` wurde in `dist/` als ZIP verpackt.
- Verwendeter Befehl:
```bash
cd dist
zip -r BooktrackQR.zip BooktrackQR.app
```

## 12. ZIP-Test
- ZIP wurde in einen separaten Testordner entpackt.
- Die entpackte `.app` wurde gestartet.
- Auch dieser Test war erfolgreich.

Beispielablauf:
```bash
cd ..
unzip dist/BooktrackQR.zip -d test_install
open test_install/BooktrackQR.app
```

## 13. Bewertung des aktuellen Standes
- `.app` Build funktioniert.
- `.app` startet erfolgreich.
- `.env` Sicherheitskonzept funktioniert.
- App läuft außerhalb des Projektordners.
- ZIP-Testpaket funktioniert.
- Interne Testverteilung ist grundsätzlich möglich.
- Phase 4 gilt damit als erfolgreich abgeschlossen.

## 14. Noch nicht gelöst
- Noch keine `.dmg`.
- Kein Signing.
- Keine Notarization.
- Keine finale Verteilungslösung.
- `.env` muss manuell erstellt werden.
- Drucklogik ist weiterhin nur Stub.
- QR-Scanner bleibt nachrangig.

## 15. Nächste Schritte
- Phase-4-Dokumentation abschließen.
- Danach `.dmg` als nächster Verteilungsschritt.
- Optional weitere Team-Tests.
- Später Verbesserungen an Deployment und Error Handling.
