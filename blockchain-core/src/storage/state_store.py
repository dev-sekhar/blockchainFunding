# src/storage/state_store.py
from typing import Optional, Any
from .db import Database


class StateStore:
    def __init__(self, db: Database):
        self.db = db
        self.cache = {}

    async def get(self, key: str) -> Optional[Any]:
        """Retrieve state from storage"""
        if key in self.cache:
            return self.cache[key]

        async with self.db.connection() as conn:
            result = await conn.execute(
                "SELECT value FROM state WHERE key = ?",
                (key,)
            )
            row = await result.fetchone()
            return row[0] if row else None

    async def put(self, key: str, value: Any) -> bool:
        """Store state in storage"""
        try:
            async with self.db.connection() as conn:
                await conn.execute(
                    "INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)",
                    (key, value)
                )
                await conn.commit()
                self.cache[key] = value
                return True
        except Exception:
            return False
