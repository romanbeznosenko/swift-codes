from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import swift_codes
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    yield

    pass

app = FastAPI(lifespan=lifespan)

app.include_router(swift_codes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)