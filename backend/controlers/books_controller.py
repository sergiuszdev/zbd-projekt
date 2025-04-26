import asyncpg
from fastapi import APIRouter, Depends, Query, HTTPException

from db.db_handler import get_db

router = APIRouter()


@router.get("/all")
async def get_all(db=Depends(get_db)):
    query = "SELECT * FROM books"
    return await db.fetch(query)


@router.get("/search")
async def search_book(
    db=Depends(get_db),
    q: str = Query(min_length=1, description="Fraza wyszukiwana po tytule"),
):
    query = """
        SELECT books.title, authors.name AS authors_name
        FROM books
        JOIN books_authors ON books.id = books_authors.book_id
        JOIN authors ON authors.id = books_authors.author_id
        WHERE books.title ILIKE $1 OR authors.name ILIKE $1
    """ 
    params = [f"%{q}%"]

    results = await db.fetch(query, *params)
    return {"ilość rekordów": len(results), "wyniki": results}


@router.get("/advanced_search")
async def search_book(
    db=Depends(get_db),
    q: str | None = Query(None, description="Fraza wyszukiwana po tytule lub autorze"),
    filter: str | None = Query(None, description="Kategoria książki"),
):
    query = """
        SELECT books.title, authors.name AS authors_name 
        FROM books 
        JOIN books_authors ON books.id = books_authors.book_id 
        JOIN authors ON authors.id = books_authors.author_id
        JOIN books_genres ON books.id = books_genres.book_id 
        JOIN genres ON books_genres.genre_id = genres.id 
    """

    conditions = []
    params = []
    param_counter = 1

    if q:
        conditions.append(
            f"(books.title ILIKE ${param_counter} OR authors.name ILIKE ${param_counter})"
        )
        params.append(f"%{q}%")
        param_counter += 1

    if filter:
        conditions.append(f"genres.name = ${param_counter}")
        params.append(filter)
        param_counter += 1

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    results = await db.fetch(query, *params)

    return {"ilość rekordów": len(results), "wyniki": results}

 #apache bekchmark, sieg, dociążenie bazy lub zwiększenie zasobów