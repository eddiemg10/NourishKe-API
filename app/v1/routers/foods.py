from fastapi import APIRouter, Depends, status, HTTPException, Query
from app.core.database import get_database
from app.core.schemas.Food import FoodOut, FoodBase, FoodUpdate
from app.core.schemas.NutritionalInfo import NutritionalInfo
from app.core.lib.auth import oauth2
from app.core.lib.auth.hashing import Hash
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.core.lib.food import FoodController, NutritionController



router = APIRouter(tags=["Foods"], prefix="/foods")


@router.get("", response_model=list[FoodOut])
async def get_foods(db = Depends(get_database),
                    page: int = Query(1, description="Page number, starting from 1"),
                    size: int = Query(10, description="Number of items per page"),
                    groups: list[str] = Query(None, description="Filter by specifying the food group(s) using Group Ids")):
    """
    Returns a list of food items with pagination and size
    """
    return FoodController.index(page=page, size=size , db=db, groups=groups)


@router.post("", response_model=FoodOut)
async def add_food(request: FoodBase, db = Depends(get_database)):
    """
    Add a new food item
    """
    return FoodController.create(request=request, db=db)


@router.get("/random", response_model=FoodOut)
async def get_single_random_food(db = Depends(get_database)):
    """
    Get a random food item
    """
    return FoodController.random(db=db)


@router.get("/{id}", response_model=FoodOut)
async def get_single_food(id: str, db = Depends(get_database)):
    """
    Returns a food item with the specified id
    """
    return FoodController.show(id=id, db=db)

@router.put("/{id}")
async def update_food(id: str, request: FoodUpdate, db = Depends(get_database), user=Depends(oauth2.get_current_user)):
    """
    Updates a food item with the fields specified
    """
    return FoodController.update(food_update=request, db=db, id=id)


@router.delete("/{id}")
async def delete_food(id: str, db = Depends(get_database), user=Depends(oauth2.get_current_user)):
    """
    Deleted a food item by ID
    """
    return FoodController.delete(db=db, id=id)

@router.get("/{id}/nutrition", response_model = list[NutritionalInfo])
async def get_nutritional_information(id: str, db = Depends(get_database)):
    """
    Returns nutritional information about a food item
    """
    return NutritionController.showNutrition(id=id, db=db)




