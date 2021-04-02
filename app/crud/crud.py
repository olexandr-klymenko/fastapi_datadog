from typing import Dict

from sqlalchemy.orm import Session

from app.crud import models, schemas


def get_dealer(db: Session, dealer_id: int):
    return db.query(models.Dealer).filter(models.Dealer.id == dealer_id).first()


def get_dealer_by_email(db: Session, email: str):
    return db.query(models.Dealer).filter(models.Dealer.email == email).first()


def create_dealer(db: Session, dealer: schemas.DealerCreate):
    db_dealer = models.Dealer(
        location=dealer.location,
        email=dealer.email,
        phone=dealer.phone,
        website=dealer.website,
    )
    db.add(db_dealer)
    db.commit()
    db.refresh(db_dealer)
    return db_dealer


def get_dealers(db: Session, email: str = None, skip: int = 0, limit: int = 100):
    if email is None:
        return db.query(models.Dealer).offset(skip).limit(limit).all()
    return db.query(models.Dealer).filter(models.Dealer.email == email).all()


def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()


def create_vehicle(db: Session, vehicle: schemas.VehicleCreate, dealer_id: int):
    db_vehicle = models.Vehicle(**vehicle.dict(), dealer_id=dealer_id)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


def get_vehicles_at_a_dealer(
    db: Session, dealer_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Vehicle)
        .filter(models.Vehicle.dealer_id == dealer_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()


def update_record(db: Session, db_record: models.Base, data: Dict):
    for key, value in data.items():
        setattr(db_record, key, value)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def delete_record(db: Session, db_record: models.Base):
    db.delete(db_record)
    db.commit()
