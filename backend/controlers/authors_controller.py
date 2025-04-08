from fastapi import APIRouter, Depends

from db.db_handler import get_db

router = APIRouter()


@router.get("/all")
async def get_all(db=Depends(get_db)):
    query = "SELECT * FROM authors"
    return await db.fetch(query)
