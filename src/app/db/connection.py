# app/db/connection.py
import asyncpg
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:admin123@db:5432/sistemas_distribuidos"
)

async def get_connection():
    return await asyncpg.connect(DATABASE_URL)