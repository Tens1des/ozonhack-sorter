FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY control/ control/
COPY simulation/ simulation/
COPY scripts/ scripts/
COPY docs/ docs/
COPY cad/ cad/
COPY tests/ tests/
COPY Makefile .

ENV PYTHONPATH=/app

CMD ["python", "simulation/run.py", "--scenario", "all", "--duration", "3600"]
