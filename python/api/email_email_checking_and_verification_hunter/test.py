class BaseClient(object):
    def __init__(self, api_key):
        self.m_api_key = api_key
        self.client_domain_search = ClientDomainSearch(self.m_api_key)
        self.client_email_count = ClientEmailCount(self.m_api_key)
        self.client_email_finder = ClientEmailFinder(self.m_api_key)
        self.client_email_verifier = ClientEmailVerifier(self.m_api_key)
        self.client_account_information = ClientAccountInformation(self.m_api_key)


class ClientDomainSearch(BaseClient):

    def domain_search(self, domain, company, limit=10, offset=0, email_type=None,
                      seniority=None, department=None, required_field=None, raw=False):
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
        print(f"request: {request}")
        return request


# hunter_check_mail/api_clients/client_email_count.py

class ClientEmailCount(BaseClient):
    def email_count(self, domain=None, company=None, raw=False):
        params = {
            "domain": domain,
            "company": company,
            "raw": raw
        }
        return self.make_request("GET", params=params)


# hunter_check_mail/api_clients/client_email_finder.py


class ClientEmailFinder(BaseClient):
    def email_finder(self, domain, company, first_name=None, last_name=None,
                     full_name=None, max_duration=None, raw=False):
        params = {
            "domain": domain,
            "company": company,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "max_duration": max_duration,
            "raw": raw
        }
        return self.make_request("GET", params=params)


# hunter_check_mail/api_clients/client_email_verifier.py


class ClientEmailVerifier(BaseClient):
    def email_verifier(self, email, raw=False):
        params = {
            "email": email,
            "raw": raw
        }
        return self.make_request("GET", params=params)


# hunter_check_mail/api_clients/hunter_client_factory.py
class ClientAccountInformation:
    def __init__(self):
        self.m_base_url = Config.BASE_URL
        self.m_api_key = Config.API_KEY
        self.m_logger = logger
