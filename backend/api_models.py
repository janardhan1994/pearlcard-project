# backend/api_models.py

from pydantic import BaseModel, conlist
from typing import List

# Pydantic models are used for data validation and serialization.
# They define the expected structure of data for API requests and responses.

class Journey(BaseModel):
    """Defines the structure for a single journey in an API request."""
    from_zone: int
    to_zone: int

class DailyJourneysRequest(BaseModel):
    """Defines the structure of the request body for the daily fare calculation."""
    # 'conlist' is a constrained list, ensuring we receive a maximum of 20 items.
    journeys: conlist(Journey, max_length=20)

class TripResult(BaseModel):
    """Defines the structure for a single trip's result in an API response."""
    from_zone: int
    to_zone: int
    fare: int

class FareResponse(BaseModel):
    """Defines the structure of the successful response for the daily fare calculation."""
    trip_results: List[TripResult]
    total_daily_fare: int