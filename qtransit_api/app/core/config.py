import os


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/qtransit",
    )
    APP_ENV: str = os.getenv("APP_ENV", "development")


settings = Settings()
