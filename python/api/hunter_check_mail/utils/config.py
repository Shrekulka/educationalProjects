import os

from colorama import Fore, Style


class Config:
    """
    Configuration class for Hunter API client.

    Attributes:
        BASE_URL (str): Base URL for the Hunter API.
        API_KEY (str): API key for authentication.
        DB_FILENAME (str): Database filename.
        LOG_DIR (str): Log directory path.
        LOG_FILENAME (str): Log filename.
        LOG_FILE_PATH (str): Full path to the log file.
        DB_DIR (str): Database directory path.
        DB_PATH (str): Full path to the database file.
    """
    # Base URL for the Hunter API
    BASE_URL: str = "https://api.hunter.io/v2/"

    # API key for authentication
    API_KEY: str = "test-api-key"

    # Database filename
    DB_FILENAME: str = "my_database.db"

    # Log directory and filename
    LOG_DIR: str = os.path.join(os.path.dirname(__file__), "LOG")
    LOG_FILENAME: str = "logs.txt"
    LOG_FILE_PATH: str = os.path.join(LOG_DIR, LOG_FILENAME)

    # Check if the log directory exists, and create it if not
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Database directory and path
    DB_DIR: str = os.path.join(os.path.dirname(__file__), "DB")
    DB_PATH: str = os.path.join(DB_DIR, DB_FILENAME)

    # Check if the database directory exists, and create it if not
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)


# Color codes for console output
RED: str = Fore.RED
CYAN: str = Fore.CYAN
YELLOW: str = Fore.YELLOW
MAGENTA: str = Fore.MAGENTA
BLUE: str = Fore.BLUE
GREEN: str = Fore.GREEN
RESET_ALL: str = Style.RESET_ALL
