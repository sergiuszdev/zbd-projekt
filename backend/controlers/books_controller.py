import asyncpg
from fastapi import APIRouter, Depends, Query, HTTPException

from db.db_handler import get_db

router = APIRouter()


@router.get("/all")
async def get_all(db=Depends(get_db)):
    query = "SELECT * FROM books"
    return await db.fetch(query)


@router.get("/search")
async def search_book(db=Depends(get_db), q: str = Query(min_length=1, description="Fraza wyszukiwana po tytule")):

    query = f"SELECT title FROM books WHERE title ILIKE '%{q}%'"

    results = await db.fetch(query)
    return {
        "ilość rekordów": len(results),
        "wyniki": results
    }