from fastapi import APIRouter, Depends, status, HTTPException



router = APIRouter(tags=["Users"], prefix="/users")

@router.get("")
def users():
    return {"users" : "List of users"}