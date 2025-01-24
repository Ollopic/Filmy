import os

APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "your_secret_key")
API_URL = os.getenv("API_URL", "http://localhost:8002")