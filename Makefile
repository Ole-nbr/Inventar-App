# Recipes stick to "cd dir && command", so they run in sh (Git Bash, Linux, macOS)
# as well as cmd.exe, which GNU make on Windows uses when no sh is on the PATH.

.PHONY: dev rebuild test lint format

# Start db, backend (:8000) and frontend (:5173) with hot reload.
dev:
	docker compose up --build

# Like dev, but also renews the containers' node_modules after dependency changes.
rebuild:
	docker compose up --build --renew-anon-volumes

# Backend tests need the database; --wait blocks until it is healthy.
test:
	docker compose up -d --wait db
	cd backend && uv run pytest
	cd frontend && npm test -- --run

# Checks only, same as CI.
lint:
	cd backend && uv run ruff check . && uv run ruff format --check . && uv run mypy app tests
	cd frontend && npm run lint && npm run format:check && npm run typecheck

# Rewrites files to match the formatters.
format:
	cd backend && uv run ruff format .
	cd frontend && npm run format
