"""
SQLAlchemy database setup, models, and session management.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.pool import QueuePool
from datetime import datetime
import os

# Database connection URL
# Supports both direct DATABASE_URL or individual components
# DB_PORT defaults to 5432 for inside Docker, use 15432 for localhost
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
    f"{os.getenv('DB_PASSWORD', 'postgres')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'pipeline')}"
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    echo=True  # Set to True to see SQL queries in logs
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# ============================================================================
# MUSIC STREAMING DATABASE SCHEMA
# Star schema optimized for analytics and data engineering pipelines
# ============================================================================


# Dimension Table: Users
class User(Base):
    __tablename__ = "users"

    user_id = Column(String(50), primary_key=True)  # e.g., U4521
    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    country = Column(String(2), nullable=False)  # ISO country code
    subscription_tier = Column(String(20), nullable=False)  # free, premium, family
    signup_date = Column(DateTime, nullable=False)
    last_active = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    plays = relationship("Play", back_populates="user")

    def __repr__(self):
        return f"<User(user_id='{self.user_id}', username='{self.username}', country='{self.country}')>"


# Dimension Table: Artists
class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(Integer, primary_key=True, autoincrement=True)
    artist_name = Column(String(200), nullable=False, unique=True)
    musicbrainz_id = Column(String(36), unique=True)
    spotify_artist_id = Column(String(50), unique=True)
    genre_primary = Column(String(50), nullable=False)
    country = Column(String(2))
    verified = Column(Integer, default=0)  # 0=no, 1=yes (boolean as int)
    monthly_listeners = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tracks = relationship("Track", back_populates="artist")

    def __repr__(self):
        return f"<Artist(id={self.artist_id}, name='{self.artist_name}', genre='{self.genre_primary}')>"


# Dimension Table: Tracks
class Track(Base):
    __tablename__ = "tracks"

    track_id = Column(Integer, primary_key=True, autoincrement=True)
    track_name = Column(String(300), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.artist_id"), nullable=False)
    musicbrainz_recording_id = Column(String(36), unique=True)
    musicbrainz_release_id = Column(String(36))
    spotify_track_id = Column(String(50), unique=True)
    spotify_album_id = Column(String(50))
    album = Column(String(300))
    genre = Column(String(50), nullable=False)
    duration_sec = Column(Integer, nullable=False)
    release_date = Column(DateTime)
    explicit = Column(Integer, default=0)  # 0=clean, 1=explicit
    popularity_score = Column(Float)  # 0-100 score
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    artist = relationship("Artist", back_populates="tracks")
    plays = relationship("Play", back_populates="track")

    def __repr__(self):
        return f"<Track(id={self.track_id}, name='{self.track_name}', duration={self.duration_sec}s)>"


# Fact Table: Plays (the main event/transaction table)
class Play(Base):
    __tablename__ = "plays"

    play_id = Column(String(50), primary_key=True)  # e.g., S10001
    user_id = Column(String(50), ForeignKey("users.user_id"), nullable=False)
    track_id = Column(Integer, ForeignKey("tracks.track_id"), nullable=False)
    
    # Play metadata
    played_at = Column(DateTime, nullable=False, index=True)  # Indexed for time-based queries
    played_sec = Column(Integer, nullable=False)  # How long user listened
    completion_rate = Column(Float)  # played_sec / duration_sec * 100
    
    # Context
    device_type = Column(String(20), nullable=False)  # mobile, desktop, smart_speaker, car
    country = Column(String(2), nullable=False)
    
    # User interaction
    skip_reason = Column(String(50))  # null=completed, next_track, disliked, ad_break, error
    liked = Column(Integer)  # null=no action, 1=liked, 0=disliked
    added_to_playlist = Column(Integer, default=0)
    
    # Data lineage
    source = Column(String(50), default='csv_import')  # csv_import, api, kafka_stream
    ingested_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="plays")
    track = relationship("Track", back_populates="plays")

    def __repr__(self):
        return f"<Play(id='{self.play_id}', user='{self.user_id}', track_id={self.track_id}, completion={self.completion_rate}%)>"


def get_session():
    """
    Get a database session.
    Usage:
        session = get_session()
        try:
            # Do database operations
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()
    """
    return SessionLocal()
