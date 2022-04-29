import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.config import Config

Base = declarative_base()

engine = create_engine(Config.DATABASE_URI)
db = databases.Database(Config.DATABASE_URI)
