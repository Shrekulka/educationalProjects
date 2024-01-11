# hunter_check_mail/api_clients/client_domain_search.py
from typing import Union, Dict, Optional

from api_clients.base_client import BaseClient


class ClientDomainSearch(BaseClient):
    """
        ClientDomainSearch class for interacting with the domain search endpoint.

        Inherits from BaseClient for making HTTP requests.
        """

    def domain_search(self, domain: str, company: str, limit: int = 10, offset: int = 0,
                      email_type: Optional[str] = None, seniority: Optional[str] = None,
                      department: Optional[str] = None, required_field: Optional[str] = None,
                      raw: bool = False) -> Union[Dict[str, Union[str, int]], None]:
        """
        Performs a domain search based on specified parameters.

        Args:
            domain (str): The domain to search.
            company (str): The company associated with the domain.
            limit (int, optional): The maximum number of results to retrieve (default is 10).
            offset (int, optional): The offset for paginating through results (default is 0).
            email_type (str, optional): The type of email addresses to filter by.
            seniority (str, optional): The seniority level to filter by.
            department (str, optional): The department to filter by.
            required_field (str, optional): A required field for filtering.
            raw (bool, optional): Flag to request raw data.

        Returns:
            Union[Dict[str, Union[str, int]], None]:
            Dictionary with domain search results or None if no content is returned.
        """
        params = {
            "domain": domain,
            "company": company,
            "limit": limit,
            "offset": offset,
            "type": email_type,
            "seniority": seniority,
            "department": department,
            "required_field": required_field,
            "raw": raw
        }
        request = self.make_request("GET", params=params)
        return request
