from fastapi import APIRouter,Path,Depends, Request,status,HTTPException,Response
from fastapi.templating import Jinja2Templates
from ..models import Todos
from pydantic import BaseModel,Field
from .auth import get_current_user
from ..utils import db_dependency,user_dependency
from starlette.responses import RedirectResponse

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
)

templates = Jinja2Templates(directory="Todo/templates")

class TodoRequest(BaseModel):
    title: str = Field(min_length=5)
    description: str = Field(min_length=5,max_length=100)
    completed: bool = Field(default=False)
    priority: int = Field(gt=0,lt=6)
    

def rediredt_to_login():
    rediredt = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    rediredt.delete_cookie(key="access_token")
    return rediredt


@router.get('/todo-page')
async def todo_page(request: Request, db: db_dependency):
    if request.cookies.get('access_token') is None:
        return rediredt_to_login()
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return rediredt_to_login()
        todos = db.query(Todos).filter(Todos.user_id == user['id']).all()
        return templates.TemplateResponse("todo_page.html", {"request": request,"todos":todos,"user":user})
    except Exception as e:
        return Response(content=str(e), media_type="text/plain", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@router.get('/add-todo-page')
async def add_todo_page(request: Request):
    if request.cookies.get('access_token') is None:
        return rediredt_to_login()
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return rediredt_to_login()
        return templates.TemplateResponse("add-todo.html", {"request": request,"user":user})
    except Exception as e:
        return Response(content=str(e), media_type="text/plain", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/edit-todo-page/{id}')
async def edit_todo_page(request: Request,id: int, db: db_dependency):
    if request.cookies.get('access_token') is None:
        return rediredt_to_login()
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return rediredt_to_login()
        todo = db.query(Todos).filter(Todos.id == id).first()
        if todo is None:
            return Response(content="Todo not found", media_type="text/plain", status_code=status.HTTP_404_NOT_FOUND)
        return templates.TemplateResponse("edit-todo.html", {"request": request,"todo":todo,"user":user})
    except Exception as e:
        return Response(content=str(e), media_type="text/plain", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get('/todo',status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")
    return db.query(Todos).filter(Todos.user_id==user['id']).all()


@router.get('/todo/{id}',status_code=status.HTTP_200_OK)
async def read_one(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")
    todo=db.query(Todos).filter(Todos.id == id).filter(Todos.user_id==user['id']).first()
    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    return db.query(Todos).filter(Todos.id == id).first()

@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, todo: TodoRequest, db: db_dependency):
    try:
        if not user:
            raise HTTPException(status_code=401,detail="Unauthorized")
        db_todo = Todos(**todo.model_dump(), user_id=user['id'])
        db.add(db_todo)
        db.commit()
        return todo.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.put('/todo/{id}', status_code=status.HTTP_200_OK)
async def update_todo(todo: TodoRequest, user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    print(todo)
    if not user:
        raise HTTPException(status_code=401,detail="Unauthorized")
    db_todo = db.query(Todos).filter(Todos.id == id).filter(Todos.user_id==user['id']).first()
    if not db_todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = todo.completed
    db_todo.priority = todo.priority
    db.add(db_todo)
    db.commit()
    return db_todo
    
@router.delete('/todo/{id}', status_code=status.HTTP_200_OK)
async def delete_todo(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=401,detail="Unauthorized")
    db_todo = db.query(Todos).filter(Todos.id == id).filter(Todos.user_id==user['id']).first()
    if not db_todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}