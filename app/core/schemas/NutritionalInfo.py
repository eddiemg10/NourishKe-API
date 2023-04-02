from pydantic import BaseModel, Field

class NutritionalInfo(BaseModel):
    value: int = Field(description="Measured value of the nutritional component", example=492)
    name: str = Field(description="Name of the nutritional component", example="Energy")
    unit: str = Field(description="Unit of measurement used", example="kcal")
    infoods_tagname: str = Field(description="International Network of Food Data Systems tagname", example="ENERC")
    denominator: str = Field(description="All values have been measured with the same denomiator (/100g of Edible Portion)", example="/100 g EP")
    analysis_method: str = Field(description="Analysis method used to derive the value", example="ISO 6496")

    class Config:
        orm_mode = True
    