FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./
COPY README.md ./

COPY serve.py ./src/serve.py
COPY text_utils.py ./src/text_utils.py
COPY pipeline_v1.pickle ./

RUN pip install --upgrade pip setuptools wheel \
    && pip install .

# Expose API port
EXPOSE 8080

# Start the API using Gunicorn
ENTRYPOINT ["uvicorn", "serve:app", "--host=0.0.0.0", "--port=8000"]
