import os
from datetime import timedelta


def get_from_env(var_name: str) -> str:
    value = os.environ.get(var_name)

    if not value:
        raise ValueError(f"{var_name} is not set. Check that your .env file is present and complete.")

    return value


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "BANANA"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "echo": False
    }

    @property
    def ADMIN_REFRESH_TOKEN(self):
        return get_from_env("ADMIN_REFRESH_TOKEN")

    @property
    def ADMIN_TOKEN_FILEPATH(self):
        return get_from_env("ADMIN_TOKEN_FILEPATH")


class DevelopmentConfig(Config):
    DEBUG = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return get_from_env("DB_URI")


class ProductionConfig(Config):
    @property
    def JWT_SECRET_KEY(self):
        return get_from_env("JWT_SECRET_KEY")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


environment = os.environ.get("FLASK_ENV")

if environment == "production":
    app_config: Config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()
