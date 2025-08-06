# backend/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .settings import settings # <-- Import the settings object

# Defines the connection string for the database.
# 'sqlite+aiosqlite' specifies the database type (SQLite) and the async driver.
# '///./pearlcard.db' is a relative path, meaning the database file 'pearlcard.db'
# will be created in the directory where the server is launched.

# Use the DATABASE_URL from our settings object
DATABASE_URL = settings.DATABASE_URL

# The engine is the core interface to the database, managing connections.
# 'echo=False' is set to prevent SQLAlchemy from logging every single SQL query to the console.
engine = create_async_engine(DATABASE_URL, echo=False)

# A sessionmaker is a factory that creates new database session objects.
# A session represents a single "conversation" with the database.
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    """
    A FastAPI dependency that provides a database session for a single API request.
    
    This function uses a 'yield' pattern, which allows FastAPI to manage the
    session's lifecycle: it opens a session when a request comes in, "injects"
    it into the API route, and ensures the session is closed after the request is finished.
    """
    async with async_session() as session:
        yield session