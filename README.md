# Inventar-App

Eine Web-App zur Verwaltung von Inventar.

## Lokale Entwicklung

Voraussetzungen: [Docker](https://docs.docker.com/get-docker/), [uv](https://docs.astral.sh/uv/)
und [Node.js](https://nodejs.org/) 24.

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
   uv run alembic upgrade head
   uv run fastapi dev app/main.py
   ```

   Healthcheck: <http://localhost:8000/api/v1/health>, mit Datenbank: <http://localhost:8000/api/v1/health/db>

4. Frontend starten (in `frontend/`, Backend sollte laufen):

   ```bash
   npm install
   npm run dev
   ```

   App: <http://localhost:5173>. Der Vite-Dev-Server leitet `/api` an das Backend auf Port 8000
   weiter, deshalb gibt es keine CORS-Probleme.

### Tests

Frontend (in `frontend/`): `npm test` startet Vitest im Watch-Modus, `npm run lint`,
`npm run format:check` und `npm run typecheck` prüfen Stil und Typen.

Backend:

Die Integrationstests laufen gegen eine eigene Datenbank `inventar_test`, damit eure
Entwicklungsdaten unberührt bleiben. Einmalig anlegen:

```bash
docker compose exec db createdb -U inventar inventar_test
```

Danach in `backend/`: `uv run pytest`. Eine andere Test-Datenbank lässt sich über
`TEST_DATABASE_URL` setzen.

### Migrationen

Schemaänderungen laufen über Alembic (in `backend/`):

```bash
uv run alembic revision --autogenerate -m "add items table"   # Entwurf erzeugen, immer prüfen
uv run alembic upgrade head                                     # anwenden
uv run alembic downgrade -1                                     # letzte Revision zurücknehmen
```

### API-Typen

Die TypeScript-Typen in `frontend/src/api/types.ts` werden aus der OpenAPI-Spec des Backends
erzeugt, nie von Hand bearbeitet. Nach Änderungen an Endpunkten oder Schemas bei laufendem
Backend (in `frontend/`) ausführen und die Datei im selben PR committen:

```bash
npm run generate:api
```

Datenbank stoppen mit `docker compose down` (Daten bleiben erhalten).
Zurücksetzen mit `docker compose down -v` (löscht alle Daten).
