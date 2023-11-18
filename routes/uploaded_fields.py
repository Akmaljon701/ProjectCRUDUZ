import shutil
import typing
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from db import Base, engine, get_db
from sqlalchemy.orm import Session

from functions.uploaded_files import create_uploaded_file
from routes.auth import get_current_active_user
from schemas.users import UserCurrent
from utils.role_verification import role_verification, allowed_image_types, allowed_video_types

Base.metadata.create_all(bind=engine)

router_uploaded_files = APIRouter()


@router_uploaded_files.post("/add")
def order_s(source_id: int = Body(..., ge=0),
            comment: typing.Optional[str] = Body(''),
            source: typing.Optional[str] = Body(''),
            files: typing.Optional[typing.List[UploadFile]] = File(None), db: Session = Depends(get_db),
            current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, 'create_uploaded_file')
    for file in files:
        if (file.content_type in allowed_image_types) or (file.content_type in allowed_video_types):
            with open("media/" + f"{uuid.uuid4()}-{file.filename}", 'wb') as image:
                shutil.copyfileobj(file.file, image)
            file_name = str('media/' + f"{uuid.uuid4()}-{file.filename}")
            create_uploaded_file(source_id=source_id, source=source, file_name=file_name, comment=comment,
                                 user=current_user, db=db)
            raise HTTPException(status_code=201, detail="Added successfully!")
