import token
from logging import Logger, getLogger

import requests


class Client:
    BASE_URL: str = "http://172.17.0.1:8002"

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

    def get_popular_movies(self, page: int = 1):
        response = requests.get(f"{self.BASE_URL}/movies/popular?page={page}")
        response.raise_for_status()

        return response.json()

    def get_trending_movies(self, page: int = 2):
        response = requests.get(f"{self.BASE_URL}/movies/trending?page={page}")
        response.raise_for_status()

        return response.json()

    def get_top_rating_movies(self, page: int = 1):
        response = requests.get(f"{self.BASE_URL}/movies/top_rated?page={page}")
        response.raise_for_status()

        return response.json()

    def get_upcoming_movies(self, page: int = 1):
        response = requests.get(f"{self.BASE_URL}/movies/upcoming?page={page}")
        response.raise_for_status()

        return response.json()

    def get_movies_now_playing(self, page: int = 1):
        response = requests.get(f"{self.BASE_URL}/movies/now_playing?page={page}")
        response.raise_for_status()

        return response.json()

    def get_movie_by_id(self, movie_id: int, token: str = None):
        headers = {}
        if token:
            headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{self.BASE_URL}/movies/{movie_id}", headers=headers)
        response.raise_for_status()
        return response.json()

    def get_movie_credits(self, movie_id: int):
        response = requests.get(f"{self.BASE_URL}/movies/{movie_id}/credits")
        response.raise_for_status()
        return response.json()

    def get_movie_by_title(self, title: str):
        response = requests.get(f"{self.BASE_URL}/movies?title={title}")
        response.raise_for_status()
        return response.json()

    def get_artist_by_name(self, name: str):
        response = requests.get(f"{self.BASE_URL}/person?name={name}")
        response.raise_for_status()
        return response.json()

    def get_popular_persons(self):
        response = requests.get(f"{self.BASE_URL}/person/popular")
        response.raise_for_status()
        return response.json()

    def get_person(self, person_id: int):
        response = requests.get(f"{self.BASE_URL}/person/{person_id}")
        response.raise_for_status()
        return response.json()

    def get_all_collections(self, token: str):
        response = requests.get(f"{self.BASE_URL}/collection",
                                headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
        return response.json()

    def get_collection(self, token: str, collection_id: str | int):
        response = requests.get(f"{self.BASE_URL}/collection/{collection_id}",
                                headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
        return response.json()

    def add_item_into_collection(self, token: str, collection_id: str, film_id: str, state: str):
        response = requests.post(
            f"{self.BASE_URL}/collection/{collection_id if collection_id != "default" else 0}",
            json={"film_id": film_id, "state": state},
            headers={"Authorization": f"Bearer {token}"},
        )
        return response.json()

    def create_collection(self, token: str, name: str):
        response = requests.post(
            f"{self.BASE_URL}/collection",
            json={"name": name},
            headers={"Authorization": f"Bearer {token}"},
        )
        return response.json()

    def delete_collection(self, token: str, collection_id: str):
        response = requests.delete(
            f"{self.BASE_URL}/collection/{collection_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"id": collection_id},
        )
        return response.json()

    def update_collection(self, token: str, collection_id: str, collection_data: dict):
        response = requests.patch(
            f"{self.BASE_URL}/collection/{collection_id}",
            json=collection_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        return response.json()

    def update_collection_item(self, token: str, collection_id: int, film_id: int, collection_item_data: dict):
        response = requests.patch(
            f"{self.BASE_URL}/collection/{collection_id}/{film_id}",
            json=collection_item_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        return response.json()
