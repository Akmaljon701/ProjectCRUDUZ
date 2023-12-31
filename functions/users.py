from passlib.context import CryptContext
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from models.users import Users
from routes.auth import get_password_hash
from utils.pagination import pagination


pwd_context = CryptContext(schemes=['bcrypt'])


def all_users(search, status, role, page, limit, db):
    users = db.query(Users)

    if search:
        search_formatted = f"%{search}%"
        users = users.filter(
            Users.name.ilike(search_formatted) | Users.username.ilike(search_formatted)
        )

    if status is not None:
        users = users.filter(Users.status == status)

    if role:
        users = users.filter(Users.role == role)

    users = users.order_by(Users.name.asc())

    return pagination(users, page, limit)


def one_user(id, db):
    return db.query(Users.name.label("name")).filter(
        Users.id == id).first()


def create_user(form, db):
    user_verification = db.query(Users).filter(Users.username == form.username).first()
    if user_verification:
        raise HTTPException(status_code=403, detail="User already exists!")
    number_verification = db.query(Users).filter(Users.number == form.number).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="The phone number already exists!")

    new_user_db = Users(
        name=form.name,
        username=form.username,
        number=form.number,
        password=get_password_hash(form.password),
        role=form.role,
        status=form.status,

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)
    return new_user_db


def update_user(form, user, db):
    if one_user(form.id, db) is None:
        raise HTTPException(status_code=404, detail="User not found!")

    db.query(Users).filter(Users.id == form.id).update({
        Users.name: form.name,
        Users.username: form.username,
        Users.password: get_password_hash(form.password),
        Users.role: form.role,
        Users.status: form.status,
        Users.number: form.number,

    })
    db.commit()

    return one_user(form.id, db)