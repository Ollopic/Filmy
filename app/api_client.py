from logging import Logger, getLogger

import requests


class Client:
    BASE_URL: str = "http://172.17.0.1:8001"

    _logger: Logger = None

    def __init__(self, logger: Logger = getLogger(__name__)):
        self._logger = logger

    def get_token(self, mail: str, password: str) -> str:
        response = requests.post(
            f"{self.BASE_URL}/token",
            json={"mail": mail, "password": password},
        )

        response.raise_for_status()
        dict_response = response.json()

        return dict_response["token"]

    def get_me(self, token: str):
        response = requests.get(
            f"{self.BASE_URL}/user/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()

        return response.json()

    def create_user(self, username: str, mail: str, password: str):
        response = requests.post(
            f"{self.BASE_URL}/user",
            json={"username": username, "mail": mail, "password": password},
        )
        response.raise_for_status()

        return response.json()

    def update_user(self, token: str, profile_data: dict):
        response = requests.patch(
            f"{self.BASE_URL}/user",
            headers={"Authorization": f"Bearer {token}"},
            json=profile_data,
        )
        response.raise_for_status()

        return response.json()
