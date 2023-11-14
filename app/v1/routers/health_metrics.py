from fastapi import APIRouter, Query
from app.core.database import get_database
from app.core.repository.healthmetrics import amdr, bmi, eer, pal, blood_sugar
from app.core.schemas.HealthMetrics import EEROut, EERIn, BmiOut, BmiIn, PAL, PALIn, BloodSugarUnits, BloodSugarIn, BloodSugarOut


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

# @router.get("/bloodsugar")
# async def bloog_sugar_levels():
#     """
#     Converts and interprets blood sugar levels from different types of tests
#     """
#     return "Hello"

@router.post("/bloodsugar", response_model=BloodSugarOut)
async def bloog_sugar_levels(request: BloodSugarIn):
    """
    Converts and interprets blood sugar levels from different types of tests
    """
    return blood_sugar.interpret_blood_sugar(request)
