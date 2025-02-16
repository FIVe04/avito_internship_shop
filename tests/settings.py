from pydantic_settings import BaseSettings
from pydantic import Field, Extra


class Config(BaseSettings):
    TEST_DB_HOST: str = Field(..., env="TEST_DB_HOST")
    TEST_DB_PORT: int = Field(5432, env="TEST_DB_PORT")
    TEST_DB_USER: str = Field(..., env="TEST_DB_USER")
    TEST_DB_PASSWORD: str = Field(..., env="TEST_DB_PASSWORD")
    TEST_DB_NAME: str = Field(..., env="TEST_DB_NAME")

    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = Extra.allow


settings = Config()
