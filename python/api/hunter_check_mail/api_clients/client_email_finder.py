# hunter_check_mail/api_clients/client_email_finder.py
from typing import Optional, Union, Dict, Any

from api_clients.base_client import BaseClient


class ClientEmailFinder(BaseClient):
    """
    ClientEmailFinder class for interacting with the email finder endpoint.

    Inherits from BaseClient for making HTTP requests.
    """

    def email_finder(
            self,
            domain: str,
            company: str,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            full_name: Optional[str] = None,
            max_duration: Optional[int] = None,
            raw: bool = False
    ) -> Union[Dict[str, Any], None]:
        """
        Performs an email search based on specified parameters.

        Args:
            domain (str): The domain to search.
            company (str): The company associated with the domain.
            first_name (str, optional): The first name of the person.
            last_name (str, optional): The last name of the person.
            full_name (str, optional): The full name of the person.
            max_duration (int, optional): The maximum duration for the search.
            raw (bool, optional): Flag to request raw data.

        Returns:
            Union[Dict[str, Any], None]: Dictionary with email finder results or None if no content is returned.
        """
        params = {
            "domain": domain,
            "company": company,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "max_duration": max_duration,
            "raw": raw
        }
        request = self.make_request("GET", params=params)
        return request
