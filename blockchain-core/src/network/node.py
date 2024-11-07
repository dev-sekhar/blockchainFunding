# src/network/node.py
from typing import Set, Dict
import asyncio
from .p2p import P2PProtocol
from ..core.block import Block
from ..core.transaction import Transaction


class Node:
    def __init__(self, node_id: str, config: Dict):
        self.node_id = node_id
        self.peers: Set[str] = set()
        self.blockchain = BlockChain()
        self.mempool = TransactionPool()
        self.protocol = P2PProtocol(self)

    async def start(self):
        """Starts the node"""
        await self.protocol.start()
        await self.sync_with_network()

    async def broadcast_transaction(self, transaction: Transaction):
        """Broadcasts transaction to network"""
        if await self.validate_transaction(transaction):
            await self.protocol.broadcast_transaction(transaction)
            await self.mempool.add_transaction(transaction)

    async def broadcast_block(self, block: Block):
        """Broadcasts block to network"""
        if await self.blockchain.add_block(block):
            await self.protocol.broadcast_block(block)
