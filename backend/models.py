# backend/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

# The base class that all our database models will inherit from.
# It provides the basic functionality for SQLAlchemy's ORM (Object-Relational Mapper).
Base = declarative_base()

class Zone(Base):
    """Represents a single fare zone in the metro system."""
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __str__(self):
        """
        Defines the human-readable string representation of a Zone object.
        This is used by the admin panel to display a zone's name instead of
        a generic object description like '<Zone object at 0x...>'.
        """
        return self.name

    # These relationships link a Zone to all Fares that start or end here.
    # 'back_populates' tells SQLAlchemy that this relationship is the other
    # side of the 'source_zone' and 'destination_zone' relationships in the Fare model.
    source_fares = relationship("Fare", back_populates="source_zone", foreign_keys="Fare.source_id")
    destination_fares = relationship("Fare", back_populates="destination_zone", foreign_keys="Fare.destination_id")

class Fare(Base):
    """Represents the price of a journey between two zones."""
    __tablename__ = "fares"

    id = Column(Integer, primary_key=True)
    # These are the actual database columns for the foreign keys, linking to the 'zones' table.
    source_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False) # Stores price with 2 decimal places.

    # These relationships create the "magic" Python attributes that SQLAdmin and our code use.
    # They link a Fare object directly to its corresponding source and destination Zone objects.
    source_zone = relationship("Zone", foreign_keys=[source_id], back_populates="source_fares")
    destination_zone = relationship("Zone", foreign_keys=[destination_id], back_populates="destination_fares")