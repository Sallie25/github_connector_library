import os
import logging
from dotenv import load_dotenv  
from github_connector.client import GitHubClient 


def main():
    """
    Entry point of the application.
    Demonstrates how to use GitHubClient to fetch repo details.
    """

    # Load environment variables from .env file
    load_dotenv()

    # Optional: ensure logs also print to console
    logging.basicConfig(level=logging.INFO)

    # Create GitHub client instance (will read token and base URL from env)
    client = GitHubClient()

    # GitHub username (fixed)
    owner = "Sallie25"


    # # Ask user for a repository name OR hardcode one
    # repo = input("Enter the repository name to fetch details for: ").strip()

    # logging.info(f"Fetching details for {owner}/{repo}...")

    # try:
    #     # Make the API request using your resilient client
    #     response = client.get_repo_details(owner, repo)

    #     # Display result if valid dict returned
    #     if isinstance(response, dict):
    #         print("\n=== Repository Details ===")
    #         for key, value in response.items():
    #             print(f"{key}: {value}")
    #     else:
    #         # If a custom exception instance was returned
    #         print(f"\nError occurred: {response}")

    # except Exception as e:
    #     print(f"Unexpected error: {e}")


     # Ask user for a repository name OR hardcode one

    logging.info(f"Fetching details for {owner}/repos...")

    try:
        # Make the API request using your resilient client
        response = client.get_all_repos(owner)

        # # Display result if valid dict returned
        # if isinstance(response, dict):
        #     print("\n=== Repository Details ===")
        #     for key, value in response.items():
        #         print(f"{key}: {value}")
        # else:
            # If a custom exception instance was returned
            # print(f"\nError occurred: {response}")

        print(response)

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
