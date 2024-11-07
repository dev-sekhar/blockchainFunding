import logging
import hashlib
import time
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@dataclass
class BlockHeader:
    version: int
    previous_hash: str
    merkle_root: str
    timestamp: int
    height: int
    validator: str

    def __init__(self, version, previous_hash, merkle_root, timestamp, height, validator):
        self.version = version
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.height = height
        self.validator = validator


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        logging.debug(f"Block created: {self.index} with hash: {self.hash}")

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode(
        )
        hash_value = hashlib.sha256(block_string).hexdigest()
        logging.debug(f"Hash calculated for block {self.index}: {hash_value}")
        return hash_value

    def validate(self) -> bool:
        """Validates the block's internal consistency"""
        logging.info(f"\n=== Starting Block {self.index} Validation ===")

        # Verify hash matches contents
        calculated_hash = self.calculate_hash()
        logging.info(f"Hash Validation:")
        logging.info(f"  Stored Hash:      {self.hash}")
        logging.info(f"  Calculated Hash:  {calculated_hash}")
        if self.hash != calculated_hash:
            logging.error(f"Block {self.index}: Invalid hash")
            return False
        logging.info("  ✅ Hash validation passed")

        # Verify timestamp is not in future
        current_time = time.time()
        logging.info(f"Timestamp Validation:")
        logging.info(f"  Block Timestamp:  {self.timestamp}")
        logging.info(f"  Current Time:     {current_time}")
        if self.timestamp > current_time:
            logging.error(f"Block {self.index}: Future timestamp")
            return False
        logging.info("  ✅ Timestamp validation passed")

        logging.info(f"=== Block {self.index} Basic Validation Complete ===\n")
        return True

    def validate_transaction_data(self) -> bool:
        """Validates the transaction data in the block"""
        from src.core.transaction import Transaction
        
        logging.info(f"\n=== Block {self.index} Transaction Validation ===")
        
        # Genesis Block Check
        if self.index == 0:
            logging.info("Genesis Block Check: ✅")
            return isinstance(self.data, str)

        # Transaction Type Check
        logging.info("\nTransaction Type Check:")
        if not isinstance(self.data, Transaction):
            logging.error(f"  ❌ Invalid data type. Expected Transaction, got {type(self.data)}")
            return False
        logging.info("  ✅ Transaction type check passed")

        # Transaction Data Structure Check
        logging.info("\nTransaction Data Structure Check:")
        if not isinstance(self.data.data, dict):
            logging.error("  ❌ Transaction data must be a dictionary")
            return False

        required_fields = ['from', 'to', 'amount']
        for field in required_fields:
            if field not in self.data.data:
                logging.error(f"  ❌ Missing required field: {field}")
                return False
            logging.info(f"  • {field}: {self.data.data[field]}")
        logging.info("  ✅ Transaction data structure valid")

        # Transaction Signature Check
        logging.info("\nSignature Check:")
        if not self.data.signature:
            logging.error("  ❌ Transaction must be signed")
            return False
        logging.info("  ✅ Transaction is signed")

        # All checks passed
        logging.info("\n✅ All transaction validation checks passed")
        return True
