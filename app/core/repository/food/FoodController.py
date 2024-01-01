from ...schemas import Food
from ...database import get_database
from ..serialize import serializeDict, serializeList
from .. import helpers
from fastapi import Depends, status, HTTPException
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from random import randint
from app.core.repository.expertipy.engine import FoodGroups

def noGI(db):
    foods = db.foods.find({ "GI": { "$exists": False } })
    # return len(serializeList(foods))
    return serializeList(foods)


def index(page, size, db, groups):
    skip = (page - 1) * size
    if groups:
        group_objectids = []
        for group_id in groups:
            try:
                group_objectids.append(ObjectId(group_id))
            except:
                raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Food Group Id given"
        )
        foods = db.foods.find({'foodgroup_id': {'$in': group_objectids}}).skip(skip).limit(size)
    else:
        foods = db.foods.find().skip(skip).limit(size)


    return serializeList(foods)

def show(id, db):
    helpers.itemExists(id, db.foods, "Food item not found")
    food =  db.foods.find_one({"_id": ObjectId(id)})

    return serializeDict(food)

def create(request: Food.BaseModel, db):
    if db.foods.find_one({"code_kfct": request.code_kfct}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A food with a similar KFCT code already exists")

    food = {
            "code_kfct": request.code_kfct,
            "code_ken": request.code_ken,
            "english_name": request.english_name,
            "scientific_name": request.scientific_name,
            "foodgroup_id": ObjectId(request.foodgroup_id),
            "biblio_id": request.biblio_id,
        }
    try:
        inserted_food =  db.foods.insert_one(food)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Food already exists")
    return serializeDict(db.foods.find_one({"_id" : inserted_food.inserted_id}))


def update(id, food_update, db):
    food =  db.foods.find_one({"_id": ObjectId(id)})
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food not found"
        )
    
    result = db.foods.update_one({"_id": ObjectId(id)}, {"$set": food_update.dict(exclude_unset=True)})
    if not result:
        raise HTTPException(status_code=404, detail="Food item not found")
    updated_food = db.foods.find_one({"_id": ObjectId(id)})
    return serializeDict(updated_food)

def delete(id, db):
    result = db.foods.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")
    return {"message": "Food item deleted successfully"}

def random(db):
    count = 582
    random_index = randint(0, count - 1)
    random_food = db.foods.find_one(skip=random_index)
    if random_food is None:
        raise HTTPException(status_code=404, detail="No food items found")
    return serializeDict(random_food)

def filter(db, query, sort_by="GI"):
    FG = FoodGroups()
    # Define the base query
    base_query = {}

    # Check if "GI" filter is provided
    if "GI" in query:
        min_gi, max_gi = query["GI"]
        base_query["GI"] = {"$gte": min_gi, "$lte": max_gi}

    # Check other filters
    if "location" in query:
        base_query["location"] = query["location"]

    if "group" in query:
        # groups = []
        # # for grp in query["group"]:
        # #     groups.append(grp)
        # base_query["foodgroup_id"] = {"$in": [ObjectId(query["group"])]}
        groups = query["group"]
        base_query["foodgroup_id"] = {"$in": [ObjectId(group) for group in groups]}

    if "tags" in query:
        tags_value = query["tags"]
        if tags_value == "":
            # If tags is an empty string, retrieve foods where the tag field is empty
            base_query["$or"] = [{"tag": {"$exists": False}}, {"tag": ""}]
        else:
            # Otherwise, perform the regex query
            tags_query = {"tag": {"$regex": f'{tags_value},|,{tags_value}$|^ {tags_value},|, {tags_value},|, {tags_value}$'}}
            base_query.update(tags_query)

    if "exclude" in query:
        exclude_options = {"meat": FG.meats_and_poultry, "fish": FG.fish, "dairy": FG.dairy}  # Map exclude options to group_ids
        exclude_values = query["exclude"]
        exclude_group_ids = [exclude_options.get(exclude_value) for exclude_value in exclude_values if exclude_options.get(exclude_value)]
        if exclude_group_ids:
            base_query["foodgroup_id"] = {"$nin": [ObjectId(group_id) for group_id in exclude_group_ids]}

    # Sort by the specified field (default: "GI")
    sort_field = sort_by if sort_by in ["GI", "location", "group", "tags"] else "GI"
    cursor = db.foods.find(base_query).sort(sort_field)

    grouped_results = {}
    for food in serializeList(cursor):
        group_id = str(food.get("foodgroup_id", ""))
        if group_id not in grouped_results:
            grouped_results[group_id] = []
        grouped_results[group_id].append(food)

    # for group_id, foods in grouped_results.items():
    #     grouped_results[group_id] = sorted(foods, key=lambda x: x.get("GI", 0))
    return grouped_results
    return serializeDict(grouped_results)
    # Perform the query
    result = serializeList(cursor)
    # result = serializeList(db.foods.find(base_query))

    return result
