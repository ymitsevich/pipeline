# Music Streaming Database Schema

## Overview

**Star Schema** optimized for analytics and data engineering pipelines. Designed for dimensional modeling with clear fact/dimension separation.

## Schema Diagram

```
┌─────────────┐
│   USERS     │ (Dimension)
├─────────────┤
│ user_id PK  │──┐
│ username    │  │
│ email       │  │
│ country     │  │
│ sub_tier    │  │
│ signup_date │  │
└─────────────┘  │
                 │
┌─────────────┐  │     ┌──────────────┐
│  ARTISTS    │  │     │    PLAYS     │ (Fact)
├─────────────┤  │     ├──────────────┤
│ artist_id PK│──┼────→│ play_id PK   │
│ name        │  │     │ user_id FK   │←──┘
│ genre_pri   │  │     │ track_id FK  │←──┐
│ country     │  │     │ played_at    │   │
│ verified    │  │     │ played_sec   │   │
│ monthly_lis │  │     │ completion_%│   │
└─────────────┘  │     │ device_type  │   │
       ↓         │     │ country      │   │
┌─────────────┐  │     │ skip_reason  │   │
│   TRACKS    │  │     │ liked        │   │
├─────────────┤  │     │ add_playlist │   │
│ track_id PK │──┘     │ source       │   │
│ artist_id FK│        │ ingested_at  │   │
│ track_name  │        └──────────────┘   │
│ album       │                            │
│ genre       │────────────────────────────┘
│ duration    │
│ explicit    │
│ popularity  │
└─────────────┘
```

## Tables

### 🎵 `plays` (Fact Table)
Main transaction table for all listening events.

**Purpose**: Track every song play with user behavior and context.

**Key Fields**:
- `play_id`: Unique identifier (S10001, S10002...)
- `user_id`, `track_id`: Foreign keys to dimensions
- `played_at`: Timestamp (indexed for time-series queries)
- `completion_rate`: Calculated field (played_sec / duration_sec * 100)
- `skip_reason`: Why song ended (null = completed)
- `source`: Data lineage tracking (csv_import, api, kafka_stream)

**Use Cases**:
- User listening patterns
- Track popularity metrics
- Skip rate analysis
- Device usage trends
- Time-based aggregations

---

### 👤 `users` (Dimension Table)
User profile and subscription data.

**Purpose**: Demographic and subscription information for cohort analysis.

**Key Fields**:
- `user_id`: Natural key (U4521, U4522...)
- `subscription_tier`: free, premium, family
- `country`: ISO 2-letter code
- `signup_date`, `last_active`: Engagement tracking

**Use Cases**:
- User segmentation
- Churn analysis
- Country-based analytics
- Subscription tier comparisons

---

### 🎤 `artists` (Dimension Table)
Artist metadata and popularity metrics.

**Purpose**: Artist information for attribution and discovery.

**Key Fields**:
- `artist_id`: Surrogate key (auto-increment)
- `artist_name`: Unique constraint
- `genre_primary`: Main genre classification
- `verified`: Boolean (0/1) for official accounts
- `monthly_listeners`: Popularity metric

**Use Cases**:
- Artist rankings
- Genre trends
- Verified vs indie comparisons

---

### 🎶 `tracks` (Dimension Table)
Song catalog with metadata.

**Purpose**: Track library with rich metadata for filtering/analysis.

**Key Fields**:
- `track_id`: Surrogate key (auto-increment)
- `artist_id`: Foreign key to artists
- `duration_sec`: Track length
- `explicit`: Content rating (0/1)
- `popularity_score`: 0-100 ranking

**Use Cases**:
- Track search/discovery
- Duration analysis
- Explicit content filtering
- Popularity trends

## Design Decisions

### ✅ Why Star Schema?

1. **Simple Joins**: Fact table joins directly to dimensions (no snowflaking)
2. **Query Performance**: Optimized for aggregations and filtering
3. **Easy to Understand**: Clear business entities
4. **Scalable**: Add dimensions without breaking existing queries

### ✅ Surrogate vs Natural Keys

- **Users**: Natural key (`user_id` = U4521) - already unique and stable
- **Artists/Tracks**: Surrogate keys - easier for data pipeline updates

### ✅ Denormalization

- `country` duplicated in `plays` and `users` → Fast filtering without joins
- `genre` in both `tracks` and `artists` → Flexibility in analysis

### ✅ Data Lineage

- `source` field tracks data origin (CSV, API, Kafka)
- `ingested_at` for debugging and reprocessing
- `created_at`, `updated_at` for audit trails

## Sample Queries

```sql
-- Most popular tracks today
SELECT t.track_name, a.artist_name, COUNT(*) as play_count
FROM plays p
JOIN tracks t ON p.track_id = t.track_id
JOIN artists a ON t.artist_id = a.artist_id
WHERE DATE(p.played_at) = CURRENT_DATE
GROUP BY t.track_id, t.track_name, a.artist_name
ORDER BY play_count DESC
LIMIT 10;

-- Skip rate by device type
SELECT 
    device_type,
    COUNT(*) as total_plays,
    SUM(CASE WHEN skip_reason IS NOT NULL THEN 1 ELSE 0 END) as skips,
    ROUND(100.0 * SUM(CASE WHEN skip_reason IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) as skip_rate_pct
FROM plays
GROUP BY device_type
ORDER BY skip_rate_pct DESC;

-- Premium vs Free user engagement
SELECT 
    u.subscription_tier,
    COUNT(DISTINCT p.user_id) as active_users,
    COUNT(p.play_id) as total_plays,
    ROUND(AVG(p.completion_rate), 2) as avg_completion_rate
FROM plays p
JOIN users u ON p.user_id = u.user_id
GROUP BY u.subscription_tier;
```

## Data Pipeline Flow

```
CSV Files          pandas Transform      Database
─────────────      ────────────────      ────────────
users.csv      →   validate/clean    →   users table
artists.csv    →   dedup/enrich      →   artists table
plays_raw.csv  →   normalize/join    →   tracks table
                   calculate fields   →   plays table
```

## Next Steps for Airflow

1. **Extract**: Read CSVs from data lake (S3/local)
2. **Transform**: pandas pipeline (clean, calculate completion_rate)
3. **Load**: Upsert to Postgres with idempotency
4. **Schedule**: Daily at 2 AM UTC
5. **Monitor**: Track row counts, data quality metrics
6. **Alert**: Slack notification on failure

## Indexes (To Add Later)

```sql
CREATE INDEX idx_plays_played_at ON plays(played_at);
CREATE INDEX idx_plays_user_id ON plays(user_id);
CREATE INDEX idx_plays_track_id ON plays(track_id);
CREATE INDEX idx_tracks_artist_id ON tracks(artist_id);
```


