from pydantic import BaseModel, Field


class BotUserSchema(BaseModel):
    balance: int = Field(ge=0)
    language_id: int = Field(ge=1)


class BotUserSchemaInDBSchema(BotUserSchema):
    id: int = Field(ge=1)