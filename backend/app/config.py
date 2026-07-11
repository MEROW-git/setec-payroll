import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def database_url() -> str:
    url = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://hrm_user:strong_password@localhost:3306/hrm_backend?charset=utf8mb4",
    )
    if url.startswith("mysql://"):
        return url.replace("mysql://", "mysql+pymysql://", 1)
    return url


def engine_options() -> dict:
    options = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    ssl_ca = os.getenv("MYSQL_SSL_CA")
    if ssl_ca:
        ssl_ca_path = Path(ssl_ca)
        if not ssl_ca_path.is_absolute():
            ssl_ca_path = BASE_DIR / ssl_ca_path
        options["connect_args"] = {"ssl": {"ca": str(ssl_ca_path)}}

    return options


def cors_origins() -> list[str]:
    origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    return [origin.strip() for origin in origins.split(",") if origin.strip()]


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-too")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = database_url()
    SQLALCHEMY_ENGINE_OPTIONS = engine_options()
    CORS_ORIGINS = cors_origins()
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
