# Phase 5 – DMG-Vorbereitung für interne Testverteilung

## Ziel
Nach erfolgreichem `.app`-Build (Phase 4) soll die Verteilung benutzerfreundlicher werden.
Dazu wird eine erste, einfache `.dmg`-Lösung vorbereitet – **nur für interne Tests**,
ohne App Store, Signing oder Notarization.

## Warum jetzt `.dmg`?
- Die `.app` funktioniert bereits.
- Ein `.dmg` ist für Teammitglieder der typische macOS-Installationsweg.
- Der Test-Build wird einfacher verteilt, ohne ZIP-Handling.

## Ausgangsbasis
- Vorhandene App: `dist/BooktrackQR.app`
- ZIP-Testverteilung war bereits erfolgreich.

## Voraussetzungen
- macOS-System
- `dist/BooktrackQR.app` existiert (Build abgeschlossen)
- Kein Signing / keine Notarization (explizit ausgeschlossen)

## Externe `.env`-Strategie (unverändert)
- `.env` wird **nicht** in die `.dmg` eingebunden.
- `.env` wird **nicht** im Repository gespeichert.
- Nutzer müssen die Datei manuell anlegen:
  - `~/Library/Application Support/BooktrackQR/.env`
- Ohne `.env` ist kein erfolgreicher Start möglich.
- Das ist eine bewusste Sicherheitsentscheidung.

## Nutzung für Teammitglieder (Ablauf)
1. `.dmg` öffnen.
2. `BooktrackQR.app` nach `Applications` ziehen.
3. Ordner anlegen:
   - `~/Library/Application Support/BooktrackQR`
4. `.env` dort ablegen:
   - `~/Library/Application Support/BooktrackQR/.env`
5. App starten.

## Typische Einschränkungen ohne Signing/Notarization
- macOS kann beim ersten Start warnen (Gatekeeper).
- „App stammt von einem nicht verifizierten Entwickler“ ist erwartbar.
- Nutzer müssen das manuell freigeben (Systemeinstellungen → Datenschutz/Sicherheit).

## Minimaler DMG-Erstellungsweg (nicht ausführen)
Es wird ein einfacher, teamtauglicher Weg dokumentiert.
Grundlage ist die existierende `dist/BooktrackQR.app`.

Beispiel mit `hdiutil`:
```bash
cd <lokaler-repo-ordner>
./scripts/create_dmg.sh
```

## Was jetzt testbar ist
- `.dmg`-Verteilung an Teammitglieder
- Installation per Drag & Drop
- Start der App außerhalb des Projektordners
- Externe `.env`-Strategie

## Nicht Teil der finalen Lösung
- Keine finale `.dmg`-Optik (Hintergrundbild, Icon-Layout)
- Kein Signing / keine Notarization
- Kein App-Store-Workflow
- Keine automatisierte Release-Pipeline

## Abschluss (Phase 5)
Mit dieser Vorbereitung kann die `.dmg`-Erstellung kontrolliert getestet werden,
ohne die App-Logik zu ändern.
