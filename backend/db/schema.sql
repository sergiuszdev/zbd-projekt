CREATE TABLE "authors" (
  "id" uuid PRIMARY KEY,
  "name" varchar NOT NULL,
  "bio" text,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "genres" (
  "id" uuid PRIMARY KEY,
  "name" varchar UNIQUE NOT NULL
);

CREATE TABLE "books" (
  "id" uuid PRIMARY KEY,
  "title" varchar NOT NULL,
  "isbn" varchar(13) UNIQUE NOT NULL,
  "publish_date" date,
  "description" text,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "storage" (
    "id" UUID PRIMARY KEY,
    "book_id" UUID,                       
    "is_available" BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_book_id FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

CREATE TABLE "users" (
  "id" uuid PRIMARY KEY,
  "email" varchar(255) UNIQUE NOT NULL,
  "password" varchar NOT NULL,
  "is_employee" boolean NOT NULL DEFAULT false,
  "first_name" varchar(255) NOT NULL,
  "last_name" varchar(255) NOT NULL,
  "phone_number" varchar(20) NOT NULL,
  "created_at" timestamp DEFAULT (now()),
  CHECK (phone_number ~ '^[0-9]+$')
);

CREATE TABLE "books_authors" (
  "book_id" uuid NOT NULL REFERENCES books(id) ON DELETE CASCADE,
  "author_id" uuid NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
  PRIMARY KEY ("book_id", "author_id")
);

CREATE TABLE "books_genres" (
  "book_id" uuid NOT NULL REFERENCES books(id) ON DELETE CASCADE,
  "genre_id" uuid NOT NULL REFERENCES genres(id) ON DELETE CASCADE,
  PRIMARY KEY ("book_id", "genre_id")
);

CREATE TABLE "borrowings" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid REFERENCES users(id) ON DELETE SET NULL,
  "book_copy_id" uuid NOT NULL REFERENCES storage(id)  ON DELETE CASCADE,
  "borrowed_at" timestamp DEFAULT (now()),
  "due_at" timestamp NOT NULL,
  "returned_at" timestamp,
  CHECK (due_at > borrowed_at),
  CHECK (returned_at IS NULL OR returned_at >= borrowed_at)
);