FROM python:3.11-slim

# Instalar Docker CLI para ejecutar contenedores
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements del worker
COPY worker/requirements.txt ./worker/
RUN pip install --no-cache-dir -r worker/requirements.txt

# Copiar código backend y worker
COPY backend ./backend
COPY worker ./worker

CMD ["python", "-m", "rq.cli", "worker", "--url", "redis://redis:6379/0", "submissions"]
