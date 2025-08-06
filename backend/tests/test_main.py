# backend/tests/test_main.py

import pytest
from httpx import AsyncClient
from sqlalchemy.future import select

# Import the app and dependency function needed for advanced tests
from backend.main import app
from backend.database import get_session

# Import our models to query the database in tests
from backend.models import Fare

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.asyncio


async def test_get_fare_from_db(client: AsyncClient, db_session):
    """
    Tests the /fare endpoint by querying the test DB for the expected value first.
    """
    # Arrange: Get the expected value directly from our test database.
    result = await db_session.execute(
        select(Fare).where(Fare.source_id == 1, Fare.destination_id == 2)
    )
    expected_fare_obj = result.scalars().one()
    
    # Act: Call the API endpoint.
    response = await client.get("/fare", params={"from_zone": 1, "to_zone": 2})

    # Assert: Check that the API response matches the value from the database.
    assert response.status_code == 200
    assert response.json() == {"fare": expected_fare_obj.price}


async def test_get_fare_bidirectional(client: AsyncClient):
    """Tests that the fare is the same regardless of journey direction."""
    response1 = await client.get("/fare", params={"from_zone": 1, "to_zone": 2})
    response2 = await client.get("/fare", params={"from_zone": 2, "to_zone": 1})

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json() == response2.json()


async def test_get_fare_not_found(client: AsyncClient):
    """Tests for a 404 error when a fare does not exist."""
    response = await client.get("/fare", params={"from_zone": 1, "to_zone": 99})
    assert response.status_code == 404


async def test_get_fare_invalid_input(client: AsyncClient):
    """Tests for a 422 validation error when input is not an integer."""
    response = await client.get("/fare", params={"from_zone": 1, "to_zone": "abc"})
    assert response.status_code == 422


async def test_admin_panel_loads(client: AsyncClient):
    """Tests that the admin panel URL returns a successful HTML response."""
    response = await client.get("/admin")
    assert response.status_code == 200
    assert "Admin" in response.text


async def test_get_config_on_empty_db(client: AsyncClient, empty_db_session):
    """
    Tests that the /config endpoint returns an empty list when the database has no zones.
    """
    # Temporarily override the app's database dependency to use the empty DB
    app.dependency_overrides[get_session] = lambda: empty_db_session
    
    response = await client.get("/config")

    assert response.status_code == 200
    assert response.json() == {"available_zones": []}

    # Clean up the override so it doesn't affect other tests
    del app.dependency_overrides[get_session]