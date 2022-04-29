from app.models import *  # noqa

from .db import Base, engine


def create_all():
    Base.metadata.create_all(engine)
