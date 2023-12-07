from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from models.targets import Targets
from functions.projects import one_project
from utils.pagination import save_in_db
from uuid import uuid4


def one_target(target_id, db):
    return db.query(Targets).filter_by(id=target_id)


def create_target(form, user, db):
    target = db.query(Targets).filter_by(comment=form.comment).first()
    if target is None:
        project = one_project(form.project_id, db).first()
        if project is None:
            return False
        new_category = Targets(
            link=f"{project.url}/{uuid4()}",
            status=form.status,
            comment=form.comment,
            project_id=form.project_id,
            user_id=user.id
        )
        save_in_db(db, new_category)
        return True
    return False


def all_targets(db):
    return db.query(Targets).filter_by(status=True).options(joinedload(Targets.project)).order_by(desc(Targets.id)).all()


def update_target(form, user, db):
    target = one_target(form.target_id, db)
    if target.first():
        target.update({
            Targets.status: form.status,
            Targets.comment: form.comment,
            Targets.project_id: form.project_id,
            Targets.user_id: user.id
        })
        db.commit()
        return True
    return False


def update_count_watches(link, db):
    target = db.query(Targets).filter_by(link=link, status=True).first()
    if target:
        target.count_watches += 1
        db.commit()
        return True
    return False
