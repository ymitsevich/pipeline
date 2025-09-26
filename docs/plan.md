# 🚀 4-Week Roadmap: Python + Data (No ML)

## 🔹 Week 1 — Python Foundations + Data Basics

**Goals:** Be productive in Python; show you can manipulate data.

**Learning Focus:**
- Syntax, packaging, venv/Poetry, logging, testing (pytest)
- Core libs: requests, json, os, pathlib
- Data wrangling with pandas
- Connect to DB with SQLAlchemy

**Mini-project:** Ingest CSV + API → transform → store in Postgres.

---

## 🔹 Week 2 — Pipelines & Orchestration

**Goals:** Show you can design workflows, not just scripts.

**Learning Focus:**
- Airflow (preferred) or Prefect basics: DAGs, tasks, retries, monitoring
- Scheduling jobs, handling failures
- Learn to dockerize & run locally

**Mini-project:** Daily ETL with Airflow → fetch API → transform with pandas → load into Postgres → notify via Slack/Telegram.

---

## 🔹 Week 3 — Streaming & Scalability

**Goals:** Understand event-driven / streaming pipelines.

**Learning Focus:**
- Kafka (or RabbitMQ) concepts: topics, partitions, producers/consumers, offsets
- Write simple Python producer + consumer
- Store results in DB or data lake (Parquet on disk/S3)

**Mini-project:** Simulate clickstream events → Kafka → consumer → transform → store in Postgres.

---

## 🔹 Week 4 — Cloud & Production-Readiness

**Goals:** Show you can deploy + operate pipelines.

**Learning Focus:**
- Deploy pipeline (Week 2/3) to AWS/GCP/Azure free tier
- Work with S3/BigQuery/Redshift (basic load & query)
- Add monitoring/logging (Prometheus/Grafana or cloud equivalents)

**Mini-project:** Full ETL in cloud: API → transform → S3 (Parquet) → query with BigQuery/Redshift.

---

## 🛠️ How to use Copilot / AI

- Let Copilot write boilerplate (Airflow DAG, Kafka client code)
- Force yourself to rewrite one version manually — you'll learn debugging this way
- Use AI for "teach me tradeoffs" questions, not just code gen

---

## 🎯 Outcome after 4 Weeks

- GitHub with 2–3 small but end-to-end projects (batch ETL, streaming, cloud deploy)
- Ability to talk through pipelines, orchestration, data stores, and scaling tradeoffs
- Positioning: "Senior Backend Engineer → now focused on Python + Data Engineering (pipelines, orchestration, cloud)"
- Ready to apply to Senior Backend/Data Engineer roles, not "junior Python dev"

---

*Last Updated: September 25, 2025*  
*Status: In Progress - Week 1*