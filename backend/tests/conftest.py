import os

# Tests always run against a separate test database, never the one from .env or the shell:
# env vars take precedence over .env, and we overwrite DATABASE_URL unconditionally.
# Set before any test module imports app.main, which loads the settings.
os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL", "postgresql+psycopg://inventar:changeme@127.0.0.1:5432/inventar_test"
)
