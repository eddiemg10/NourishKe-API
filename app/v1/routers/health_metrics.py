from fastapi import APIRouter, Query
from app.core.database import get_database
from app.core.repository.healthmetrics import amdr, bmi, eer, pal
from app.core.schemas.HealthMetrics import EEROut, EERIn, BmiOut, BmiIn, PAL, PALIn


router = APIRouter(tags=["Health metrics"], prefix="/healthmetrics")

@router.post("/bmi",response_model=BmiOut)
async def calculate_bmi(request: BmiIn):
    """
    Calculates the bmi given an individuals height and weight
    """
    return bmi.calculate_bmi(request)

@router.get("/pal", response_model=list[PAL])
async def get_physical_activity_level_activities():
    return pal.retrieve_pal_activites()

@router.post("/pal")
async def determine_physical_activity_level(request: list[PALIn]):
    return pal.calculate_pal(request)

@router.post("/eer", response_model=EEROut)
async def calculate_estimated_energy_requirements(request: EERIn):
    """
    Claculates the estimated energy requirements of an individual based on parameters x
    """
    return eer.calculate_eer(request)

@router.get("/amdr")
async def acceptable_macronutrient_distribution_range():
    """
    Claculates the acceptable_macronutrient_distribution_range
    """
    return "Hello"

