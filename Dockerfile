# 1. Слой для сборки зависимостей
FROM python:3.10-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY services/requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# 2. Финальный слой
FROM python:3.10-slim

WORKDIR /app

# Создание пользователя без прав root
RUN addgroup --system app && adduser --system --group app

# Копирование зависимостей и установка
COPY --from=builder /app/wheels /wheels
COPY services/requirements.txt .
RUN pip install --no-cache-dir /wheels/*

# Копирование исходного кода
COPY src/ .
COPY services/gateway/main.py .

# Установка владельца и запуск от его имени
USER app