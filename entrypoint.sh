alembic upgrade head
uvicorn app.main:app --root-path "/offices" --host 0.0.0.0 --port $1