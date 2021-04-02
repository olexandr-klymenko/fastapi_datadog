from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Dealer(Base):
    __tablename__ = "dealers"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    website = Column(String, unique=True)

    vehicles = relationship(
        "Vehicle", back_populates="dealer", cascade="all, delete, delete-orphan"
    )


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, unique=True, index=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    trim = Column(String)

    dealer_id = Column(Integer, ForeignKey("dealers.id"))
    dealer = relationship("Dealer", back_populates="vehicles")
