import uvicorn

from app import app
from app.db import create_all
from app.routes import auth_router, form_router


@app.get("/")
async def home():
    return {"message": "Hello Dev! Go to /docs for swagger API documentation."}


app.include_router(auth_router)
app.include_router(form_router)

if __name__ == "__main__":
    create_all()
    uvicorn.run(app, host="127.0.0.1", port=8000)
