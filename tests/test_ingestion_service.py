import pandas as pd

from pipeline.services.ingestion import IngestionService


class DummyClient:
    def __init__(self):
        self.last_min_ts = None

    def fetch_listens(self, min_ts=None):
        self.last_min_ts = min_ts
        df = pd.DataFrame([
            {
                "recording_msid": "abc",
                "listened_at": pd.Timestamp("2024-12-16T08:04:37Z"),
            }
        ])
        payload = {"user_id": "dummy", "latest_listen_ts": 123}
        return df, payload


class DummyCursorProvider:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_cursor(self):
        return self.cursor


class DummyLogger:
    def info(self, *args, **kwargs):
        pass

    def warning(self, *args, **kwargs):
        pass

    def debug(self, *args, **kwargs):
        pass


def test_ingestion_uses_cursor(monkeypatch):
    client = DummyClient()
    cursor_provider = DummyCursorProvider(cursor=42)
    service = IngestionService(client, cursor_provider, logger=DummyLogger())

    result = service.fetch(full_resync=False)

    assert client.last_min_ts == 42
    assert not result.listens.empty
    assert result.cursor_used == 42


def test_ingestion_full_resync_bypasses_cursor():
    client = DummyClient()
    cursor_provider = DummyCursorProvider(cursor=99)
    service = IngestionService(client, cursor_provider, logger=DummyLogger())

    result = service.fetch(full_resync=True)

    assert client.last_min_ts is None
    assert result.cursor_used is None
