# 🚀 4-Week Roadmap: Python + Data Engineering (No ML)

## 🎵 Real Project — Music Pulse (Listening Analytics)

- **Objective**: Build an end-to-end pipeline that ingests listening events, enriches with track/artist info, computes daily stats, and exports Parquet snapshots.
- **Data source**: ListenBrainz public listens (e.g., `user/iliekcomputers` (curl -sI "https://listenbrainz.org/user/iliekcomputers" | head -n1) or `latest` endpoint); fallback to a small synthetic generator if offline.
e.g. curl "https://api.listenbrainz.org/1/user/iliekcomputers/listens?count=3"
- **Minimal schema**:
  - `listen_events`: `user_id`, `played_at_ts`, `track`, `artist`, `album`, `source`
  - `tracks`: `track_id`, `track_name`, `artist_id`, `album`
  - `artists`: `artist_id`, `artist_name`
  - `daily_aggregates`: `day`, `metric`, `dimension`, `value`
- **Week 1 MVP**:
  - Fetch listens JSON → normalize to CSV (`listen_events`)
  - pandas transforms: dedupe, parse timestamps, derive `day`
  - Compute daily top artists/tracks and minutes listened
  - Load to Postgres via SQLAlchemy + export Parquet to `data/warehouse/`
- **Weeks 2–4 mapping**:
  - Week 2: Airflow DAG (daily batch) and Spark re-implementation of key transforms
  - Week 3: Kafka stream of listens; rolling 5-minute “now trending” aggregates; DB/Parquet sinks
  - Week 4: Push Parquet to S3/GCS; run against cloud DB; schedule and monitor

## 🔹 Week 1 — Python Foundations + Data Basics

**Goals:** Be productive in Python; show you can manipulate data.

**Learning Focus:**
- Syntax, packaging, venv/Poetry, logging, testing (pytest)
- Core libs: requests, json, os, pathlib
- Data wrangling with pandas
- Connect to DB with SQLAlchemy

**Mini-project:** Ingest CSV + API → transform → store in Postgres.

---

## 🔹 Week 2 — Orchestration + Distributed Processing

**Goals:** Show you can design workflows and understand distributed computing.

**Learning Focus:**
- Airflow: DAGs, tasks, retries, monitoring, scheduling
- PySpark: distributed data processing with DataFrames
- Batch processing patterns at scale
- Dockerize & run locally

**Mini-project:** Daily ETL with Airflow → fetch API → transform with pandas/Spark → load into Postgres.

---

## 🔹 Week 3 — Streaming Pipelines

**Goals:** Understand event-driven / streaming pipelines and processing.

**Learning Focus:**
- Kafka: topics, partitions, producers/consumers, offsets
- Write simple Python producer + consumer
- Spark Structured Streaming: read from Kafka, transformations, sinks
- Stateful stream processing and checkpointing
- Store results in DB or data lake (Parquet on disk/S3)

**Mini-project:** Simulate clickstream events → Kafka → Spark Streaming → transform → store in Postgres.

---

## 🔹 Week 4 — Cloud & Production-Readiness

**Goals:** Show you can deploy + operate pipelines in the cloud.

**Learning Focus:**
- Deploy pipeline (Week 2/3) to AWS/GCP free tier
- Work with S3/GCS and cloud databases (RDS, Cloud SQL)
- Containerize and orchestrate full stack (Docker Compose)
- Cloud monitoring/logging (CloudWatch, Stackdriver)
- Build comprehensive end-to-end project

**Mini-project:** Full pipeline in cloud: batch ETL (Airflow + Spark) + streaming (Kafka + Spark Streaming) → cloud storage → monitoring.

---

## 🛠️ How to use Copilot / AI

- Let Copilot write boilerplate (Airflow DAG, Kafka client code)
- Force yourself to rewrite one version manually — you'll learn debugging this way
- Use AI for "teach me tradeoffs" questions, not just code gen

---

## 🎯 Outcome after 4 Weeks

- GitHub with 2–3 small but end-to-end projects (batch ETL, streaming, cloud deploy)
- **Tech stack:** Python, pandas, PySpark, SQLAlchemy, Postgres, Airflow, Kafka, Spark Streaming, Docker, AWS/GCP
- Ability to talk through pipelines, orchestration, data stores, distributed processing, and scaling tradeoffs
- Understand when to use pandas vs Spark, custom consumers vs Spark Streaming
- Positioning: "Senior Backend Engineer → now focused on Python + Data Engineering (pipelines, orchestration, distributed processing, cloud)"
- Ready to apply to Senior Backend/Data Engineer roles, not "junior Python dev"

---

*Last Updated: October 5, 2025*  
*Status: In Progress - Week 1, Day 5*