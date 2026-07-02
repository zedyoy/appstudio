FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PROGRESS_DB_PATH=/app/instance/user_progress.db

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /app/instance

EXPOSE 5000

CMD sh -c "gunicorn --bind 0.0.0.0:${PORT:-5000} app:app"
