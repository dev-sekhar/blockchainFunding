# src/network/p2p.py

import asyncio
import websockets
import json


class P2PProtocol:
    def __init__(self, node):
        self.node = node
        self.peers = set()

    async def start(self):
        """Start the WebSocket server for P2P communication."""
        server = await websockets.serve(self.handler, "localhost", 8765)
        print("P2P server started on ws://localhost:8765")
        await server.wait_closed()

    async def handler(self, websocket, path):
        """Handle incoming WebSocket connections."""
        self.peers.add(websocket)
        try:
            async for message in websocket:
                await self.process_message(message)
        finally:
            self.peers.remove(websocket)

    async def process_message(self, message):
        """Process incoming messages from peers."""
        data = json.loads(message)
        if data['type'] == 'transaction':
            await self.node.process_transaction(data['transaction'])
        elif data['type'] == 'block':
            await self.node.process_block(data['block'])

    async def broadcast_transaction(self, transaction):
        """Broadcast a transaction to all connected peers."""
        message = json.dumps({
            'type': 'transaction',
            'transaction': transaction
        })
        await self._broadcast(message)

    async def broadcast_block(self, block):
        """Broadcast a block to all connected peers."""
        message = json.dumps({
            'type': 'block',
            'block': block
        })
        await self._broadcast(message)

    async def _broadcast(self, message):
        """Send a message to all connected peers."""
        if self.peers:
            await asyncio.wait([peer.send(message) for peer in self.peers])
