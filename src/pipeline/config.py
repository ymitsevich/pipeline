from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ListenBrainzConfig:
    user: str = os.getenv("LISTENBRAINZ_USER", "iliekcomputers")
    fetch_count: int = int(os.getenv("LISTENBRAINZ_FETCH_COUNT", "30"))


@dataclass(frozen=True)
class AppConfig:
    listenbrainz: ListenBrainzConfig = ListenBrainzConfig()


def load_config() -> AppConfig:
    """
    Load application configuration from environment variables.
    """
    return AppConfig()

