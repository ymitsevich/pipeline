from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Optional

import pandas as pd

from pipeline.clients import ListenBrainzClient


@dataclass
class IngestionResult:
    listens: pd.DataFrame
    payload: Dict
    cursor_used: Optional[int]


class IngestionService:
    def __init__(
        self,
        listen_client: ListenBrainzClient,
        cursor_provider,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._client = listen_client
        self._cursor_provider = cursor_provider
        self._logger = logger or logging.getLogger(__name__)

    def fetch(self, full_resync: bool = False) -> IngestionResult:
        cursor = None if full_resync else self._cursor_provider.get_cursor()
        listens_df, payload = self._client.fetch_listens(min_ts=cursor)

        fetch_metadata = {
            "event": "ingest.fetch",
            "fetched": int(len(listens_df)),
            "min_ts": cursor,
            "full_resync": full_resync,
        }
        self._logger.info(
            "Fetched %d listens for user %s",
            len(listens_df),
            payload.get("user_id"),
            extra=fetch_metadata,
        )

        return IngestionResult(listens=listens_df, payload=payload, cursor_used=cursor)

