# backend/tests/conftest.py

import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.models import Base, Zone, Fare
from backend.database import get_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession
)

@pytest.fixture(scope="session")
async def test_db_setup():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(test_db_setup) -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a clean database session for each test, seeded with expanded data.
    """
    async with TestingSessionLocal() as session:
        # --- EXPANDED TEST DATA ---
        # Seed the database with 4 zones
        zone1 = Zone(id=1, name="Zone 1")
        zone2 = Zone(id=2, name="Zone 2")
        zone3 = Zone(id=3, name="Zone 3")
        session.add_all([zone1, zone2, zone3])
        await session.commit()
        
        # Seed the database with a variety of fares
        fares_to_add = [
            Fare(source_id=1, destination_id=1, price=40),
            Fare(source_id=1, destination_id=2, price=55),
            Fare(source_id=1, destination_id=3, price=65),
            Fare(source_id=2, destination_id=2, price=35),
            Fare(source_id=2, destination_id=3, price=45),
            Fare(source_id=3, destination_id=3, price=30),
        ]
        session.add_all(fares_to_add)
        await session.commit()
        
        yield session # The test runs with this session

        # Clean up by deleting all data after the test
        await session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    def override_get_session() -> AsyncSession:
        return db_session

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
    del app.dependency_overrides[get_session]

# The empty_db_session fixture from the previous step is still useful
@pytest.fixture
async def empty_db_session(test_db_setup) -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()