# Blockchain Funding Platform

A consortium blockchain platform for project funding management. This project aims to provide a decentralized solution for managing project proposals, funding, and governance through a blockchain network.

## Project Structure

### blockchain-core

The core of the blockchain implementation, responsible for the fundamental blockchain functionalities.

- **src/core/**

  - `__init__.py`: Initializes the core package.
  - `block.py`: Defines the structure and behavior of blocks in the blockchain.
  - `transaction.py`: Manages transaction creation, validation, and signing.
  - `chain.py`: Handles the blockchain itself, including adding and validating blocks.
  - `state.py`: Manages the state of the blockchain, including state retrieval and updates.
  - `mempool.py`: Manages the pool of unconfirmed transactions.
  - `account.py`: Defines account structures and behaviors.

- **src/consensus/**

  - `__init__.py`: Initializes the consensus package.
  - `vote_consensus.py`: Implements the consensus mechanism based on voting.
  - `validator.py`: Manages the validators in the network.
  - `vote_pool.py`: Handles the collection and management of votes.

- **src/network/**

  - `__init__.py`: Initializes the network package.
  - `node.py`: Defines the node structure and behavior in the network.
  - `p2p.py`: Manages peer-to-peer communication between nodes.
  - `protocol.py`: Defines the communication protocol used by nodes.
  - `message.py`: Structures for messages exchanged between nodes.
  - `sync.py`: Handles synchronization of the blockchain state across nodes.

- **src/storage/**

  - `__init__.py`: Initializes the storage package.
  - `db.py`: Manages database connections and operations.
  - `state_store.py`: Handles storage and retrieval of blockchain state.
  - `block_store.py`: Manages storage of blocks in the database.
  - `tx_store.py`: Handles storage of transactions.

- **src/utils/**

  - `__init__.py`: Initializes the utilities package.
  - `crypto.py`: Provides cryptographic functions for signing and verifying messages, generating key pairs, and hashing data.
  - `merkle.py`: Implements Merkle tree functionalities for efficient data verification.
  - `serializer.py`: Handles serialization and deserialization of data structures.
  - `logger.py`: Provides logging functionalities for the application.
  - `config.py`: Manages configuration settings for the application.

- **tests/**: Contains unit tests for each component of the core.

  - **core/**: Tests for core functionalities.
  - **consensus/**: Tests for consensus mechanisms.
  - **network/**: Tests for network functionalities.
  - **storage/**: Tests for storage operations.

- **config/**: Contains configuration files for network, consensus, and storage settings.

### consortium-layer

This layer manages the consortium's governance and membership functionalities.

- **src/membership/**

  - `__init__.py`: Initializes the membership package.
  - `member.py`: Defines the structure and behavior of consortium members.
  - `permissions.py`: Manages permissions for different member roles.
  - `registry.py`: Handles the registration and management of members.

- **src/governance/**

  - `__init__.py`: Initializes the governance package.
  - `rules.py`: Defines the rules governing the consortium.
  - `voting_power.py`: Manages the calculation of voting power for members.
  - `policy.py`: Handles policies related to governance.

- **src/network/**

  - `__init__.py`: Initializes the network package for the consortium layer.
  - `node_manager.py`: Manages nodes within the consortium.
  - `access_control.py`: Handles access control for network operations.

- **tests/**: Contains unit tests for each component of the consortium layer.

### funding-dapp

The decentralized application (DApp) built on top of the blockchain for managing project funding.

- **src/projects/**

  - `__init__.py`: Initializes the projects package.
  - `proposal.py`: Manages project proposals and their lifecycle.
  - `milestone.py`: Handles milestones associated with project proposals.
  - `review.py`: Manages the review process for proposals.
  - `validation.py`: Validates project proposals and associated data.

- **src/funding/**

  - `__init__.py`: Initializes the funding package.
  - `fund_manager.py`: Manages the allocation and distribution of funds.
  - `treasury.py`: Handles treasury operations related to funding.
  - `distribution.py`: Manages the distribution of funds to projects.

- **src/api/**

  - `__init__.py`: Initializes the API package.
  - `routes.py`: Defines the API routes for the DApp.
  - `schemas.py`: Defines data schemas for API requests and responses.
  - `middleware.py`: Handles middleware functions for the API.
  - `handlers/`: Contains specific handlers for different API endpoints.

- **src/utils/**

  - `__init__.py`: Initializes the utilities package for the DApp.
  - `validation.py`: Provides validation functions for user input and data.
  - `notifications.py`: Manages notifications for users.
  - `logger.py`: Provides logging functionalities for the DApp.

- **tests/**: Contains unit tests for each component of the DApp.

### docs

Documentation for the project, including architecture, setup instructions, and API documentation.

## Getting Started

1. Clone the repository.
2. Navigate to the project directory.
3. Run the `create-project-structure.ps1` script to set up the project structure.
4. Install the required dependencies listed in the `requirements.txt` files.
5. Start the blockchain network and the DApp.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by various blockchain projects and community contributions.
