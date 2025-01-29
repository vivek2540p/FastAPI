from fastapi import APIRouter,status,HTTPException
from ..models import User
from pydantic import BaseModel,Field
from .auth import bcrypt_context
from ..utils import db_dependency,user_dependency


router = APIRouter(
    prefix="/user",
    tags=["User"],
)


class PasswordVerification(BaseModel):
    old_password: str
    new_password: str

class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str = Field(min_length=10,max_length=10)
    


@router.get('/get_user', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid user")
    return db.query(User).filter(User.id==user.get('id')).first()

@router.put('/password', status_code=status.HTTP_200_OK)
async def change_password(db: db_dependency, user: user_dependency, verification: PasswordVerification):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid user")
    user = db.query(User).filter(User.id==user.get('id')).first()
    if not bcrypt_context.verify(verification.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid user")
    if not user.password!=verification.old_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid old password")
    user.password = bcrypt_context.hash(verification.new_password)
    db.add(user)
    db.commit()
    return {"message": "Password changed successfully"}

@router.put('/update', status_code=status.HTTP_200_OK)
async def update_user(db: db_dependency, user: user_dependency, user_update: UserUpdate):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid user")
    user = db.query(User).filter(User.id==user.get('id')).first()
    user.first_name = user_update.first_name
    user.last_name = user_update.last_name
    user.phone_number = user_update.phone_number
    db.add(user)
    db.commit()
    return {"message": "User updated successfully"}