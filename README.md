# The Resilient GitHub Connector

This project implements a production-ready Python library, github_connector, designed to interface with the GitHub REST API (https://api.github.com). It features robust error handling, automatic exponential backoff for rate limiting, and secure authentication via environment variables.

## Project Structure

.
├── github_connector/
│   ├── __init__.py
│   ├── client.py               # Main GitHubClient implementation
│   └── custom_exceptions.py    # Custom exception classes
├── tests/
│   └── test_client.py          # Unit tests for client resilience
├── main.py                     # Demonstration script
├── pyproject.toml              # Poetry dependency manager configuration
└── .env.example                # Example for secure token storage


## Setup and Installation

**Install Poetry** : If you don't have it, install Poetry:

`pip install poetry`


**Clone the Repository**:

`git clone github-connector-project`
`cd github-connector-project`


**Install Dependencies**:

`poetry install`


`**Configuration (Authentication)**:
Create a file named `.env` in the root directory and add your GitHub Personal Access Token (PAT).
CRITICAL: Never commit your `.env` file. It is already listed in `.gitignore`

## Run the Demo:

`poetry run python main.py`


Tests use `pytest` and `pytest-mock` to ensure the resilience and error handling work correctly without making any real network calls.

`poetry run pytest tests/`


