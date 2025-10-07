#!/usr/bin/env python
"""
SQLAlchemy Learning Script - Basic CRUD operations and queries
"""
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline.database import get_session, User, Artist, Track, Play


def insert_sample_data(session):
    """Create sample users, artists, tracks, and plays."""
    print("\n" + "=" * 70)
    print("📝 INSERTING SAMPLE DATA")
    print("=" * 70)
    
    # Create Users
    print("\n→ Creating users...")
    users = [
        User(
            user_id="U001",
            username="alice_music",
            email="alice@example.com",
            country="US",
            subscription_tier="premium",
            signup_date=datetime(2024, 1, 15),
            last_active=datetime.now()
        ),
        User(
            user_id="U002",
            username="bob_beats",
            email="bob@example.com",
            country="GB",
            subscription_tier="free",
            signup_date=datetime(2024, 3, 20),
            last_active=datetime.now()
        ),
        User(
            user_id="U003",
            username="charlie_tunes",
            email="charlie@example.com",
            country="CA",
            subscription_tier="family",
            signup_date=datetime(2024, 5, 10),
            last_active=datetime.now()
        ),
    ]
    session.add_all(users)
    session.commit()
    print(f"   ✅ Created {len(users)} users")
    
    # Create Artists
    print("\n→ Creating artists...")
    artists = [
        Artist(
            artist_name="Taylor Swift",
            genre_primary="pop",
            country="US",
            verified=1,
            monthly_listeners=80000000
        ),
        Artist(
            artist_name="The Weeknd",
            genre_primary="rnb",
            country="CA",
            verified=1,
            monthly_listeners=110000000
        ),
        Artist(
            artist_name="Billie Eilish",
            genre_primary="alternative",
            country="US",
            verified=1,
            monthly_listeners=95000000
        ),
    ]
    session.add_all(artists)
    session.commit()
    print(f"   ✅ Created {len(artists)} artists")
    
    # Get artist IDs for creating tracks
    taylor = session.query(Artist).filter(Artist.artist_name == "Taylor Swift").first()
    weeknd = session.query(Artist).filter(Artist.artist_name == "The Weeknd").first()
    billie = session.query(Artist).filter(Artist.artist_name == "Billie Eilish").first()
    
    # Create Tracks
    print("\n→ Creating tracks...")
    tracks = [
        Track(
            track_name="Anti-Hero",
            artist_id=taylor.artist_id,
            album="Midnights",
            genre="pop",
            duration_sec=200,
            release_date=datetime(2022, 10, 21),
            explicit=0,
            popularity_score=95.0
        ),
        Track(
            track_name="Blinding Lights",
            artist_id=weeknd.artist_id,
            album="After Hours",
            genre="rnb",
            duration_sec=200,
            release_date=datetime(2019, 11, 29),
            explicit=0,
            popularity_score=98.0
        ),
        Track(
            track_name="bad guy",
            artist_id=billie.artist_id,
            album="When We All Fall Asleep",
            genre="alternative",
            duration_sec=194,
            release_date=datetime(2019, 3, 29),
            explicit=0,
            popularity_score=94.0
        ),
    ]
    session.add_all(tracks)
    session.commit()
    print(f"   ✅ Created {len(tracks)} tracks")
    
    # Create Plays
    print("\n→ Creating play events...")
    plays = [
        # Alice plays
        Play(
            play_id="P001",
            user_id="U001",
            track_id=tracks[0].track_id,
            played_at=datetime.now() - timedelta(hours=2),
            played_sec=200,
            completion_rate=100.0,
            device_type="mobile",
            country="US",
            liked=1
        ),
        Play(
            play_id="P002",
            user_id="U001",
            track_id=tracks[1].track_id,
            played_at=datetime.now() - timedelta(hours=1),
            played_sec=150,
            completion_rate=75.0,
            device_type="mobile",
            country="US",
            skip_reason="next_track"
        ),
        # Bob plays
        Play(
            play_id="P003",
            user_id="U002",
            track_id=tracks[2].track_id,
            played_at=datetime.now() - timedelta(minutes=30),
            played_sec=194,
            completion_rate=100.0,
            device_type="desktop",
            country="GB",
            liked=1,
            added_to_playlist=1
        ),
        # Charlie plays
        Play(
            play_id="P004",
            user_id="U003",
            track_id=tracks[1].track_id,
            played_at=datetime.now() - timedelta(minutes=15),
            played_sec=200,
            completion_rate=100.0,
            device_type="smart_speaker",
            country="CA"
        ),
    ]
    session.add_all(plays)
    session.commit()
    print(f"   ✅ Created {len(plays)} play events")


