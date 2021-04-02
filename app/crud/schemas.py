from typing import List, Optional

from pydantic import BaseModel
from pydantic.fields import Field

VIN_LENGTH = 17


class VehicleBase(BaseModel):
    vin: str = Field(
        ...,
        min_length=VIN_LENGTH,
        max_length=VIN_LENGTH,
        title="Vehicle Identification Number",
    )
    make: str
    model: str
    year: int
    trim: str


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(VehicleBase):
    vin: Optional[str] = Field(
        None,
        min_length=VIN_LENGTH,
        max_length=VIN_LENGTH,
        title="Vehicle Identification Number",
    )
    make: Optional[str]
    model: Optional[str]
    year: Optional[int]
    trim: Optional[str]


class Vehicle(VehicleBase):
    id: str
    dealer_id: int

    class Config:
        orm_mode = True


class DealerBase(BaseModel):
    location: str
    email: str
    phone: str
    website: str


class DealerCreate(DealerBase):
    pass


class DealerUpdate(DealerBase):
    location: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    website: Optional[str]


class Dealer(DealerBase):
    id: int

    vehicles: List[Vehicle] = []

    class Config:
        orm_mode = True
