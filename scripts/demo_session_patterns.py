#!/usr/bin/env python
"""
Demonstration: SQLAlchemy Session as Unit of Work and Entity Manager
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline.database import get_session, User, Play
from datetime import datetime

print("=" * 70)
print("SQLAlchemy Session: Unit of Work + Entity Manager Pattern")
print("=" * 70)

# ============================================================================
# ENTITY MANAGER PATTERN
# ============================================================================
print("\n📦 ENTITY MANAGER Pattern")
print("   Session manages the lifecycle of entities (objects)")
print("-" * 70)

session = get_session()

# Create a new user (Transient state)
user = User(
    user_id="U999",
    username="demo_user",
    email="demo@example.com",
    country="US",
    subscription_tier="premium",
    signup_date=datetime.now()
)
print(f"\n1. New object created: {user}")
print(f"   In session? {user in session}")
print(f"   State: TRANSIENT (not tracked by session)")

# Add to session (Pending state)
session.add(user)
print(f"\n2. After session.add(user)")
print(f"   In session? {user in session}")
print(f"   State: PENDING (tracked, but not in DB yet)")

# Commit (Persistent state)
try:
    session.commit()
    print(f"\n3. After session.commit()")
    print(f"   In session? {user in session}")
    print(f"   State: PERSISTENT (tracked AND in DB)")
    print(f"   Has ID? {user.user_id}")
except Exception as e:
    session.rollback()
    print(f"   (Skipped - user might already exist)")

# Modify object (Dirty state)
user.subscription_tier = "family"
print(f"\n4. After modifying user.subscription_tier")
print(f"   State: DIRTY (tracked, in DB, but has uncommitted changes)")
print(f"   Session knows it's dirty!")

# ============================================================================
# UNIT OF WORK PATTERN
# ============================================================================
print("\n\n🔄 UNIT OF WORK Pattern")
print("   Session batches multiple operations into a single transaction")
print("-" * 70)

print("\n   Session tracks ALL changes until you commit:")
print("   ┌──────────────────────────────────────┐")
print("   │  Session (Unit of Work)              │")
print("   ├──────────────────────────────────────┤")
print("   │  • New objects to INSERT             │")
print("   │  • Modified objects to UPDATE        │")
print("   │  • Deleted objects to DELETE         │")
print("   │  • Identity map (cache)              │")
print("   └──────────────────────────────────────┘")

# Example: Multiple operations in one transaction
print("\n   Example: Multiple operations batched together:")

try:
    # Operation 1: Update user
    user.last_active = datetime.now()
    print("   1. Modified user.last_active")
    
    # Operation 2: Add another user
    user2 = User(
        user_id="U998",
        username="another_user",
        email="another@example.com",
        country="CA",
        subscription_tier="free",
        signup_date=datetime.now()
    )
    session.add(user2)
    print("   2. Added new user")
    
    # Nothing hit the database yet!
    print("\n   ⏸️  No SQL executed yet! Everything is in memory.")
    print("   💾 Session is tracking 2 operations...")
    
    # Now commit - BOTH operations execute in ONE transaction
    session.commit()
    print("\n   ✅ session.commit() executed:")
    print("      - UPDATE users SET last_active = ... WHERE user_id = 'U999'")
    print("      - INSERT INTO users (...) VALUES (...)")
    print("      - Both succeed or both fail (atomicity)")
    
except Exception as e:
    session.rollback()
    print(f"\n   ❌ If ANY operation fails, ALL are rolled back!")
    print(f"      This is the Unit of Work guarantee!")

# ============================================================================
# IDENTITY MAP (Part of Entity Manager)
# ============================================================================
print("\n\n🗺️  IDENTITY MAP Pattern")
print("   Session caches objects - same ID = same Python object")
print("-" * 70)

try:
    # Query for user twice
    user_ref1 = session.query(User).filter(User.user_id == "U999").first()
    user_ref2 = session.query(User).filter(User.user_id == "U999").first()
    
    print(f"\n   First query:  {id(user_ref1)} (memory address)")
    print(f"   Second query: {id(user_ref2)} (memory address)")
    print(f"\n   Same object? {user_ref1 is user_ref2}")
    print("\n   ✅ Yes! Session returns the SAME Python object")
    print("      This prevents duplicate objects and data inconsistencies")
except Exception:
    print("   (Demo user not in DB)")

session.close()

# ============================================================================
# COMPARISON TO OTHER PATTERNS
# ============================================================================
print("\n\n📚 Pattern Comparison")
print("=" * 70)

patterns = [
    ("Unit of Work", "✅", "Batches operations, tracks changes, atomic commits"),
    ("Entity Manager", "✅", "Manages entity lifecycle (transient → persistent)"),
    ("Identity Map", "✅", "Caches objects, ensures one instance per ID"),
    ("Repository", "⚠️", "Not built-in, but you can build on top of Session"),
    ("Data Mapper", "✅", "Separates domain objects from database logic"),
]

print("\n Pattern              | SQLAlchemy | Description")
print("-" * 70)
for pattern, support, desc in patterns:
    print(f" {pattern:18} | {support:10} | {desc}")

print("\n\n💡 Key Takeaways:")
print("-" * 70)
print("1. Session = Unit of Work: Batches changes, commits atomically")
print("2. Session = Entity Manager: Tracks object lifecycle")
print("3. Session = Identity Map: Caches objects for consistency")
print("4. Always follow the pattern:")
print("   - Open session")
print("   - Do work (add, query, modify)")
print("   - Commit or rollback")
print("   - Close session")
print("=" * 70)

