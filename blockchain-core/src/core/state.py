# src/core/state.py

from typing import Dict, Any, Optional, List
from enum import Enum
import json
import hashlib
from ..utils.merkle import MerkleTree
from ..storage.state_store import StateStore
from src.utils.merkle import MerkleTree


class StateType(Enum):
    ACCOUNT = "ACCOUNT"
    PROJECT = "PROJECT"
    VOTE = "VOTE"
    FUNDING = "FUNDING"


class State:
    def __init__(self):
        self.state_tree = MerkleTree()
        self.state_store = StateStore()
        self._state_cache: Dict[str, Any] = {}

    async def get(self, key: str) -> Optional[Any]:
        """Get state value for key"""
        # Check cache first
        if key in self._state_cache:
            return self._state_cache[key]

        # Get from storage
        value = await self.state_store.get(key)
        if value:
            self._state_cache[key] = value
        return value

    async def put(self, key: str, value: Any) -> bool:
        """Update state with new value"""
        # Update storage
        if await self.state_store.put(key, value):
            # Update cache
            self._state_cache[key] = value
            # Update merkle tree
            self.state_tree.update(key, value)
            return True
        return False

    def get_root_hash(self) -> str:
        """Get current state root hash"""
        return self.state_tree.get_root_hash()

    async def get_proof(self, key: str) -> List[str]:
        """Get merkle proof for key"""
        return self.state_tree.get_proof(key)


class StateManager:
    def __init__(self):
        self.state = {}  # Initialize the state as a dictionary

    def update_state(self, key, value):
        """Update the state with a new key-value pair."""
        self.state[key] = value

    def get_state(self, key):
        """Retrieve a value from the state by key."""
        return self.state.get(key, None)

    # Add other state management methods as needed
