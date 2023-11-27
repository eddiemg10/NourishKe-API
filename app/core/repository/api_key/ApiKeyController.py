from ...schemas.Project import Project, ProjectOut, APIKey
from ...database import get_database
from ..serialize import serializeDict, serializeList
from fastapi import Depends, status, HTTPException, Path
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from .. import helpers



def get_user_keys(db, user_id):
    # api_keys = db.apikeys.find({'foodgroup_id':})
    pass