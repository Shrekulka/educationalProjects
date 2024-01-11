# hunter_check_mail/api_clients/client_account_information.py

from typing import Union, Dict

from api_clients.base_client import BaseClient


class ClientAccountInformation(BaseClient):
    """
    ClientAccountInformation class for interacting with the client account information endpoint.

    Inherits from BaseClient for making HTTP requests.
    """

    def account_information(self, raw: bool = False) -> Union[Dict[str, str], None]:
        """
        Retrieves account information from the API.

        Args:
            raw (bool, optional): Flag to request raw data.

        Returns:
            Union[Dict[str, str], None]: Dictionary with account information or None if no content is returned.
        """
        params = {
            "raw": raw
        }
        return self.make_request("GET", params=params)
