from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://quiz_user:quiz_pass@postgres:5432/quiz_db"
    REDIS_URL: str = "redis://redis:6379"
    SECRET_KEY: str = "super-secret-key-change-in-production-32chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = {"env_file": ".env"}

    def model_post_init(self, __context: object) -> None:
        # Railway postgres:// formatini asyncpg ga o'zgartirish
        if self.DATABASE_URL.startswith("postgres://"):
            object.__setattr__(self, "DATABASE_URL", self.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1))
        elif self.DATABASE_URL.startswith("postgresql://"):
            object.__setattr__(self, "DATABASE_URL", self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1))


settings = Settings()
