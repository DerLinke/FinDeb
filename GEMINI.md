# `findeb` – Gemini CLI Context

Dieses Projekt ist eine Kooperation zwischen Dan und der Gemini CLI.

## Projektziel
Ein universelles Tool zur Suche und Installation von Paketen unter Debian-basierten Systemen, das die Grenzen zwischen Standard-Repos (`apt`), Drittanbieter-Repos (`extrepo`) und GitHub-Releases (`deb-get`) aufhebt.

## Entwicklungskonventionen
- **Sprache:** Python 3.x
- **UI-Libraries:** `rich` (Tabellen), `questionary` (Interaktive Menüs).
- **Logik:**
  - Jede Paketquelle (`apt`, `extrepo`, etc.) erhält ein eigenes Modul in `sources/`.
  - Suchergebnisse werden in einem einheitlichen Objektmodell gespeichert.
  - Priorisierung der neuesten Version (Semantic Versioning).
  - Automatisierung von `sudo`-Befehlsketten (besonders bei `extrepo`).

## Befehle
- `findeb <query>`: Sucht nach Paketen.
- `findeb --setup`: Initialisiert das Tool und prüft Abhängigkeiten.
- `findeb --refresh`: Aktualisiert den lokalen Cache.
