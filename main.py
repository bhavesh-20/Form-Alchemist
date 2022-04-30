import uvicorn

from app import app, db, scheduler
from app.routes import (
    auth_router,
    form_router,
    pipeline_router,
    question_router,
    response_router,
)
from app.triggers import PostResposeSubmitTrigger
from setup_db import create_all


@app.on_event("startup")
async def connect():
    await db.connect()
    print("Successfully connected to the database")


@app.on_event("startup")
def start_scheduler():
    scheduler.add_job(
        func=PostResposeSubmitTrigger.trigger, trigger="interval", seconds=5
    )
    scheduler.start()
    print("Scheduler started")


@app.on_event("shutdown")
async def disconnect():
    await db.disconnect()
    print("Successfully disconnected from the database")


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown(wait=False)
    print("Scheduler shutdown")


@app.get("/")
async def home():
    return {"message": "Hello Dev! Go to /docs for swagger API documentation."}


app.include_router(auth_router)
app.include_router(form_router)
app.include_router(question_router)
app.include_router(response_router)
app.include_router(pipeline_router)

if __name__ == "__main__":
    create_all()
    uvicorn.run(app, host="127.0.0.1", port=8000)
