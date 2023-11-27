from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user
from functions.users import one_user, all_users, update_user, create_user
from schemas.users import UserBase, UserCreate, UserUpdate, UserCurrent

Base.metadata.create_all(bind=engine)

router_user = APIRouter()


@router_user.post('/add', )
def add_user(form: UserCreate,
             db: Session = Depends(get_db), ):
    if create_user(form, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_user.get('/', status_code=200)
def get_users(search: str = None, status: bool = True, id: int = 0, role: str = None, page: int = 1, limit: int = 25,
              db: Session = Depends(get_db)):
    if id:
        return one_user(id, db)
    else:
        return all_users(search, status, role, page, limit, db)


@router_user.put("/update")
def user_update(form: UserUpdate, db: Session = Depends(get_db),
                current_user: UserCurrent = Depends(get_current_active_user)):
    if update_user(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
