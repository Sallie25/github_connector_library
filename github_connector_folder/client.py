import os
import logging
import requests
import time
from typing import Dict, Any, Optional
import logging
from requests.exceptions import HTTPError, ConnectionError, Timeout
from .custom_exceptions import GitHubAPIError, ResourceNotFound, AuthenticationError, ClientError, ServerError


class GitHubClient:
    """A resilient client for interacting with the GitHub API."""

    def __init__(self) -> None:
        """Initializes the client, loading the API key from environment variables."""

        # Load API token used for authenticating requests to GitHub
        self.token = os.getenv("GITHUB_TOKEN")
        
        # Load base URL for the GitHub API 
        self.base_url = os.getenv("BASE_URL")

        # Configure logging for the entire application
        logging.basicConfig(
            filename="app.log",          # File where logs will be written
            encoding="utf-8",            # Use UTF-8 encoding
            filemode="a",                # Append to the log file, do not overwrite
            format="{asctime} - {levelname} - {message}",  # Log format
            style="{",                   # Use `{}` style formatting
            datefmt="%Y-%m-%d %H:%M",    # Timestamp format
            level=logging.DEBUG          # Log level: DEBUG catches all logs
        )


    def _get_headers(self) -> Dict[str, str]:
        """Constructs and returns request headers for GitHub API calls."""

        # If token is not found, raise an AuthenticationError
        if not self.token:
            raise AuthenticationError()
        
        # Build and return the required request headers
        return {
            "Accept": "application/vnd.github.text-match+json",
            "Authorization": f"Bearer {self.token}"
        }


    def _make_request(self, method: str, endpoint: str, max_retries, base_delay) -> Dict[str, Any]:
        """
        Internal helper that makes HTTP requests with retry and backoff logic.
        - `method`: GET, POST, etc.
        - `endpoint`: API path such as "/repos/user/repo"
        - `max_retries`: Number of retries for transient failures
        - `base_delay`: Initial delay for exponential backoff
        """

        # Construct the full API URL
        url = self.base_url + endpoint
        
        # Build authentication + accept headers
        headers = self._get_headers()

        self.max_retries = max_retries       # Store retry attempts
        self.wait_time = base_delay          # Initial wait time for rate limit backoff

        # Attempt the request up to `max_retries` times
        for attempt in range(self.max_retries):
            try:
                # Dynamically call requests.get / requests.post depending on `method`
                # self.response = getattr(requests, method.lower())(url, headers=headers)
                self.response = requests.get(url,headers=headers)
                

                # If success (HTTP 200 OK)
                if self.response.status_code == 200:
                    logging.info("Successful")
                    return self.response.json()

                # HTTP 204 = No Content
                elif self.response.status_code == 204:
                    raise Exception(f"{self.response.status_code} indicates that there is no content")

                # Raise exception for 4xx and 5xx status codes
                self.response.raise_for_status()

            except ConnectionError:
                # Raised when the client cannot reach GitHub servers
                logging.error("Network problem: Could not reach GitHub servers.")

            except Timeout:
                # Raised when response takes too long
                logging.error("The request took too long and timed out.")

            except HTTPError as http_err:
                # Get HTTP status code from GitHub's response
                status = http_err.response.status_code

                # 404 = Not Found
                if status == 404:
                    return ResourceNotFound(url)

                # GitHub rate limit or temporary server errors
                elif status in [429, 500, 502, 503, 504]:
                    logging.info(
                        f"Temporary retryable error or rate limit: waiting {self.wait_time}s before {attempt + 1} attempt"
                    )
                    time.sleep(self.wait_time)

                    # Exponential backoff: wait_time doubles each retry
                    self.wait_time = base_delay * (2 ** attempt)

                    continue  # Retry the loop

                # Handle any 4xx (client-side errors)
                elif 400 <= status <= 499:
                    return ClientError(status, url)

                # Handle any 5xx (server-side errors)
                elif 500 <= status <= 599:
                    return ServerError(status, url)

                else:
                    # Unknown HTTP error
                    logging.error(f"HTTP error {status} occurred: {http_err}")
                    raise GitHubAPIError(f"HTTP error {status}")

        # If loop finishes without returning, all retries failed
        raise GitHubAPIError(f"Failed to fetch {url} after {max_retries} attempts.")
        # raise Exception(f"Failed to fetch {url} after {max_retries} attempts.")


    def get_repo_details(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetches details for a specific GitHub repository (high-level wrapper)."""

        # Build the endpoint for the GitHub repo
        endpoint_specific_repo = f"/repos/{owner}/{repo}"
        # endpoint_repos = f"/users/{owner}/{repo}"
      
        

        # Call internal request handler
        return self._make_request("GET", endpoint_specific_repo, 3, 1)
    
    def get_all_repos(self, owner: str) -> Dict[str, Any]:
        """Fetches details for a specific GitHub repository (high-level wrapper)."""

        # Build the endpoint for the GitHub repo
        endpoint_all_repos = f"/users/{owner}/repos"
        # endpoint_repos = f"/users/{owner}/{repo}"
     
        

        # Call internal request handler
        return self._make_request("GET", endpoint_all_repos, 3, 1)
    
