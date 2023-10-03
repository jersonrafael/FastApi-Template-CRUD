from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models import postModel
from schema import post
from db.database import SessionLocal, engine

postModel.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


home_route = APIRouter()

templates = Jinja2Templates(directory="templates")



@home_route.get('/', response_class=HTMLResponse)
@home_route.post('/', response_class=HTMLResponse)
async def home(request: Request, db: SessionLocal = Depends(get_db)):
    data = db.query(postModel.Post).all()
    context = {
        "request":request,
        "data":data
    }
    return templates.TemplateResponse("home.html", context)


@home_route.get( '/createpost', response_class=HTMLResponse)
async def create_post(request: Request):
    context = {
        "request":request
    }
    return templates.TemplateResponse("create_post.html", context)

@home_route.post('/createpost')
def create_post(title:Annotated[str, Form()],description:Annotated[str, Form()] , db: SessionLocal = Depends(get_db)): 
    create_post = postModel.Post(title=title, description=description)
    db.add(create_post)
    db.commit()
    # db.refresh(create_post)
    return RedirectResponse("/")


@home_route.get('/edit_task/{id_task}', response_class=HTMLResponse)
def edit_task(id_task , request:Request ,db: SessionLocal = Depends(get_db)):
    find_task = db.query(postModel.Post).filter(postModel.Post.id == id_task).first()
    if not find_task:
        raise HTTPException(status_code=404, detail="Item not found")

    context= {
        "request":request,
        "find_task" : find_task
    }
    
    return templates.TemplateResponse("edit_task.html", context)
        

@home_route.post('/edit_task/{id_task}')
def edit_task(id_task , title: str = Form(...), description: str = Form(...)  ,db: SessionLocal = Depends(get_db)):
    find_task = db.query(postModel.Post).filter(postModel.Post.id == id_task).first()
    if not find_task:
        raise HTTPException(status_code=404, detail="Item not found")

    find_task.title = title
    find_task.description = description
    db.commit()
    return RedirectResponse('/')



@home_route.get('/deletetask/{id_task}', response_model=post.getPost)
def delete_task(id_task,db: SessionLocal = Depends(get_db)):
    find_task = db.query(postModel.Post).filter(postModel.Post.id == id_task).first()
    if find_task:
        db.delete(find_task)
        db.commit()
        return RedirectResponse('/')
    else:
        return RedirectResponse('/')
    
