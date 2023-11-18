from db import SessionLocal
from fastapi import FastAPI, Request, Response
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session
import traceback
from fastapi.openapi.utils import get_openapi
from routes import auth, users, projects, categories, targets, uploaded_fields
from db import Base, engine

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crud group",
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"message": "Welcome"}


app.include_router(auth.login_router, prefix='/auth', tags=['User auth section'],)
app.include_router(users.router_user, prefix='/user', tags=['User apis'],)
app.include_router(projects.router_project, prefix='/project', tags=['Project apis'],)
app.include_router(categories.router_category, prefix='/category', tags=['Category apis'],)
app.include_router(targets.router_target, prefix='/target', tags=['Target apis'],)
app.include_router(uploaded_fields.router_uploaded_files, prefix='/file', tags=['File apis'],)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Crud group",
        version="3.8.10",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi