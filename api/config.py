import os

HOST = os.getenv("API_HOST", "0.0.0.0")
PORT = os.getenv("API_PORT", 8000)
MAX_CONTENT_SIZE = int(os.getenv("MAX_CONTENT_SIZE", 5 * 1024 * 1024))  # 5MB
