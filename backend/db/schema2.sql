CREATE EXTENSION IF NOT EXISTS "pgcrypto";


INSERT INTO authors (id, name, bio) VALUES
(gen_random_uuid(), 'George Orwell', 'English novelist and journalist.'),
(gen_random_uuid(), 'J.K. Rowling', 'British author, best known for Harry Potter.'),
(gen_random_uuid(), 'J.R.R. Tolkien', 'Author of The Lord of the Rings.'),
(gen_random_uuid(), 'Dan Brown', 'American author of thriller novels.'),
(gen_random_uuid(), 'Isaac Asimov', 'Prolific science fiction author.');


INSERT INTO genres (id, name) VALUES
(gen_random_uuid(), 'Science Fiction'),
(gen_random_uuid(), 'Fantasy'),
(gen_random_uuid(), 'Thriller'),
(gen_random_uuid(), 'Dystopian'),
(gen_random_uuid(), 'Adventure');


INSERT INTO books (id, title, isbn, publish_date, description) VALUES
(gen_random_uuid(), '1984', '9780451524935', '1949-06-08', 'Dystopian novel about totalitarian regime.'),
(gen_random_uuid(), 'Harry Potter and the Sorcerer''s Stone', '9780439708180', '1997-06-26', 'Boy discovers he is a wizard.'),
(gen_random_uuid(), 'The Hobbit', '9780547928227', '1937-09-21', 'Bilbo Baggins goes on an adventure.'),
(gen_random_uuid(), 'The Da Vinci Code', '9780307474278', '2003-04-03', 'A mystery thriller that involves secret societies.'),
(gen_random_uuid(), 'Foundation', '9780553293357', '1951-05-01', 'Sci-fi epic about the fall of the Galactic Empire.');
