from datetime import date

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int = Field(default=None, readOnly=True)
    name: str = Field(max_length=25)
    description: str = None
    price: float = Field(ge=0, format="double")
    tax: float = Field(default=None, ge=0, format="double")
    listed_since: date = Field(default=None, readOnly=True)
    manufacturer: str

    class Config:
        orm_mode = True
