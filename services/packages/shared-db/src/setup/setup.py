"""Setup script for the shared-db package."""

from shared_db import client

sql = """
CREATE TABLE IF NOT EXISTS listening_instances (
    user_id UUID,
    instance_id UUID,
    timestamp DateTime64(3),
    song_name String,
    artist_name String,
    song_duration_ms Float64,
    genre LowCardinality(String),
    artist_id String,
    song_id String
)
ENGINE = MergeTree()
PRIMARY KEY (user_id, timestamp)
ORDER BY (user_id, timestamp, instance_id)
PARTITION BY toYYYYMM(timestamp);
"""

try:
    client.command(sql)
except Exception as e:
    print(f"Failed to set up database: {e}")
