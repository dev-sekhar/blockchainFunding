# src/storage/tx_store.py
from typing import Optional, List
from .db import Database
from ..core.transaction import Transaction

class TransactionStore:
    def __init__(self, db: Database):
        self.db = db
        
    async def get_transaction(self, tx_hash: str) -> Optional[Transaction]:
        """Retrieve transaction by hash"""
        async with self.db.connection() as conn:
            result = await conn.execute(
                "SELECT data FROM transactions WHERE hash = ?",
                (tx_hash,)
            )
            row = await result.fetchone()
            return Transaction.deserialize(row[0]) if row else None
            
    async def save_transaction(self, transaction: Transaction) -> bool:
        """Store transaction"""
        try:
            async with self.db.connection() as conn:
                await conn.execute(
                    "INSERT INTO transactions (hash, data) VALUES (?, ?)",
                    (transaction.hash, transaction.serialize())
                )
                await conn.commit()
                return True
        except Exception:
            return False