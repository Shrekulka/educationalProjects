# hunter_check_mail/api_clients/base_client.py

import time
from typing import Optional, Dict, Union
from urllib.parse import urljoin

import requests
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from utils.config import RED, RESET_ALL, CYAN
from utils.logger import logger


class BaseClient:
    """
    BaseClient class for making HTTP requests.

    Attributes:
        m_base_url (str): The base URL for the API.
        m_api_key (str): The API key used for authentication.
        m_logger (Logger): The logger instance for logging.
        m_url (str): The complete URL for the API endpoint.
        m_session (Session): The requests session for making HTTP requests.
    """

    def __init__(self, endpoint: str, base_url: str, api_key: str):
        """
        Initializes a new BaseClient instance.

        Args:
            endpoint (str): The endpoint for the API.
            base_url (str): The base URL for the API.
            api_key (str): The API key used for authentication.
        """
        # Initializing the base URL attribute with the provided 'base_url'
        self.m_base_url: str = base_url

        # Initializing the API key attribute with the provided 'api_key'
        self.m_api_key: str = api_key

        # Initializing the logger attribute with the 'logger' instance
        self.m_logger = logger

        # Constructing the complete URL using 'urljoin' by combining 'base_url' and 'endpoint'
        self.m_url: str = urljoin(base_url, endpoint)

        # Initializing the 'm_session' attribute with the result of '_create_session()' method
        self.m_session: Session = self._create_session()

    @staticmethod
    def _create_session() -> Session:
        """
        Creates a new requests session with retries and mounts adapters.

        Returns:
            Session: The configured requests session.
        """
        # Creating a new requests session object
        session: Session = requests.Session()

        # Configuring retry settings for handling transient errors
        retries: Retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])

        # Creating a new HTTPAdapter with the configured retry settings
        adapter: HTTPAdapter = HTTPAdapter(max_retries=retries, pool_maxsize=5)

        # Mounting the HTTPAdapter to handle requests for 'http://' and 'https://'
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        # Returning the configured session with retries and mounted adapter
        return session

    def make_request(self, method: str, params: Optional[Dict[str, Union[str, int]]] = None,
                     data: Optional[Dict[str, Union[str, int]]] = None) -> Optional[Response] or Dict[str, str]:
        """
        Makes an HTTP request using the specified method, parameters, and data.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST').
            params (dict, optional): The query parameters for the request.
            data (dict, optional): The data to be included in the request body.

        Returns:
            Response: The response object from the HTTP request.
        """
        try:
            # Ensure that 'params' is a dictionary; if not, set it to an empty dictionary
            params = params or {}

            # Include the API key in the request parameters
            params['api_key'] = self.m_api_key

            # Log the details of the request using the logger's debug level
            self.m_logger.debug(f"{CYAN}Making request with method: {method}, url: {self.m_url}, "
                                f"params: {params}, data: {data}{RESET_ALL}")

            # Create a request object with the specified method, URL, parameters, and data
            request: requests.Request = requests.Request(method=method, url=self.m_url, params=params, data=data)

            # Prepare the request for sending
            prepared_request: requests.PreparedRequest = request.prepare()

            # Send the prepared request using the configured session
            response: Response = self.m_session.send(prepared_request)

            # Check if the response status code indicates no content (204)
            if response.status_code == 204:
                # Log that the request was successful, but no content was returned
                self.m_logger.debug(f"{CYAN}Request successful, but no content returned (status code 204){RESET_ALL}")

                # Return None to indicate no content in the response
                return None

            # Check if the response status code is not 200 (success)
            if response.status_code != 200:
                # Raise an exception for non-successful status codes
                response.raise_for_status()

            # Introduce a brief pause between requests to comply with rate limits
            time.sleep(0.1)

            # Return the response object for successful requests
            return response

        except requests.RequestException as e:
            # Handle any exception that may occur during the request
            error_message: str = (f"Error making request. Method: {method}, URL: {self.m_url}, "
                                  f"Params: {params}, Data: {data}. Error: {e}")

            # Log a warning with the error message
            self.m_logger.warning(f"{RED}{error_message}{RESET_ALL}")

            # Return a dictionary indicating an error with the error message
            return {'error': error_message}
