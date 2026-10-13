# syntax=docker/dockerfile:1

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY bot.py ./
COPY src ./src

RUN python -m pip install --no-cache-dir .

# NoneBot's Telegram adapter uses outbound connections, so no host port is
# required for the default polling setup.
CMD ["python", "-m", "uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "8080"]