def query_all_users(session):
    """SELECT * FROM users"""
    print("\n" + "=" * 70)
    print("🔍 QUERY 1: All Users")
    print("=" * 70)
    print("SQL: SELECT * FROM users;\n")
    
    users = session.query(User).all()
    for user in users:
        print(f"  {user.user_id} | {user.username:15} | {user.country} | {user.subscription_tier}")
    print(f"\n  Total: {len(users)} users")


def query_with_filter(session):
    """SELECT with WHERE clause"""
    print("\n" + "=" * 70)
    print("🔍 QUERY 2: Premium Users Only")
    print("=" * 70)
    print("SQL: SELECT * FROM users WHERE subscription_tier = 'premium';\n")
    
    premium_users = session.query(User).filter(User.subscription_tier == "premium").all()
    for user in premium_users:
        print(f"  {user.username} - {user.subscription_tier}")
    print(f"\n  Total: {len(premium_users)} premium users")


def query_with_joins(session):
    """Join users and their plays"""
    print("\n" + "=" * 70)
    print("🔍 QUERY 3: Users with Their Play History (JOIN)")
    print("=" * 70)
    print("SQL: SELECT u.username, p.play_id, t.track_name")
    print("     FROM users u JOIN plays p ON u.user_id = p.user_id")
    print("     JOIN tracks t ON p.track_id = t.track_id;\n")
    
    # Using SQLAlchemy relationships (easier way)
    users = session.query(User).all()
    for user in users:
        print(f"\n  👤 {user.username} ({user.subscription_tier}):")
        if user.plays:
            for play in user.plays:
                completion = f"{play.completion_rate:.0f}%" if play.completion_rate else "N/A"
                print(f"     • {play.track.track_name} by {play.track.artist.artist_name} - {completion} completed")
        else:
            print("     (no plays yet)")


def query_aggregates(session):
    """Aggregate functions: COUNT, AVG, SUM"""
    print("\n" + "=" * 70)
    print("🔍 QUERY 4: Aggregate Statistics")
    print("=" * 70)
    
    from sqlalchemy import func
    
    # Count total plays
    total_plays = session.query(func.count(Play.play_id)).scalar()
    print(f"  Total plays: {total_plays}")
    
    # Average completion rate
    avg_completion = session.query(func.avg(Play.completion_rate)).scalar()
    print(f"  Average completion rate: {avg_completion:.1f}%")
    
    # Count plays per user
    print("\n  Plays per user:")
    results = session.query(
        User.username,
        func.count(Play.play_id).label('play_count')
    ).join(Play).group_by(User.username).all()
    
    for username, count in results:
        print(f"     {username}: {count} plays")


def update_record(session):
    """UPDATE operation"""
    print("\n" + "=" * 70)
    print("✏️  UPDATE: Change user subscription")
    print("=" * 70)
    print("SQL: UPDATE users SET subscription_tier = 'premium' WHERE user_id = 'U002';\n")
    
    user = session.query(User).filter(User.user_id == "U002").first()
    if user:
        print(f"  Before: {user.username} - {user.subscription_tier}")
        user.subscription_tier = "premium"
        session.commit()
        print(f"  After:  {user.username} - {user.subscription_tier}")
        print("  ✅ Updated successfully!")


def delete_record(session):
    """DELETE operation"""
    print("\n" + "=" * 70)
    print("🗑️  DELETE: Remove a play event")
    print("=" * 70)
    print("SQL: DELETE FROM plays WHERE play_id = 'P004';\n")
    
    play = session.query(Play).filter(Play.play_id == "P004").first()
    if play:
        print(f"  Deleting: {play}")
        session.delete(play)
        session.commit()
        print("  ✅ Deleted successfully!")
        
        # Verify
        remaining = session.query(Play).count()
        print(f"  Remaining plays: {remaining}")


def main():
    """Main learning flow."""
    print("\n" + "=" * 70)
    print("🎓 SQLAlchemy Learning Session")
    print("   ORM Basics, Sessions, and CRUD Operations")
    print("=" * 70)
    
    # Create a session
    session = get_session()
    
    try:
        # Insert sample data
        insert_sample_data(session)
        
        # Query operations
        query_all_users(session)
        query_with_filter(session)
        query_with_joins(session)
        query_aggregates(session)
        
        # Update operation
        update_record(session)
        
        # Delete operation
        delete_record(session)
        
        print("\n" + "=" * 70)
        print("✅ Session Complete!")
        print("=" * 70)
        print("\nWhat you learned:")
        print("  ✓ Creating database sessions")
        print("  ✓ INSERT: session.add() and session.add_all()")
        print("  ✓ SELECT: session.query().all()")
        print("  ✓ WHERE: .filter()")
        print("  ✓ JOIN: Using relationships")
        print("  ✓ Aggregates: COUNT, AVG, SUM")
        print("  ✓ UPDATE: Modify object and commit")
        print("  ✓ DELETE: session.delete()")
        print("  ✓ Transaction management: commit() and rollback()")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()

