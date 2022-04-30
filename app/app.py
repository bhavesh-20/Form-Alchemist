import gspread
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer

from .db import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()
scheduler = BackgroundScheduler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
spreadsheet_service = gspread.service_account(filename="credentials.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Atlan Challenge",
        version="1.0",
        description="This is a OpenAPI schema for Atlan Challenge",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
