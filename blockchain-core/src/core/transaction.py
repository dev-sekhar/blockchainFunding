# src/core/transaction.py
from enum import Enum
from typing import Dict, Any
import hashlib
import json
from datetime import datetime
from src.utils.crypto import sign_message, verify_signature
import logging
import time


class TransactionType(Enum):
    REGULAR = "REGULAR"
    VOTE = "VOTE"
    STATE_UPDATE = "STATE_UPDATE"


class Transaction:
    def __init__(self, tx_type: TransactionType, data: Dict[str, Any]):
        logging.info("Creating new transaction")
        logging.info(f"  • Type: {tx_type}")
        logging.info(f"  • Data: {data}")
        self.tx_type = tx_type
        self.data = data
        self.signature = None
        self.timestamp = time.time()
        logging.info(f"  • Timestamp added: {self.timestamp}")

    def calculate_hash(self):
        """Calculate the hash of the transaction."""
        transaction_string = f"{self.tx_type}{self.data}{self.timestamp}"
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def to_dict(self):
        """Convert the transaction to a dictionary."""
        return {
            'tx_type': self.tx_type,
            'data': self.data,
            'timestamp': self.timestamp,
            'signature': self.signature
        }

    def sign(self, private_key: str) -> None:
        """Signs the transaction with the given private key"""
        logging.info("\n=== Signing Transaction ===")
        logging.info(f"  • Transaction before signing: {self.__dict__}")
        try:
            message = self.to_dict()
            message_string = json.dumps(message, sort_keys=True)
            self.signature = sign_message(message_string, private_key)
            logging.info(f"  • Signature created: {self.signature}")
        except Exception as e:
            logging.error(f"  ❌ Signing failed: {str(e)}")
            raise

    def verify(self) -> bool:
        """Verifies transaction signature and structure"""
        if not self.signature:
            return False
        message = self.to_dict()
        return verify_signature(message, self.signature)

    def __str__(self):
        return f"Transaction(type={self.tx_type}, data={self.data}, timestamp={self.timestamp}, signature={self.signature})"

    def __repr__(self):
        return self.__str__()


def is_valid_transaction(obj) -> bool:
    """Check if an object is a valid Transaction instance"""
    return (
        isinstance(obj, Transaction) and
        hasattr(obj, 'tx_type') and
        hasattr(obj, 'data') and
        hasattr(obj, 'signature') and
        hasattr(obj, 'verify_signature')
    )
