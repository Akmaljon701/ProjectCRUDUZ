from models.uploaded_files import UploadedFiles
from utils.pagination import save_in_db


def create_uploaded_file(source_id, source, file_name, comment, user, db):
    new_up_file = UploadedFiles(
        source_id=source_id,
        source=source,
        file=file_name,
        comment=comment,
        user_id=user.id
    )
    save_in_db(db, new_up_file)
    return True
