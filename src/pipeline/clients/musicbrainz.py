from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional, TypeVar
from pathlib import Path

import requests


F = TypeVar("F", bound=Callable[..., Any])


def retry_with_backoff(
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[type[BaseException], ...] = (requests.RequestException,),
) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    attempt += 1
                    if attempt > retries:
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff
                    if hasattr(args[0], "logger"):
                        args[0].logger.warning(
                            "Retrying MusicBrainz request",
                            extra={"attempt": attempt, "error": str(exc)},
                        )

        return wrapper  # type: ignore[return-value]

    return decorator

MUSICBRAINZ_BASE_URL = "https://musicbrainz.org/ws/2"


def extract_primary_genre(metadata: Dict) -> Optional[str]:
    genres = metadata.get("genres") or []
    if genres:
        return max(genres, key=lambda g: g.get("count", 0)).get("name")

    tags = metadata.get("tags") or []
    if tags:
        return max(tags, key=lambda t: t.get("count", 0)).get("name")

    return None


def extract_country(metadata: Dict) -> Optional[str]:
    if metadata.get("country"):
        return metadata["country"]

    area = metadata.get("area") or {}
    codes = area.get("iso-3166-1-codes") or []
    if codes:
        return codes[0]

    return None


@dataclass
class MusicBrainzClient:
    user_agent: str = field(
        default_factory=lambda: os.getenv(
            "MUSICBRAINZ_USER_AGENT", "pipeline-app/0.1 (contact@example.com)"
        )
    )
    base_url: str = MUSICBRAINZ_BASE_URL
    session: requests.Session = field(default_factory=requests.Session)
    logger: logging.Logger = field(default_factory=lambda: logging.getLogger(__name__))
    cache_path: Optional[str] = field(
        default_factory=lambda: os.getenv(
            "MUSICBRAINZ_CACHE_PATH", "data/cache/musicbrainz_artists.json"
        )
    )
    _artist_cache: Dict[str, Dict] = field(default_factory=dict, init=False)
    _warned_default_user_agent: bool = field(default=False, init=False)
    _last_request_ts: float = field(default=0.0, init=False)

    def __post_init__(self) -> None:
        if not self.cache_path:
            return

        cache_file = Path(self.cache_path)
        if cache_file.exists():
            try:
                with cache_file.open("r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    if isinstance(data, dict):
                        self._artist_cache.update(
                            {str(k): v for k, v in data.items() if isinstance(v, dict)}
                        )
            except (OSError, json.JSONDecodeError) as exc:
                self.logger.warning(
                    "Failed to load MusicBrainz cache",
                    extra={"path": str(cache_file), "error": str(exc)},
                )
        else:
            cache_file.parent.mkdir(parents=True, exist_ok=True)

    def fetch_artist(self, artist_mbid: Optional[str]) -> Dict:
        if not artist_mbid:
            return {}

        if artist_mbid in self._artist_cache:
            return self._artist_cache[artist_mbid]

        if "example.com" in self.user_agent and not self._warned_default_user_agent:
            self.logger.warning(
                "Using default MusicBrainz User-Agent. Set MUSICBRAINZ_USER_AGENT env var."
            )
            self._warned_default_user_agent = True

        headers = {"User-Agent": self.user_agent}
        params = {"fmt": "json", "inc": "genres+tags"}

        try:
            metadata = self._request_artist(artist_mbid, headers, params)
        except requests.RequestException as exc:
            self.logger.warning(
                "MusicBrainz artist lookup failed",
                extra={"artist_mbid": artist_mbid, "error": str(exc)},
            )
            return {}

        self._artist_cache[artist_mbid] = metadata
        self._persist_cache()
        return metadata

    @retry_with_backoff()
    def _request_artist(
        self, artist_mbid: str, headers: Dict[str, str], params: Dict[str, str]
    ) -> Dict:
        now = time.monotonic()
        delta = now - self._last_request_ts
        if delta < 1.0:
            time.sleep(1.0 - delta)

        response = self.session.get(
            f"{self.base_url}/artist/{artist_mbid}",
            params=params,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        self._last_request_ts = time.monotonic()
        return response.json()

    def _persist_cache(self) -> None:
        if not self.cache_path:
            return

        cache_file = Path(self.cache_path)
        try:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            with cache_file.open("w", encoding="utf-8") as fh:
                json.dump(self._artist_cache, fh)
        except OSError as exc:
            self.logger.warning(
                "Failed to persist MusicBrainz cache",
                extra={"path": str(cache_file), "error": str(exc)},
            )
