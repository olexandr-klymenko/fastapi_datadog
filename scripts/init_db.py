from app.crud import models
from app.crud.database import engine


def init_db():
    models.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
