from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from controlers.search_controller import router as search_router
from fastapi import Request
from fastapi import FastAPI
from controlers.books_controller import router as books_router
from controlers.authors_controller import router as authors_router
from controlers.genres_controller import router as genres_controller
from controlers.search_controller import router as search_controller

from db.db_handler import startup_db, shutdown_db
templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db()
    yield
    await shutdown_db()

app = FastAPI(lifespan=lifespan)


app.include_router(router=books_router, prefix="/books")
app.include_router(router=genres_controller, prefix="/genres")
app.include_router(router=authors_router, prefix="/authors")
app.include_router(router=search_controller, prefix="/search")
