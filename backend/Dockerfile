FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Railway uses PORT environment variable
ENV PORT=8000
EXPOSE $PORT

# Use production-ready command (no reload in production)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}