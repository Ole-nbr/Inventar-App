# CLAUDE.md – Inventar-App

Diese Datei gibt Claude Code den Kontext für dieses Repository. Lies sie vor jeder Aufgabe.

## Projekt

Die Inventar-App soll eine Web-App zur Inventarverwaltung werden, entwickelt von zwei
Studierenden der Wirtschaftsinformatik. Welche Funktionen genau hinzukommen, ist noch offen und
wird Schritt für Schritt über Issues festgelegt. Sauberkeit, Lesbarkeit und eine nachvollziehbare
Git-Historie sind wichtiger als Feature-Menge.

- Sprache im Code (Bezeichner, Kommentare, Commits, PR-Titel): **Englisch**
- Sprache in Gesprächen mit uns: **Deutsch**

## Tech-Stack

| Bereich   | Technologie |
|-----------|-------------|
| Backend   | Python, FastAPI, Pydantic, SQLAlchemy, Alembic |
| Datenbank | PostgreSQL |
| Frontend  | React, TypeScript, Vite, TanStack Query, Tailwind CSS |
| Tooling   | uv, Ruff, mypy, pytest · ESLint, Prettier, Vitest |
| Infra     | Docker Compose, GitHub Actions |

## Repository-Struktur

| Ordner      | Inhalt |
|-------------|--------|
| `backend/`  | FastAPI-App (`app/`, `alembic/`, `tests/`) |
| `frontend/` | React-App (`src/features/…`) |
| `docs/`     | Dokumentation, ADRs in `docs/adr/` |
| `.github/`  | CI-Workflows, Issue- und PR-Vorlagen |

Projektweite Konfiguration (`.editorconfig`, `.gitattributes`, `.gitignore`, `.env.example`)
liegt im Root.

## Wichtige Befehle

Gelten, sobald das jeweilige Tooling eingerichtet ist. Existiert eine Datei wie `Makefile`
oder `docker-compose.yml` noch nicht, den Befehl nicht ausführen, sondern darauf hinweisen.

```bash
make dev            # docker compose up – DB, Backend (:8000), Frontend (:5173)
make test           # alle Tests (Backend + Frontend)
make lint           # Ruff, mypy, ESLint, tsc

# Backend (in backend/)
uv run pytest
uv run ruff check . && uv run ruff format .
uv run mypy app tests
uv run alembic revision --autogenerate -m "<beschreibung>"
uv run alembic upgrade head

# Frontend (in frontend/)
npm run dev
npm run test
npm run lint
npm run generate:api   # API-Typen aus OpenAPI-Spec erzeugen
```

## Architekturregeln Backend

Schichten: `api/v1/routes` → `services` → `repositories` → `models`.
Jede Schicht ruft nur die direkt darunter liegende auf.

- **Routes**: nur HTTP – Request entgegennehmen, Service aufrufen, Schema zurückgeben. Keine Logik, keine Queries.
- **Services**: Geschäftslogik. Werfen eigene Exceptions aus `app/core/exceptions.py`, niemals `HTTPException`.
- **Repositories**: einziger Ort mit SQLAlchemy-Queries. Keine Geschäftslogik.
- **Schemas** (Pydantic): getrennt nach `XCreate`, `XUpdate`, `XRead`. Models nie direkt zurückgeben.
- Konfiguration nur über `app/core/config.py` (Settings aus `.env`), keine hartkodierten Werte.
- Jede Modelländerung braucht eine Alembic-Migration. Kein `Base.metadata.create_all()`.
- Falls Lagerbestände verwaltet werden: Bestand nie direkt überschreiben, sondern über
  Bewegungsbuchungen (z. B. `stock_movements`) ändern, damit jede Änderung nachvollziehbar bleibt.
- Alle Endpunkte unter `/api/v1/`, mit Typannotationen und `response_model`.

## Architekturregeln Frontend

- Feature-basierte Ordner: `src/features/<feature>/{components,hooks,pages}`.
- Serverdaten nur über TanStack-Query-Hooks laden, kein `fetch` in Komponenten.
- API-Typen werden generiert (`src/api/types.ts`), nicht von Hand geschrieben.
- `src/components/ui/` enthält nur generische Komponenten ohne Fachlogik.
- Kein `any` in TypeScript.

## Code-Stil

- Python: Ruff-Formatierung, vollständige Typannotationen, Docstrings für öffentliche Services.
- TypeScript: Prettier, funktionale Komponenten, benannte Exporte.
- Kleine, fokussierte Funktionen; sprechende Namen statt Kommentare.
- Einrückung und Zeilenenden regeln `.editorconfig` und `.gitattributes` (LF).

## Tests

- Neue Funktionalität kommt immer mit Tests.
- Backend: `tests/unit/` für Services, `tests/integration/` für Endpunkte gegen eine Test-Datenbank.
- Ziel: ≥ 80 % Testabdeckung in `backend/app/services/`.
- Vor jedem Abschluss einer Aufgabe: Lint und Tests ausführen und Fehler beheben.

## Git-Workflow

- `main` ist geschützt; Änderungen nur über Pull Requests mit Review und grüner CI.
- Zu jeder Änderung gehört ein **Issue** und ein eigener **Branch**.
- Branch-Namen: `<issue-nummer>-kurzer-name`, z. B. `1-projektstruktur`, `12-item-crud`.
- Merge per **Squash**: Auf `main` landet ein Commit pro PR, mit dem PR-Titel als Message.
- `.env` wird nie committet. Neue Variablen kommen ohne echte Werte in `.env.example`.

