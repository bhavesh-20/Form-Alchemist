import uvicorn

from app import app
from app.db import create_all


@app.get("/")
async def home():
    return {"message": "Hello Dev! Go to /docs for swagger API documentation."}


if __name__ == "__main__":
    create_all()
    uvicorn.run(app, host="127.0.0.1", port=8000)
