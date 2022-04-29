import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Databse Connection
    DATABASE_URI = os.getenv("DATABASE_URI")

    # JWT Secret
    SECRET_KEY = os.environ.get("SECRET_KEY")
