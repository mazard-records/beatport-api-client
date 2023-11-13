from typing import Any, Generic, TypeVar

from httpx import Client

from ._const import (
    DEFAULT_API_URL,
    DEFAULT_HEADERS,
    LOGIN_HEADERS,
)
from ._models import (
    BeatportCredentials,
    BeatportPlaylist,
    BeatportSearchQuery,
    BeatportSearchResults,
)

# TODO: bound to base type.
ModelClass = TypeVar("ModelClass")


class BaseProxy(Generic[ModelClass]):
    """ Base proxy class for client extension object. """

    def __init__(self, transport: Client, model: ModelClass) -> None:
        self._model = model
        self._transport = transport

    def __getattr__(self, attr: str) -> Any:
        # TODO: check if exist first.
        return getattr(self._model, attr)


class BeatportPlaylistProxy(BaseProxy):
    """ """

    def add(self, track_ids: list[int]) -> None:
        endpoint = f"/api/v4/my/playlists/{self.id}/tracks/bulk"
        payload = {"track_ids": track_ids}
        response = self._transport.post(endpoint, json=payload)
        response.raise_for_status()

    def remove(self, track_id: int) -> None:
        endpoint = f"/api/v4/my/playlists/{self.id}/tracks/{track_id}"
        response = self._transport.delete(endpoint)
        response.raise_for_status()


class BeatportClient(object):
    """
    """

    def __init__(self) -> None:
        self._transport = Client(
            base_url=DEFAULT_API_URL,
            headers=DEFAULT_HEADERS,
        )

    def login(self, credentials: BeatportCredentials) -> None:
        """
        Authenticate to Beatport API with the given credentials,
        after performing some prior call to fill cookies and get a
        valid CSRF token first.
        """
        self._transport.get("/api/my-beatport")
        self._transport.get("/api/account")
        self._transport.get("/api/csrfcheck")
        csrf_token = self._transport.cookies.get("_csrf_token")
        if csrf_token is None:
            raise ValueError("Missing CSRF token")
        headers = LOGIN_HEADERS.copy()
        headers["X-CSRFToken"] = csrf_token
        response = self._transport.post(
            "/api/account/login",
            headers=headers,
            json=credentials.dict(),
        )
        response.raise_for_status()
    
    def playlist(self, playlist_id: int) -> BeatportPlaylistProxy:
        endpoint = f"/api/v4/my/playlists/{playlist_id}"
        response = self._transport.get(endpoint)
        response.raise_for_status()
        playlist = BeatportPlaylist(**response.json())
        return BeatportPlaylistProxy(
            model=playlist,
            transport=self._transport,
        )

    def search(self, query: BeatportSearchQuery) -> BeatportSearchResults:
        endpoint = f"/api/v4/catalog/search?{query}"
        response = self._transport.get(endpoint)
        response.raise_for_status()
        return BeatportSearchResults(**response.json())
