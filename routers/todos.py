import sys
# TODO: Add the parent directory to the system path to allow importing modules from the parent directory
sys.path.append("..")

from typing import Optional
from fastapi import Depends, HTTPException, APIRouter, Request
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user, get_user_exception

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# TODO: Initialize APIRouter with a prefix and tags for the todos endpoint
router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)

# TODO: Create all database tables defined in models.py if they do not exist
models.Base.metadata.create_all(bind=engine)

# TODO: Add Jinja2 templates directory for rendering HTML responses
templates = Jinja2Templates(directory="templates")

# TODO: Dependency to get the database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# TODO: Define the endpoint to read all todos by the current user, returning an HTML response
@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request): 
    return templates.TemplateResponse("home.html", {"request": request})

# TODO: Define the endpoint to add a new todo, returning an HTML response
@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request): 
    return templates.TemplateResponse("add-todo.html", {"request": request})

# TODO: Define the endpoint to edit an existing todo, returning an HTML response
@router.get("/edit-todo", response_class=HTMLResponse)
async def edit_todo(request: Request): 
    return templates.TemplateResponse("edit-todo.html", {"request": request})
