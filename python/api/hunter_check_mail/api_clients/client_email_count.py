# hunter_check_mail/api_clients/client_email_count.py
from typing import Union, Dict, Optional

from api_clients.base_client import BaseClient


class ClientEmailCount(BaseClient):
    """
    ClientEmailCount class for interacting with the email count endpoint.

    Inherits from BaseClient for making HTTP requests.

    """

    def email_count(self, domain: Optional[str] = None, company: Optional[str] = None, raw: bool = False) -> (
            Union)[Dict[str, Union[str, int]], None]:
        """
        Retrieves email count based on specified parameters.

        Args:
            domain (str, optional): The domain for which to retrieve email count.
            company (str, optional): The company associated with the domain for email count.
            raw (bool, optional): Flag to request raw data.

        Returns:
            Union[Dict[str, Union[str, int]], None]:
            Dictionary with email count information or None if no content is returned.
        """
        params = {
            "domain": domain,
            "company": company,
            "raw": raw
        }
        request = self.make_request("GET", params=params)
        return request
