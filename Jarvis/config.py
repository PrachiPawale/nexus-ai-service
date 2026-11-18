import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    # Application
    APP_NAME = "Nexus JARVIS AI Service"
    APP_VERSION = "2.0.0"

    # Server
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8000))

    # AI Provider
    AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()

    # OpenAI
    AI_API_KEY = os.getenv("AI_API_KEY", "")

    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # AI Model
    AI_MODEL = os.getenv(
        "AI_MODEL",
        "gemini-3.5-flash-lite"
    )

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "")

    # Backend
    BACKEND_URL = os.getenv(
        "BACKEND_URL",
        "http://localhost:5000"
    )

    # CORS
    ALLOWED_ORIGINS = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:4200"
    ).split(",")


settings = Settings()