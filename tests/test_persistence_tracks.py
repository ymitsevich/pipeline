import pandas as pd

from pipeline.persistence import DataWarehouseWriter


class DummyArtist:
    def __init__(self, artist_id):
        self.artist_id = artist_id


class DummyTrack:
    def __init__(self):
        self.album = None
        self.genre = None
        self.duration_sec = 0
        self.musicbrainz_recording_id = None
        self.musicbrainz_release_id = None
        self.spotify_track_id = None
        self.spotify_album_id = None


class DummySession:
    def __init__(self):
        self.created = []

    def query(self, model):  # pragma: no cover - minimal stub
        return self

    def filter(self, *args, **kwargs):  # pragma: no cover
        return self

    def one_or_none(self):  # pragma: no cover
        return None

    def add(self, obj):
        self.created.append(obj)

    def flush(self):  # pragma: no cover
        pass


class DummyWriter(DataWarehouseWriter):
    def __init__(self):
        super().__init__(session_factory=lambda: None)


def test_normalize_track_record_valid():
    writer = DummyWriter()
    normalized = writer._normalize_track_record(
        {
            "track_key": "key",
            "recording_mbid": "mbid",
            "track_name": "Name",
            "primary_artist_name": "Artist",
            "duration_sec": 200,
            "genre": "rock",
        }
    )

    assert normalized is not None
    assert normalized["genre"] == "rock"
    assert normalized["duration_sec"] == 200


def test_normalize_track_record_missing_keys():
    writer = DummyWriter()
    assert writer._normalize_track_record({}) is None
    assert writer._normalize_track_record({"track_name": "N"}) is None
