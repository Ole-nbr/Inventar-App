import os

# Tests must not depend on a local .env; env vars take precedence over the .env file.
# Set before any test module imports app.main, which loads the settings.
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")
