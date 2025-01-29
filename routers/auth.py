from datetime import datetime, timedelta, timezone
from fastapi import APIRouter,Depends, HTTPException,status,Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from ..models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..database import SessionLocal
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt



router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = 'fgw4yhtw74tc7w4t73t7947t4nc947t4t437yt7cyn'
ALGORITH = 'HS256'

bcrypt_context =CryptContext(schemes=["bcrypt"],deprecated='auto')

templates = Jinja2Templates(directory="Todo/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
        # return db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")



class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str = Field(min_length=10,max_length=10, example="1234567890")
    role: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    




def authenticate_user(username: str,password: str,db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username")
    if not bcrypt_context.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta | None = None):
    to_encode = {'username': username, 'id': user_id, 'role': role}
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)
    return encoded_jwt
        
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer )]):
    try:
        payload= jwt.decode(token,SECRET_KEY,algorithms=[ALGORITH])
        username: str = payload.get("username")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials")
        return {'username':username, 'id':user_id, 'role':user_role}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials")




@router.get('/login-page')
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get('/register-page')
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get('/')
async def read_users(db: db_dependency):
    return db.query(User).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, request: CreateUserRequest):
    try:
        user = User(
            username=request.username,
            email=request.email,
            password=bcrypt_context.hash(request.password),
            first_name=request.first_name,
            last_name=request.last_name,
            role=request.role
        )
        db.add(user)
        db.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post('/token',response_model=Token)
async def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user( form_data.username, form_data.password, db)
    token= create_access_token(                   
        username= user.username, 
        user_id= user.id,
        role=user.role,
        expires_delta=timedelta(minutes=30),
        )
    return {"access_token": token, "token_type": "bearer" }

    
    