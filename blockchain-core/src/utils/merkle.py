# src/utils/merkle.py

import hashlib


class MerkleTree:
    def __init__(self, data):
        self.leaves = [self.hash(data_item) for data_item in data]
        self.root = self.build_tree(self.leaves)

    def hash(self, data):
        """Create a SHA-256 hash of the given data."""
        return hashlib.sha256(data.encode()).hexdigest()

    def build_tree(self, leaves):
        """Build the Merkle tree and return the root hash."""
        if len(leaves) == 1:
            return leaves[0]

        new_level = []
        for i in range(0, len(leaves), 2):
            if i + 1 < len(leaves):
                new_level.append(self.hash(leaves[i] + leaves[i + 1]))
            else:
                new_level.append(leaves[i])  # Handle odd number of leaves

        return self.build_tree(new_level)

    def get_root(self):
        """Return the root hash of the Merkle tree."""
        return self.root
