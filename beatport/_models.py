from urllib.parse import urlencode

from pydantic import BaseModel


class BeatportCredentials(BaseModel):
    username: str
    password: str
    remember: bool = False


class BeatportSearchQuery(BaseModel):
    title: str
    artist: str
    type: str = "tracks"

    def __str__(self) -> str:
        return urlencode(
            dict(
                type=self.type,
                q=self.title,
                artist_name=self.artist,
            ),
        )
