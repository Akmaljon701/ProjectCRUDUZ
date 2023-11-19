from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from models.projects import Projects
from utils.pagination import save_in_db


def one_project(id, db):
    return db.query(Projects).filter_by(id=id, status=True)


def create_project(form, user, db):
    project = db.query(Projects).filter_by(name=form.name, status=True).first()
    if project is None:
        new_project = Projects(
            name=form.name,
            comment=form.comment,
            status=form.status,
            url=form.url,
            source_id=form.source_id,
            user_id=user.id
        )
        save_in_db(db, new_project)
        return True
    return False


def all_projects(db):
    return db.query(Projects).filter_by(status=True).options(joinedload(Projects.user)).order_by(desc(Projects.id)).all()


def update_project(form, user, db):
    project = one_project(form.id, db)
    if project.first():
        project.update({
            Projects.name: form.name,
            Projects.comment: form.comment,
            Projects.status: form.status,
            Projects.url: form.url,
            Projects.source_id: form.source_id,
            Projects.user_id: user.id,
        })
        db.commit()
        return True
    return False


def delete_project(project_id, user, db):
    project = db.query(Projects).filter_by(id=project_id, status=True)
    if project.first():
        project.update({
            Projects.status: False,
            Projects.user_id: user.id,
        })
        db.commit()
        return True
    return False
