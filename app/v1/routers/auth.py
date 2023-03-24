from fastapi import APIRouter



router = APIRouter(tags=["Auth"], prefix="/auth")

@router.get("/login")
def login():
    return {"Home" : "Login User"}

@router.get("/signup")
def signup():
    return {"Home" : "Sign Up User"}