# hunter_check_mail/api_clients/hunter_client_factory.py

from typing import TypeVar

from api_clients.base_client import BaseClient
from api_clients.client_account_information import ClientAccountInformation
from api_clients.client_domain_search import ClientDomainSearch
from api_clients.client_email_count import ClientEmailCount
from api_clients.client_email_finder import ClientEmailFinder
from api_clients.client_email_verifier import ClientEmailVerifier
from utils.config import Config
from utils.logger import logger

T = TypeVar('T', bound=BaseClient)


class HunterClientFactory:
    """
    HunterClientFactory class for creating instances of different API client classes.

    Methods:
        create_client(endpoint: str) -> BaseClient:
            Creates and returns an instance of the specified API client class.

        create_domain_search() -> ClientDomainSearch:
            Creates and returns an instance of the ClientDomainSearch class.

        create_email_finder() -> ClientEmailFinder:
            Creates and returns an instance of the ClientEmailFinder class.

        create_email_verifier() -> ClientEmailVerifier:
            Creates and returns an instance of the ClientEmailVerifier class.

        create_email_count() -> ClientEmailCount:
            Creates and returns an instance of the ClientEmailCount class.

        create_account_information() -> ClientAccountInformation:
            Creates and returns an instance of the ClientAccountInformation class.
    """

    def __init__(self):
        self.m_base_url: str = Config.BASE_URL
        self.m_api_key: str = Config.API_KEY
        self.m_logger = logger

        # Dictionary mapping endpoints to client classes
        self.client_mapping = {
            "domain-search": ClientDomainSearch,
            "email-finder": ClientEmailFinder,
            "email-verifier": ClientEmailVerifier,
            "email-count": ClientEmailCount,
            "account": ClientAccountInformation,
        }

    def create_client(self, endpoint: str) -> T:
        """
        Creates and returns an instance of the specified API client class.

        Args:
            endpoint (str): The endpoint for which to create the client.

        Returns:
            T: An instance of the specified API client class.
        """
        # Get the client class from the dictionary
        client_class = self.client_mapping.get(endpoint)

        if not client_class:
            raise ValueError(f"Unknown endpoint: {endpoint}")

        # Return an instance of the client class with type hint
        return client_class(endpoint, self.m_base_url, self.m_api_key)

    def create_domain_search(self) -> ClientDomainSearch:
        """
        Creates and returns an instance of the ClientDomainSearch class.

        Returns:
            ClientDomainSearch: An instance of the ClientDomainSearch class.
        """
        return self.create_client("domain-search")

    def create_email_finder(self) -> ClientEmailFinder:
        """
        Creates and returns an instance of the ClientEmailFinder class.

        Returns:
            ClientEmailFinder: An instance of the ClientEmailFinder class.
        """
        return self.create_client("email-finder")

    def create_email_verifier(self) -> ClientEmailVerifier:
        """
        Creates and returns an instance of the ClientEmailVerifier class.

        Returns:
            ClientEmailVerifier: An instance of the ClientEmailVerifier class.
        """
        return self.create_client("email-verifier")

    def create_email_count(self) -> ClientEmailCount:
        """
        Creates and returns an instance of the ClientEmailCount class.

        Returns:
            ClientEmailCount: An instance of the ClientEmailCount class.
        """
        return self.create_client("email-count")

    def create_account_information(self) -> ClientAccountInformation:
        """
        Creates and returns an instance of the ClientAccountInformation class.

        Returns:
            ClientAccountInformation: An instance of the ClientAccountInformation class.
        """
        return self.create_client("account")
