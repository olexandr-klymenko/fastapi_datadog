from typing import List

from fastapi import Depends, HTTPException, APIRouter, status, Response
from sqlalchemy.orm import Session

from app.crud import crud, schemas
from app.crud.database import get_db

router = APIRouter()

VehicleNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
)


@router.get("/{vehicle_id}", response_model=schemas.Vehicle)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = crud.get_vehicle(db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise VehicleNotFound
    return db_vehicle


@router.patch("/{vehicle_id}", response_model=schemas.Vehicle)
def update_vehicle(
    vehicle_id: int, vehicle: schemas.VehicleUpdate, db: Session = Depends(get_db)
):
    db_vehicle = crud.get_vehicle(db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise VehicleNotFound

    return crud.update_record(
        db=db, db_record=db_vehicle, data=vehicle.dict(exclude_unset=True)
    )


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = crud.get_vehicle(db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise VehicleNotFound

    crud.delete_record(db, db_record=db_vehicle)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=List[schemas.Vehicle])
def read_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vehicles(db, skip=skip, limit=limit)
