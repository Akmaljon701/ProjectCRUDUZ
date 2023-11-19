import os
import shutil
import typing
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body, Form
from db import Base, engine, get_db
from sqlalchemy.orm import Session

from functions.uploaded_files import create_uploaded_file, read_files_by_source_id, read_file_by_id, update_file_by_id
from models.uploaded_files import UploadedFiles
from routes.auth import get_current_active_user
from schemas.users import UserCurrent
from utils.role_verification import role_verification, allowed_image_types, allowed_video_types

Base.metadata.create_all(bind=engine)

router_uploaded_files = APIRouter()


@router_uploaded_files.post("/add")
async def write_data(source_id: int = Body(..., ge=0),
                     comment: typing.Optional[str] = Body(''),
                     source: typing.Optional[str] = Body(''),
                     files: typing.Optional[typing.List[UploadFile]] = File(None),
                     db: Session = Depends(get_db),
                     current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'create_uploaded_file')
    for file in files:
        if (file.content_type in allowed_image_types) or (file.content_type in allowed_video_types):
            file.filename = f"{uuid.uuid4()}-{file.filename}"
            contents = await file.read()

            with open(f"media/{file.filename}", "wb") as f:
                f.write(contents)
            create_uploaded_file(source_id=source_id, source=source, file_name=file.filename, comment=comment,
                                 user=current_user, db=db)
            raise HTTPException(status_code=201, detail="Added successfully!")


@router_uploaded_files.post("/files_by_source_id")
async def read_data(source_id: int = File(ge=0),
                    db: Session = Depends(get_db)):
    return read_files_by_source_id(source_id, db)


@router_uploaded_files.post("/file_by_id")
async def read_data(file_id: int = File(ge=0),
                    db: Session = Depends(get_db)):
    if read_file_by_id(file_id, db) is False: raise HTTPException(status_code=404, detail="id does not exist!")
    return read_file_by_id(file_id, db)


@router_uploaded_files.put("/update_file_by_id")
async def update_data(file_id: int = File(ge=0), file: UploadFile = File(None),
                      comment: str = Form(None), source: str = Form(None),
                      db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)):
    file_data = db.query(UploadedFiles).filter_by(id=file_id).first()
    if file_data:
        if file:
            if (file.content_type in allowed_image_types) or (file.content_type in allowed_video_types):
                file.filename = f"{uuid.uuid4()}-{file.filename}"
                contents = await file.read()
                with open(f"media/{file.filename}", "wb") as f:
                    f.write(contents)
            if file_data.file:
                if os.path.exists(file_data.file):
                    os.unlink(file_data.file)
            if file: file_data.file = f"media/{file.filename}"
            if comment: file_data.comment = comment
            if source: file_data.source = source
            file_data.user_id = current_user.id
            db.commit()
            raise HTTPException(status_code=200, detail="Updated")
    else:
        raise HTTPException(status_code=404, detail="id does not exist!")
