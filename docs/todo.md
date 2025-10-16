# 4-Week Day-by-Day Plan: Python + Data Engineering (Oct 1 – Nov 7, 2025)

Busy (avoid scheduling): 07:30–08:45, 13:15–13:50, 14:50–16:00 (Mon–Fri)

Note: You already completed Python syntax, packaging, and core `json`. The plan skips these.

**Schedule updated on Oct 15 to catch up from delays; new end date Nov 7 with Nov 8–9 reserved as buffer.**

## ✅ Wed, 1 Oct 2025
- ✅ 09:00–10:30: Python logging essentials; structured logs; log levels; handlers

## ✅ Thu, 2 Oct 2025
- ✅ 09:00–10:30: Python environments (venv/virtualenv): create, activate, per-project deps, freeze
- ✅ 10:45–12:15: pytest basics; test discovery, fixtures, parametrize; write 3 sample tests
- ✅ 12:30–13:10: `requests` essentials; timeouts, retries, error handling; small API script
- ✅ 16:15–17:30: File/OS: `pathlib`, `os`, env vars; project layout for data tasks

## ✅ Fri, 3 Oct 2025
- ✅ 09:00–10:30: `pandas` intro: Series/DataFrame, indexing, selection
- ✅ 09:00–10:30: pandas IO: `read_csv`, `to_csv`, types, parsing dates; basic transforms

## ✅ Sun, 5 Oct 2025
- ✅ 10:45–12:15: SQLAlchemy ORM/Core overview; models, sessions; local Postgres via Docker
- 🔁 Rescheduled to Wed, 15 Oct 2025 09:00–10:30: `pandas` transforms: groupby, joins/merge, reshape; small exercises

## 🔄 Wed, 15 Oct 2025 (TODAY — Resume Here)
- 09:00–10:30: `pandas` transforms: groupby, joins/merge, reshape; small exercises
- 10:45–12:15: Postgres (Docker): start DB, psql basics, SQL joins + window intro
- 16:15–17:30: SQLAlchemy: connect and CRUD; create tables and insert sample data

## Thu, 16 Oct 2025
- 09:00–10:30: SQLAlchemy: upserts (ON CONFLICT), sessions lifecycle, engine pooling
- 10:45–12:15: Mini-project setup: CSV ingest → transform → Postgres schema design
- 16:15–17:30: Implement CSV ingest + transforms (pandas); validate with tests

## Fri, 17 Oct 2025
- 09:00–10:30: Load to Postgres with SQLAlchemy; idempotency keys
- 10:45–12:15: API ingest (`requests`); pagination, rate limits; merge with CSV dataset
- 16:15–17:30: Mini-project: end-to-end run; add logging; basic CLI entry point

## Sat, 18 Oct 2025
- 09:00–10:30: Docs: mini-project README; capture decisions and next steps
- 10:45–12:15: Mini-project polish: tests, configs, packaging review
- 14:00–15:30: Prep for Airflow week: recap concepts, outline DAG tasks

## Sun, 19 Oct 2025
- 10:00–12:00: Optional catch-up or rest
- 14:00–15:30: Light review of Airflow terminology and UI tour videos

## Mon, 20 Oct 2025
- 09:00–10:30: Airflow concepts: DAGs, tasks, scheduler, web UI
- 10:45–12:15: Run Airflow locally (Docker Compose); create first DAG
- 16:15–17:30: Airflow DAG: convert mini-project into tasks; set dependencies

## Tue, 21 Oct 2025
- 09:00–10:30: Airflow robustness: retries, timeouts, failure callbacks
- 10:45–12:15: Airflow connections/variables; secrets via env; parameterize DAG
- 16:15–17:30: Airflow schedules and backfills; SLAs; manual trigger practice

## Wed, 22 Oct 2025
- 09:00–10:30: Airflow observability: task logs, XComs; simple metrics export
- 10:45–12:15: Airflow notifications: Slack/Telegram on failure (local webhook)
- 16:15–17:30: Airflow DAG integration tests; document runbook

## Thu, 23 Oct 2025
- 09:00–10:30: Airflow testing: dagbag import test, unit tests with pytest
- 10:45–12:15: Airflow: finalize ETL; clean configs; ensure reproducibility
- 16:15–17:30: PySpark intro: why Spark? RDDs vs DataFrames; local setup (Docker/standalone)

## Fri, 24 Oct 2025
- 09:00–10:30: PySpark DataFrames: read CSV/Parquet; select, filter, groupBy, joins
- 10:45–12:15: PySpark transformations: UDFs, window functions; lazy evaluation
- 16:15–17:30: PySpark actions & performance: collect, write; partitioning basics

