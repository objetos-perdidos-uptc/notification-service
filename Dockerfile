# syntax=docker/dockerfile:1.7
FROM python:3.11-slim

# Usuario no-root
RUN groupadd --system --gid 1000 app \
 && useradd  --system --uid 1000 --gid 1000 --create-home --shell /sbin/nologin app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 1) Dependencias
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# 2) Codigo
COPY app ./app

# 3) Permisos
RUN chown -R app:app /app
USER app

# Sin EXPOSE: es un worker (consume de RabbitMQ), no atiende HTTP.
# Sin HEALTHCHECK: no hay puerto que sondear. La salud real es "PID 1 vivo",
# que Docker ya controla con restart: unless-stopped si el proceso muere.
# Si quieres un healthcheck semantico (consumer conectado a RabbitMQ), hay que
# exponer un endpoint /health o escribir un archivo heartbeat desde el codigo.

CMD ["python", "-m", "app.main"]