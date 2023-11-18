from math import ceil
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from db import Base, get_db


def pagination(form, page, limit):
    return {"current_page": page, "limit": limit, "pages": ceil(form.count() / limit),
            "data": form.offset((page - 1) * limit).limit(limit).all()}


def save_in_db(db, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def the_one(db, model, id):
    the_one = db.query(model).filter(model.id == id).first()
    if not the_one:
        raise HTTPException(status_code=400, detail=f"Bazada bunday {model} yo'q!")
    return the_one