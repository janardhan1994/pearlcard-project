# backend/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from contextlib import asynccontextmanager
from sqladmin import Admin
from .settings import settings # <-- Import the settings object

# Import our own project modules using relative paths
from .database import engine, get_session, async_session
from .models import Base, Zone, Fare
from .api_models import DailyJourneysRequest, FareResponse, TripResult
from .admin import ZoneAdmin, FareAdmin



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    A lifespan context manager for the FastAPI application.
    Code before the 'yield' runs on application startup.
    Code after the 'yield' would run on application shutdown.
    """
    await create_initial_data()
    yield

async def create_initial_data():
    """
    Initializes the database. It creates tables if they don't exist
    and seeds the database with default zones and fares on the very first run.
    """
    async with engine.begin() as conn:
        # This line ensures that tables are created based on our models,
        # but it will not try to recreate them if they already exist.
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # We check if any zones exist. If they do, we skip seeding the data.
        if (await session.execute(select(Zone))).scalars().first() is None:
            print("Database is empty. Populating with initial data...")
            zone1, zone2, zone3 = Zone(name="Zone 1"), Zone(name="Zone 2"), Zone(name="Zone 3")
            session.add_all([zone1, zone2, zone3])
            await session.commit() 

            # Create the default fares using the new model column names.
            fares_to_add = [
                Fare(source_id=zone1.id, destination_id=zone1.id, price=40),
                Fare(source_id=zone1.id, destination_id=zone2.id, price=55),
                Fare(source_id=zone1.id, destination_id=zone3.id, price=65),
                Fare(source_id=zone2.id, destination_id=zone2.id, price=35),
                Fare(source_id=zone2.id, destination_id=zone3.id, price=45),
                Fare(source_id=zone3.id, destination_id=zone3.id, price=30),
            ]
            session.add_all(fares_to_add)
            await session.commit()
            print("Initial data has been populated.")


# Create the main FastAPI application instance, attaching the lifespan event handler.
app = FastAPI(title="PearlCard API", lifespan=lifespan)


# Create the SQLAdmin instance and link it to our FastAPI app and database engine.
admin = Admin(app, engine)

# Configure CORS (Cross-Origin Resource Sharing) to allow our frontend
# (running on localhost:3000) to make requests to our backend (on localhost:8000).
# Configure CORS using the value from our settings object
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS, # <-- Use the setting here
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# Register the admin views we defined in admin.py with the admin panel.
admin.add_view(ZoneAdmin)
admin.add_view(FareAdmin)


# --- API Endpoints ---

@app.get("/config", tags=["Configuration"])
async def get_app_config(session: AsyncSession = Depends(get_session)):
    """API endpoint to provide the frontend with the list of available zones."""
    result = await session.execute(select(Zone).order_by(Zone.id))
    return {"available_zones": [zone.id for zone in result.scalars().all()]}

@app.get("/fare", tags=["Fares"])
async def get_single_fare(
    from_zone: int, to_zone: int, session: AsyncSession = Depends(get_session)
):
    """API endpoint to calculate and return the fare for a single journey."""

    # Sort the zone IDs to handle bidirectional travel (e.g., 1->3 is the same as 3->1).
    # This assumes we store fares with the lower zone ID as the source.
    source = min(from_zone, to_zone)
    destination = max(from_zone, to_zone)

    # Query the database for a fare matching the sorted zones.
    res = await session.execute(
        select(Fare).where(Fare.source_id == source, Fare.destination_id == destination)
    )
    fare_obj = res.scalars().first()

    if not fare_obj:
        # If no fare is found, return a 404 Not Found error.
        raise HTTPException(
            status_code=404, detail="Fare not found for the specified journey."
        )
    
    return {"fare": fare_obj.price}