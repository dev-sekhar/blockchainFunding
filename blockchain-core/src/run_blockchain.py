import asyncio
import logging
import sys
from src.core.chain import BlockChain
from src.core.transaction import Transaction
from src.utils.crypto import generate_keypair

# Configure logging for this script
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [%(filename)s:%(lineno)d - %(funcName)s()] - %(levelname)s - %(message)s',
    stream=sys.stdout  # Ensure logs go to stdout
)


async def validate_and_print_chain_status(blockchain):
    """Validate the entire chain and print its status"""
    print("\n=== Blockchain Validation Status ===")
    print("=" * 50)

    is_valid = True
    for i in range(1, len(blockchain.get_blocks())):
        current_block = blockchain.get_blocks()[i]
        previous_block = blockchain.get_blocks()[i-1]

        print(f"\nValidating Block {i}:")
        if blockchain.is_valid_block(current_block, previous_block):
            print(f"  ✅ Block {i} is valid")
        else:
            print(f"  ❌ Block {i} is invalid")
            is_valid = False
            break

    print("\nFinal Status:")
    print(f"Chain Status: {'✅ Valid' if is_valid else '❌ Invalid'}")
    print(f"Current Chain Length: {len(blockchain.get_blocks())}")
    print("=" * 50)


async def process_transaction(blockchain, transaction_data, private_key, public_key):
    """Process a single transaction"""
    logging.info(
        f"\n=== Processing transaction to {transaction_data['to']} ===")

    # Create transaction
    transaction = Transaction(
        tx_type="REGULAR",
        data={
            "from": public_key.decode(),
            "to": transaction_data['to'],
            "amount": transaction_data['amount']
        }
    )

    # Sign transaction
    try:
        transaction.sign(private_key.decode())

        # Verify transaction is properly signed
        if not transaction.signature:
            logging.error("❌ Transaction signing failed")
            return False
        logging.info("✅ Transaction successfully signed")

        # Log transaction details
        logging.debug(f"Transaction type: {type(transaction)}")
        logging.info(f"Processing transaction to {transaction_data['to']}")

        # Add to blockchain
        result = await blockchain.add_block(transaction)
        if not result:
            logging.error(
                f"Failed to add block for transaction to {transaction_data['to']}")
            return False

        return True

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return False


async def main():
    """Main function to run the blockchain"""
    logging.info("Starting the blockchain application...")

    # Initialize blockchain
    blockchain = await initialize_blockchain()

    # Generate keypair
    private_key, public_key = generate_keypair()

    # Process transactions
    transactions = [
        {"to": "Charlie", "amount": 10},
        {"to": "Alice", "amount": 20},
        {"to": "Charlie", "amount": 20}
    ]

    for tx_data in transactions:
        await process_transaction(blockchain, tx_data, private_key, public_key)

    # Print final blockchain state
    await print_blockchain_status(blockchain)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
