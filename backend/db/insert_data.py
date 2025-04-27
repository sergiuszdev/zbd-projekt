import asyncio
import asyncpg
import uuid
import random
from faker import Faker
import settings as conf

DB_URL = f"postgresql://{conf.USER}:{conf.PASSWORD}@localhost:5432/{conf.DB_NAME}"

fake = Faker()

GENRES = [
    "Fantasy", "Science Fiction", "Mystery", "Thriller", "Romance",
    "Horror", "Historical", "Adventure", "Drama", "Biography",
    "Poetry", "Philosophy", "Science", "Self-Help", "Travel",
    "Health", "Cooking", "Art", "Children", "Business"
]

async def insert_genres(conn):
    genre_ids = []
    for genre in GENRES:
        genre_id = str(uuid.uuid4())
        await conn.execute("INSERT INTO genres (id, name) VALUES ($1, $2)", genre_id, genre)
        genre_ids.append(genre_id)
    return genre_ids

async def insert_authors(conn, n=500):
    author_ids = []
    for _ in range(n):
        author_id = str(uuid.uuid4())
        name = fake.name()
        bio = fake.text(300)
        await conn.execute("INSERT INTO authors (id, name, bio) VALUES ($1, $2, $3)", author_id, name, bio)
        author_ids.append(author_id)
    return author_ids

async def insert_users(conn, n=2000):
    for _ in range(n):
        user_id = str(uuid.uuid4())
        email = fake.unique.email()
        password = fake.password()
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone_number = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        is_employee = random.choice([True, False])

        await conn.execute(
            """INSERT INTO users (id, email, password, first_name, last_name, phone_number, is_employee)
               VALUES ($1, $2, $3, $4, $5, $6, $7)""",
            user_id, email, password, first_name, last_name, phone_number, is_employee
        )

async def insert_books(conn, author_ids, genre_ids, n=10000):
    book_ids = []
    for _ in range(n):
        book_id = str(uuid.uuid4())
        title = fake.sentence(nb_words=4).rstrip('.')
        isbn = ''.join([str(random.randint(0, 9)) for _ in range(13)])
        publish_date = fake.date_between(start_date='-30y', end_date='today')
        description = fake.text(500)

        await conn.execute(
            "INSERT INTO books (id, title, isbn, publish_date, description) VALUES ($1, $2, $3, $4, $5)",
            book_id, title, isbn, publish_date, description
        )
        book_ids.append(book_id)

        # books_authors
        author_sample = random.sample(author_ids, random.choice([1, 2]))
        for author_id in author_sample:
            await conn.execute(
                "INSERT INTO books_authors (book_id, author_id) VALUES ($1, $2)",
                book_id, author_id
            )

        # books_genres
        genre_sample = random.sample(genre_ids, random.choice([1, 2]))
        for genre_id in genre_sample:
            await conn.execute(
                "INSERT INTO books_genres (book_id, genre_id) VALUES ($1, $2)",
                book_id, genre_id
            )

    return book_ids

async def insert_storage(conn, book_ids):
    for book_id in book_ids:
        copies = random.choice([1, 2])
        for _ in range(copies):
            storage_id = str(uuid.uuid4())
            is_available = True
            await conn.execute(
                "INSERT INTO storage (id, book_id, is_available) VALUES ($1, $2, $3)",
                storage_id, book_id, is_available
            )

async def main():
    pool = await asyncpg.create_pool(DB_URL, min_size=5, max_size=20)
    async with pool.acquire() as conn:
        print("Dodaję gatunki...")
        genre_ids = await insert_genres(conn)

        print("Dodaję autorów...")
        author_ids = await insert_authors(conn)

        print("Dodaję użytkowników...")
        await insert_users(conn)

        print("Dodaję książki i powiązania...")
        book_ids = await insert_books(conn, author_ids, genre_ids)

        print("Dodaję magazyn (storage)...")
        await insert_storage(conn, book_ids)

    await pool.close()
    print("Wszystko gotowe!")

if __name__ == "__main__":
    asyncio.run(main())
