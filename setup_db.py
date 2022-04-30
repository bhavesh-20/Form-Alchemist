from app.models import *  # noqa

from app.db import Base, engine


def create_all():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_all()