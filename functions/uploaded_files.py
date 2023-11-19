from fastapi import HTTPException

from models.uploaded_files import UploadedFiles
from utils.pagination import save_in_db


def create_uploaded_file(source_id, source, file_name, comment, user, db):
    new_up_file = UploadedFiles(
        source_id=source_id,
        source=source,
        file=f"media/{file_name}",
        comment=comment,
        user_id=user.id
    )
    save_in_db(db, new_up_file)
    return True


def read_files_by_source_id(source_id, db):
    return db.query(UploadedFiles).filter_by(source_id=source_id).all()


def read_file_by_id(file_id, db):
    file = db.query(UploadedFiles).filter_by(id=file_id).first()
    if file: return file
    return False


async def update_file_by_id(file_id, file, comment, source, user, db):
    file_data = db.query(UploadedFiles).filter_by(id=file_id).first()
    return file_data