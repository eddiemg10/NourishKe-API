from fastapi import APIRouter, Query
from app.core.repository.expertipy import engine


router = APIRouter(tags=["Recommendations"], prefix="/recommendations")

@router.get("/test")
async def get_recommendation():
    return engine.recommend()