from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from .db import Base, db, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.on_event("startup")
async def connect():
    await db.connect()
    print("Successfully connected to the database")


@app.on_event("shutdown")
async def disconnect():
    await db.disconnect()
    print("Successfully disconnected from the database")
