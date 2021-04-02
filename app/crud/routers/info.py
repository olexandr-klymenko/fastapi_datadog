from fastapi import APIRouter

router = APIRouter()


@router.get("/info/", include_in_schema=False)
def info():
    return {"title": "Cars API"}
