from pydantic import BaseModel, PostgresDsn, Field


class DatabaseSchema(BaseModel):
    URL: PostgresDsn
    ASYNC_URL: PostgresDsn


class AuthSchema(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE: int = Field(default=30)


class ConfigSchema(BaseModel):
    DATABASE: DatabaseSchema
    AUTH: AuthSchema
