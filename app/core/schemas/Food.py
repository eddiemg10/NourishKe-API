from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class FoodBase(BaseModel):
    code_kfct: str = Field(description="Code in the Kenya Food Composition Tables(2018)", example="1002")
    code_ken: str|None = Field(None, description="", example="47")
    english_name: str = Field(description="Common English name of the Food", example="Amaranth, whole grain,flour")
    scientific_name: str = Field(description="Scientific name of the food", example="Amaranthus spp")
    foodgroup_id: str = Field(description="reference to the group the food belongs in", example="64204d95b840774efbbe6cb0")
    biblio_id: str|None = Field(None, description="", example="KEN93-59, US28-20001,IN17-A001,IN17-A002")

    class Config:
        orm_mode = True

class FoodUpdate(BaseModel):
    code_kfct: str = Field(None, description="")
    code_ken: str = Field(None, description="")
    english_name: str = Field(None, description="Common English name of the Food")
    scientific_name: str = Field(None, description="Scientific name of the food")
    foodgroup_id: str = Field(None, description="reference to the group the food belongs in")
    biblio_id: str = Field(None, description="")

class FoodOut(FoodBase):
    id: str = Field(..., alias="_id")

    class Config:
        orm_mode = True
    
