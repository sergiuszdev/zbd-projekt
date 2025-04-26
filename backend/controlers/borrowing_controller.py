from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, timedelta
from db.db_handler import get_db  # Twój handler połączenia do asyncpg

router = APIRouter(prefix="/borrowings", tags=["Borrowings"])

class BorrowRequest(BaseModel):
    user_id: UUID
    book_id: UUID


@router.post("/borrow")
async def borrow_book(data: BorrowRequest, db=Depends(get_db)):
    # Sprawdzenie czy użytkownik istnieje
    user = await db.fetchrow("SELECT * FROM users WHERE id = $1", data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Szukanie dostępnego egzemplarza książki
    storage = await db.fetchrow(
        "SELECT * FROM storage WHERE book_id = $1 AND is_available = true",
        data.book_id
    )
    if not storage:
        raise HTTPException(status_code=404, detail="No available copies")

    # Wypożyczenie książki
    due_date = datetime.utcnow() + timedelta(days=14)
    borrow_query = """
        INSERT INTO borrowings (id, user_id, book_copy_id, due_at)
        VALUES (gen_random_uuid(), $1, $2, $3)
        RETURNING id, due_at
    """
    borrowing = await db.fetchrow(borrow_query, data.user_id, storage["id"], due_date)

    # Aktualizacja dostępności
    await db.execute("UPDATE storage SET is_available = false WHERE id = $1", storage["id"])

    return {
        "message": "Book successfully borrowed",
        "borrowing_id": str(borrowing["id"]),
        "due_at": borrowing["due_at"]
    }
