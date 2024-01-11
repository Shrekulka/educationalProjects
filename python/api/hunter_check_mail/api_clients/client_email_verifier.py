# hunter_check_mail/api_clients/client_email_verifier.py
from typing import Union, Dict, Any

from api_clients.base_client import BaseClient


class ClientEmailVerifier(BaseClient):
    """
    ClientEmailVerifier class for interacting with the email verifier endpoint.

    Inherits from BaseClient for making HTTP requests.
    """

    def email_verifier(self, email: str, raw: bool = False) -> Union[Dict[str, Any], None]:
        """
        Performs email verification for the specified email address.

        Args:
            email (str): The email address to verify.
            raw (bool, optional): Flag to request raw data.

        Returns:
            Union[Dict[str, Any], None]: Dictionary with email verification results or None if no content is returned.
        """
        params = {
            "email": email,
            "raw": raw
        }
        request = self.make_request("GET", params=params)
        return request
