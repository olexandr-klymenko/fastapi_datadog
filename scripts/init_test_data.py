from sqlalchemy.exc import IntegrityError

from app.crud import crud, schemas
from app.crud.database import SessionLocal
from scripts.init_db import init_db

TEST_DEALERS = [
    {
        "id": 1,
        "location": "Houston Texas",
        "email": "info@fast_deal.com",
        "phone": "832-555-2002",
        "website": "fast_deal.com",
        "vehicles": [
            {
                "vin": "JH4KA8160PC000949",
                "make": "Acura",
                "model": "Legend",
                "year": 1993,
                "trim": "DX",
            },
            {
                "vin": "2GCHG31K6J4141689",
                "make": "Chevrolet",
                "model": "G30",
                "year": 1988,
                "trim": "LX",
            },
            {
                "vin": "ZAMGJ45A480037578",
                "make": "Maserati",
                "model": "GranTurismo",
                "year": 2008,
                "trim": "DX",
            },
        ],
    },
    {
        "id": 2,
        "location": "Los Angeles CA",
        "email": "info@best_cars.com",
        "phone": "323-372-2515",
        "website": "best_cars.com",
        "vehicles": [],
    },
    {
        "id": 3,
        "location": "Chicago, IL",
        "email": "info@cheap_cars.com",
        "phone": "217-300-2642",
        "website": "cheap_cars.com",
        "vehicles": [
            {
                "vin": "1HD1KEM15CB610062",
                "make": "Harley Davidson",
                "model": "Flhtk",
                "year": 2012,
                "trim": "SE",
            }
        ],
    },
    {
        "id": 4,
        "location": "New York, NY",
        "email": "info@cool_cars.com",
        "phone": "212-200-1266",
        "website": "cool_cars.com",
        "vehicles": [
            {
                "vin": "JHMCG56492C003897",
                "make": "Honda",
                "model": "Accord",
                "year": 2002,
                "trim": "DX",
            }
        ],
    },
]


def init_test_data():
    db = SessionLocal()
    try:
        for dealer_data in TEST_DEALERS:
            vehicles = dealer_data.pop("vehicles")
            dealer = schemas.DealerCreate(**dealer_data)
            crud.create_dealer(db=db, dealer=dealer)

            for vehicle_data in vehicles:
                vehicle = schemas.VehicleCreate(**vehicle_data)
                crud.create_vehicle(db=db, vehicle=vehicle, dealer_id=dealer_data["id"])
    except IntegrityError:
        print("Already created")


if __name__ == "__main__":
    init_db()
    init_test_data()
