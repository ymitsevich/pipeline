from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import pandas as pd
import requests


def _extract_spotify_id(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    return url.rstrip("/").split("/")[-1]


def _extract_spotify_ids(urls: Optional[List[str]]) -> List[str]:
    if not urls:
        return []
    return [
        spotify_id
        for spotify_id in (_extract_spotify_id(url) for url in urls)
        if spotify_id
    ]


@dataclass
class ListenBrainzClient:
    user: str
    count: int = 30
    base_url: str = "https://api.listenbrainz.org/1"
    session: requests.Session = field(default_factory=requests.Session)
    logger: logging.Logger = field(default_factory=lambda: logging.getLogger(__name__))

    def fetch_listens(self, min_ts: Optional[int] = None) -> Tuple[pd.DataFrame, Dict]:
        url = f"{self.base_url}/user/{self.user}/listens"
        params = {"count": self.count}
        if min_ts is not None:
            params["min_ts"] = int(min_ts)

        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()

        payload = response.json().get("payload", {})
        listens = payload.get("listens", [])

        if not listens:
            self.logger.warning("No listens returned for url=%s", url)
            return pd.DataFrame(), payload

        rows = []
        for listen in listens:
            metadata: Dict = listen.get("track_metadata", {})
            additional: Dict = metadata.get("additional_info", {})
            mbid_mapping: Dict = metadata.get("mbid_mapping", {})

            artist_mbids = mbid_mapping.get("artist_mbids") or []
            artist_names = additional.get("artist_names") or [
                metadata.get("artist_name")
            ]
            spotify_artist_ids = _extract_spotify_ids(
                additional.get("spotify_artist_ids")
            )

            rows.append(
                {
                    "user_name": listen.get("user_name"),
                    "inserted_at": pd.to_datetime(
                        listen.get("inserted_at"), unit="s", errors="coerce"
                    ),
                    "listened_at": pd.to_datetime(
                        listen.get("listened_at"), unit="s", errors="coerce"
                    ),
                    "recording_msid": listen.get("recording_msid"),
                    "recording_mbid": mbid_mapping.get("recording_mbid"),
                    "release_mbid": mbid_mapping.get("release_mbid"),
                    "track_name": metadata.get("track_name"),
                    "artist_credit_name": metadata.get("artist_name"),
                    "artist_names": artist_names,
                    "artist_mbids": artist_mbids,
                    "release_name": metadata.get("release_name"),
                    "duration_ms": additional.get("duration_ms"),
                    "origin_url": additional.get("origin_url"),
                    "music_service": additional.get("music_service"),
                    "spotify_track_id": _extract_spotify_id(
                        additional.get("spotify_id")
                    ),
                    "spotify_album_id": _extract_spotify_id(
                        additional.get("spotify_album_id")
                    ),
                    "spotify_artist_ids": spotify_artist_ids,
                    "track_number": additional.get("tracknumber"),
                    "disc_number": additional.get("discnumber"),
                    "release_artist_names": additional.get("release_artist_names"),
                    "device_id": listen.get("device_id"),
                    "listening_from": additional.get("listening_from"),
                    "listening_url": additional.get("listening_url"),
                    "listening_country": additional.get("listening_country"),
                    "submission_client": additional.get("submission_client"),
                    "origin_country": additional.get("origin_country"),
                }
        )

        df = pd.DataFrame(rows)

        if min_ts is not None and not df.empty:
            listened_sec = df["listened_at"].astype("int64") // 1_000_000_000
            df = df[listened_sec > int(min_ts)]

        return df, payload
