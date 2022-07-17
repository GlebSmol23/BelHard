from typing import Optional
from pydantic import BaseModel, validator
import json


class User(BaseModel):
    id: int
    name: str
    birthDate: str
    firstName: str
    inn: str
    lastName: str
    middleName: str
    oms: None
    passport: str
    snils: Optional[None]
    type: str

with open("input.json", "r", encoding="utf-8") as f_json:
        data = json.load(f_json)


@validator("data")
def validate_data(id):
    if isinstance(id, (int, float)):
        return id
    if isinstance(id, str):
        raise TypeError("no str")

print(data)