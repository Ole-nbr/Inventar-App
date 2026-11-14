# Inventar-App

Eine Web-App zur Verwaltung von Inventar.

## Lokale Entwicklung

Voraussetzungen: [Docker](https://docs.docker.com/get-docker/) und [uv](https://docs.astral.sh/uv/).

1. Umgebungsvariablen anlegen (im Root) und bei Bedarf anpassen:

   ```bash
   cp .env.example .env
   ```

2. Datenbank starten und prüfen, ob sie `healthy` ist:

   ```bash
   docker compose up -d db
   docker compose ps
   ```

3. Backend starten (in `backend/`):

   ```bash
   uv sync
   uv run fastapi dev app/main.py
   ```

   Healthcheck: <http://localhost:8000/api/v1/health>

Datenbank stoppen mit `docker compose down` (Daten bleiben erhalten).
Zurücksetzen mit `docker compose down -v` (löscht alle Daten).
