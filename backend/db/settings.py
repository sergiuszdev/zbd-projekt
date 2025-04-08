import os

USER = '' if os.getenv('DB_HOST') is None else os.getenv('DB_HOST')
PASSWORD = '' if os.getenv('DB_PASSWORD') is None else os.getenv('DB_PASSWORD')
DB_NAME = '' if os.getenv('DB_NAME') is None else os.getenv('DB_NAME')
