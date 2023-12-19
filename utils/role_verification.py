from fastapi import HTTPException


def role_verification(user, function):

    allowed_functions_for_admins = ['create_project_data', 'update_project_data', 'delete_project_data',
                                    'create_category_items_data', 'create_category_data',
                                    'category_update_data', 'category_item_update_data',
                                    'create_target_data', 'all_targets_data', 'update_target_data',
                                    'create_uploaded_file_data', 'update_uploaded_file_data']

    allowed_functions_for_smms = []

    if user.role == "admin" and function in allowed_functions_for_admins:
        return True
    elif user.role == "smm" and function in allowed_functions_for_smms:
        return True
    raise HTTPException(status_code=400, detail='Sizga ruhsat berilmagan!')


allowed_image_types = ["image/png", "image/jpg", "image/jpeg"]
allowed_video_types = ["video/mp4", "video/avi"]
allowed_audio_types = ["audio/mp3", "audio/wav"]
allowed_voice_types = ["audio/ogg", "audio/mpeg"]  # Ovozli habar fayllari
allowed_document_types = ["application/pdf", "application/msword"]  # Hujjat fayllari
allowed_other_types = ["application/octet-stream"]  # Boshqa fayl formatlari
