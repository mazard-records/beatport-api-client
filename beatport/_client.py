from ._models import (
    BeatportCredentials,
    BeatportSearchQuery,
)


class Beatport(object):
    """
    """

    def login(self, credentials: BeatportCredentials) -> None:
        # NOTE: perform some prior call to fill cookies
        #       and get a valid CSRF token.
        self._transport.get("/api/my-beatport")
        self._transport.get("/api/account")
        self._transport.get("/api/csrfcheck")
        csrf_token = self._transport.cookies.get("_csrf_token")
        headers = self.LOGIN_HEADERS.copy()
        if csrf_token is None:
            raise ValueError("Missing CSRF token")
        headers["X-CSRFToken"] = csrf_token
        response = self._transport.post(
            "/api/account/login", headers=headers, json=credentials.dict()
        )
        response.raise_for_status()

    def playlist(self, playlist_id: ...) -> ...:
        pass

    def search(self, query: BeatportSearchQuery) -> ...:
        endpoint = f"/api/v4/catalog/search?{query}"
        response = self._transport.get(endpoint)
        response.raise_for_status()
        results = BeatportTrackSearchResult(**response.json())
        return [result.to_track() for result in results.tracks]
