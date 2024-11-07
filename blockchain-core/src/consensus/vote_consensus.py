# src/consensus/vote_consensus.py
from typing import List, Dict
from ..core.block import Block


class VoteConsensus:
    def __init__(self, config: Dict):
        self.validators = set()
        self.vote_pool = VotePool()
        self.config = config

    async def validate_block(self, block: Block) -> bool:
        """Validates block according to consensus rules"""
        # Check if validator is authorized
        if block.header.validator not in self.validators:
            return False

        # Check votes
        votes = await self.vote_pool.get_votes(block.hash)
        if not self._has_sufficient_votes(votes):
            return False

        return True

    def _has_sufficient_votes(self, votes: List[str]) -> bool:
        """Checks if block has sufficient votes"""
        required_votes = len(self.validators) * 2 // 3 + 1
        return len(votes) >= required_votes
