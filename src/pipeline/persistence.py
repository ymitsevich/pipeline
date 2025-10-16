from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, Iterable, Optional

import pandas as pd
from sqlalchemy.orm import Session

from pipeline.database import Artist, Play, Track, User, get_session


class DataWarehouseWriter:
    def __init__(
        self,
        session_factory=get_session,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._session_factory = session_factory
        self._logger = logger or logging.getLogger(__name__)

    def persist(self, tables: Dict[str, pd.DataFrame]) -> None:
        session = self._session_factory()
        try:
            artists_df = tables.get("artists", pd.DataFrame())
            tracks_df = tables.get("tracks", pd.DataFrame())
            plays_df = tables.get("plays", pd.DataFrame())

            artist_map = self._upsert_artists(session, artists_df)
            track_map = self._upsert_tracks(session, tracks_df, artist_map)
            self._ensure_users(session, plays_df)
            self._upsert_plays(session, plays_df, track_map)

            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def _upsert_artists(
        self, session: Session, artists_df: pd.DataFrame
    ) -> Dict[str, Artist]:
        if artists_df is None or artists_df.empty:
            return {}

        artist_map: Dict[str, Artist] = {}

        for record in artists_df.to_dict(orient="records"):
            name = record.get("artist_name")
            if pd.isna(name):
                name = None
            if not name:
                continue

            genre_primary = record.get("genre_primary")
            if pd.isna(genre_primary) or not genre_primary:
                genre_primary = "unknown"

            mbid = record.get("artist_mbid")
            if pd.isna(mbid):
                mbid = None

            country = record.get("country")
            if pd.isna(country):
                country = None

            spotify_id = record.get("spotify_artist_id")
            if pd.isna(spotify_id):
                spotify_id = None

            artist = None
            if mbid:
                artist = (
                    session.query(Artist)
                    .filter(Artist.musicbrainz_id == mbid)
                    .one_or_none()
                )

            if not artist and spotify_id:
                artist = (
                    session.query(Artist)
                    .filter(Artist.spotify_artist_id == spotify_id)
                    .one_or_none()
                )

            if not artist and name:
                artist = (
                    session.query(Artist)
                    .filter(Artist.artist_name == name)
                    .one_or_none()
                )

            if artist:
                artist.genre_primary = genre_primary or artist.genre_primary
                artist.country = country or artist.country
                if mbid and not artist.musicbrainz_id:
                    artist.musicbrainz_id = mbid
                if spotify_id and not artist.spotify_artist_id:
                    artist.spotify_artist_id = spotify_id
            else:
                artist = Artist(
                    artist_name=name,
                    genre_primary=genre_primary or "unknown",
                    country=country,
                    musicbrainz_id=mbid,
                    spotify_artist_id=spotify_id,
                )
                session.add(artist)
                session.flush()

            if name:
                artist_map[name] = artist
            if mbid:
                artist_map[mbid] = artist
            if spotify_id:
                artist_map[spotify_id] = artist

        return artist_map

    def _upsert_tracks(
        self,
        session: Session,
        tracks_df: pd.DataFrame,
        artist_map: Dict[str, Artist],
    ) -> Dict[str, Track]:
        track_map: Dict[str, Track] = {}
        if tracks_df.empty:
            return track_map

        for record in tracks_df.to_dict(orient="records"):
            sanitized = self._normalize_track_record(record)
            if sanitized is None:
                continue

            artist = self._locate_artist(
                session,
                artist_map,
                sanitized["primary_artist_mbid"],
                sanitized["primary_artist_name"],
            )
            if artist is None:
                continue

            track = self._locate_track(
                session,
                artist,
                sanitized["recording_mbid"],
                sanitized["spotify_track_id"],
                sanitized["name"],
            )
            if track is None:
                track = self._create_track(session, artist, sanitized)

            self._apply_track_updates(track, sanitized)
            self._register_track_keys(
                track_map,
                sanitized["track_key"],
                sanitized["recording_mbid"],
                sanitized["spotify_track_id"],
                track,
            )

        return track_map

    def _normalize_track_record(self, record: Dict) -> Optional[Dict]:
        track_key = record.get("track_key")
        recording_mbid = self._clean_string(record.get("recording_mbid"))
        if not track_key and not recording_mbid:
            return None

        name = self._clean_string(record.get("track_name"))
        if not name:
            return None

        primary_artist_name = self._clean_string(record.get("primary_artist_name"))
        primary_artist_mbid = self._clean_string(record.get("primary_artist_mbid"))
        if not primary_artist_name and not primary_artist_mbid:
            return None

        return {
            "track_key": track_key,
            "name": name,
            "primary_artist_name": primary_artist_name,
            "primary_artist_mbid": primary_artist_mbid,
            "duration_sec": self._clean_int(record.get("duration_sec")),
            "album": self._clean_string(record.get("album")),
            "genre": self._clean_string(record.get("genre")) or "unknown",
            "recording_mbid": recording_mbid,
            "release_mbid": self._clean_string(record.get("release_mbid")),
            "spotify_track_id": self._clean_string(record.get("spotify_track_id")),
            "spotify_album_id": self._clean_string(record.get("spotify_album_id")),
        }

    def _locate_artist(
        self,
        session: Session,
        artist_map: Dict[str, Artist],
        primary_artist_mbid: Optional[str],
        primary_artist_name: Optional[str],
    ) -> Optional[Artist]:
        if primary_artist_mbid:
            artist = artist_map.get(primary_artist_mbid)
            if artist:
                return artist

        if primary_artist_name:
            artist = artist_map.get(primary_artist_name)
            if artist:
                return artist

        if primary_artist_mbid:
            artist = (
                session.query(Artist)
                .filter(Artist.musicbrainz_id == primary_artist_mbid)
                .one_or_none()
            )
            if artist:
                return artist

        if not primary_artist_name:
            return None

        return (
            session.query(Artist)
            .filter(Artist.artist_name == primary_artist_name)
            .one_or_none()
        )

    def _locate_track(
        self,
        session: Session,
        artist: Artist,
        recording_mbid: Optional[str],
        spotify_track_id: Optional[str],
        name: str,
    ) -> Optional[Track]:
        if recording_mbid:
            track = (
                session.query(Track)
                .filter(Track.musicbrainz_recording_id == recording_mbid)
                .one_or_none()
            )
            if track:
                return track

        if spotify_track_id:
            track = (
                session.query(Track)
                .filter(Track.spotify_track_id == spotify_track_id)
                .one_or_none()
            )
            if track:
                return track

        return (
            session.query(Track)
            .filter(Track.track_name == name, Track.artist_id == artist.artist_id)
            .one_or_none()
        )

    def _create_track(
        self,
        session: Session,
        artist: Artist,
        record: Dict,
    ) -> Track:
        track = Track(
            track_name=record["name"],
            artist_id=artist.artist_id,
            album=record["album"],
            genre=record["genre"],
            duration_sec=record["duration_sec"],
            musicbrainz_recording_id=record["recording_mbid"],
            musicbrainz_release_id=record["release_mbid"],
            spotify_track_id=record["spotify_track_id"],
            spotify_album_id=record["spotify_album_id"],
        )
        session.add(track)
        session.flush()
        return track

    def _apply_track_updates(self, track: Track, record: Dict) -> None:
        if record["album"]:
            track.album = record["album"]
        if record["genre"]:
            track.genre = record["genre"]
        if record["duration_sec"]:
            track.duration_sec = record["duration_sec"]
        if record["recording_mbid"] and not track.musicbrainz_recording_id:
            track.musicbrainz_recording_id = record["recording_mbid"]
        if record["release_mbid"] and not track.musicbrainz_release_id:
            track.musicbrainz_release_id = record["release_mbid"]
        if record["spotify_track_id"] and not track.spotify_track_id:
            track.spotify_track_id = record["spotify_track_id"]
        if record["spotify_album_id"] and not track.spotify_album_id:
            track.spotify_album_id = record["spotify_album_id"]

    def _register_track_keys(
        self,
        track_map: Dict[str, Track],
        track_key: Optional[str],
        recording_mbid: Optional[str],
        spotify_track_id: Optional[str],
        track: Track,
    ) -> None:
        keys = [
            track_key,
            recording_mbid,
            spotify_track_id,
        ]
        for key in keys:
            if not key:
                continue
            track_map[str(key)] = track

    def _clean_string(self, value) -> Optional[str]:
        if pd.isna(value):
            return None
        if value is None:
            return None
        value = str(value).strip()
        if not value:
            return None
        return value

    def _clean_int(self, value) -> int:
        if value is None or pd.isna(value):
            return 0
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def _ensure_users(self, session: Session, plays_df: pd.DataFrame) -> None:
        if plays_df.empty:
            return

        seen: set[str] = set()
        for record in plays_df.to_dict(orient="records"):
            user_id = record.get("user_name")
            if not user_id or user_id in seen:
                continue
            seen.add(user_id)

            user = session.get(User, user_id)
            if user:
                continue

            listened_at = record.get("listened_at")
            signup_date = self._to_datetime(listened_at) or datetime.utcnow()

            user = User(
                user_id=user_id,
                username=user_id,
                email=None,
                country="ZZ",
                subscription_tier="free",
                signup_date=signup_date,
                last_active=signup_date,
            )
            session.add(user)

    def _upsert_plays(
        self,
        session: Session,
        plays_df: pd.DataFrame,
        track_map: Dict[str, Track],
    ) -> None:
        if plays_df.empty:
            return

        for record in plays_df.to_dict(orient="records"):
            play_id = record.get("play_id")
            if not play_id:
                continue

            possible_keys = [
                record.get("recording_mbid"),
                record.get("recording_msid"),
                record.get("spotify_track_id"),
            ]
            track = None
            for key in possible_keys:
                if pd.isna(key):
                    continue
                track = track_map.get(str(key))
                if track:
                    break

            if not track:
                continue

            played_at = self._to_datetime(record.get("listened_at"))
            if not played_at:
                continue

            played_sec = record.get("duration_sec") or 0
            if pd.isna(played_sec):
                played_sec = 0
            played_sec = int(played_sec)

            device_type = record.get("device_type") or "unknown"
            country = record.get("country") or "ZZ"
            skip_reason = record.get("skip_reason")
            liked = record.get("liked")
            added_to_playlist = record.get("added_to_playlist")
            if pd.isna(added_to_playlist):
                added_to_playlist = 0
            added_to_playlist = int(added_to_playlist)

            play = session.get(Play, play_id)
            if play:
                play.track_id = track.track_id
                play.user_id = record.get("user_name")
                play.played_at = played_at
                play.played_sec = played_sec
                play.completion_rate = record.get("completion_rate")
                play.device_type = device_type
                play.country = country
                play.source = "listenbrainz_api"
                play.skip_reason = skip_reason
                play.liked = liked
                play.added_to_playlist = added_to_playlist
            else:
                play = Play(
                    play_id=play_id,
                    user_id=record.get("user_name"),
                    track_id=track.track_id,
                    played_at=played_at,
                    played_sec=played_sec,
                    completion_rate=record.get("completion_rate"),
                    device_type=device_type,
                    country=country,
                    source="listenbrainz_api",
                    skip_reason=skip_reason,
                    liked=liked,
                    added_to_playlist=added_to_playlist,
                )
                session.add(play)

    @staticmethod
    def _to_datetime(value) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, pd.Timestamp):
            if pd.isna(value):
                return None
            return value.to_pydatetime()
        return None
