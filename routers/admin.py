from fastapi import APIRouter,Path,Depends,status,HTTPException
from ..models import Todos
from pydantic import BaseModel,Field
from typing import Annotated
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..utils import user_dependency,db_dependency



router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

@router.get('/todo', status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency, user: user_dependency ):
    if not user or user.get('role',None) != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")
    todos = db.query(Todos).all()
    return todos