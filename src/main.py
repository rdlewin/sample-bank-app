import uvicorn
from fastapi import APIRouter, FastAPI, status

from src.api import accounts, transactions, users
from src.core.config import settings
from src.core.db import Base, engine

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/", status_code=status.HTTP_200_OK)
def heartbeat():
    return {"status": "ok"}


def init_db():
    Base.metadata.create_all(bind=engine)


v1_router = APIRouter(prefix=settings.API_V1_PREFIX)
v1_router.include_router(accounts.router, prefix="/accounts")
v1_router.include_router(transactions.router, prefix="/transactions")
v1_router.include_router(users.router, prefix="/users")
app.include_router(v1_router)

init_db()

if __name__ == "__main__":
    uvicorn.run(app)
