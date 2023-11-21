from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db
from sqlalchemy.orm import Session
from functions.projects import create_project, all_projects, update_project, delete_project, one_project
from routes.auth import get_current_active_user
from schemas.projects import ProjectCreate, ProjectUpdate
from schemas.users import UserCurrent
from utils.role_verification import role_verification

Base.metadata.create_all(bind=engine)

router_project = APIRouter()


@router_project.post('/create')
async def write_data(form: ProjectCreate,
                     db: Session = Depends(get_db),
                     current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'create_project')
    if create_project(form, current_user, db):
        raise HTTPException(status_code=201, detail="Created successfully!")
    raise HTTPException(status_code=400, detail="Category has already been added!")


@router_project.get('/all')
async def read_data(db: Session = Depends(get_db)):
    return all_projects(db)


@router_project.put('/update')
async def update_data(form: ProjectUpdate,
                      db: Session = Depends(get_db),
                      current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'update_project')
    if update_project(form, current_user, db):
        raise HTTPException(status_code=200, detail="Updated successfully")
    raise HTTPException(status_code=400, detail="id does not exist!")


@router_project.get('/one_project')
async def read_data(project_id: int, db: Session = Depends(get_db)):
    return one_project(project_id, db).first()
