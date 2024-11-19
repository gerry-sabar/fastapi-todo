from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from database import Base, SessionLocal
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session

import models,schemas, repositories
import logging

#create FastAPI application instance
app = FastAPI()


def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()


# Create routers for different route groups
todo_router_v1 = APIRouter(prefix="/todos", tags=["todos v1"])

'''
 -  Here we injected schemas / serializer from TodoRead to response since this can 
    show more than one todo result we put use list 
 -  We create a simple repository to perform database process here
 -  Last we put proper http status using status_code decorator.
    Common status codes in the status module:
    status.HTTP_200_OK (default for successful responses)
    status.HTTP_201_CREATED
    status.HTTP_204_NO_CONTENT
    status.HTTP_400_BAD_REQUEST
    status.HTTP_404_NOT_FOUND
    status.HTTP_500_INTERNAL_SERVER_ERROR

'''
@todo_router_v1.get("", summary="List all todos", status_code=status.HTTP_200_OK, response_model=list[schemas.TodoRead])
async def get_todo_v1(db:Session=Depends(get_db)):
    return repositories.get_todos(db)


'''
 -  We use response from TodoRead schema so it'll show all 4 properties of the record.
 -  Incoming request uses Todo schema. According to the schema two parameters are mandatory
    it'll act as a validation as well
'''
@todo_router_v1.post("", summary="Create a new todo", status_code=status.HTTP_201_CREATED, response_model=schemas.TodoRead)
async def post_todo_v1(todo:schemas.Todo, db:Session=Depends(get_db)):
    return repositories.create_todo(db, todo)


'''
 -  To get todo detail we only need one parameter to fetch a todo based on its id
 -  Throw http exception if record is not found
'''
@todo_router_v1.get("/{todo_id}", summary="Get todo detail", status_code=status.HTTP_200_OK, response_model=schemas.TodoRead)
async def patch_todo_v1(todo_id: str, db:Session=Depends(get_db)):
    todo = repositories.get_todo(db, todo_id)
    if todo is not None:
        return todo
    else:
        raise HTTPException(status_code=400, detail="Todo is not found")


'''
 -  Patch is only partial update therefore we use TodoPatch schemas which we put optional parameter
    for title & status. If any of these parameters are added then the value of these parameters will
    be updated
 '''
@todo_router_v1.patch("/{todo_id}", summary="Partial update todo", status_code=status.HTTP_200_OK, response_model=schemas.TodoRead)
async def patch_todo_v1(todo_id: str, update_todo:schemas.TodoPatch, db:Session=Depends(get_db)):
    todo = repositories.get_todo(db, todo_id)
    if todo is not None:
        repositories.update_todo(db, update_todo, todo_id)
        db.commit()
        db.refresh(todo)      

        return todo
    else:
        raise HTTPException(status_code=400, detail="Todo is not found")


'''
 -  Put request means all update according to the REST best practice. On this case 
    the required parameters are identical with post so we use the same schema for 
    incoming request with post which is Todo
'''
@todo_router_v1.put("/{todo_id}", summary="Update todo",status_code=status.HTTP_200_OK, response_model=schemas.TodoRead)
async def put_todo_v1(todo_id: str, update_todo:schemas.Todo, db:Session=Depends(get_db)):
    todo = repositories.get_todo(db, todo_id)
    if todo is not None:
        repositories.update_todo(db, update_todo, todo_id)
        db.commit()
        db.refresh(todo)      

        return todo
    else:
        raise HTTPException(status_code=400, detail="Todo is not found")


@todo_router_v1.delete("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT, summary="Delete todo")
async def delete_todo_v1(todo_id: str, db:Session=Depends(get_db)):
    todo = repositories.get_todo(db, todo_id)
    if todo is not None:
        db.delete(todo)
        db.commit()
        return
    else:
        raise HTTPException(status_code=400, detail="Todo is not found")


# Create versioning for API endpoint by incorporating todo_router_v1 into FastAPI application instance
app.include_router(todo_router_v1, prefix="/v1")