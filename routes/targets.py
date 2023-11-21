from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db
from sqlalchemy.orm import Session

from functions.targets import create_target, all_targets, update_target, update_count_watches, one_target
from routes.auth import get_current_active_user
from schemas.target import TargetCreate, TargetUpdate
from schemas.users import UserCurrent
from utils.role_verification import role_verification

Base.metadata.create_all(bind=engine)

router_target = APIRouter()


@router_target.post('/create')
async def create_target_data(form: TargetCreate,
                             db: Session = Depends(get_db),
                             current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'create_target_data')
    if create_target(form, current_user, db):
        raise HTTPException(status_code=201, detail="Created successfully!")
    raise HTTPException(status_code=400, detail="Category has already been added or project id doesn't exited!")


@router_target.get('/all')
async def all_targets_data(db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'all_targets_data')
    return all_targets(db)


@router_target.put('/update')
async def update_target_data(form: TargetUpdate,
                             db: Session = Depends(get_db),
                             current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'update_target_data')
    if update_target(form, current_user, db):
        raise HTTPException(status_code=200, detail="Updated successfully")
    raise HTTPException(status_code=400, detail="id does not exist!")


@router_target.put('/update_count_watches')
async def update_data(link: str,
                      db: Session = Depends(get_db)):
    if update_count_watches(link, db):
        raise HTTPException(status_code=200, detail="Updated successfully")
    raise HTTPException(status_code=400, detail="id does not exist!")


@router_target.get('/one_target')
async def all_targets_data(target_id: int, db: Session = Depends(get_db),
                           current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'all_targets_data')
    return one_target(target_id, db)
