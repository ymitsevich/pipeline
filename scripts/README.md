# Scripts Directory

Utility scripts for database management and other administrative tasks.

## Database Setup (`setup_db.py`)

Manage database tables for local development and testing.

### Usage

```bash
# Create all tables (first time setup)
python scripts/setup_db.py init

# Drop all tables (with confirmation prompt)
python scripts/setup_db.py drop

# Reset database (drop + recreate)
python scripts/setup_db.py reset

# Show help
python scripts/setup_db.py help
```

### Safety Features

- **Production Protection**: Cannot drop/reset in production (checks `ENV` environment variable)
- **Confirmation Prompts**: Requires explicit 'yes' confirmation for destructive operations
- **Clear Feedback**: Uses emojis and colors for better visibility

### When to Use

| Command | Use Case |
|---------|----------|
| `init` | First time setup, creating tables in fresh database |
| `drop` | Remove all tables (testing, cleanup) |
| `reset` | Fresh start with clean tables |

### Production Deployments

⚠️ **Do NOT use these scripts in production!**

For production schema changes, use proper migration tools like Alembic:
```bash
alembic upgrade head
```

