from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

# One engine (and connection pool) per process. pool_pre_ping drops connections
# that died in the meantime, e.g. after a database restart.
engine = create_engine(get_settings().database_url.get_secret_value(), pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
