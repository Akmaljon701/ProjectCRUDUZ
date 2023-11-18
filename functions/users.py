from passlib.context import CryptContext
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from models.users import Users
from routes.auth import get_password_hash
from utils.pagination import pagination


pwd_context = CryptContext(schemes=['bcrypt'])


def all_users(search, status, roll, page, limit, db):
    users = db.query(Users)
    if search:
        search_formatted = "%{}%".format(search)
        users = users.filter(Users.name.like(search_formatted) | Users.number.like(search_formatted) | Users.username.like(
            search_formatted) | Users.title.like(search_formatted))
    if status in [True, False]:
        users = users.filter(Users.status == status)
    if roll:
        users = users.filter(Users.roll == roll)
    users = users.order_by(Users.name.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_user(id, db):
    return db.query(Users.name.label("name")).filter(
        Users.id == id).first()


def create_user(form, db):
    user_verification = db.query(Users).filter(Users.username == form.username).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
    number_verification = db.query(Users).filter(Users.number == form.number).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")

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
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Users).filter(Users.username == form.username).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

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