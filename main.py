from fastapi import FastAPI,status,Request
from .database import engine
from .models import Base
from .routers import auth,todos,admin,user
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="Todo/templates")

app.mount("/static", StaticFiles(directory="Todo/static"), name="static" )

@app.get('/')
def read_root(request: Request):
    return templates.TemplateResponse('home.html',{"request":request})

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)




    

