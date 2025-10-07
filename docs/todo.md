# 4-Week Day-by-Day Plan: Python + Data Engineering (Oct 1–28, 2025)

Busy (avoid scheduling): 07:30–08:45, 13:15–13:50, 14:50–16:00 (Mon–Fri)

Note: You already completed Python syntax, packaging, and core `json`. The plan skips these.

**Schedule updated on Oct 5 to add Spark and extend to Oct 28. Content redistributed for natural knowledge flow.**

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

## Sun, 5 Oct 2025 (TODAY - Resume from here)
- ✅ 10:45–12:15: SQLAlchemy ORM/Core overview; models, sessions; local Postgres via Docker
- 14:00–15:30: `pandas` transforms: groupby, joins/merge, reshape; small exercises

## Mon, 6 Oct 2025
- 09:00–10:30: Postgres (Docker): start DB, psql basics, SQL joins + window intro
- 10:45–12:15: SQLAlchemy: Connect and CRUD; create tables and insert sample data
- 16:15–17:30: SQLAlchemy: upserts (ON CONFLICT), sessions lifecycle, engine pooling

## Tue, 7 Oct 2025
- 09:00–10:30: Mini-project setup: CSV ingest → transform → Postgres schema design
- 10:45–12:15: Implement CSV ingest + transforms (pandas); validate with tests
- 16:15–17:30: Load to Postgres with SQLAlchemy; idempotency keys

## Wed, 8 Oct 2025
- 09:00–10:30: API ingest (`requests`); pagination, rate limits; merge with CSV dataset
- 10:45–12:15: Mini-project: end-to-end run; add logging; basic CLI entry point
- 16:15–17:30: Docs: mini-project README; capture decisions and next steps

## Thu, 9 Oct 2025
- 09:00–10:30: Airflow concepts: DAGs, tasks, scheduler, web UI
- 10:45–12:15: Run Airflow locally (Docker Compose); create first DAG
- 16:15–17:30: Airflow DAG: convert mini-project into tasks; set dependencies

## Fri, 10 Oct 2025
- 09:00–10:30: Airflow robustness: retries, timeouts, failure callbacks
- 10:45–12:15: Airflow connections/variables; secrets via env; parameterize DAG
- 16:15–17:30: Airflow schedules and backfills; SLAs; manual trigger practice

## Sat, 11 Oct 2025
- 09:00–10:30: Airflow observability: task logs, XComs; simple metrics export
- 10:45–12:15: Airflow notifications: Slack/Telegram on failure (local webhook)
- 14:00–15:30: Airflow DAG integration tests; document runbook

## Mon, 13 Oct 2025
- 09:00–10:30: Airflow testing: dagbag import test, unit tests with pytest
- 10:45–12:15: Airflow: finalize ETL; clean configs; ensure reproducibility
- 16:15–17:30: PySpark intro: why Spark? RDDs vs DataFrames; local setup (Docker/standalone)

## Tue, 14 Oct 2025
- 09:00–10:30: PySpark DataFrames: read CSV/Parquet; select, filter, groupBy, joins
- 10:45–12:15: PySpark transformations: UDFs, window functions; lazy evaluation
- 16:15–17:30: PySpark actions & performance: collect, write; partitioning basics

## Wed, 15 Oct 2025
- 09:00–10:30: Kafka streaming concepts: topics, partitions, offsets, consumer groups
- 10:45–12:15: Kafka/Redpanda: run locally; CLI basics; create topic(s)
- 16:15–17:30: Kafka: define event schema for simulated clickstream

## Thu, 16 Oct 2025
- 09:00–10:30: Kafka producer: generate events; keys/partitions; delivery guarantees
- 10:45–12:15: Kafka producer: rate control, batching; error handling and retries
- 16:15–17:30: Kafka producer: metrics/logs; write basic tests

## Fri, 17 Oct 2025
- 09:00–10:30: Kafka consumer: subscribe, poll loop, commit strategies
- 10:45–12:15: Kafka consumer: transform and persist to Postgres or Parquet (local lake)
- 16:15–17:30: Kafka consumer: handle duplicates/idempotency; checkpointing; smoke tests

## Sat, 18 Oct 2025
- 09:00–10:30: Kafka consumer reliability: commit strategies and lag monitoring in code
- 10:45–12:15: Kafka producer/consumer soak test: throughput and backpressure checks
- 14:00–15:30: Parquet sink: write partitioned files with pandas/pyarrow; validate

## Mon, 20 Oct 2025
- 09:00–10:30: Kafka end-to-end demo: producer → Kafka → consumer → store
- 10:45–12:15: Spark Streaming intro: DStreams vs Structured Streaming; micro-batches
- 16:15–17:30: Spark Structured Streaming: read from Kafka; basic transformations

## Tue, 21 Oct 2025
- 09:00–10:30: Spark Structured Streaming: window operations; watermarks; stateful processing
- 10:45–12:15: Spark Streaming sinks: write to Parquet, Postgres; checkpointing
- 16:15–17:30: Spark Streaming: mini-project (Kafka → Spark → store); compare with custom consumer

## Wed, 22 Oct 2025
- 09:00–10:30: Docker: containerize Spark jobs; multi-stage builds; resource configs
- 10:45–12:15: Docker Compose: integrate Spark, Airflow, Kafka; orchestrate full stack
- 16:15–17:30: Cloud prep: AWS/GCP account setup; IAM basics; S3/GCS bucket creation

## Thu, 23 Oct 2025
- 09:00–10:30: Cloud storage: upload data to S3/GCS; read with pandas and Spark
- 10:45–12:15: Cloud databases: RDS/Cloud SQL Postgres; connection from local scripts
- 16:15–17:30: Deploy simple ETL: scheduled script on EC2/Compute Engine or Cloud Functions

## Fri, 24 Oct 2025
- 09:00–10:30: Cloud Airflow: Managed Composer/MWAA or self-hosted on cloud VM
- 10:45–12:15: Cloud monitoring: CloudWatch/Stackdriver logs; basic alerts
- 16:15–17:30: Cloud costs: review bill; optimization strategies; free tier limits

## Sat, 25 Oct 2025
- 09:00–10:30: Final project planning: design end-to-end pipeline (batch + streaming)
- 10:45–12:15: Final project: implement batch component (Airflow + Spark/pandas → cloud storage)
- 14:00–15:30: Final project: implement streaming component (Kafka → Spark/consumer → storage)

## Mon, 27 Oct 2025
- 09:00–10:30: Final project: testing, error handling, logging; end-to-end validation
- 10:45–12:15: Final project: documentation (architecture, setup, tradeoffs)
- 16:15–17:30: Final project: deploy to cloud; verify scheduled runs

## Tue, 28 Oct 2025
- 09:00–10:30: Repo polish: README, Makefile, requirements; clear setup instructions
- 10:45–12:15: Portfolio prep: write clear project descriptions; highlight key decisions
- 16:15–17:30: Reflection + next steps: gaps to fill; topics to deepen; interview prep outline

---

Tips
- Keep sessions focused; if you finish early, write a 5–10 line note on what you learned
- Prefer small end-to-end wins over breadth; ship something daily
- Use tests to lock in behavior before refactors

