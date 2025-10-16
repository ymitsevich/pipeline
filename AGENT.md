# UI Agent Handbook

Unified guidance for any UI-based AI assistant working on the Pipeline project. This is the single source of truth for context, workflows, and collaboration expectations.

## Project Snapshot
- Modern Python data engineering stack focused on music streaming analytics.
- Core code in `src/pipeline/`; data and orchestration assets live under `data/`, `docs/`, and `scripts/`.
- Star-schema PostgreSQL database (see `src/pipeline/database.py`) with fact `plays` and dimension tables for users, artists, and tracks.
- Docker Compose provides local services; Poetry/Makefile manage dependencies and commands.

## Core Workflows
- **Environment setup**: `make dev-setup` then `make health` to validate.
- **Testing**: Run `make test` (pytest + coverage). Keep fixtures in `tests/conftest.py` in mind before adding new tests.
- **Quality checks**: `make audit` runs black, isort, flake8, and mypy; keep the codebase passing before handing work back.

## Development Conventions
- SQLAlchemy models inherit from `Base`, include `created_at`/`updated_at`, and use integer flags instead of booleans.
- Database access goes through `SessionLocal` context managers with explicit commits.
- Rely on environment variables for sensitive configuration, with defaults in `stage.json`.
- Logging is structured (JSON) and should carry correlation IDs for traceability.
- Service layer lives under `pipeline/services/`. The ingestion flow is composed of dedicated services (`IngestionService`, `PlaybackCursorProvider`, enrichment, and persistence). Extend functionality by adding or composing services rather than expanding entrypoints.
- Incremental ingest derives its cursor from Postgres (`MAX(plays.played_at)`); avoid reintroducing filesystem state unless explicitly requested.
- Functions should stay short (≈30 lines max) and rely on guard clauses—avoid `else`/`elif` chains by returning early.

## Collaboration Guidelines
- **Plan-first rule**: Before changing files or executing commands that modify project state, present a concise summary of the intended changes to the user. The summary must be visible in the conversation; no confirmation is required unless the user asks.
- When suggesting AI-assisted code generation, prefer boilerplate or repetitive sections; encourage manual review for complex logic.
- Mention relevant learning milestones or roadmap context when it affects suggested changes (see `docs/plan.md`).

## Reference Materials
- Detailed roadmap and study plan: `docs/plan.md`
- Historical Copilot guidance (now superseded by this document): `.github/copilot-instructions.md`
- Makefile targets and scripts: `Makefile`, `scripts/`
