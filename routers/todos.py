import sys
# TODO: Add the parent directory to the system path to allow importing modules from the parent directory
sys.path.append("..")
from fastapi import Depends, Form , APIRouter, Request,status
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse 
from starlette import status
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
async def read_all_by_user(request: Request, db: Session = Depends(get_db)): 
    user = await get_current_user(request)

    if user is None : 
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    
    todos = db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all() 
    
    return templates.TemplateResponse("home.html", {"request": request, "todos": todos, "user" : user})

# TODO: Define the endpoint to add a new todo, returning an HTML response
@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request): 
    user = await get_current_user(request)
    if user is None : 
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("add-todo.html", {"request": request})

@router.post("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request, title: str = Form(...), 
                       description : str = Form(...) , 
                       priority: int = Form(...) , 
                       db: Session = Depends(get_db)) :
    
    user = await get_current_user(request)
    if user is None : 
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    
    todo_model = models.Todos() 
    todo_model.title = title 
    todo_model.description = description 
    todo_model.priority = priority 
    todo_model.complete = False 
    todo_model.owner_id = user.get("id")
    
    
    db.add(todo_model)
    db.commit() 
    
    return RedirectResponse(url="/todos/", status_code=status.HTTP_302_FOUND)

# TODO: Define the endpoint to edit an existing todo, returning an HTML response
@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id:int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None : 
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first() 
    return templates.TemplateResponse("edit-todo.html", {"request": request, "todo" : todo})

@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_commit(request: Request, todo_id :int , title : str = Form(...),
                           description: str = Form(...),
                           priority: int = Form(...), 
                           db : Session = Depends(get_db)) : 
    user = await get_current_user(request)
    if user is None : 
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first() 
    
    todo_model.title = title
    todo_model.description = description 
    todo_model.priority = priority 
    
    db.add(todo_model)
    
    db.commit() 
    
    return RedirectResponse(url="/todos", status_code = status.HTTP_302_FOUND)

@router.get("/delete/{todo_id}")
async def delete_todo(request: Request, todo_id : int, db: Session = Depends(get_db)): 
    user = await get_current_user(request)
    if user is None : 
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
     
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get("id")).first()
    
    if todo_model is None : 
        return RedirectResponse(url="/todos", status_code=status.HTTP_404_NOT_FOUND)
    
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    
    db.commit() 
    
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/complete/{todo_id}", response_class=HTMLResponse)
async def complete_todo(request: Request , todo_id : int , db : Session = Depends(get_db)) : 
    user = await get_current_user(request)
    if user is None : 
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first() 
    
    todo.complete = not todo.complete 
    
    db.add(todo)
    
    db.commit() 
    
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

