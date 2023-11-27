from fastapi import APIRouter, Depends, status, HTTPException
from app.core.database import get_database
from app.core.schemas import User
from app.core.repository import serialize
from app.core.repository.auth.hashing import Hash
from app.core.repository.auth import oauth2
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.core.repository.auth import users as UserController



router = APIRouter(tags=["Api Keys"], prefix="/api-keys",dependencies=[Depends(oauth2.get_current_user)])


@router.get("")
async def get_api_keys(db = Depends(get_database), user=Depends(oauth2.get_current_user)):
    return user


@router.post("", response_model=User.UserOut)
async def generate_api_key(request: User.UserIn, db = Depends(get_database), user=Depends(oauth2.get_current_user)):
    return UserController.create(request=request, db=db)

@router.get("/{id}", response_model=User.UserOut)
async def get_single_user(id: str, db = Depends(get_database)):
    return UserController.show(id=id, db=db)

