import logging

# Module-level logging setup
logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG
)


class GitHubAPIError(Exception):
    """Base exception for all GitHub API errors."""
    def __init__(self, message: str):
        super().__init__(message)
        logging.error(message)


class ResourceNotFound(GitHubAPIError):
    """Raised for 404 errors."""
    def __init__(self, url: str, message: str = "Resource not found"):
        full_message = f"{message} - URL: {url}"
        super().__init__(full_message)


class AuthenticationError(GitHubAPIError):
    """Raised for 401 errors."""
    def __init__(self, message: str = "Authentication failed. Check your token or credentials"):
        super().__init__(message)


class ServerError(GitHubAPIError):
    """Raised for 500-level server errors."""
    def __init__(self, status_code: int, url: str, message: str = "Server error occurred"):
        full_message = f"{message} - HTTP {status_code} - URL: {url}"
        super().__init__(full_message)


class ClientError(GitHubAPIError):
    """Raised for other 400-level client errors."""
    def __init__(self, status_code: int, url: str, message: str = "Client error occurred"):
        full_message = f"{message} - HTTP {status_code} - URL: {url}"
        super().__init__(full_message)
