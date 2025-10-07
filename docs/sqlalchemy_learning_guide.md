# SQLAlchemy Learning Guide

Complete hands-on guide for your learning session (Sun, 5 Oct 2025, 10:45-12:15)

## Prerequisites

- Docker and Docker Compose installed
- Python 3.9+ with dependencies from requirements.txt

## Step-by-Step Instructions

### Step 1: Start Postgres Container (2 min)

```bash
# Start only the Postgres service
docker compose up -d postgres

# Verify it's running
docker compose ps

# Check logs (optional)
docker compose logs postgres
```

**What's happening:**
- Docker starts a PostgreSQL 15 container
- It's accessible on `localhost:15432` (external) or `postgres:5432` (internal)
- Database: `pipeline`, User: `postgres`, Password: `postgres`

---

### Step 2: Create Database Tables (1 min)

```bash
# Set environment variables for local connection
export DB_HOST=localhost
export DB_PORT=15432

# Create all tables from your models
python scripts/setup_db.py init
```

**What's happening:**
- Reads models from `src/pipeline/database.py`
- Generates CREATE TABLE SQL for: users, artists, tracks, plays
- Executes them in the correct order (respecting foreign keys)

**Expected output:**
```
✅ Database tables created successfully!
```

---

### Step 3: Run the Learning Script (15-20 min)

```bash
# Run the comprehensive SQLAlchemy tutorial
DB_HOST=localhost DB_PORT=15432 python scripts/learn_sqlalchemy.py
```

**What you'll see:**

1. **INSERT operations** - Creating users, artists, tracks, and plays
2. **SELECT queries** - Basic selects and filters
3. **JOIN queries** - Combining tables using relationships
4. **Aggregate functions** - COUNT, AVG, SUM
5. **UPDATE** - Modifying records
6. **DELETE** - Removing records

**Expected output:** ~70 lines showing all operations with data

---

### Step 4: Explore Interactively (30-40 min)

#### Option A: Python REPL

```bash
# Start Python with proper environment
DB_HOST=localhost DB_PORT=15432 python
```

```python
# Import everything you need
from src.pipeline.database import get_session, User, Artist, Track, Play
from sqlalchemy import func

# Create a session
session = get_session()

# Try queries yourself
users = session.query(User).all()
print(users)

# Count plays per user
results = session.query(
    User.username,
    func.count(Play.play_id).label('play_count')
).join(Play).group_by(User.username).all()

for username, count in results:
    print(f"{username}: {count} plays")

# Always close when done
session.close()
```

#### Option B: Use psql (SQL directly)

```bash
# Connect to Postgres
docker compose exec postgres psql -U postgres -d pipeline

# Or from host:
psql -h localhost -p 15432 -U postgres -d pipeline
```

```sql
-- See all tables
\dt

-- Query users
SELECT * FROM users;

-- Join query
SELECT u.username, t.track_name, p.completion_rate
FROM users u
JOIN plays p ON u.user_id = p.user_id
JOIN tracks t ON p.track_id = t.track_id;

-- Exit
\q
```

---

## Key Concepts to Practice

### 1. **Sessions** (The Database Conversation)

```python
from src.pipeline.database import get_session

session = get_session()
try:
    # Do work
    session.commit()
except Exception:
    session.rollback()
finally:
    session.close()
```

**Think of it as:** Opening a conversation with the database, doing work, then closing it.

### 2. **ORM vs Core**

**ORM (Object-Relational Mapping) - High level:**
```python
# Work with Python objects
user = User(user_id="U999", username="newuser", ...)
session.add(user)
session.commit()
```

**Core - Lower level (closer to SQL):**
```python
# Direct SQL expression
from sqlalchemy import insert
stmt = insert(User).values(user_id="U999", username="newuser")
session.execute(stmt)
```

### 3. **Relationships** (Automatic JOINs)

```python
# Instead of manual JOIN, use relationships
user = session.query(User).filter(User.user_id == "U001").first()

# Automatically fetches related plays
for play in user.plays:
    print(play.track.track_name)  # Follows play -> track relationship
```

### 4. **Common Query Patterns**

```python
# Get all
users = session.query(User).all()

# Get one
user = session.query(User).filter(User.user_id == "U001").first()

# Get or None
user = session.query(User).get("U001")

# Filter
premium = session.query(User).filter(User.subscription_tier == "premium").all()

# Multiple filters (AND)
results = session.query(User).filter(
    User.country == "US",
    User.subscription_tier == "premium"
).all()

# OR condition
from sqlalchemy import or_
results = session.query(User).filter(
    or_(User.country == "US", User.country == "CA")
).all()

# Order by
users = session.query(User).order_by(User.username).all()

# Limit
top_5 = session.query(Play).limit(5).all()
```

---

## Practice Exercises (Remaining Time)

Try implementing these queries yourself:

1. **Find all tracks by "The Weeknd"**
   - Hint: Join Track and Artist

2. **Calculate total listening time per user**
   - Hint: SUM of played_sec grouped by user_id

3. **Find users who liked at least one song**
   - Hint: JOIN with Play where liked = 1

4. **Most popular track** (most plays)
   - Hint: COUNT plays grouped by track_id

5. **Add a new user and their first play**
   - Practice INSERT with relationships

---

## Cleanup

```bash
# When done, stop Postgres
docker compose down

# To completely reset (delete all data)
docker compose down -v  # Removes volumes too
```

---

## Troubleshooting

### Can't connect to database
```bash
# Check Postgres is running
docker compose ps

# Check logs
docker compose logs postgres

# Ensure environment variables are set
echo $DB_HOST $DB_PORT
```

### Tables already exist
```bash
# Reset database (destroys all data)
DB_HOST=localhost DB_PORT=15432 python scripts/setup_db.py reset
```

### See generated SQL
Edit `src/pipeline/database.py` line 28:
```python
echo=True  # Shows all SQL queries in logs
```

---

## Next Steps (Tomorrow's Session)

- Mon, 6 Oct: Deep dive into SQL joins and window functions
- Then: SQLAlchemy CRUD, upserts, sessions lifecycle
- Later: Connect Airflow to this database

---

## Quick Reference

| Task | Command |
|------|---------|
| Start DB | `docker compose up -d postgres` |
| Create tables | `DB_HOST=localhost DB_PORT=15432 python scripts/setup_db.py init` |
| Run learning script | `DB_HOST=localhost DB_PORT=15432 python scripts/learn_sqlalchemy.py` |
| Reset DB | `DB_HOST=localhost DB_PORT=15432 python scripts/setup_db.py reset` |
| Connect with psql | `psql -h localhost -p 15432 -U postgres -d pipeline` |
| Stop DB | `docker compose down` |

**Password:** `postgres` (if prompted)

