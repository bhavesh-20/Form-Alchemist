from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid4().hex))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    mobile_number = Column(String, unique=True, nullable=False)
    is_admin = Column(Boolean, server_default="0")
    created_at = Column(DateTime, default=datetime.utcnow)

    forms = relationship("Form", cascade="all, delete", backref="users")