## Sat, 25 Oct 2025
- 09:00–10:30: Kafka streaming concepts: topics, partitions, offsets, consumer groups
- 10:45–12:15: Kafka/Redpanda: run locally; CLI basics; create topic(s)
- 14:00–15:30: Kafka: define event schema for simulated clickstream

## Sun, 26 Oct 2025
- 10:00–12:00: Optional catch-up or rest
- 14:00–15:30: Plan producer/consumer interface contracts

## Mon, 27 Oct 2025
- 09:00–10:30: Kafka producer: generate events; keys/partitions; delivery guarantees
- 10:45–12:15: Kafka producer: rate control, batching; error handling and retries
- 16:15–17:30: Kafka producer: metrics/logs; write basic tests

## Tue, 28 Oct 2025
- 09:00–10:30: Kafka consumer: subscribe, poll loop, commit strategies
- 10:45–12:15: Kafka consumer: transform and persist to Postgres or Parquet (local lake)
- 16:15–17:30: Kafka consumer: handle duplicates/idempotency; checkpointing; smoke tests

## Wed, 29 Oct 2025
- 09:00–10:30: Kafka consumer reliability: lag monitoring in code
- 10:45–12:15: Kafka producer/consumer soak test: throughput and backpressure checks
- 16:15–17:30: Parquet sink: write partitioned files with pandas/pyarrow; validate

## Thu, 30 Oct 2025
- 09:00–10:30: Kafka end-to-end demo: producer → Kafka → consumer → store
- 10:45–12:15: Spark Streaming intro: DStreams vs Structured Streaming; micro-batches
- 16:15–17:30: Spark Structured Streaming: read from Kafka; basic transformations

## Fri, 31 Oct 2025
- 09:00–10:30: Spark Structured Streaming: window operations; watermarks; stateful processing
- 10:45–12:15: Spark Streaming sinks: write to Parquet, Postgres; checkpointing
- 16:15–17:30: Spark Streaming: mini-project (Kafka → Spark → store); compare with custom consumer

## Sat, 1 Nov 2025
- 09:00–10:30: Docker: containerize Spark jobs; multi-stage builds; resource configs
- 10:45–12:15: Docker Compose: integrate Spark, Airflow, Kafka; orchestrate full stack
- 14:00–15:30: Cloud prep: AWS/GCP account setup; IAM basics; S3/GCS bucket creation

## Sun, 2 Nov 2025
- 10:00–12:00: Optional catch-up or rest
- 14:00–15:30: Outline cloud deployment runbook and checklist

## Mon, 3 Nov 2025
- 09:00–10:30: Cloud storage: upload data to S3/GCS; read with pandas and Spark
- 10:45–12:15: Cloud databases: RDS/Cloud SQL Postgres; connection from local scripts
- 16:15–17:30: Deploy simple ETL: scheduled script on EC2/Compute Engine or Cloud Functions

## Tue, 4 Nov 2025
- 09:00–10:30: Cloud Airflow: Managed Composer/MWAA or self-hosted on cloud VM
- 10:45–12:15: Cloud monitoring: CloudWatch/Stackdriver logs; basic alerts
- 16:15–17:30: Cloud costs: review bill; optimization strategies; free tier limits

## Wed, 5 Nov 2025
- 09:00–10:30: Final project planning: design end-to-end pipeline (batch + streaming)
- 10:45–12:15: Final project: implement batch component (Airflow + Spark/pandas → cloud storage)
- 16:15–17:30: Final project: implement streaming component (Kafka → Spark/consumer → storage)

## Thu, 6 Nov 2025
- 09:00–10:30: Final project: testing, error handling, logging; end-to-end validation
- 10:45–12:15: Final project: documentation (architecture, setup, tradeoffs)
- 16:15–17:30: Final project: deploy to cloud; verify scheduled runs

## Fri, 7 Nov 2025
- 09:00–10:30: Repo polish: README, Makefile, requirements; clear setup instructions
- 10:45–12:15: Portfolio prep: write clear project descriptions; highlight key decisions
- 16:15–17:30: Reflection + next steps: gaps to fill; topics to deepen; interview prep outline

## Sat, 8 Nov 2025
- 10:00–12:00: Buffer/review day — tidy loose ends or additional practice
- 14:00–15:30: Optional demo recording or blog draft

## Sun, 9 Nov 2025
- 10:00–12:00: Rest or catch-up
- 14:00–15:30: Plan post-roadmap learning focus
