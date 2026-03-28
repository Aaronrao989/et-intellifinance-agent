import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()


class Settings(BaseModel):
    # App Info
    APP_NAME: str = "ET IntelliFinance Agent"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Groq Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")  # fast + powerful

    # File Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    LOG_DIR: str = os.path.join(BASE_DIR, "logs")
    OUTPUT_DIR: str = os.path.join(BASE_DIR, "outputs")

    # Logging
    LOG_LEVEL: str = "INFO"

    # Compliance Settings
    MAX_TRANSACTION_THRESHOLD: float = 1_000_000  # example rule
    ALLOWED_CURRENCIES: list = ["INR"]

    # Feature Flags (for scalability)
    ENABLE_INSIGHTS: bool = True
    ENABLE_AUDIT_LOGS: bool = True


# Singleton config instance
settings = Settings()


# Ensure required directories exist
def create_directories():
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)


# Run at import
create_directories()