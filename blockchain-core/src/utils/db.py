# src/storage/db.py
from typing import Optional, Any
import aiosqlite


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def init(self):
        """Initializes database tables"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS blocks (
                    hash TEXT PRIMARY KEY,
                    height INTEGER,
                    data BLOB
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS state (
                    key TEXT PRIMARY KEY,
                    value BLOB
                )
            """)
            await db.commit()
