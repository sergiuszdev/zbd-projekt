from contextlib import asynccontextmanager

from fastapi import FastAPI
from controlers.books_controller import router as books_router
from controlers.authors_controller import router as authors_router
from controlers.genres_controller import router as genres_controller

from db.db_handler import startup_db, shutdown_db


@asynccontextmanager
async def lifespan():
    await startup_db()
    yield
    await shutdown_db()

app = FastAPI(lifespan=lifespan)


app.include_router(router=books_router, prefix="/books")
app.include_router(router=genres_controller, prefix="/genres")
app.include_router(router=authors_router, prefix="/authors")
