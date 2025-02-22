from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict, Extra


class Config(BaseSettings):
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_NAME: str = Field(..., env="DB_NAME")

    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(15, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    INITIAL_COINS: int = Field(1000, env="INITIAL_COINS")

    TEST_DB_HOST: str = Field(..., env="TEST_DB_HOST")
    TEST_DB_PORT: int = Field(5432, env="TEST_DB_PORT")
    TEST_DB_USER: str = Field(..., env="TEST_DB_USER")
    TEST_DB_PASSWORD: str = Field(..., env="TEST_DB_PASSWORD")
    TEST_DB_NAME: str = Field(..., env="TEST_DB_NAME")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = Extra.allow


settings = Config()
