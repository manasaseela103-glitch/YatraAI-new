import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

# Check for .env in current backend directory, then root directory, then default environment
if (BASE_DIR / ".env").exists():
    load_dotenv(dotenv_path=BASE_DIR / ".env")
if (ROOT_DIR / ".env").exists():
    load_dotenv(dotenv_path=ROOT_DIR / ".env", override=False)
load_dotenv()

class Settings:
    PROJECT_NAME: str = "YatraAI API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    MONGODB_USERNAME: str = os.getenv("MONGODB_USERNAME", "")
    MONGODB_PASSWORD: str = os.getenv("MONGODB_PASSWORD", "")
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "yatra_ai")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    VITE_API_URL: str = os.getenv("VITE_API_URL", "http://127.0.0.1:8000/api")
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    @property
    def effective_mongodb_uri(self) -> str:
        if self.MONGODB_URI:
            return self.MONGODB_URI
        if self.MONGODB_USERNAME and self.MONGODB_PASSWORD:
            from urllib.parse import quote_plus
            user = quote_plus(self.MONGODB_USERNAME)
            pwd = quote_plus(self.MONGODB_PASSWORD)
            return f"mongodb://{user}:{pwd}@localhost:27017/{self.DATABASE_NAME}"
        return ""

settings = Settings()
