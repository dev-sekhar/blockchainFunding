import logging
import hashlib
import time


# Configure logging to display messages in the console
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index  # Add this line to define the index
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
        # Verify hash matches contents
        if self.hash != self.calculate_hash():
            logging.error(f"Block {self.index}: Invalid hash")
            return False

        # Verify timestamp is not in future
        if self.timestamp > time.time():
            logging.error(f"Block {self.index}: Future timestamp")
            return False

        return True

    def validate_transaction_data(self) -> bool:
        """Validates the transaction data in the block"""
        if not hasattr(self.data, 'verify_signature'):
            logging.error(f"Block {self.index}: Invalid data type")
            return False

        return True


class BlockHeader:
    def __init__(self, version, previous_hash, merkle_root, timestamp, height, validator):
        self.version = version
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.height = height
        self.validator = validator


class BlockChain:  # Keeping the class name as BlockChain
    def __init__(self):
        logging.info("Initializing the blockchain...")
        # Initialize with the genesis block
        self.blocks = [self.create_genesis_block()]
        logging.info(
            f"Blockchain initialized with {len(self.blocks)} block(s).")

    def create_genesis_block(self):
        # Create the genesis block
        genesis_block = Block(0, "Genesis Block", "0")
        logging.info(
            f"Genesis block created: {genesis_block.index} with hash: {genesis_block.hash}")
        return genesis_block

    def get_blocks(self):
        """Return the list of blocks in the blockchain."""
        logging.debug(f"Retrieving blocks: {len(self.blocks)} blocks found.")
        return self.blocks

    def is_valid_block(self, new_block, previous_block) -> bool:
        """Enhanced block validation"""
        logging.info(f"\n=== Validating Block {new_block.index} ===")
        
        # Step 1: Basic Block Validation
        logging.info("Basic Block Validation:")
        logging.info(f"  • Index: {new_block.index}")
        logging.info(f"  • Previous Hash: {new_block.previous_hash}")
        logging.info(f"  • Hash: {new_block.hash}")
        
        # Step 2: Transaction Data Validation
        logging.info("\nTransaction Data Validation:")
        if not new_block.validate_transaction_data():
            logging.error(f"  ❌ Transaction validation failed")
            if hasattr(new_block.data, '__dict__'):
                logging.error(f"  • Transaction details: {new_block.data.__dict__}")
            return False
        logging.info("  ✅ Transaction validation passed")
        
        return True

    def validate_chain(self) -> bool:
        """Validates the entire blockchain"""
        for i in range(1, len(self.blocks)):
            current_block = self.blocks[i]
            previous_block = self.blocks[i-1]

            if not self.is_valid_block(current_block, previous_block):
                logging.error(f"Chain validation failed at block {i}")
                return False

        return True

    async def add_block(self, data):
        """Attempt to add a block to the blockchain."""
        try:
            logging.info("\n=== Starting Block Addition Process ===")
            logging.info("Input Transaction Data:")
            logging.info(f"  Type: {type(data)}")
            logging.info(f"  Content: {data}")
            if hasattr(data, '__dict__'):
                logging.info(f"  Attributes: {data.__dict__}")

            previous_block = self.blocks[-1]

            # Create new block
            new_block = Block(
                index=len(self.blocks),
                data=data,
                previous_hash=previous_block.hash
            )

            logging.info(f"\nCreated new block:")
            logging.info(f"  Index: {new_block.index}")
            logging.info(f"  Previous Hash: {new_block.previous_hash}")
            logging.info(f"  Hash: {new_block.hash}")
            logging.info(f"  Data Type: {type(new_block.data)}")
            logging.info(f"  Data Content: {new_block.data}")

            # Validate the new block
            if not self.is_valid_block(new_block, previous_block):
                logging.error("Block validation failed")
                return False

            # Add block to chain
            self.blocks.append(new_block)
            logging.info(f"✅ Block {new_block.index} added successfully")
            logging.info("=== Block Addition Complete ===\n")
            return True

        except Exception as e:
            logging.error(f"❌ Error adding block: {str(e)}")
            logging.error(f"Stack trace: ", exc_info=True)
            return False


# Example usage
if __name__ == "__main__":
    blockchain = BlockChain()  # Instantiate the BlockChain class
    # Example block to add
    import asyncio
    asyncio.run(blockchain.add_block("Example block data"))
