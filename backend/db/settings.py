import os

USER = os.getenv('POSTGRES_USER', 'postgres')
PASSWORD = os.getenv('POSTGRES_PASSWORD', 'bazydanych')
DB_NAME = os.getenv('POSTGRES_DB', 'biblioteka_zdb')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')

HOST = os.getenv('POSTGRES_HOST', 'localhost')

DB_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{DB_PORT}/{DB_NAME}"
