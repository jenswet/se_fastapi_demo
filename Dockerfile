FROM tiangolo/uvicorn-gunicorn:python3.8-slim

RUN python -m pip install --no-cache-dir fastapi sqlalchemy

COPY *.py /app