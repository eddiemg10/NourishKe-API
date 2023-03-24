from fastapi import APIRouter, Depends, status, HTTPException

from .routers import auth, users


router = APIRouter(prefix="/v1")
router.include_router(auth.router)
router.include_router(users.router)

@router.get("/home")
def home():
    return {"Home" : "Welcome to version 1"}