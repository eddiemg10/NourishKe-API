from bson import ObjectId
from pydantic import BaseModel, Field

class FoodGroupBase(BaseModel):
    code: str = Field(description="Unique code identifying the food group", example="1")
    name: str = Field(description="Name of the feed group", example="Cereals and cereal Products")


class FoodGroupOut(FoodGroupBase):
    id: str = Field(..., alias="_id")

    class Config:
        orm_mode = True
    