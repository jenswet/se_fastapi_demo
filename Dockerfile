FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN python -m pip --no-cache-dir install sqlalchemy

COPY *.py /app/