"""
Application Settings and Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""

    # API Configuration
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"

    # Database Configuration
    DB_PATH = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "data", "databases"
    )
    DB_NAME = "jewelry_store.db"

    # App Configuration
    APP_TITLE = "💎 Nashad Jewellers Assistant"
    APP_ICON = "💎"

    # Feature Configuration
    PRODUCTS_PER_ROW = 3
    MAX_PRODUCTS_PER_SEARCH = 9
    DEFAULT_SEARCH_TERM = "jewelry"

    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    LOG_LEVEL = "WARNING"


# Configuration selector
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.environ.get("ENVIRONMENT", "development")
    return config.get(env, config["default"])
