from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy import func

from pipeline.database import Play, get_session


class PlaybackCursorProvider:
    """
    Provides the latest play timestamp from the warehouse to use as an ingestion cursor.
    """

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self._logger = logger or logging.getLogger(__name__)

    def get_cursor(self) -> Optional[int]:
        session = get_session()
        try:
            last_played = session.query(func.max(Play.played_at)).scalar()
            if last_played is None:
                self._logger.info(
                    "No existing plays found; starting from scratch",
                    extra={"event": "cursor.empty"},
                )
                return None
            cursor = int(last_played.timestamp())
            self._logger.debug(
                "Using cursor derived from warehouse",
                extra={"event": "cursor.loaded", "cursor": cursor},
            )
            return cursor
        finally:
            session.close()

