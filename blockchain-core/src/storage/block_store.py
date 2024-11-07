# src/storage/block_store.py
from typing import Optional, List
from .db import Database
from ..core.block import Block

class BlockStore:
    def __init__(self, db: Database):
        self.db = db
        
    async def get_block(self, block_hash: str) -> Optional[Block]:
        """Retrieve block by hash"""
        async with self.db.connection() as conn:
            result = await conn.execute(
                "SELECT data FROM blocks WHERE hash = ?",
                (block_hash,)
            )
            row = await result.fetchone()
            return Block.deserialize(row[0]) if row else None
            
    async def save_block(self, block: Block) -> bool:
        """Store block"""
        try:
            async with self.db.connection() as conn:
                await conn.execute(
                    "INSERT INTO blocks (hash, height, data) VALUES (?, ?, ?)",
                    (block.hash, block.header.height, block.serialize())
                )
                await conn.commit()
                return True
        except Exception:
            return False