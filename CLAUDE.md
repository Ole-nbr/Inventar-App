# Inventar-App

Web-App zur Verwaltung von Inventar mit Backend und Frontend.

## Stand

Das Projekt ist im Aufbau. docker-compose.yml, Makefile und die Pre-commit-Konfiguration kommen später, weil sie Backend und Frontend voraussetzen.

## Regeln

- Zu jeder Änderung gehört ein Issue und ein eigener Branch nach dem Muster `<issue-nummer>-kurzer-name`.
- `.env` wird nie committet. Neue Variablen kommen ohne echte Werte in `.env.example`.

## Git

- Keine AI-Attribution in Commit-Nachrichten oder PR-Beschreibungen:
  kein "Co-Authored-By: Claude", kein "Generated with Claude Code",
  kein "Claude-Session:"-Trailer.
- Commit-Nachrichten werden auf Englisch geschrieben.
