from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, Optional

import pandas as pd

from pipeline.clients import MusicBrainzClient, extract_country, extract_primary_genre


def _normalize_country(code: Optional[str]) -> str:
    if not code or not isinstance(code, str):
        return "ZZ"
    code = code.strip().upper()
    if len(code) == 2 and code.isalpha():
        return code
    if len(code) >= 2 and code[:2].isalpha():
        return code[:2]
    return "ZZ"


def _infer_device_type(
    listening_from: Optional[str],
    submission_client: Optional[str],
    origin_url: Optional[str],
) -> str:
    candidates = [
        (listening_from or "").lower(),
        (submission_client or "").lower(),
        (origin_url or "").lower(),
    ]
    for value in candidates:
        if not value:
            continue
        if any(keyword in value for keyword in ["car", "auto", "androidauto"]):
            return "car"
        if any(keyword in value for keyword in ["watch", "wear"]):
            return "wearable"
        if any(keyword in value for keyword in ["smart speaker", "smart_speaker", "alexa", "googlehome", "google home"]):
            return "smart_speaker"
        if any(keyword in value for keyword in ["tv", "roku", "chromecast"]):
            return "tv"
        if any(keyword in value for keyword in ["mobile", "phone", "ios", "android", "iphone", "ipad"]):
            return "mobile"
        if any(keyword in value for keyword in ["desktop", "mac", "windows", "linux"]):
            return "desktop"
        if "web" in value or "browser" in value:
            return "web"
        if "spotify" in value:
            return "spotify_app"
        if "apple" in value:
            return "apple_music"
    return "unknown"


@dataclass
class ListenEnricher:
    music_client: MusicBrainzClient
    logger: logging.Logger = field(default_factory=lambda: logging.getLogger(__name__))

    def enrich(self, listens_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        if listens_df.empty:
            self.logger.info("No listens to enrich")
            empty = pd.DataFrame()
            return {"plays": empty, "tracks": empty, "artists": empty}

        plays_df = self._build_plays(listens_df)
        tracks_df = self._build_tracks(listens_df)
        artists_df = self._build_artists(listens_df)

        return {"plays": plays_df, "tracks": tracks_df, "artists": artists_df}

    def _build_plays(self, listens_df: pd.DataFrame) -> pd.DataFrame:
        plays_df = listens_df.copy()
        plays_df["duration_sec"] = (
            plays_df["duration_ms"].fillna(0).astype("Int64") // 1000
        )
        plays_df["completion_rate"] = 100.0
        plays_df["source"] = "listenbrainz_api"
        plays_df["device_type"] = plays_df.apply(
            lambda row: _infer_device_type(
                row.get("listening_from"),
                row.get("submission_client"),
                row.get("origin_url"),
            ),
            axis=1,
        )
        plays_df["country"] = plays_df.apply(
            lambda row: _normalize_country(
                row.get("listening_country") or row.get("origin_country")
            ),
            axis=1,
        )
        plays_df["played_sec"] = plays_df["duration_sec"]
        plays_df["skip_reason"] = None
        plays_df["liked"] = None
        plays_df["added_to_playlist"] = 0
        plays_df["play_id"] = plays_df.apply(
            lambda row: f"{row['recording_msid']}_{int(row['listened_at'].timestamp())}"
            if pd.notna(row["recording_msid"]) and pd.notna(row["listened_at"])
            else row["recording_msid"],
            axis=1,
        )
        return plays_df

    def _build_tracks(self, listens_df: pd.DataFrame) -> pd.DataFrame:
        track_records = []
        for _, row in listens_df.iterrows():
            track_key = row["recording_mbid"] or row["recording_msid"]
            artist_mbids = row.get("artist_mbids") or []
            artist_names = row.get("artist_names") or [row["artist_credit_name"]]
            primary_artist_mbid = next(
                (mbid for mbid in artist_mbids if mbid), None
            )
            primary_genre = None
            if primary_artist_mbid:
                artist_metadata = self.music_client.fetch_artist(primary_artist_mbid)
                primary_genre = extract_primary_genre(artist_metadata)

            track_records.append(
                {
                    "track_key": track_key,
                    "track_name": row["track_name"],
                    "artist_credit": row["artist_credit_name"],
                    "primary_artist_name": artist_names[0] if artist_names else None,
                    "primary_artist_mbid": primary_artist_mbid,
                    "album": row["release_name"],
                    "duration_sec": (
                        int(row["duration_ms"] // 1000)
                        if pd.notna(row["duration_ms"])
                        else None
                    ),
                    "recording_mbid": row["recording_mbid"],
                    "release_mbid": row["release_mbid"],
                    "spotify_track_id": row["spotify_track_id"],
                    "spotify_album_id": row["spotify_album_id"],
                    "track_number": row["track_number"],
                    "disc_number": row["disc_number"],
                    "music_service": row["music_service"],
                    "genre": primary_genre or "unknown",
                }
            )

        return pd.DataFrame(track_records).drop_duplicates("track_key")

    def _build_artists(self, listens_df: pd.DataFrame) -> pd.DataFrame:
        artist_records = []
        for _, row in listens_df.iterrows():
            names = row.get("artist_names") or [row["artist_credit_name"]]
            mbids = row.get("artist_mbids") or [None] * len(names)
            spotify_ids = row.get("spotify_artist_ids") or [None] * len(names)
            for idx, name in enumerate(names):
                mbid = mbids[idx] if idx < len(mbids) else None
                metadata = self.music_client.fetch_artist(mbid) if mbid else {}
                genre_primary = extract_primary_genre(metadata) or "unknown"
                country = extract_country(metadata)
                artist_records.append(
                    {
                        "artist_key": mbid or name.lower(),
                        "artist_name": name,
                        "artist_mbid": mbid,
                        "spotify_artist_id": (
                            spotify_ids[idx] if idx < len(spotify_ids) else None
                        ),
                        "genre_primary": genre_primary,
                        "country": country,
                        "disambiguation": metadata.get("disambiguation"),
                    }
                )

        return (
            pd.DataFrame(artist_records)
            .drop_duplicates("artist_key")
            .reset_index(drop=True)
        )
