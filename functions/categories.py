from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from models.categories import Categories, CategoryItems
from utils.pagination import save_in_db


def one_category(category_id, db):
    items = db.query(CategoryItems).filter_by(category_id=category_id).order_by(desc('id')).all()
    category = db.query(Categories).filter_by(id=category_id).first()
    if category: category.category_items = items
    else: return HTTPException(detail='Category not found!', status_code=404)
    return category


def one_category_item(category_item_id, db):
    return db.query(CategoryItems).filter_by(id=category_item_id)


def create_category(form, user, db):
    category = db.query(Categories).filter_by(name=form.name).first()
    if category is None:
        new_category = Categories(
            name=form.name,
            comment=form.comment,
            user_id=user.id
        )
        save_in_db(db, new_category)
        return True
    return False


def create_category_items(form, user, db):
    for item in form:
        if db.query(CategoryItems).filter_by(text=item.text, category_id=item.category_id).first(): pass
        else:
            new_category_item = CategoryItems(
                text=item.text,
                category_id=item.category_id,
                user_id=user.id
            )
            save_in_db(db, new_category_item)
    return True


def all_categories(db):
    return db.query(Categories).options(joinedload('category_items')).all()


def category_update(form, db):
    category = one_category(form.category_id, db)
    if category.first():
        category.update({
            Categories.name: form.name,
            Categories.comment: form.comment,
        })
        db.commit()
        return True
    return False


def category_item_update(form, db):
    category_item = one_category_item(form.category_item_id, db)
    if category_item.first():
        category_item.update({
            CategoryItems.text: form.text
        })
        db.commit()
        return True
    return False
