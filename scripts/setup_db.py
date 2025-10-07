#!/usr/bin/env python
"""
Database setup and management utilities.
Use this for local development and testing only.
"""
import sys
import os

# Add parent directory to path so we can import pipeline
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline.database import Base, engine


def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def drop_all_tables():
    """Drop all tables (use with caution!)"""
    env = os.getenv('ENVIRONMENT', os.getenv('ENV', 'development'))
    
    if env == 'production':
        print("❌ Cannot drop tables in production!")
        sys.exit(1)
    
    print("⚠️  WARNING: This will delete ALL tables and data!")
    confirm = input("Type 'yes' to confirm: ")
    
    if confirm.lower() != 'yes':
        print("❌ Operation cancelled")
        sys.exit(0)
    
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped!")


def reset_db():
    """Drop all tables and recreate them (fresh start)."""
    env = os.getenv('ENVIRONMENT', os.getenv('ENV', 'development'))
    
    if env == 'production':
        print("❌ Cannot reset database in production!")
        sys.exit(1)
    
    print("⚠️  WARNING: This will delete ALL data and recreate tables!")
    confirm = input("Type 'yes' to confirm: ")
    
    if confirm.lower() != 'yes':
        print("❌ Operation cancelled")
        sys.exit(0)
    
    Base.metadata.drop_all(bind=engine)
    print("🗑️  Tables dropped")
    
    Base.metadata.create_all(bind=engine)
    print("✅ Database reset complete!")


def show_help():
    """Display help message."""
    print("""
Database Setup Utility

Usage:
    python scripts/setup_db.py <command>

Commands:
    init      Create all database tables
    drop      Drop all tables (prompts for confirmation)
    reset     Drop and recreate all tables (prompts for confirmation)
    help      Show this help message

Examples:
    python scripts/setup_db.py init
    python scripts/setup_db.py reset
    """)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'init':
        init_db()
    elif command == 'drop':
        drop_all_tables()
    elif command == 'reset':
        reset_db()
    elif command == 'help':
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        sys.exit(1)

