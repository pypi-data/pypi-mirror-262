import requests
from kopeechka.config import sft_id
from kopeechka.error import TimeOut


class Methods:
    def __init__(self, api_token: str, timeout: int = 5):
        self.api_token: str = api_token
        self.default_query = {
            "token": self.api_token,
            "type": "JSON",
            "api": 2.0
        }
        self.timeout_time = timeout
        self.valid_token()

    def valid_token(self):
        self.user_balance()

    def request(self, url: str = "", params: dict = None) -> requests.Response:
        params.update(self.default_query)
        response = requests.get(url, params=params, timeout=self.timeout_time)
        return response

    def user_balance(self, **kwargs) -> dict:
        query = {
            **kwargs
        }

        response = self.request("http://api.kopeechka.store/user-balance", params=query)

        return response.json()

    def mailbox_get_email(self, site: str, mail_type: str = "", regex: str = "",
                          soft_id: int = sft_id, investor: int = "", subject: str = "", password: int = 0,
                          **kwargs) -> dict:
        query = {
            "site": site,
            "mail_type": mail_type,
            "regex": regex,
            "soft": soft_id,
            "investor": investor,
            "subject": subject,
            "password": password,
            **kwargs
        }

        response = self.request("http://api.kopeechka.store/mailbox-get-email", params=query)
        return response.json()

    def mailbox_get_message(self, task_id: int, full: int = "", **kwargs) -> dict:
        query = {
            "id": task_id,
            "full": full,
            **kwargs
        }

        response = self.request("http://api.kopeechka.store/mailbox-get-message", params=query)
        return response.json()

    def mailbox_cancel(self, task_id: int, **kwargs) -> dict:
        query = {
            "id": task_id,
            **kwargs
        }

        response = self.request("http://api.kopeechka.store/mailbox-cancel", params=query)
        return response.json()

    def mailbox_reorder(self, site: str, email: str, regex: str = "", subject: str = "", password: int = "",
                        **kwargs) -> dict:
        query = {
            "site": site,
            "email": email,
            "regex": regex,
            "subject": subject,
            "password": password,
            **kwargs
        }

        response = self.request("http://api.kopeechka.store/mailbox-reorder", params=query)
        return response.json()

    def mailbox_get_fresh_id(self, site: str, email: str, **kwargs) -> dict:
        query = {
            "site": site,
            "email": email,
            **kwargs
        }

        response = self.request("http://api.kopeechka.store/mailbox-get-fresh-id", params=query)
        return response.json()

    def mailbox_get_domains(self, **kwargs) -> dict:
        query = {
            **kwargs
        }

        response = self.request("http://api.kopeechka.store/mailbox-get-domains", params=query)
        return response.json()

    def mailbox_zones(self, popular: int = "", zones: int = "", site: str = "", **kwargs) -> dict:
        query = {
            "popular": popular,
            "zones": zones,
            "site": site,
            **kwargs
        }

        response = self.request("https://api.kopeechka.store/mailbox-zones", params=query)
        return response.json()
