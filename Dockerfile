FROM python:3.13-slim

# Configuración de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copiar archivos de dependencias primero (aprovecha la caché)
COPY pyproject.toml uv.lock* ./

# Instalar dependencias
RUN uv sync --frozen --no-dev

# Copiar el código
COPY . .

# Puerto de FastAPI
EXPOSE 8000

# Ejecutar migraciones y levantar la API
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn main:app --host 0.0.0.0 --port 8000"]