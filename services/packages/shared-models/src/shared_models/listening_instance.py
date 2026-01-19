"""A pydantic model for a user's listening instance."""
from clickhouse_connect.datatypes.temporal import DateTime
from pydantic import UUID4, UUID7, BaseModel


class ListeningInstance(BaseModel):
    """A listening instance in Rewindify."""

    user_id: UUID4
    instance_id: UUID7
    timestamp: DateTime
    song_name: str
    artist_name: str
    song_duration_ms: float
    genre: str
    artist_id: str
    song_id: str
