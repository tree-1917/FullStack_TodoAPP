# === libs
import sys
sys.path.append("..")
from starlette.responses import RedirectResponse
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form
from pydantic import BaseModel, Field
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .auth import create_access_token, get_current_user

# === Common
router = APIRouter(
    prefix="/user",
    tags=["user"]
)
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === Global
# TODO: Create Validtion Class 
class PasswordIn(BaseModel) : 
    username : str 
    password : str 
    new_password : str = Field(min=5)

# TODO: Dependency
def get_db() : 
    try : 
        db = SessionLocal() # open db session 
        yield db # generate db
    finally : 
        db.close() # close db session 


# === Routes 
# UI
@router.get("/password", response_class=HTMLResponse)
async def test(request: Request): 
    return templates.TemplateResponse("edit-passwd.html", {"request" : request})
# BK
@router.post("/password",status_code=status.HTTP_204_NO_CONTENT)
async def test(request:Request ,username:str = Form(...), password: str = Form(...), new_password : str= Form(...) ,User = Depends(get_current_user), db: Session = Depends(get_db)) : 
    #TODO: Vaildate Current User 
    current_user = db.query(models.Users).filter(models.Users.id == User.get("id")).first() 
    if current_user.username != username or not pwd_context.verify(password, current_user.hashed_password): 
        msg = "Username or Password Error"
        return templates.TemplateResponse("edit-passwd.html", {"request" : request, "msg" : msg})
    # #TODO: Hashed User Password and update
    hashed_password = pwd_context.hash(new_password)
    current_user.hashed_password = hashed_password
    # #TODO: Save User Password 

    db.add(current_user)
    db.commit()
    # #TODO: Generate new token
    token_expires = timedelta(minutes=60)
    new_token = create_access_token(current_user.username, current_user.id, expires_delta=token_expires)
    
    # TODO: Fetch data from backend 
    todos = db.query(models.Todos).filter(models.Todos.owner_id == current_user.id).all()

    # Set new token in the response
    response = templates.TemplateResponse("home.html", {"request": request, "msg": "Successfully Changed", "todos": todos})
    response.set_cookie(key="access_token", value=new_token, httponly=True)
    
    return response