### Commit- und PR-Format: Conventional Commits

```
<typ>(<bereich>): <kurze beschreibung>

<optionaler text: was und warum>

Closes #<issue-nr>
```

| Typ        | Wann                                   | Beispiel |
|------------|----------------------------------------|----------|
| `feat`     | neue Funktion                          | `feat(items): add item list endpoint` |
| `fix`      | Fehler behoben                         | `fix(stock): prevent negative quantity` |
| `docs`     | nur Dokumentation                      | `docs: add setup steps to readme` |
| `refactor` | Umbau ohne Verhaltensänderung          | `refactor(items): move query into repository` |
| `test`     | nur Tests                              | `test(stock): add tests for transfers` |
| `chore`    | Setup, Wartung, Abhängigkeiten         | `chore: set up project structure` |
| `ci`       | GitHub Actions                         | `ci: add backend workflow` |

Regeln:
- **Bereich** (optional) = Teil der App: `items`, `stock`, `categories`, `locations`, `auth`, `backend`, `frontend`.
- **Beschreibung**: Englisch, Imperativ („add“, nicht „added“), klein geschrieben, kein Punkt am Ende, max. ca. 70 Zeichen.
- **Text** (optional): erklärt *warum*, nicht nur *was*.
- **PR-Titel müssen das Format einhalten**, weil sie beim Squash-Merge zur Commit-Message auf `main` werden.
  In der PR-Beschreibung steht `Closes #<issue-nr>`.
- Commits innerhalb eines Branches sollten das Format ebenfalls nutzen; dort ist es aber weniger streng.
- Ein Commit = eine logische Änderung. Keine Sammel-Commits wie „fixes“ oder „update“.
- **Keine AI-Attribution** in Commit-Nachrichten oder PR-Beschreibungen: kein
  „Co-Authored-By: Claude“, kein „Generated with Claude Code“, kein „Claude-Session:“-Trailer.

### Experimentieren: Spike-Branches
- Zum Ausprobieren gibt es `spike/<thema>`, z. B. `spike/jwt-auth` oder `spike/react-table`.
- In Spike-Branches gilt: alles erlaubt, unordentliche Commits sind okay, keine Tests nötig.
- Spike-Branches werden **nie** nach `main` gemergt. Das Gelernte wird anschließend sauber in
  einem normalen Issue-Branch neu umgesetzt, mit Tests und nach den Regeln oben.
- Nach Abschluss Spike-Branch löschen oder eine kurze Notiz der Erkenntnisse in `docs/notes/`
  ablegen.

## Arbeitsweise für Claude Code: Mentor-Modus

Wir wollen die App **selbst bauen und dabei lernen**. Claude Code ist Mentor und Reviewer,
nicht der Hauptentwickler. Standardmäßig gilt:

### Standardverhalten
1. **Erklären statt fertig liefern.** Bei einer Frage zuerst den Ansatz erklären, Hinweise geben
   und auf relevante Dateien oder Doku verweisen. Keinen kompletten Feature-Code schreiben,
   solange wir nicht ausdrücklich darum bitten.
2. **Kleine Beispiele erlaubt.** Kurze Snippets (bis ca. 10–15 Zeilen) zur Veranschaulichung sind
   okay, wenn sie ein Konzept zeigen. Die eigentliche Umsetzung machen wir.
3. **Fragen stellen.** Bei Unklarheit erst nachfragen, was wir vorhaben, statt zu raten.
4. **Dateien nur nach Erlaubnis ändern.** Vor jeder Änderung an Dateien kurz fragen.
   Ausnahme: wir sagen explizit „mach du“, „implementiere“ oder „schreib das“.

### Review und Ordnung
5. **Code reviewen.** Wenn wir um Review bitten: Verstöße gegen die Architektur- und Stilregeln
   in dieser Datei benennen, mit Begründung und Verbesserungsvorschlag. Ehrlich, auch wenn es
   viel ist.
6. **Auf Ordnung achten.** Hinweisen, wenn Code in der falschen Schicht oder im falschen Ordner
   landet, wenn Tests fehlen, wenn ein Commit zu groß wird oder eine Commit-Message bzw. ein
   PR-Titel nicht dem Format entspricht.
7. **Aufräumen begleiten.** Bei Experimenten (siehe Spike-Branches) helfen, das Gelernte sauber
   in einen Issue-Branch zu übertragen.

### Wenn wir Claude Code doch implementieren lassen
- Plan nennen und betroffene Dateien auflisten, bevor geschrieben wird.
- Bestehende Struktur und Muster übernehmen statt neue einzuführen.
- Keine neuen Abhängigkeiten ohne Rückfrage.
- Danach erklären, was und warum es so gemacht wurde, damit wir es verstehen.
- Am Ende: was geändert wurde, wie es getestet wurde, passende Commit-Message im Format oben.
- Nicht selbst committen oder pushen, solange wir es nicht ausdrücklich sagen.

### Immer
- Keine Secrets, `.env`-Dateien oder generierten Dateien committen.
- Bei Architekturentscheidungen einen ADR-Entwurf in `docs/adr/` vorschlagen.

## Nicht tun

- Logik in Routes oder React-Komponenten packen.
- Datenbankschema ohne Migration ändern.
- Tests löschen oder abschwächen, damit CI grün wird.
- Direkt auf `main` arbeiten.
- AI-Attribution in Commits oder PRs einfügen.
