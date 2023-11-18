from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field
from db import Base, engine, get_db
from sqlalchemy.orm import Session
from functions.categories import create_category, create_category_items, all_categories, category_update, \
    category_item_update
from routes.auth import get_current_active_user
from schemas.categories import CategoryItemsCreate, CategoryCreate, CategoryUpdate, CategoryItemUpdate
from schemas.users import UserCurrent
from utils.role_verification import role_verification

Base.metadata.create_all(bind=engine)

router_category = APIRouter()


@router_category.post("/create")
async def write_data(form: CategoryCreate,
                     db: Session = Depends(get_db),
                     current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'create_category')
    if create_category(form, current_user, db):
        raise HTTPException(status_code=201, detail="Created successfully!")
    raise HTTPException(status_code=400, detail="Category has already been added!")


@router_category.post("/create_items")
async def write_data(form: List[CategoryItemsCreate],
                     db: Session = Depends(get_db),
                     current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'create_category_items')
    if create_category_items(form, current_user, db):
        raise HTTPException(status_code=201, detail="Created successfully!")
    raise HTTPException(status_code=400, detail="Somthing error!")


@router_category.get("/all")
async def read_data(db: Session = Depends(get_db),
                    current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'all_categories')
    return all_categories(db)


@router_category.put('/update')
async def update_data(form: CategoryUpdate,
                      db: Session = Depends(get_db),
                      current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'category_update')
    if category_update(form, db):
        raise HTTPException(status_code=200, detail="Updated successfully")
    raise HTTPException(status_code=400, detail="id does not exist!")


@router_category.put('/update_item')
async def update_data(form: CategoryItemUpdate,
                      db: Session = Depends(get_db),
                      current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'category_item_update')
    if category_item_update(form, db):
        raise HTTPException(status_code=200, detail="Updated successfully")
    raise HTTPException(status_code=400, detail="id does not exist!")
