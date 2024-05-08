import uvicorn
from fastapi import APIRouter, FastAPI, status

from src.core.config import settings
app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/", status_code=status.HTTP_200_OK)
def heartbeat():
    return {"status": "ok"}

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_world():
    return {"Hello": "World"}
if __name__ == "__main__":
    uvicorn.run(app)
