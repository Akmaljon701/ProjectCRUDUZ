from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db
from sqlalchemy.orm import Session
from models.users import Users
from routes.auth import get_current_active_user
from functions.users import one_user, all_users, update_user, create_user
from schemas.users import UserBase, UserCreate, UserUpdate, UserCurrent

Base.metadata.create_all(bind=engine)

router_user = APIRouter()


@router_user.post('/add', )
def add_user(form: UserCreate,
             db: Session = Depends(get_db), ):
    if create_user(form, db):
        raise HTTPException(status_code=201, detail="Created successfully!")


@router_user.get('')
def get_users(search: str = None, status: bool = True, id: int = 0, role: str = None, page: int = 1, limit: int = 25,
              db: Session = Depends(get_db)):
    if id:
        return one_user(id, db)
    else:
        return all_users(search, status, role, page, limit, db)


@router_user.get('/all_active_users')
async def active_users(db: Session = Depends(get_db)):
    return db.query(Users).filter_by(status=True).all()


@router_user.get('/auth_user')
async def auth_user(current_user: UserCurrent = Depends(get_current_active_user)):
    return current_user


@router_user.put("/update")
def user_update(form: UserUpdate, db: Session = Depends(get_db),
                current_user: UserCurrent = Depends(get_current_active_user)):
    if update_user(form, current_user, db):
        raise HTTPException(status_code=204, detail="Updated successfully!")
