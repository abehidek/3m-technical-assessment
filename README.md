# 3M Technical Assessment

## Run

```sh
cd server

# Run migrations
uv run alembic upgrade head

# Run server
uv run uvicorn src.main:app
```