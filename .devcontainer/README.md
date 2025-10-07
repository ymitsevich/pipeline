# Dev Container Setup

This directory contains the configuration to run your development environment inside a Docker container using VS Code/Cursor Dev Containers.

## How to Use

1. **Install Dev Containers Extension**
   - In VS Code/Cursor, install the "Dev Containers" extension

2. **Reopen in Container**
   - Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
   - Select "Dev Containers: Reopen in Container"
   - Wait for the container to build and start (first time takes a few minutes)

3. **Start Coding**
   - All Python imports (like `pydantic`) will now resolve
   - The terminal runs inside the container
   - Postgres and Redis are automatically started
   - Your code is live-synced between host and container

## What Happens

- The `pipeline` service starts with `sleep infinity` (stays alive)
- Dependencies from `requirements-dev.txt` are installed automatically
- Postgres and Redis services start in the background
- VS Code/Cursor runs its language server inside the container
- You're running as `root` user to avoid permission issues

## Running Your Scripts

Inside the container terminal:
```bash
# Run your main script
python -m pipeline.main

# Or run via docker-compose from outside
docker compose run --rm pipeline python -m pipeline.main
```

## Switching Users

If you need to run as the `pipeline` user:
```bash
su pipeline
```

## Troubleshooting

- **Container won't start**: Check `docker ps -a` and `docker logs pipeline_app`
- **Import errors persist**: Make sure `postCreateCommand` ran successfully
- **Permission issues**: You're running as root, but you can `chown` files if needed

