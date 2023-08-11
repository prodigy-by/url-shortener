import os

SERVICE_ROOT = os.getenv("SERVICE_ROOT", 'http://localhost:8000/')

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6400)